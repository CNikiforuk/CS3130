#!/usr/bin/env python3

#make message protocol to specify login, message, special, source user, etc.
#implement threads

import argparse, random, socket, sys, getpass, db, threading, re
from datetime import datetime

MAX_BYTES = 65535

class message:

    def __init__(self, type, text):
        self.type = type
        #self.time
        self.text = text
        
    def toString(self):
        return self.type+':'+self.text
        
def toMessage(text):
        fields = text.split(':',1)
        return message(fields[0], fields[1])
        
def loginPrompt(sock, delay):
    print("\n-----Signin to MMS!-----\n")
    user = input('Enter username: ')
    password = getpass.getpass()
    
    msg = message('0',(user+':'+password))
    text = msg.toString()
    data = str(text).encode('ascii')
    
    while True:
        sock.send(data)
        sock.settimeout(delay)
        try:
            inData = sock.recv(MAX_BYTES)
            inMsg = toMessage(inData.decode('ascii'))
        except socket.timeout as exc:
            delay *= 2  # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc
        else:
            break
            
    return(inMsg)
    
    
    
def server(interface, port):                                        #SERVER
    userDB = db.database('users')
    helpText = "The following commands are supported:\n\nwhoIsOn\nsend <user> <message>\nsignout"
    
    msgFiles = {}
    for k in userDB.users.keys():
        try:
            msgFiles[k] = open('messages/'+k, 'r+')
        except FileNotFoundError:
            msgFiles[k] = open('messages/'+k, 'w+')
            
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())

    while True:
        inData, address = sock.recvfrom(MAX_BYTES)
        inMsg = toMessage(inData.decode('ascii'))
        
        if(inMsg.type == '0'):
            print("Attempt login!") #check database
            name, pw = inMsg.text.split(':',1)
            attempt = userDB.loginUser(name, pw, address)
            if(attempt == 0):
                msgFiles[name].seek(0)
                msg = message('0',"Login Successful!\n\n-----Welcome to MMS!-----\n\n"+helpText+"\n\n")
                for line in msgFiles[name]:
                    msg.text = msg.text + '>>' + line +'\n'
                print(msgFiles[name].read())
                msgFiles[name].seek(0)
                msgFiles[name].truncate()
                user = userDB.getUser(address)
                #THREAD DELEGATION MAYBE
                
            elif(attempt == -1):
                msg = message('-1',"Inocorrect username or password!")
            else:
                msg = message('-1',"User is already logged in!")
            
        elif(inMsg.type == '1'):
            tokens = inMsg.text.lstrip().split(' ',2)
            print(tokens)
            if(tokens[0] == 'send'):
                if(len(tokens) >= 3):
                    msg = message('1', 'sent!')
                    outMsg = message('1', user+': '+tokens[2])
                    outData = outMsg.toString().encode('ascii')
                    if tokens[1] in userDB.users.keys():
                        if(userDB.users[tokens[1]][2] == 1):
                            print("ATTEMPTING SEND")
                            sock.sendto(outData, userDB.users[tokens[1]][0])
                        else:
                            msg = message('1', 'User is offline, message will be sent when they signin.')
                            msgFiles[tokens[1]].write(outMsg.text+'\n')
                            msgFiles[tokens[1]].flush()
                    else:
                        msg = message('1', 'User doesnt exist!')
                else:
                    msg = message('1', 'Incorrect send format!')

            elif(tokens[0] == 'signout'):
                msg = message('5', 'signout!')
                userDB.signOut(user)
                #signout
            elif(tokens[0] == 'whoison'):
                msg = message('1',userDB.whoison())
            else:
                msg = message('1', helpText)
        
        #print("Sending out: '" + outMsg.text +"'")
        data = msg.toString().encode('ascii')
        sock.sendto(data, address)
        
def receiver(sock):
    while True:
        sock.setblocking(True)
        data = sock.recv(MAX_BYTES)
        rmsg = toMessage(data.decode('ascii'))
        print('>'+(rmsg.text))
        if(rmsg.type == '5'):
            sys.exit(0)
        print('>',end='',flush=True)
            
def sender(sock):
     while True:
        delay = 0.1  # seconds
        #t = "{}: ".format(datetime.now().strftime('%b %d %Y %H:%M:%S')); #nice format
        text = input('>')
        msg = message('1',text)
        text = msg.toString()
        data = text.encode('ascii')
        sock.send(data)
        if(msg.text == 'signout'):
            sys.exit(0)
            
def client(hostname, port):                                         #CLIENT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))
    
    while (True):
        login = message('','')
        while(login.type != '0'):
            login = loginPrompt(sock, 0.1)
            print(login.text)
            
        
        receive = threading.Thread(target=receiver, args=(sock,))
        receive.start()
        send = threading.Thread(target=sender, args=(sock,))
        send.start()
        
        while(receive.isAlive()):
            pass
        
        
        

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive UDP,'
                                     ' pretending packets are often dropped')
    parser.add_argument('role', choices=choices, help='which role to take')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='UDP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)