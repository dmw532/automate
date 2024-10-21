import pyperclip
import re
import argparse

# TODO: Add more usable search terms - Finish URLS
# TODO: Add Concatenate feature for Temp Account Printing
# TODO: Fix Number parser/regex so that it can grab 07XXX XXXXXX numbers

class ClipboardParser:

    phone_regex = re.compile(r'''(
    ((\+44)|(0))?
    (\d{4})?
    (\d{6})
    )''', re.VERBOSE)

    email_regex = re.compile(r'''(
    [a-zA-Z0-9._%+-]+       # Username part
    @                       # @ symbol
    [a-zA-Z0-9.-]+          # Domain name
    \.[a-zA-Z]{2,4}         # Dot-something (TLD, e.g., .com, .net)
    )''', re.VERBOSE)

    URLS = re.compile(r'''(
    http
    )''', re.VERBOSE)

    username = re.compile(r'''(
    [a-zA-Z0-9]+
    )''', re.VERBOSE)

    workorder = re.compile(r'''(
    (?<=\s)
    \d+
    )''', re.VERBOSE)

    def __init__(self):
        """ Grab information from Clipboard and do something with it"""
        self.text = None
        self.parse_A = None
        self.parse_B = None
        self.arg_parser()
        self.set_parse_terms()
        
        if (self.parse_A != None) or (self.parse_B != None):
            self.get_results()

    def get_results(self):
        self.text = str(pyperclip.paste())
        matches = []
        print(self.parse_A.findall(self.text))
        for groups in self.parse_A.findall(self.text):
            matches.append(''.join(groups[0]+groups[1]))

        for groups in self.parse_B.findall(self.text):
            matches.append(groups)

        if len(matches) > 0:
            pyperclip.copy('\n'.join(matches))
            print('Matches copied to Clipboard!')
            print('\n'.join(matches))

        else:
            print("No matches found..")

    def set_parse_terms(self):
        if self.args.contacts:
            self.contact_details()

        elif self.args.workorders:
            self.override_workorders()
        else:
            print("Please select a search term, see --help for more info")

    def contact_details(self):
        self.parse_A = self.phone_regex
        self.parse_B = self.email_regex

    def find_links(self):
        self.parse_A = self.URLS

    def override_workorders(self):
        """ Process clipboard line by line to extract username and workorder and format as username|workorder|FALSE """
        self.text = str(pyperclip.paste())

        # Split the clipboard text into lines
        lines = self.text.splitlines()

        results = []

        for line in lines:
            # Try to extract a username and a workorder from the line
            username_match = self.username.search(line)
            workorder_match = self.workorder.search(line)

            if username_match and workorder_match:
                # If both a username and a workorder are found, format them
                username = username_match.group(0)
                workorder = workorder_match.group(0)
                results.append(f"{username}|{workorder}|FALSE")
            else:
                # Handle missing data (either username or workorder is missing)
                print(f"Skipping line due to missing data: '{line}'")

        if results:
            formatted_result = '\n'.join(results)
            pyperclip.copy(formatted_result)
            print("Formatted work orders copied to Clipboard!")
            print(formatted_result)
        else:
            print("No valid username and workorder pairs found..")

    def arg_parser(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('-c', '--contacts', action='store_true', help="Contact Details flag")
        self.parser.add_argument('-u', '--urls', action='store_true', help="Grab links from clipboard")
        self.parser.add_argument('-w', '--workorders', action='store_true', help="Grab and build workorder")
        self.args = self.parser.parse_args()

cp = ClipboardParser()
