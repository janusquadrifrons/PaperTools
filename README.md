# PaperTools

**PaperTools** is a Python command-line app to manage and organize research paper PDF files.  
The first implemented function is `rename`, which automatically renames `.pdf` files based on their metadata or parsed content.



## Features

- **Rename PDFs** into the format:
```

[<Index,Scoring for to fill>] - <AuthorSurname> - <Paper Title> (<Year>).pdf

````
- Skips:
    - Non-PDF files
    - Files already starting with `[` (already renamed)
- Extracts:
    - **Author surname**
    - **Paper title**
    - **Publication year**
- Uses a hybrid approach:
    1. **PDF metadata** (if available)
    2. **First pages until "Abstract"** text, parsed via the **OpenAI API**
- Interactive prompt for the **OpenAI API key** if not already set.


## Requirements

- Python 3.10+, pdfplumber, PyPDF2
- OpenAI API Subscription (Beware its independent from ChatGPT Subscription)
- Packages:
```bash
pip install openai pdfplumber PyPDF2
````

## Usage

Run commands from the root of the project:

### Rename PDFs

```bash
python papertools.py rename --path <folder_path>
```

**Examples:**

* Rename PDFs in the current directory:

  ```bash
  python papertools.py rename --path .
  ```

* Rename PDFs in another folder:

  ```bash
  python papertools.py rename --path "D:\Research\Papers"
  ```

When you run `rename`, if the app cannot find an API key, it will prompt:

```
No API key found. You'll be prompted now (input is hidden).
Enter your OpenAI API key:
```

Paste your key (hidden input), press Enter, and renaming will proceed.

## API Key Management

Currently the API key is **stored in memory only during a single run**.
Each time you call the CLI, the app will ask you again if no key is found in the environment.

* **Environment variable (optional, advanced users):**
  You may set your API key once per session:

  ```powershell
  $env:OPENAI_API_KEY = "sk-yourkey"
  python papertools.py rename --path .
  ```

* **Global variable in code (current design):**
  The app binds the key to a global variable (`API_KEY`) so that in the future,
  when we add more subcommands (e.g., `summarize`, `scoring`),
  the key can be shared across functions within the same run.

## Roadmap / Notes

* ✅ `rename` command
* 🚧 Future functions:

  * `scoring`: quick evaluation and scoring within the given context
  * `summarize`: generate paper summaries
  * `extract-refs`: extract references section
  * `bibtex`: export metadata to `.bib` format
* 🔒 Security:

  * The API key is never written to disk
  * Only in-memory use or environment variable
  * If you publish this repo, **your key is safe** unless you hardcode it yourself
* 📂 Ignore caches:

  * Python creates `__pycache__/` folders automatically

## Quick Reminders (for me)

* Main entry point: **`papertools.py`**
* Utilities: **`utils/pdf_tools.py`**
* CLI arguments:

  * `rename` → runs the renaming
  * `--path` → specify folder of PDFs
* API key:

  * Stored globally in `API_KEY`
  * Accessed via `load_api_key()`
  * If missing → prompt via `store_api_key()`

## Example Session

```powershell
PS> python papertools.py rename --path "G:\Drive\Research"
No API key found. You'll be prompted now (input is hidden).
Enter your OpenAI API key:
Renamed: oldfilename.pdf -> [ ] - Smith - Graph Neural Networks (2020).pdf
Renamed: another.pdf -> [ ] - Doe - A Study on AI (2019).pdf
```


