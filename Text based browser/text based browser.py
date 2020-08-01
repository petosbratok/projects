#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8

import os
import sys
import requests
from bs4 import BeautifulSoup
import colorama
from colorama import Fore, Back
colorama.init()

def urlIsValid(user_responce):
    if '.' in list(user_responce):
        return True
    else:
        printError('Incorrect URL')


def printError(errorname):
    print(f'Error: {errorname}')


def main():
    opened_pages = []
    arglist = sys.argv
    responceEqualsBack = False

    if len(arglist) == 2:
        filename = arglist[1]
        if not os.path.exists(filename):
            os.makedirs(filename)

    while True:
        responceEqualsBack = False
        user_responce = input('> ')
        if user_responce == 'exit':
            exit(0)
        if user_responce == 'back':
            if len(opened_pages) >= 2:
                opened_pages.pop(-1)
                user_responce = f'{opened_pages.pop(-1)}'
                responceEqualsBack = True
            else:
                printError('No pages come back to')
                continue
        if not urlIsValid(user_responce):
            continue
        site_name = user_responce
        print(site_name)
        try:
            site_responce = requests.get(site_name)
        except:
            printError(f'Could not connect to the {user_responce}')
            continue
        site_responce = parseHTML(site_responce)
        print(site_responce)
        opened_pages.append(user_responce)


def nSplit(paragraphs):
    """
    Converts ['1\n2'] to ['1', '2']
    """
    for i in range(len(paragraphs)):
        ispl = paragraphs[i].split('\n')
        if len(ispl) > 1:
            paragraphs[i] = ispl.pop(0)
            for element in ispl[::-1]:
                paragraphs.insert(i+1, element)
            nSplit(paragraphs)
    return paragraphs

def deleteCopies(text, delete_text):
    """
    if text is ['1', '2'] and delete_text is ['1', '1', '2', '2', '2', '3']
    the result is ['1', '2', '2', 3]
    """
    result = []
    for line in text:
        if not line in delete_text:
            result.append(line)

def parseHTML(site_responce):
    """
    Makes the whole text readable, highlights links with blue font
    """
    #tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'ol']
    result = ''
    soup = BeautifulSoup(site_responce.content, 'html.parser')
    text = [element.get_text() for element in soup.find_all(tags)]
    links = [element.get_text() for element in soup.find_all('a')]
    text = nSplit(text)
    for element in text:
        if element in links:
            element = (Fore.BLUE + element + Fore.WHITE)
        result += f'{element}\n'
    return result

if __name__ == '__main__':
    main()
