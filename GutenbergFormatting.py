#! python3

import re

def remove_lines_endings(text):
    text = text.replace('\r', '')   #Doesn't need space because it doesn't seperate lines
    text = text.replace('\n', ' ')  #Need a space here to seperate words on next line
    return text

def trim_gutenberg_text(text):
    header_regex = re.compile(r'\*{3}\s?START.+?\*{3}')   #*** START OF THE/THIS PROJECT GUTENBERG EBOOK ***
    footer_regex = re.compile(r'\*{3}\s?END.+?\*{3}')     #*** END OF THE/THIS PROJECT GUTENBERG EBOOK ***
    headerLoc, footerLoc = header_regex.search(text), footer_regex.search(text)
    try:
        trimmed_text = text[headerLoc.span()[1] : footerLoc.span()[0]]    #Unpadded text runs from end of header line to beginning of footer line
    except Exception as exc:
        print(f'Could not remove text padding: {exc}')
    return trimmed_text

#Optional remove_lines arg allows for optional analysis of linecounts, etc. True by default for simpler character analysis.
def format_gutenberg_text(unformatted_books, remove_lines = True):
    formatted_books = []
    for book in unformatted_books:
        book_text = book[1].text
        if remove_lines:
            book_text = remove_lines_endings(book_text)
        book_text = trim_gutenberg_text(book_text)
        formatted_books.append([book[0], book_text])
    return formatted_books