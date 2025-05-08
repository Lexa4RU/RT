"""Search for a word in the following files: PDF, Excel, TXT and HTML.

Using the functions: pdf(), excel(), txt() and html() respectively
All of them using the same parameters : (folder_path:str, search_word:str,\
    case_sensitive:bool)
"""

import os
import warnings
import pandas as pd
from PyPDF2 import PdfReader
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")


def pdf(folder_path, search_word, case_sensitive=False):
    """
    Search for a specific word in all PDF files within a folder.

    Args:
        folder_path (str): The path to the folder containing PDF files.
        search_word (str): The word to search for.
        case_sensitive (bool): Whether the search should be case-sensitive.

    Returns:
        dict: A dictionary where keys are file names and values are lists of \
            page numbers where the word was found.
    """
    results = {}

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.pdf'):
            file_path = os.path.join(folder_path, file_name)
            try:
                pdf_reader = PdfReader(file_path)
                pages_with_word = []
                for page_number, page in enumerate(pdf_reader.pages, start=1):
                    try:
                        text = page.extract_text()
                        if case_sensitive:
                            if search_word in text:
                                pages_with_word.append(page_number)
                        else:
                            if search_word.lower() in text.lower():
                                pages_with_word.append(page_number)
                    except Exception as e:
                        print(f"Error reading page {page_number} in {file_name}: {e}")

                if pages_with_word:
                    results[file_name] = pages_with_word
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    return results


def excel(folder_path, search_word, case_sensitive=False):
    """
    Search for a specific word in all Excel files within a folder.

    Args:
        folder_path (str): The path to the folder containing Excel files.
        search_word (str): The word to search for.
        case_sensitive (bool): Whether the search should be case-sensitive.

    Returns:
        dict: A dictionary where keys are file names and values are lists of \
            dictionaries with sheet name and cell details.
    """
    results = {}

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.xls', '.xlsx', '.xlsm')):
            file_path = os.path.join(folder_path, file_name)
            try:
                excel_data = pd.ExcelFile(file_path)
                file_results = []
                for sheet_name in excel_data.sheet_names:
                    sheet_data = excel_data.parse(sheet_name)
                    for row_index, row in sheet_data.iterrows():
                        for col_index, (col_name, cell_value) in enumerate(row.items()):
                            if pd.notna(cell_value):
                                cell_text = str(cell_value)
                                if case_sensitive:
                                    if search_word in cell_text:
                                        column_letter = chr(65 + col_index)
                                        cell_address = f"{column_letter}{row_index}"
                                        file_results.append({
                                            'sheet': sheet_name,
                                            'cell': cell_address
                                        })
                                else:
                                    if search_word.lower() in cell_text.lower():
                                        column_letter = chr(65 + col_index)
                                        cell_address = f"{column_letter}{row_index + 1}"
                                        file_results.append({
                                            'sheet': sheet_name,
                                            'cell': cell_address
                                        })

                if file_results:
                    results[file_name] = file_results
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    return results


def txt(folder_path, search_word, case_sensitive=False):
    """
    Search for a specific word in all text files within a folder.

    Args:
        folder_path (str): The path to the folder containing text files.
        search_word (str): The word to search for.
        case_sensitive (bool): Whether the search should be case-sensitive.

    Returns:
        dict: A dictionary where keys are file names and values are lists of \
            line numbers where the word was found.
    """
    results = {}

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    lines_with_word = []
                    for line_number, line in enumerate(file, start=1):
                        if case_sensitive:
                            if search_word in line:
                                lines_with_word.append(line_number)
                        else:
                            if search_word.lower() in line.lower():
                                lines_with_word.append(line_number)

                if lines_with_word:
                    results[file_name] = lines_with_word
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    return results


def html(folder_path, search_word, case_sensitive=False):
    """
    Search for a specific word in all HTML files within a folder.

    Args:
        folder_path (str): The path to the folder containing HTML files.
        search_word (str): The word to search for.
        case_sensitive (bool): Whether the search should be case-sensitive.

    Returns:
        dict: A dictionary where keys are file names and values are lists \
            of line numbers where the word was found.
    """
    results = {}

    for file_name in os.listdir(folder_path):
        if file_name.lower().endswith(('.html', '.htm')):
            file_path = os.path.join(folder_path, file_name)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    soup = BeautifulSoup(file, 'html.parser')
                    text = soup.get_text()
                    lines = text.splitlines()

                    lines_with_word = []
                    for line_number, line in enumerate(lines, start=1):
                        if case_sensitive:
                            if search_word in line:
                                lines_with_word.append(line_number)
                        else:
                            if search_word.lower() in line.lower():
                                lines_with_word.append(line_number)

                if lines_with_word:
                    results[file_name] = lines_with_word
            except Exception as e:
                print(f"Error reading file {file_name}: {e}")

    return results


# Example usage
if __name__ == "__main__":
    pdf_folder = "./pdf"
    excel_folder = "./excel"
    txt_folder = "./txt"
    html_folder = "./html"
    word = "pizza"

    case_sensitive = False

    search_results = pdf(pdf_folder, word, case_sensitive)
    for file, pages in search_results.items():
        print(f"Word found in {file} on pages: {pages}")

    search_results = excel(excel_folder, word, case_sensitive)
    for file, matches in search_results.items():
        print(f"Word found in {file}:")
        for match in matches:
            print(f"  Sheet: {match['sheet']}, Cell: {match['cell']}")

    search_results = txt(txt_folder, word, case_sensitive)
    for file, lines in search_results.items():
        print(f"Word found in {file} on lines: {lines}")

    search_results = html(html_folder, word, case_sensitive)
    for file, lines in search_results.items():
        print(f"Word found in {file} on lines: {lines}")
