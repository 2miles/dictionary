from bs4 import BeautifulSoup
import requests
import sys

word = ""
if len(sys.argv) != 1:
    word = sys.argv[1].replace("-", " ")

# get the html at vocabulary.com for 'word'
if word == "":
    word = "randomword"
source = requests.get(f"https://www.vocabulary.com/dictionary/{word}").text
soup = BeautifulSoup(source, "lxml")

if word == "randomword":
    word = soup.find("span", class_="word").text

definitions_exist = False

print(f"\n-------- Definitions of {word}:\n")
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
print()

print(f"\n---------- Synonyms of {word}:\n")
for count, dfn in enumerate(soup.find_all("a", class_="word")):
    syn = dfn.text
    print(f"{syn}, ", end="")
    if (count + 1) % 7 == 0:
        print()
print("\n\n")
