## main CLI
# !/usr/bin/env python3
import argparse
import os

from utils.pdf_tools import rename_pdfs, store_api_key

def main():
    parser = argparse.ArgumentParser(
        prog="PaperTools",
        description="A set of tools to manage and organize research papers in PDF format.",
    )

    subparsers = parser.add_subparsers(dest="command")

    # set key command
    key_parser = subparsers.add_parser("setkey", help="Set the OpenAI API key.")

    # rename command
    rename_parser = subparsers.add_parser("rename", help="Rename PDF files.")
    rename_parser.add_argument(
        "--path", 
        default=".", 
        help="Path to the folder containing PDF files.")

    # Parse the arguments
    args = parser.parse_args()

    if args.command == "setkey":
        store_api_key()
    elif args.command == "rename":
        rename_pdfs(args.path)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()



