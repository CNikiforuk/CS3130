#!/usr/bin/env python3

import sys
import db

################--Description--#################
#Basic employee database example main run file.

################-----Author-----#################
#Carlos Nikiforuk

#IDEA FOR FUNCTIONIZING, PRINT WHATEVER IS RETURNED. TRY/EXCEPTS, OR SUCCESS MESSAGE, OR FAILURE

ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 11

def main():

    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} <db file>".format(sys.argv[0]))
        exit()
    infile = sys.argv[1]
    
    try:
        open(infile,'r')
    except FileNotFoundError:
        print("Input file does not exist.")
        ans = input("Would you like to create it as a new database? (y/n)? ")
        if(ans == 'y'):
            open(infile, 'x')
        else:
            exit()
    except Exception as e:
        print("Error: ",e)
            

    db1 = db.database(infile)
    cont = True
    
    while(cont):
    
        choice = db.displayMenu()

        if  (choice == '1'):   #add employee
            db1.addEmployee()

        elif(choice == '2'):   #search for employee
            db1.findEmployee()

        elif(choice == '3'):   #remove employee
            db1.removeEmployee()

        elif(choice == '4'):   #show employees
            db1.showEmployees()

        elif(choice == '5'):   #quit
            cont = False
        
        if(choice != '5'):
            input("\nPress enter to continue...")


main()
