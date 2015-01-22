ID, FIRST, LAST, DEPT = range(4)
MAXNAMESIZE = 16

class database:
    def __init__(self, infile):
        self.infile = infile

#    def load(self, infile):
 #       with open(infile, 'r') as file:
 #           open(infile, 'x')
  #      with open(infile, 'r+') as tmp:  
  #          tmp.writelines(file)
  #      file.close()
  #      return tmp

    def addEmployee(self, line):
         with open(self.infile, 'a') as file:
            file.write(line+"\n")
        
    def findEmployee(self, id):
        with open(self.infile, 'r') as file:
                for line in file:
                    line = line.rstrip()
                    if line:
                        fields = line.split(":")
                        if(fields[ID] == id):
                            file.close()
                            return fields  
        return 0
        

    def removeEmployee(self, f):
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
                

    def showEmployees(self):
        print("{0:<4} {1:<{n}} {2:<15}".format("ID", "Name", "Dept", n=MAXNAMESIZE*2))
        print("{0:-<4} {0:-<{n}} {0:-<15}".format("", n=MAXNAMESIZE*2))
        with open(self.infile, 'r') as file:
                for line in file:
                    line = line.rstrip()
                    if line:
                        fields = line.split(":")
                        self.printEmployee(fields) 

    def printEmployee(self, fields):
        print("{0:<4} {1:<{n}} {2:<{n}} {3:<15}".format(fields[ID], fields[FIRST], fields[LAST], fields[DEPT], n=MAXNAMESIZE))
