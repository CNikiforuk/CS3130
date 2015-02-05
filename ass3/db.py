import argparse, random, socket, sys, getpass

MAX_BYTES = 65535

class database:

    def __init__(self, infile):
        self.infile = infile
        self.users = []
        file = open(self.infile, 'r')
        for line in file:
            line = line.rstrip()
            if line:
                name, pw = line.split(":")
                self.users.append([name, pw, 0])
                
    def loginUser(self, line):
        name, pw = line.split(':')
        for i in range(len(self.users)):
            if (self.users[i][0] == name):
                if(self.users[i][1] == pw):
                    self.users[i][2] = 1
                    return 1
            
        return 0

class user:
    def __init__(self, name, pw):
        self.info = [name,pw,0]


    

#def dbOpen(infile):
#    with open(self.infile, 'r') as file:
       
    
def main():
    db = database('users')
    for i in range(len(db.users)):
        print("name: ",db.users[i][0]," pass: ",db.users[i][1]," online: ",db.users[i][2])
    print(db.loginUser("car:super"))

#main()