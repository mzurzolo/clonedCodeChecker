#!/usr/bin/env python3

import re


class matcher:

    def __init__(self):
        #self.prototype = re.compile('[a-zA-Z0-9_]*?\s+[a-zA-Z0-9_]*?[(][a-zA-Z0-9_]*?[)];')#'.*\(.*\);')
        self.assignment = re.compile('\s*[a-zA-Z0-9_]*?\s*=.*?;')
        self.ifstatement = re.compile('\s*if.*?')
        self.comment = re.compile('\s*([/][/].*?\n|[/][*].*?[*][/]|[*].*?\n)')
        self.integer2 = re.compile('\s*[0-9]+[.][0-9]*?')

    def printMatches(self, code):

        for n in code:
            print("line: ", n)
            if self.assignment.match(n):

                input("assignment---------------------------------------------")
                input(n)
            if self.ifstatement.match(n):

                input("if---------------------------------------------")
                input(n)
            if self.comment.match(n):

                input("comment---------------------------------------------")
                input(n)
            if self.integer2.match(n):

                input("integer2---------------------------------------------")
                input(n)
