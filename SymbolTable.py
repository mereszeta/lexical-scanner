#!/usr/bin/python



class Symbol(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
    #


class SymbolTable(object):

    def __init__(self, parent, name): # parent scope and symbol table name
        self.symbols = {}
        self.parent = parent
        self.name = name
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        return self.symbols[name]
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        pass
    #

    def popScope(self):
        pass
    #


