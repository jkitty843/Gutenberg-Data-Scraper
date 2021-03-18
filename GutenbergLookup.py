#! python3

#This program serves as a working basis to build off from,
#rather than a complete project. All this program will do is:
#    retrieve the texts of various set Shakespeare works
#    trim/format the text for better usability,
#    and use regex functions to find basic word counts/patterns to analyze.
#Set IDs for each book to retrieve from gutenberg.org are used for testing.
#This is for simplicity and to minimalize data scraped from their servers.
#Future options include scraping a mirror site, working off downloaded text files,
#or using their publicly available catalog metadata.

import re
import requests
from pathlib import Path

def get_response_from_id(id):
    res = requests.get(f'http://www.gutenberg.org/files/{id}/{id}-0.txt')
    res.encoding = 'utf-8'
    try:
        res.raise_for_status()
    except Exception as exc:
        print(f'There was a problem retrieving book ID {id}: {exc}')
    return res

def get_books_from_id_list(ids):
    books = []
    for book in ids:
        res = get_response_from_id(book)
        books.append([book, res])
    return books

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

def compare_regex_instances(books, search_regex_string, book_dict):
    search_regex = re.compile(search_regex_string)
    result_string = ''
    result_dict = {}
    for book in books:
        instances = len(search_regex.findall(book[1]))
        result_string += (f'{book_dict[book[0]]} contains {instances} instances of the searched regex {search_regex_string}'+'\n')
        result_dict.update({book_dict[book[0]] : instances})
    return result_string, result_dict

def get_entry_list(entry_box_list):
    entry_list = []
    for i in range(len(entry_box_list)):
        entry_list.append(entry_box_list[i].get())
    return entry_list

def get_dict_from_entries(entry_list):
    book_dict = {}
    for i in range(0, len(entry_list), 2):
        try:
            book_dict.update({int(entry_list[i+1]) : str(entry_list[i])})
        except ValueError:
            break
    return book_dict