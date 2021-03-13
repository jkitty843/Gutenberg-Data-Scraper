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
        sys.exit(f'There was a problem: {exc!r}')
    return res

#TODO: Repeat (loop?) data retrieval for several Shakespeare works
textID = 1513  #Romeo and Juliet for testing
res = retrieve_gutenberg_text(textID)
#test
#Very simple test case with constants rather than proper regexes. Was used for proof of concept.
rjRegex = re.compile(r'Romeo')
searchFor = '"Romeo"'
rjBeginIndex = res.text.find("ACT I")
rjEndIndex = res.text.find('THE END')
occurences = rjRegex.findall(res.text[rjBeginIndex:rjEndIndex])
print('There are %s occurences of %s in the text.' % (str(len(occurences)), searchFor))