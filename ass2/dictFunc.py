MAXWORDSIZE = 100
MAXDIGITS = 8

import string
import operator

class dictionary:
    
    

    def __init__(self, infile):
        self.infile = infile
    
    def processFile(self):
        with open(self.infile, 'r') as file:
            new = ""
            scount = 0;
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
             
 
        print("{0:-<{m}}".format("", m=maxW+MAXDIGITS))
        for key, value in d.items():
            print("{0:<{m}}  {1:<{d}}".format(key, value, m=maxW, d=MAXDIGITS))


