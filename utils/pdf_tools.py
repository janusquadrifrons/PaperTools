import os
import re # --- for regular expressions
import pdfplumber # --- for PDF text extraction
import getpass # --- for secure input of API key
from openai import OpenAI
import json
import unicodedata # --- for filename sanitization

#Environment varible for OpenAI API key
API_KEY = None

# API KEY management
def store_api_key():
    # Prompt user to paste API key securely and keep it in memory for current session
    global API_KEY
    key = getpass.getpass("Enter your OpenAI API key: ").strip()
    if key:
        API_KEY = key
        os.environ["OPENAI_API_KEY"] = API_KEY
        print("API key stored successfully.")
    else:
        print("No API key entered.")

def load_api_key() -> str | None:
    # Load API key from memory
    global API_KEY
    if API_KEY:
        return API_KEY
    return os.environ.get("OPENAI_API_KEY")

## PDF Renaming
# Helper Function - Extract until "Absract" section
def extract_until_abstract(pdf_path, max_pages=3):
    """ Extract text until finding "Abstract" or up to max_pages. """
    collected = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages[:max_pages]):
            text = page.extract_text() or ""
            lines = text.split("\n")
            for line in lines:
                if re.search(r'\bAbstract\b', line, re.IGNORECASE):
                    return "\n".join(collected)
                collected.append(line.strip())
    return "\n".join(collected) # --- if abstract not found

# Helper Function - Ask OpenAI for metadata
def ask_openai_for_metadata(text, apikey):
    client = OpenAI(api_key=apikey)

    prompt = f"""You are a tool that extracts bibliographic information from research papers.
    I will give you the first section of text up to the word 'Abstract'.
    Return strict JSON only with keys:
    - "title": full paper title
    - "authors": list of author surnames only
    - "year": year of publishing (or "n.d." if not found)
              
    First part of the paper:
    ---
    {text[:3000]}
    ---
    """
    
    response = client.chat.completions.create(
        model = "gpt-4.1-nano",
        messages = [{"role": "user", "content": prompt}],
        response_format = {"type": "json_object"}
    )

    return json.loads(response.choices[0].message.content)

# Metafata Extraction
def extract_metadata(pdf_path, apikey):
    try:
        # Step 1: Try PDF metadata first
        import PyPDF2
        reader = PyPDF2.PdfReader(pdf_path)
        meta = reader.metadata
        if meta and meta.title and meta.author:
            surname = meta.author.split()[-1]
            year_match = re.search(r"(19|20)\d{2}", meta.title + meta.author)
            year = year_match.group(0) if year_match else "n.d."
            return surname, meta.title, year
    except:
        pass
        
    # Step 2: Extract text until "Abstract"
    text = extract_until_abstract(pdf_path)
    data = ask_openai_for_metadata(text, apikey)

    surname = data["authors"][0] if data.get("authors") else "Unknown"
    title = data.get("title", "Untitled")
    year = data.get("year", "n.d.")
    return surname, title, year

# Helper Function - Sanitize Filename
def sanitize_filename(name: str, max_len: int = 100) -> str:
    # Normalize unicode
    name = unicodedata.normalize("NFKC", name)
    # Remove invalid characters
    name = re.sub(r'[<>:"/\\|?*\x00-\x1F]', "_", name)
    # Remove trailing dots/spaces
    name = name.rstrip(". ")
    # Trim to avoid hitting OS path limit after adding .pdf
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name


# Rename PDFs
def rename_pdfs(folder_path):
    
    apikey = load_api_key()
    if not apikey:
        print("Error: No API key found. Please set it using the 'setkey' command.")
        store_api_key() # ask interactively
        apikey = load_api_key()
        if not apikey:
            print("Error: API key is required to proceed. Please run 'setkey' command again.")
            return

    # Skip non-PDFs and already renamed files
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".pdf"):
            continue
        if filename.startswith("["):
            continue
            
        pdf_path = os.path.join(folder_path, filename)
        try:
            surname, title, year = extract_metadata(pdf_path, apikey)

            # Sanitize components
            surname = sanitize_filename(surname)
            title = sanitize_filename(title)
            year = sanitize_filename(year)

            new_name = f"[] - {surname} - {title} ({year}).pdf"
            new_path = os.path.join(folder_path, new_name)

            os.rename(pdf_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
        except Exception as e:
            print(f"Failed to rename {filename}: {e}")    
