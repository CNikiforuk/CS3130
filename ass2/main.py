#!/usr/bin/env python3

import sys
import dictFunc

MAXWORDSIZE = 100

################--Description--#################
#Dict

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
