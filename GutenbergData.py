#! python3
import requests
import re
import sys
import os
from pathlib import Path

def get_gutenberg_text(textID):
    try:
        res = requests.get(f'http://www.gutenberg.org/files/{textID!r}/{textID!r}-0.txt')
        res.raise_for_status()
    except Exception as exc:
        sys.exit(f'There was a problem retrieving a file: {exc!r}')
    return res

def remove_text_padding(playText):
    playText = playText.replace('\r', '')   #Doesn't need space because it doesn't seperate lines
    playText = playText.replace('\n', ' ')  #Need a space here to seperate words on next line
    headerRegex = re.compile(r'\*{3}\s?START.+?\*{3}')   #*** START OF THE/THIS PROJECT GUTENBERG EBOOK ***
    footerRegex = re.compile(r'\*{3}\s?END.+?\*{3}')     #*** END OF THE/THIS PROJECT GUTENBERG EBOOK ***
    headerLoc = headerRegex.search(playText)
    footerLoc = footerRegex.search(playText)
    try:
        playText = playText[headerLoc.span()[1]:footerLoc.span()[0]]    #Unpadded text runs from end of header line to beginning of footer line
    except Exception as exc:
        print(f'Could not remove text padding: {exc!r}')
    return playText

#textID = 1513  #Romeo and Juliet for testing; Currently reading from file due to Project Gutenberg's stance on web scraping.
#res = get_gutenberg_text(textID)
allWorks = open('ShakespeareCompleteWorks.txt', encoding='utf8')
allText = allWorks.read()
playText = remove_text_padding(allText)

#table of contents to create list of works
contentStart = playText.find('THE SONNETS')
contentEnd = playText.find('ADONIS') + len('ADONIS')
toc = playText[contentStart : contentEnd]   
tocList = list(toc.split('                 '))
tocList = tocList[0::2]




# #testing using beautifulsoup to get multiple titles from Shakespeare's author pages
# #TODO: Repeat process for pageIndex +=25 (start_index=26, start_index=51, etc.) up to pageIndex = 326
# pageIndex = 1
# authorPage = 'https://www.gutenberg.org/ebooks/author/65?sort_order=title&start_index=' + str(pageIndex)
# soup = get_URLs_from_author(authorPage)

# #For debugging purposes
print(tocList)