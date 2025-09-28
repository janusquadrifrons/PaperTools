import os # --- for file/path operations
import re # --- for regular expressions

def create_bib_files(folder_path : str):
    """
    For each .pdf starting with "[", parse the name to extract
    author surname, title, and year, then create a .bib file with that info.
    """
    for filename in os.listdir(folder_path):
        if not filename.lower().endswith(".pdf"):
            continue
        if not filename.startswith("["):
            continue

        # Get PDF path
        pdf_path = os.path.join(folder_path, filename)
        # Filename without extension
        stem, _ = os.path.splitext(filename)

        # Expected format: [<index>] - <surname> - <title> (<year>).pdf
        match = re.match(r"\[.*\]\s*-\s*(.*?)\s*-\s*(.*)\s*\((\d{4}|n\.d\.)\)$", stem)
        if not match:
            print(f"Filename '{filename}' does not match expected format. Skipping.")
            continue

        surname, title, year = match.groups()

        # Create .bib key and content : lowercase all
        key = f"{surname.lower()}{year}"
        bib_content = f"""@article{{
        {key},
        author = {{{surname}}},
        title = {{{title}}},
        year = {{{year}}}
        }}"""

        bib_path = os.path.splitext(pdf_path)[0] + ".bib"
        try:
            with open(bib_path, "w", encoding="utf-8") as bib_file:
                bib_file.write(bib_content)
            print(f"Created .bib file for '{filename}' as '{os.path.basename(bib_path)}'.")
        except Exception as e:
            print(f"Error creating .bib file for '{filename}': {e}")
