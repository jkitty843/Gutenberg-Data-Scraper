#! python3
import requests
import re
import sys
from bs4 import BeautifulSoup

def retrieve_gutenberg_text(textID):
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

#TODO: Repeat (loop?) data retrieval for several Shakespeare works
textID = 1513  #Romeo and Juliet for testing; ID is variable instead of full URL because Gutenberg's simple URL structure makes it a simple replacement
res = retrieve_gutenberg_text(textID)
playText = remove_text_padding(res.text)

#For debugging purposes
start, end = playText[:100], playText[-100:]
print(f'Final text begins "{start!r}" \nand ends {end!r}"')

#Very simple test case with constants rather than proper regexes. Was used for proof of concept.
# rjRegex = re.compile(r'Romeo')
# searchFor = '"Romeo"'
# rjBeginIndex = res.text.find('ACT I')
# rjEndIndex = res.text.find('THE END')
# occurences = rjRegex.findall(res.text[rjBeginIndex:rjEndIndex])
# print('There are %s occurences of %s in the text.' % (str(len(occurences)), searchFor))