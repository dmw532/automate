# mcb.pyw - Saves and loads pieces of text to the clipboard
# Usage: py.exe mcb.pyw save <keyword> - Saves current clipboard to keyword
#        py.exe mcb.pyw <keyword> - Loads keyword to clipboard
#        py.exe mcb.pyw list - Lists all keywords and content to clipboard 

import shelve
import pyperclip
import sys
import argparse

# TODO: Add delete keyword, and delete all keywords

class MultiClipBoard:
    def __init__(self):
        self.mcbShelf = shelve.open('mcb')
        self.arg_parser()
        self.arg_handler()
        self.mcbShelf.close()

    def save_keyword(self):
        self.mcbShelf[self.args.save] = pyperclip.paste()
        print(self.args.save)
        print(pyperclip.paste())

    def list_keywords(self):
        keyword_list = str(list(self.mcbShelf.keys()))
        pyperclip.copy(keyword_list)
        print("Keys: %s" % keyword_list)

    def get_keyword(self):
        pyperclip.copy(self.mcbShelf[self.args.keyword])

    def delete_keyword():
        pass 

    def delete_all_keywords():
        pass

    def arg_handler(self):
        if self.args.save:
            self.save_keyword()
        elif self.args.list:
            self.list_keywords()
        elif self.args.keyword:
            self.get_keyword()
        else:
            print("No args used. Please see --help")

    def arg_parser(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-s', '--save', help='Save keyword to system')
        self.parser.add_argument('-l', '--list', action='store_true', help="Lists all keywords and their assigned content")
        self.parser.add_argument('-k', '--keyword', help="Returns the content for the queried keyword")
        self.args = self.parser.parse_args()

mcb = MultiClipBoard()
