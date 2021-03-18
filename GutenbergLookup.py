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
from bs4 import BeautifulSoup
from pathlib import Path

def get_titles_and_authors(titles_and_authors):
    titles = []
    authors = []
    for ta in titles_and_authors:
        titles.append(ta[0])
        authors.append(ta[1])
    return titles, authors

def get_books_from_urls(urls):
    responses = [requests.get(url) for url in urls]
    soups = [BeautifulSoup(response.text, 'html.parser') for response in responses]
    #get plain text files
    href_tags = [soup.find(href=True, text='Plain Text UTF-8') for soup in soups]
    book_urls = ['https://' +('www.gutenberg.org')+ tag.attrs['href'] for tag in href_tags]
    #Get titles and authors
    h1_tags = [soup.find('h1').getText() for soup in soups]
    titles_and_authors = [re.split(r'by', tag) for tag in h1_tags]
    titles, authors = get_titles_and_authors(titles_and_authors)
    return book_urls, titles, authors


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

def compare_regex_instances(books, search_regex_string, book_dict):
    search_regex = re.compile(search_regex_string)
    result_string = ''
    result_dict = {}
    for book in books:
        instances = len(search_regex.findall(book[1]))
        result_string += (f'{book_dict[book[0]]} contains {instances} instances of the searched regex {search_regex_string}'+'\n')
        result_dict.update({book_dict[book[0]] : instances})
    return result_string, result_dict