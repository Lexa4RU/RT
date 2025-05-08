# What is the project ? 
    The project is simply a client and server communicating information, in this case word searches in several file types (txt, html, pdf and excel).
    
    The client communicates the word searched for and the type(s) of file in which it is to be found, and the server performs the search and returns the name of the files in which the word was found, as well as the line, page or cell.
    
    The client can also choose whether or not to respect the case of the word searched for. 

# How to use ?
###  Using the IHM
    - First, start the server. 
    - Then start the client.
    - Input the word you want to search for.
    - Toggle ON or OFF the case-sensitive (ON means that it'll search only the words that stricly corresponds).
    - Toggle ON or OFF which file types you want to search the word.
    - Hit "search"

### Using the functions
    Each functions use the same principles, they need a folder path (where the files are stored), then the word to search for, then a boolean for the case sensitive. Then it returns a dictionnary containing the file name and either the line, page or cell (depending on the file type)
    
    for example : 

    results = pdf(pdf_folder, word, True)
    for file, pages in search_results.items():
        print(f"Word found in {file} on pages: {pages}")

### Authors
    Axel Ptak aka Lev_____

## Modules used 
    socket
    json
    tkinter
    threading
    os
    warnings
    pandas
    PyPDF2
    bs4

## All the modules usables for the project 
### HTML 
    BeautifulSoup (BS4)
    lxml

### PDF 
    PyPDF2
    pdfplumber 

### Excel
    openpyxl (uniquement pour xlsx)
    pandas

### License
    Licensed under GNU General Public License v3.0