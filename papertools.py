## main CLI
# !/usr/bin/env python3
import argparse
import os

from utils.pdf_tools import rename_pdfs, store_api_key
from utils.createBib import create_bib_files

def main():
    parser = argparse.ArgumentParser(
        prog="PaperTools",
        description="A set of tools to manage and organize research papers in PDF format.",
    )

    subparsers = parser.add_subparsers(dest="command")

    # rename command
    rename_parser = subparsers.add_parser("rename", help="Rename PDF files.")
    rename_parser.add_argument(
        "--path", 
        default=".", 
        help="Path to the folder containing PDF files.")
    
    # createbib command
    bib_parser = subparsers.add_parser("createbib", help="Create .bib files for PDFs.")
    bib_parser.add_argument(
        "--path", 
        default=".", 
        help="Path to the folder containing PDF files. Default is current directory.")

    # Parse the arguments
    args = parser.parse_args()

    if  args.command == "rename":
        rename_pdfs(args.path)
    elif args.command == "createbib":
        create_bib_files(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()



