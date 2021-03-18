#! python3

#For analysis without a GUI
#Using pandas instead of a convoluted set of dictionaries and lists
#Takes a list of urls as input, for now manually entered

import requests
import  re
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from GutenbergLookup import *
from GutenbergFormatting import *

urls = [
    'https://www.gutenberg.org/ebooks/1513',    #Romeo and Juliet
    'https://www.gutenberg.org/ebooks/1524',    #Hamlet
    'https://www.gutenberg.org/ebooks/23042',   #The Tempest
    'https://www.gutenberg.org/ebooks/1533',    #Macbeth
    'https://www.gutenberg.org/ebooks/1522',    #Julius Caesar
    'https://www.gutenberg.org/ebooks/1531',    #Othello
    'https://www.gutenberg.org/ebooks/1514'     #A Midsummer Night's Dream
]

#From the page urls get all the book_urls, titles, and authors
book_urls, titles, authors = get_books_from_urls(urls)

#Construct a pandas dataframe
book = pd.DataFrame({'URL': book_urls, "Title": titles, 'Author(s)': authors})
print(book)