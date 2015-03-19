#!/usr/bin/env python3
################--Description--#################
#Main Module
#Python client/server TCP database system

#https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter06/safe_tls.py

###############-----Author-----#################
#Carlos Nikiforuk


import argparse, socket, sys, threading, user, dbm, dbLog
from datetime import datetime


ADD, FIND, REMOVE, SHOW, EXIT = range(1,6)
MDict = {ADD:"ADD", FIND:"FIND", REMOVE:"REMOVE", SHOW:"SHOW", EXIT:"EXIT"}
delimiter = '\0'

##################################    
def server(interface, port):
#main server
################################## 
    
    #create log and db objects
    log = dbLog.log('db.log')
    
    employeeDB = dbm.database('employees')
    dbSem = threading.Semaphore()
    
    threads = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('  Connection accepted from', sockname)
        print('  Socket name:', sc.getsockname())
        print('  Socket peer:', sc.getpeername())
        print('  Creating Thread: #', len(threads))
        t = threading.Thread(target=serverCon, args=(sc,employeeDB, dbSem, log,))
        threads.append(t)
        t.start()

##################################
def client(host, port):
#Main Client
##################################
    import user

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())

    while True:
        choice = user.displayMenu()

        if(int(choice) == ADD):
            text = user.addEmployee()
        elif(int(choice) == FIND):
            text = user.findEmployee()
        elif(int(choice) == REMOVE):
            text = user.removeEmployee()
        elif(int(choice) == SHOW):
            text = user.showEmployees()
        elif(int(choice) == EXIT):
            text = user.exit()

        sock.sendall((text+delimiter).encode("utf-8"))
        text = recvall(sock)

        if(text == '5'):
            print("Exiting...")
            sys.exit(0)
      
        print(text)
        input("\nPress any key to continue...")
##################################
def serverCon(sc, db, sem, log):
#Server worker thread
##################################

    while True:
        outText = ''        
        text = recvall(sc)
        msg = toMessage(text)
        print('  Incoming message from '+repr(sc.getpeername())+': '+MDict[int(msg.type)]+" "+msg.text)

        if(int(msg.type) == ADD):    #ADD EMPLOYEE
            eid, fname, lname, dpt = msg.text.split(':',3)
            sem.acquire()
            suc = db.addEmployee(eid.rstrip(), fname.rstrip(), lname.rstrip(), dpt.rstrip());
            if(suc == 0):
                outText = "Employee "+eid.rstrip()+" added."
                print(outText)
                log.makeEntry(outText)
            elif(suc == 1):
                outText = "Employee "+eid.rstrip()+" already exists."
                print(outText)
            sem.release()
            
        elif(int(msg.type) == FIND):  #FIND EMPLOYEE
            eid = msg.text.rstrip()
            suc = db.findEmployee(eid)
            if(suc == -1):
                outText =eid+' not found!'
            else:
                outText = eid+' '+suc[0]+' '+suc[1]+' '+suc[2]
            
        elif(int(msg.type) == REMOVE):  #REMOVE EMPLOYEE
            sem.acquire()
            suc = db.removeEmployee(msg.text.rstrip())
            if(suc == 0):
                outText = "Employee "+msg.text.rstrip()+" removed."
                print(outText)
                log.makeEntry(outText)
            sem.release()
            
        elif(int(msg.type) == SHOW):  #SHOW EMPLOYEES
            outText = db.showEmployees()
            
        elif(int(msg.type) == EXIT):  #EXIT
            sc.sendall('5\0'.encode('utf-8'))
            sys.exit(0)
            
        outText = outText+delimiter
        sc.sendall(outText.encode('utf-8'))
        
        

##################################
class message:
#Message class, contains message type and text
##################################
    
    def __init__(self, type, text):
        self.type = type
        #self.time = datetime.now().strftime('%b %d %Y %H:%M:%S')
        self.text = text
        
    ##################################
    def toString(self):
    #Converts message to its string representation
    ##################################    
        return self.type+':'+self.text

##################################       
def toMessage(text):
#Returns message object of passed in text
##################################
        fields = text.split(':',1)
        return message(fields[0], fields[1])


##################################
def recvall(sock):
#Receives string from sock, null terminated
##################################
    data = b''
    while True:
        more = sock.recv(1)
        if (more.decode('utf-8') == delimiter):
            break
        else:
            data += more

    return data.decode('utf-8')


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=2015,
                        help='TCP port (default 2015)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)
