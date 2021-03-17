#! python3

#Testing using a simple Tkinter master GUI to accept user input.

import tkinter as tk
import GutenbergLookup as gb

def get_entry_list():
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

#Primary function from which most others are called
def search_gutenberg():
    entry_list = get_entry_list()
    book_dict = get_dict_from_entries(entry_list)   #book_dict has {bookID : 'Title'} format
    unformatted_books = gb.get_books_from_id_list(book_dict.keys())     #List of lists formatted [book_dict key, book's Response object]
    books = gb.format_gutenberg_text(unformatted_books)     #List of lists formatted [book_dict key, string containing book's text]
    search_regex_string = regex_text.get('1.0', 'end-1c')  #'1.0' = line 1, char 1. end-1c = end - last char (a newline char)
    gb.compare_regex_instances(books, search_regex_string, book_dict)
    
#Instantiates a Tkinter window and sets up GUI
master = tk.Tk()
master.title('Gutenberg Regex Finder')

#Title and column labels
title_label = tk.Label(master, text = 'Enter Project Gutenberg titles and book IDs to analyze:')
column1_label = tk.Label(master, text = 'Title')
column2_label = tk.Label(master, text = 'Book ID')
title_label.grid(row = 0, column = 0, padx = 5, pady = 2, columnspan = 2)
column1_label.grid(row = 1, column = 0, pady = 2)
column2_label.grid(row = 1, column = 1, pady = 2)

#Title and ID entries
entry_box_list = []
#Every second entry box drawn is in the second column, so every second StringVar in the list will be for IDs
#Vice versa applies for titles
for row in range(3,8):
    for column in range(2):
        entry = tk.Entry(master)
        entry_box_list.append(entry)
        entry.grid(row = row, column = column, pady = 2)

#Regex entry
regex_label = tk.Label(master, text = 'Enter a regular expression to search for:')
regex_text = tk.Text(master, height = 3, width = 30)
regex_label.grid(row = 9, column = 0, pady = 2, columnspan = 2)
regex_text.grid(row = 10, column = 0, padx = 2, pady = 5, rowspan = 2, columnspan = 2)

#Bottom buttons. The search button is where the magic happens
search_button = tk.Button(master, text = 'Search', command = search_gutenberg)
exit_button = tk.Button(master, text = 'Exit', command = master.quit)
search_button.grid(row = 13, column = 1, pady = 2)
exit_button.grid(row = 13, column = 0, pady = 2)

master.mainloop()