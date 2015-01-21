#!/usr/bin/env python3

import os

#Author: Carlos Nikiforuk
#Description: Basic employee database stored as txt file.


ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 16
infile = 'db.txt'

def main():

    tmp = load(infile)
    cont = 1
    
    while(cont):
    
        print("\nEmployee FMS\n")
        print("Select one of the following:\n")
        print("    1) Add a new employee")
        print("    2) Search for a employee")   
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
            f = findEmployee(fields[ID])
            if(len(fields[FIRST]) > MAXNAMESIZE or len(fields[LAST]) > MAXNAMESIZE or len(fields[DEPT]) > MAXNAMESIZE):
                print("    Name or dept too long!")
            elif(f == 0 and len(fields[ID]) == 4):
                addEmployee(line)
                print("    Employee ",fields[ID]," Added!")
            else:
                print("    Bad ID or duplicate entry")

        elif(a=='2'):   #search for employee
            with input("Enter employee ID to find: ") as id:
                f = findEmployee(id)
            if(f == 0):
                print("    Not found!")
            else:
                print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
                print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
                printEmployee(f)
            
        elif(a=='3'):   #remove employee
            with input("Enter employee ID to remove: ") as id:
                f = findEmployee(id)
            if(f == 0):
                print("    Employee not found!")
            else:
                removeEmployee(f)
                print("    Employee ",id," removed!")

        elif(a=='4'):   #show employees
            showEmployees()

        elif(a=='5'):    #quit
            cont = 0
        
        if(a != '5'):
            input("\nPress any key to continue")


    tmp.close()
    os.remove("~db.txt")

##Functions

def load(infile):
    with open('db.txt', 'r') as file:
        open('~db.txt', 'x')
        with open('~db.txt', 'r+') as tmp:  
            tmp.writelines(file)
    file.close()
    return tmp

def addEmployee(line):
     with open('db.txt', 'a') as file:
        file.write(line+"\n")
    
def findEmployee(id):
    with open('db.txt', 'r') as file:
            for line in file:
                line = line.rstrip()
                if line:
                    fields = line.split(":")
                    if(fields[ID] == id):
                        file.close()
                        return fields  
    return 0
    

def removeEmployee(f):
        with open(infile, 'r') as file:
            new = []
            for line in file:
                line = line.rstrip()
                fields = line.split(":")
                if(fields != f):
                    new.append(line)
        new.append("\n")
        with open(infile, 'w') as file:
            file.writelines(new)
            file.close()
            

def showEmployees():
    print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
    print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
    with open(infile, 'r') as file:
            for line in file:
                line = line.rstrip()
                if line:
                    fields = line.split(":")
                    printEmployee(fields) 

def printEmployee(fields):
    print("{0:<4} {1:<{n}} {2:<{n}} {3:<15}".format(fields[ID], fields[FIRST], fields[LAST], fields[DEPT], n=MAXNAMESIZE))


main()


