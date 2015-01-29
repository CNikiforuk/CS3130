MAXDIGITS = 8

import string
import operator

class dictionary:
    
    def __init__(self, infile):
        self.infile = infile

    ##################################
    def processFile(self):                 
    #process input file, display word table/histo
    ##################################
        with open(self.infile, 'r') as file:
            new = ""
            scount = 0
            file = file.read()
            for i in range(len(file)):
                if file[i].isalpha():
                    new = new + file[i].lower()
                    scount = 0
                elif (scount == 0):
                    new = new + " "
                    scount = scount + 1

        lista = new.strip().split(' ')

        d = {}
        for i in range(len(lista)):
            if(lista[i] in d):
                d[lista[i]] = d[lista[i]] + 1
            else:
                d[lista[i]] = 1

        maxW = 0
        for key in d.keys():
            if(len(key) > maxW):
                maxW = len(key)
             
        print("\nWord Table {0:<{m}} Histogram".format("", m=maxW+MAXDIGITS-10))
        print("{0:-<{m}}".format("", m=maxW+MAXDIGITS+15)) #15 is for 10 histogram X's + number in brackets
        for key, value in d.items():
            if(value > 10):
                print("{0:<{m}} {1:<{d}} | {2:X<{n}} ({3})".format(key, value, "", value-10,n=10, m=maxW, d=MAXDIGITS))
            else:
                print("{0:<{m}} {1:<{d}} | {2:X<{v}}".format(key, value, "", v=value, m=maxW, d=MAXDIGITS))
                


