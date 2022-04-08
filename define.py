from bs4 import BeautifulSoup
import requests
import sys

url1 = "https://www.vocabulary.com/dictionary/"


def get_word_from_argv():
    # returns unhyphenated word from command line
    word = ""
    if len(sys.argv) > 1:
        word = sys.argv[1].replace("-", " ")
    return word


def build_url_with_word(base_url, word):
    # made specifically for vocabularly.com urls
    if word == "":
        word = "randomword"
    url = base_url + word
    return url


def make_soup(url):
    # returns html parsing tree from url
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    return soup


def get_random_word(soup):
    # If user doesnt enter a word we need to find out what word
    # we got randomly directed to
    word = soup.find("span", class_="word").text
    return word


def main():
    word = get_word_from_argv()
    url = build_url_with_word(url1, word)
    soup = make_soup(url)
    if word == "":
        word = get_random_word(soup)

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


if __name__ == "__main__":
    main()
