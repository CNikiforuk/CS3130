#!/usr/bin/env python3

import sys
import dictFunc

################--Description--#################
#Dictionary program, generates a word table with frequency, and a visual histogram representation.
#Max word width is set to largest word found in dictionary.
#All extra spaces and non-aplha characters are removed.

################-----Author-----#################
#Carlos Nikiforuk

def main():

    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} <db file>".format(sys.argv[0]))
        exit()
    infile = sys.argv[1]        #check usage
    
    try:                        #check specified file
        open(infile,'r')    
    except FileNotFoundError:
        print("Input file does not exist.")
        exit()
    except Exception as e:
        print("Error: ",e)
        exit()

    
    d = dictFunc.dictionary(infile)
    d.processFile()


main()
