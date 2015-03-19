################--Description--#################
#Basic employee database functions file.

################-----Author-----#################
#Carlos Nikiforuk
import re

ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 16
MAXDPTSIZE = 23
IDLENGTH = 4
delimiter = '\0'
#<1:4:16:16:23 STRUCTURE. Maybe parse bytes?

##################################
def displayMenu():
#display start menu 
##################################
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
    return a

##################################
def padString(string, char, reqSize):
#Add padding to string, with char
##################################
    if(len(string) < reqSize):
            string = string + "{0:{c}<{i}}".format("", i=reqSize - len(string), c = char)
    return string

##################################
def addEmployee():
#Add Employee to database, expects complete string passed
##################################
    
    eid = input("Enter employee ID: ")
    format = re.match('[\d]'+'{'+repr(IDLENGTH)+'}',eid)
    while (not format):
        print("EID has to be "+repr(IDLENGTH)+" digits long.")
        eid = input("Enter employee ID: ")
        format = re.match('[\d]'+'{'+repr(IDLENGTH)+'}',eid)
    
    fname = input("Enter employee first name: ") #xxxx:first:last:dept
    lname = input("Enter employee last name: ")
    dpt = input("Enter employee department: ")
    
    
    if(MAXNAMESIZE < max([len(fname), len(lname)]) or MAXDPTSIZE < len(dpt)):
        return -1
    else:
        return str('1:'+eid+':'+fname+':'+lname+':'+dpt)    

##################################    
def findEmployee():
#Find Employee in database. ID passed in, fields returned
##################################
    try:
        eid = input("Enter employee ID to find: ")
        format = re.match('[\d]'+'{'+repr(IDLENGTH)+'}',eid)
        while(not format):
            print("Bad ID!")
            eid = input("Enter employee ID to find: ")
            format = re.match('[\d]'+'{'+repr(IDLENGTH)+'}',eid)
        string = '2:'+eid
        return string
        
    except IndexError:
        print("Error: Incomplete string!")
    except TypeError:
        print("Error: Bad String!")
        
    
##################################
def removeEmployee():
#Remove employee from database, fields passed
##################################
    try:
        eid = input("Enter employee ID to remove: ")
        format = re.match('[\d]'+'{'+repr(IDLENGTH)+'}',eid)
        while(not format):
            print("Bad ID!")
            eid = input("Enter employee ID to remove: ")
            format = re.match('[\d]'+'{'+repr(IDLENGTH)+'}',eid)
        string = '3:'+eid
        return string
        
    except IndexError:
        print("Error: Incomplete string!")
    except TypeError:
        print("Error: Bad String!")
            
##################################
def showEmployees():
#Print whole database, formatted
##################################
    try:
        string = '4:'
        return string
        
    except IndexError:
        print("Error: Incomplete string!")
    except TypeError:
        print("Error: Bad String!")
        
##################################
def exit():
#Print whole database, formatted
##################################
    string = '5:'
    return string
    

##################################    
def printEmployee(fields):
#Print an Employee line, Employee field passed
##################################
    print("{0:<{i}} {1:<{n}} {2:<{n}} {3:<{d}}".format(fields[ID], fields[FIRST], fields[LAST], fields[DEPT], i=IDLENGTH, n=MAXNAMESIZE, d=MAXNAMESIZE))
    
def main():
    print(addEmployee())
    
if __name__ == '__main__':
    main()
