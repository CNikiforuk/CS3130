
################--Description--#################
#Basic employee database functions file.

################-----Author-----#################
#Carlos Nikiforuk


ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 16

##################################
class database:
#Database class that is instantiated and associated with the infile
#Support could be added for operations between distinct databases
##################################

    def __init__(self, infile):
        self.infile = infile

    ##################################
    def addEmployee(self, line):
    #Add Employee to database, expects complete string passed
    ##################################
         with open(self.infile, 'a') as file:
            file.write(line+"\n")
    
    ##################################    
    def findEmployee(self, id):
    #Find Employee in database. ID passed in, fields returned
    ##################################
        with open(self.infile, 'r') as file:
                for line in file:
                    line = line.rstrip()
                    if line:
                        fields = line.split(":")
                        if(fields[ID] == id):
                            file.close()
                            return fields  
        return 0
        
    ##################################
    def removeEmployee(self, f):
    #Remove employee from database, fields passed
    ##################################
        new = []
        file = open(self.infile, 'r')
        for line in file:
            line = line.rstrip()
            fields = line.split(":")
            if(fields != f):
                new.append(line+'\n')
        new.append("\n")
        with open(self.infile, 'w') as file:
            file.writelines(new)
            file.close()
                
    ##################################
    def showEmployees(self):
    #Print whole database, formatted
    ##################################
        print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
        print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
        with open(self.infile, 'r') as file:
                for line in file:
                    line = line.rstrip()
                    if line:
                        fields = line.split(":")
                        self.printEmployee(fields) 

    ##################################    
    def printEmployee(self, fields):
    #Print an Employee line, Employee field passed
    ##################################
        print("{0:<4} {1:<{n}} {2:<{n}} {3:<15}".format(fields[ID], fields[FIRST], fields[LAST], fields[DEPT], n=MAXNAMESIZE))
