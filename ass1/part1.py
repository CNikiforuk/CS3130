#!/usr/bin/env python3

ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 8

def main():

    print("\nEmployee FMS\n")
    print("Select one of the following:\n")
    print("    1) Add a new employee")
    print("    2) Search for a employee")   
    print("    3) Remove an employee from FMS")
    print("    4) Display the entire employee FMS")

    a = input("\nOption? ")
    while(a < '1' or a > '4'):
        print("Bad input")
        a = input("\nOption? ")

    if  (a=='1'):
        print("Enter employee string to add: ") #xxxx:first:last:dept

    elif(a=='2'):
        id = input("Enter employee ID to find: ")
        f = findEmployee(id)
        if(f == 0):
            print("    Not found!")
        else:
            print("    Found!")
            printEmployee(f)
        
    elif(a=='3'):
        print("Enter employee ID to remove: ")

    elif(a=='4'):
        print("All Records")

def addEmployee():
    infile = open('db.txt', 'r')
    
    print("add")
    
def findEmployee(id):
    with open('db.txt', 'r') as file:
            for line in file:
                line = line.rstrip()
                if line:
                    fields = line.split(":")
                    if(fields[ID] == id):
                        return fields
    return 0
    

def removeEmployee():
    print("remove")

def showEmployees():
    print("show")

def printEmployee(fields):
    print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
    print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
    print("{0:<4} {1:<{n}} {2:<{n}} {3:<15}".format(fields[ID], fields[FIRST], fields[LAST], fields[DEPT], n=MAXNAMESIZE))
    #print("  ID:"+fields[ID]+" Name:" + fields[FIRST]+" "+fields[LAST] + " Dept:"+fields[DEPT])

main()
