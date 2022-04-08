
## Command line dictionary
This is a simple dictionary program that scrapes vocabulary.com for definitions and synomyms of a word. Given a word, it outputs all the definitions as a numbered list followed by a list of synomyms.

---
## How to use
Run the define.py script with the word you want to define given as an argument. If the word contains a " " use a "-" instead. The script can be run without any arguments to list the definitions of a random word.

---
## Requirements
This script requires: 
* beautifalsoup4 
* lxml 
* requests

---
## Motivation
I created this program to learn the basics of Python and webscraping with the BeautifulSoup4 library. Here is short list of Python functionality I learned about while building this program:

* requests library
  - get( )
* beautifulsoup4 library
  - find( )
  - find_all( )
  - get_text( )
  - decompose( )
  - child
* string formating
  - f-strings
* sys.argv
  



