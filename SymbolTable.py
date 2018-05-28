#!/usr/bin/python



class Symbol(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type
    #


class SymbolTable(object):

    def __init__(self, name, parent): # parent scope and symbol table name
        self.symbols = {}
        self.parent = parent
        self.name = name
    #

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        inscope = self.symbols.get(name)
        if inscope:
            return inscope
        else:
            if self.parent is not None:
                self.parent.get(name)
            else:
                return None # No variable of given name
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name):
        SymbolTable(self, name)
    #

    def popScope(self):
        return self.parent
    #


