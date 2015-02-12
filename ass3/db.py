################--Description--#################
#Database Module

################-----Author-----#################
#Carlos Nikiforuk

import argparse, random, socket, sys, getpass

MAX_BYTES = 65535

##################################
class database:
#Database class containing file handle and user dict.
##################################

    def __init__(self, infile):
        self.infile = infile
        self.users = {}
        file = open(self.infile, 'r')
        for line in file:
            line = line.rstrip()
            if line:
                name, pw = line.split(':',1)
                self.users[name] = [(), pw, 0]
    ##################################    
    def loginUser(self, name, pw, address):
    #login user, returns 1 if already logged in, 0 if success, -1 if fail
    ##################################
        if (name in self.users):
            if(self.users[name][1]==pw):
                if(self.users[name][2]==1):
                    return 1
                else:
                    self.users[name][0] = address
                    self.users[name][2] = 1
                    return 0
            
        return -1

    ##################################
    def signOut(self, name):
    #signout user, no return
    ##################################
        self.users[name][2] = 0
    
    ##################################   
    def whoison(self):
    #return who is online as a string
    ##################################
        online = ''
        for k in self.users.keys():
            if(self.users[k][2] == 1):
                online = online+k+'\n>>'
        return online
    
    ##################################
    def getUser(self, address):
    #Address passed in, user name returned
    ##################################
        for k in self.users.keys():
            if(self.users[k][0] == address):
                return k

class user:
    def __init__(self, name, pw):
        self.info = [name,pw,0]
       
    
def main():
    db = database('users')
    for i in range(len(db.users)):
        print("name: ",db.users[i][0]," pass: ",db.users[i][1]," online: ",db.users[i][2])
    print(db.loginUser("car:super"))

if __name__ == '__main__':
    main()
