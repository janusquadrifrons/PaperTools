import os # --- for file/path operations
import re # --- for regular expressions

# Helper Function - filename pattern looser
def parse_from_stem(stem: str):
    """ Parse "[..] - Surname - Title (Year)" or "[..] - Surname - Title" as well """
    # Normalize spaces
    s = re.sub(r"\s+", " ", stem).strip()

    # 1) Stricht explicit pattern with trailing year in parantheses
    m = re.match(
        r"""^\[.*?\]\s*-\s*(?P<surname>[^-]+?)\s*-\s*(?P<title>.+?)\s*\((?P<year>\d{4}|n\.d\.)\)$""",
        s, flags=re.IGNORECASE)
    
    if m:
        return m.group("surname").strip(), m.group("title").strip(), m.group("year").strip()

    # 2) Looser pattern without trailing year
    m = re.match(
        r"""^\[.*?\]\s*-\s*(?P<surname>[^-]+?)\s*-\s*(?P<title>.+?)$""",
        s, flags=re.IGNORECASE)
    
    if m:
        surname = m.group("surname").strip()
        title = m.group("title").strip()
        # Try to grab year from title if exists
        trail_year = re.search(r"\((19|20)\d{2}\)\s*$", title)
        if trail_year:
            year = trail_year.group(0).strip("() ")
            title = re.sub(r"\s*\((19|20)\d{2}\)\s*$", "", title).strip()
        else:
            any_year = re.search(r"(19|20)\d{2}", title)
            year = any_year.group(0) if any_year else "n.d."
        return surname, title, year
    return None

## BIB Creation
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
        stem, _ = os.path.splitext(filename) # --- filename without .pdf

        parsed = parse_from_stem(stem)

        if not parsed:
            print(f"Skipping '{filename}': Unable to parse metadata from filename.")
            continue

        surname, title, year = parsed

        # Build a simple BibTeX key: surname + year + first word of title (sanitized)
        first_word = title.split()[0].lower() if title.split() else "paper"
        key = re.sub(r"[^a-z0-9]+", "", f"{surname.lower()}{year}{first_word}")

        bib_content = f"""@article{{{key},
        author = {{{surname}}},
        title  = {{{title}}},
        year   = {{{year}}}
        }}"""

        bib_path = os.path.splitext(pdf_path)[0] + ".bib"
        try:
            with open(bib_path, "w", encoding="utf-8") as bib_file:
                bib_file.write(bib_content)
            print(f"Created .bib file for '{filename}' as '{os.path.basename(bib_path)}'.")
        except Exception as e:
            print(f"Error creating .bib file for '{filename}': {e}")
