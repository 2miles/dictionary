from bs4 import BeautifulSoup
import requests
import sys

# get word from command line
wordList = sys.argv[1:]
# 'word' is considered as one term seperated by spaces
word = " ".join(wordList)
# get the html at vocabulary.com for 'word'
if word == "":
    word = "randomword"
source = requests.get(f"https://www.vocabulary.com/dictionary/{word}").text
soup = BeautifulSoup(source, "lxml")
if word == "randomword":
    word = soup.find("span", class_="word").text

definitions_exist = False

print(f"\nDefinition of {word}:\n")
for count, dfn in enumerate(soup.find_all("div", class_="definition")):
    definitions_exist = True
    if dfn != None:
        typ = soup.find("div", class_="pos-icon")
        if typ != None:
            typ = typ.text
            for child in dfn.find_all("div"):
                child.decompose()
            dfn = dfn.get_text().strip()
            print(f"{count + 1}. ({typ})   {dfn}")
if definitions_exist == False:
    print(f"No definitions for '{word}'")
