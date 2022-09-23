#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
import sys

URL_1 = "https://www.vocabulary.com/dictionary/"

# Line width for console output
MAX_WIDTH = 70
# Column to start text on for definition for console output
INDENT_WIDTH = 13


def get_word_from_argv() -> str:
    '''
    Returns unhyphenated word from command line
    '''
    word = ""
    if len(sys.argv) > 1:
        word = sys.argv[1].replace("-", " ")
    return word


def build_url_with_word(base_url, word) -> str:
    '''
    Made specifically for vocabularly.com urls
    '''
    if word == "":
        word = "randomword"
    url = base_url + word
    return url


def make_soup(url) -> BeautifulSoup:
    '''
    Returns html parsing tree from url
    '''
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    return soup


def get_random_word(soup) -> str:
    '''
    If user doesnt enter a word we need to find out what word
    we got randomly directed to
    '''
    word = soup.find("span", class_="word").text
    return word


def get_definitions_list(soup:BeautifulSoup) -> list:
    '''
    Extracts all definition word types and definitions from soup into a 2-tuple.
    Returns a list of 2-tuples of strings:  [(typ, def), ...]
    typ:  "noun" or "verb" or ...
    def:  "a single definition"
    '''
    def_list = []
    for info in soup.find_all("div", class_="definition"):
        if info != None:
            word_type = soup.find("div", class_="pos-icon")
            if word_type != None:
                word_type = word_type.text
                if word_type == "adjective":
                    word_type = "adj."
                word_type = "(" + word_type + ")"
                for child in info.find_all("div"):
                    child.decompose()
                dfn = info.get_text().strip()
                def_list.append((word_type, dfn))
    return def_list


def get_synonyms_list(soup:BeautifulSoup) -> list:
    synonyms = []
    for syns in soup.find_all("a", class_="word"):
        syn = syns.text
        synonyms.append(syn)
    return synonyms


def display_definitions(entry_list:list, word:str) -> None:
    """
    Prints the list of definitions to the console
    """
    print(f"\nDefinitions of {word}:")
    print("-" * (MAX_WIDTH + INDENT_WIDTH))
    for count, entry in enumerate(entry_list):
        count_str = str(count + 1) + "."
        print(
            f"{count_str:<4}{entry[0]:<9}{wrap_text(entry[1].capitalize(),MAX_WIDTH, INDENT_WIDTH)}"
        )


# def display_synonyms(syn_list, word):
#     print(f"\n---------- Synonyms of {word}:\n")
#     for count, syn in enumerate(syn_list):
#         print(f"{syn}, ", end="")
#         if (count + 1) % 7 == 0:
#             print()
#     print("\n\n")


def display_synonyms(syn_list:list, word:str) -> None:
    """
    Prints the list of synonyms to the console
    """
    print(f"\nSynonyms of {word}:")
    print("-" * (MAX_WIDTH + INDENT_WIDTH))
    syn_str = ", ".join(syn_list)
    print(wrap_text(syn_str, MAX_WIDTH + INDENT_WIDTH))
    print("\n\n")


def wrap_text(text:str, max_width=80, indent_width=0) -> str:
    """
    Wraps text at word breaks at or before max_width chars, 
    each line is indented indent_width chars.
    """
    word_list = text.split(" ")
    sum_chars = 0
    new_word_list = []
    for word in word_list:
        sum_chars += len(word) + 1
        if sum_chars >= max_width:
            word = "\n" + " " * indent_width + word
            new_word_list.append(word)
            sum_chars = len(word) - 1
        else:
            new_word_list.append(word)
    return " ".join(new_word_list)


def main():

    word = get_word_from_argv()
    url = build_url_with_word(URL_1, word)
    soup = make_soup(url)
    if word == "":
        word = get_random_word(soup)

    definitions = get_definitions_list(soup)
    synonyms = get_synonyms_list(soup)

    if len(definitions) < 1:
        print(f"\nNo definitions for '{word}'\n")
    else:
        display_definitions(definitions, word)
        display_synonyms(synonyms, word)


if __name__ == "__main__":
    main()
