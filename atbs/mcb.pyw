# mcb.pyw - Saves and loads pieces of text to the clipboard
# Usage: py.exe mcb.pyw save <keyword> - Saves current clipboard to keyword
#        py.exe mcb.pyw <keyword> - Loads keyword to clipboard
#        py.exe mcb.pyw list - Lists all keywords and content to clipboard 

import shelve
import pyperclip
import sys
import argparse

class MultiClipBoard:
    def __init__(self):
        mcbShelf = shelve.open('mcb')
        self.arg_parser()
        self.arg_handler()
        # TODO: Save Clipboard content
        # TODO: List keywords
        mcbShelf.close()


    def save_keyword(self):
        mcbShelf[self.args.save] = pyperclip.paste()
        print("Saved %s clipboard as %s" % pyperclip.paste(), self.args.save)

    def list_keywords(self):
        pyperclip.copy(str(list(mcbShelf.keys())))

    def get_keyword(self):
        pyperclip.copy(mcbShelf[self.args.keyword])

    def arg_handler(self):
        if self.args.save:
            print("Save argument called")
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


