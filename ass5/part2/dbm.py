################--Description--#################
#Basic serverside database functions

################-----Author-----#################
#Carlos Nikiforuk


FIRST, LAST, DEPT = range(3)
MAXNAMESIZE = 16
MAXDPTSIZE = 22
IDLENGTH = 4


##################################
class database:
#Database class that is instantiated and associated with the infile
#Support could be added for operations between distinct databases
##################################

    def __init__(self, infile):
        self.infile = infile
        self.employees = {}
        self.file = None
        try:
            self.file = open(self.infile, 'r+')
        except FileNotFoundError:
            self.file = open(self.infile, 'w+')
            print("New database created")
            
        for line in self.file:
            line = line.rstrip()
            if line:
                id, fname, lname, dpt = line.split(':',3)
                self.employees[id] = [fname, lname, dpt]

    ##################################
    def addEmployee(self, id, fname, lname, dpt):
    #Add Employee to database, expects complete string passed
    ##################################
        try:
            if(id not in self.employees.keys()):
                self.employees[id] = [fname, lname, dpt]
                self.file.write(id+':'+fname+':'+lname+':'+dpt+'\n')
                self.file.flush()
                return 0
            else:
                return 1
            
        except FileNotFoundError:
            print("Error: Database file not found!")
    
    ##################################    
    def findEmployee(self, id):
    #Find Employee in database. ID passed in, fields returned
    ##################################

        if(id in self.employees.keys()):
            return self.employees[id]
        else:
            return -1
        
    ##################################
    def removeEmployee(self, id):
    #Remove employee from database, fields passed
    ##################################
        try:
            if(id in self.employees.keys()):
                print("Removing...")
                del self.employees[id]
                new = []
                self.file.seek(0)
                for line in self.file:
                    line = line.rstrip()
                    if(line.strip()):
                        fields = line.split(":")
                        if(fields[0] != id and fields !=""):
                            new.append(line+'\n')
                self.file.seek(0)
                self.file.truncate()
                self.file.writelines(new)
                self.file.flush()
                return 0
            else:
                return -1

        except FileNotFoundError:
            print("Error: Database file not found!")
            return 1

                
    ##################################
    def showEmployees(self):
    #Print whole database, formatted
    ##################################

        a = "{0:<{i}} {1:<{n}} {2:<{d}}\n".format("ID", "Name", "Dept",i=IDLENGTH, n=MAXNAMESIZE*2, d=MAXNAMESIZE)
        b = "{0:-<{i}} {0:-<{n}} {0:-<{d}}\n".format("", i=IDLENGTH, n=MAXNAMESIZE*2, d=MAXNAMESIZE)

        text = a+b
        for key in self.employees:
            text += formatEmployee(key, self.employees[key])
        return text
            

##################################    
def formatEmployee(ID, fields):
#Print an Employee line, Employee field passed
##################################
    return "{0:<{i}} {1:<{n}} {2:<{n}} {3:<{d}}\n".format(ID, fields[FIRST], fields[LAST], fields[DEPT], i=IDLENGTH, n=MAXNAMESIZE, d=MAXDPTSIZE)
