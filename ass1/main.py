#!/usr/bin/env python3

import sys
import db

################--Description--#################
#Basic employee database example main run file.

################-----Author-----#################
#Carlos Nikiforuk

#IDEA FOR FUNCTIONIZING, PRINT WHATEVER IS RETURNED. TRY/EXCEPTS, OR SUCCESS MESSAGE, OR FAILURE

ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 16

def main():

    if len(sys.argv) == 1 or sys.argv[1] in {"-h", "--help"}:
        print("usage: {0} <db file>".format(sys.argv[0]))
        exit()
    
    infile = sys.argv[1]

    db1 = db.database(infile)
    cont = True
    
    while(cont):
    
        print("\n-----------Employee FMS-----------\n")
        print("Select one of the following:\n")
        print("    1) Add a new employee")
        print("    2) Search for an employee")   
        print("    3) Remove an employee from FMS")
        print("    4) Display the entire employee FMS")
        print("    5) Quit")

        a = input("\nOption? ")
        while(a < '1' or a > '5'):
            print("Invalid input")
            a = input("\nOption? ")

        if  (a=='1'):   #add employee
            line = input("Enter employee string to add: ") #xxxx:first:last:dept
            line = line.rstrip()
            fields = line.split(":")
            f = db1.findEmployee(fields[ID])
            try:
                if(MAXNAMESIZE < max([len(fields[FIRST]), len(fields[LAST]), len(fields[DEPT])])):
                    print("Name or dept too long!")
                elif(f == 0 and len(fields[ID]) == 4):
                    db1.addEmployee(line)
                    print("Employee ",fields[ID]," Added!")
                else:
                    print("Error: Bad ID or duplicate entry")
            except IndexError:
                print("Error: Incomplete string!")
            except Exception as e:
                print("Error: ",e)

        elif(a=='2'):   #search for employee
            id = input("Enter employee ID to find: ")
            f = db1.findEmployee(id)
            if(f == 0):
                print("\nNot found!")
            else:
                print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
                print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
                db1.printEmployee(f)
            
        elif(a=='3'):   #remove employee
            id = input("\nEnter employee ID to remove: ")
            f = db1.findEmployee(id)
            if(f == 0):
                print("\nEmployee not found!")
            else:
                print("Employee found: ")
                print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
                print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
                db1.printEmployee(f)
                verify = input("\nAre you sure you with to delete this employee (y/n)? " )
                if(verify == 'y'):
                    db1.removeEmployee(f)
                    print("\nEmployee ",id," removed!")

        elif(a=='4'):   #show employees
            db1.showEmployees()

        elif(a=='5'):    #quit
            cont = False
        
        if(a != '5'):
            input("\nPress enter to continue...")


main()
