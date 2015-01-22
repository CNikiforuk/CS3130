
################--Description--#################
#Basic employee database functions file.

################-----Author-----#################
#Carlos Nikiforuk


ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 16
IDLENGTH = 4


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
class database:
#Database class that is instantiated and associated with the infile
#Support could be added for operations between distinct databases
##################################

    def __init__(self, infile):
        self.infile = infile

    ##################################
    def addEmployee(self):
    #Add Employee to database, expects complete string passed
    ##################################
        try:
            line = input("Enter employee string to add: ") #xxxx:first:last:dept
            line = line.rstrip()
            fields = line.split(":")
            if(MAXNAMESIZE < max([len(fields[FIRST]), len(fields[LAST]), len(fields[DEPT])])):
                print("Name or dept too long!")
            elif(len(fields[ID]) != IDLENGTH or int(fields[ID]) < 0):
                print("Bad ID!")
            
            else:
                f = self.getEmployee(fields[ID])
                if(f==0):
                    with open(self.infile, 'a') as file:
                        file.write(line+"\n")
                    print("\nEmployee {0} Added!".format(fields[ID]))
                else:
                    print("Entry already exists!")       

        except IndexError:
            print("Error: Incomplete string!")
        except TypeError:
            print("Error: Bad String!")
        except ValueError:
            print("Error: Incorrect ID format!")
        except Exception as e:
            print("Error: ",e)
    
    ##################################    
    def findEmployee(self):
    #Find Employee in database. ID passed in, fields returned
    ##################################
        try:
            id = input("Enter employee ID to find: ")
            while(len(id) != IDLENGTH):
                print("Bad ID!")
                id = input("Enter employee ID to find: ")
            with open(self.infile, 'r') as file:
                    for line in file:
                        line = line.rstrip()
                        if line:
                            fields = line.split(":")
                            if(fields[ID] == id):
                                print("\nEmployee {0} Found!".format(fields[ID]))
                                print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
                                print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
                                self.printEmployee(fields)
                                return

            print("\nEmployee {0} not found!".format(id))

        except IndexError:
            print("Error: Incomplete string!")
        except TypeError:
            print("Error: Bad String!")
        except Exception as e:
            print("Error: ",e)

    ##################################
    def getEmployee(self, id):
    #get Employee field from database. ID passed in, fields returned
    ##################################
        try:
            with open(self.infile, 'r') as file:
                for line in file:
                    line = line.rstrip()
                    if line:
                        fields = line.split(":")
                        if(fields[ID] == id):
                            file.close()
                            return fields
            return 0
        except TypeError:
            print("Error: Bad String!")
        except Exception as e:
            print("Error: ",e)
        
    ##################################
    def removeEmployee(self):
    #Remove employee from database, fields passed
    ##################################
        try:

            id = input("\nEnter employee ID to remove: ")
            f = self.getEmployee(id)
            if(f == 0):
                print("\nEmployee not found!")
                return 0
            else:
                print("Employee found: ")
                print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
                print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
                self.printEmployee(f)
                verify = input("\nAre you sure you with to delete this employee (y/n)? " )
                if(verify == 'y'):
                    new = []
                    file = open(self.infile, 'r')
                    for line in file:
                        line = line.rstrip()
                        if(line.strip()):
                            fields = line.split(":")
                            if(fields != f and fields !=""):
                                new.append(line+'\n')
                    new.append("\n")
                    with open(self.infile, 'w') as file:
                        file.writelines(new)
                        file.close()
                    print("\nEmployee ",id," removed!")
        except IndexError:
            print("Error: Incomplete string!")
        except TypeError:
            print("Error: Bad String!")
        except Exception as e:
            print("Error: ",e)
                
    ##################################
    def showEmployees(self):
    #Print whole database, formatted
    ##################################
        try:
            print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
            print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
            with open(self.infile, 'r') as file:
                    for line in file:
                        line = line.rstrip()
                        if line:
                            fields = line.split(":")
                            self.printEmployee(fields)
        except IndexError:
            print("Error: Incomplete string!")
        except TypeError:
            print("Error: Bad String!")
        except Exception as e:
            print("Error: ",e)

    ##################################    
    def printEmployee(self, fields):
    #Print an Employee line, Employee field passed
    ##################################
        print("{0:<4} {1:<{n}} {2:<{n}} {3:<15}".format(fields[ID], fields[FIRST], fields[LAST], fields[DEPT], n=MAXNAMESIZE))
