#!/usr/bin/env python3

################--Description--#################
#Main Module
#Python client server messaging system

###############-----Author-----#################
#Carlos Nikiforuk

########-CLIENT/SERVER AD HOC PROTOCOL-#########
#~~Message format~~
#<type>:<message>
#Example: 1:send franco documentation
#Example signin: 0:guest:guest

#~~Message Types~~
# -1: failure
# 0: login
# 1: user comm.
# 5: signout (server signs out client)

import argparse, random, socket, sys, getpass, db, threading, re, os
from datetime import datetime

MAX_BYTES = 65535

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
def server(interface, port):                                        #SERVER
#Main Server
##################################

    userDB = db.database('users')
    helpText = "The following commands are supported:\n\nwhoIsOn\nsend <user> <message>\nsignout"

    try:    
        logFile = open('server.log', 'r+')      #check if file exists. if not, create one.
    except FileNotFoundError:
        logFile = open('server.log', 'w+')
    logFile.seek(0,2)                           #seek to end of file.

    msgFiles = {}
    for k in userDB.users.keys():
        try:
            msgFiles[k] = open('messages/'+k, 'r+')
        except FileNotFoundError:
            msgFiles[k] = open('messages/'+k, 'w+')
            
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    
    user = ''

    while True:
        inData, address = sock.recvfrom(MAX_BYTES)
        inMsg = toMessage(inData.decode('ascii'))
        
        if(inMsg.type == '0'):  #message type 0 from client means signin attempt
            serverPrint = "{}: Login attempt by: {}".format(datetime.now().strftime('%b %d %Y %H:%M:%S'),repr(address))
            logFile.write(serverPrint+'\n')
            logFile.flush()
            print(serverPrint)
            name, pw = inMsg.text.split(':',1)
            attempt = userDB.loginUser(name, pw, address)
            if(attempt == 0):   #success
                serverPrint = "{}: {} logged in. Address:  {}".format(datetime.now().strftime('%b %d %Y %H:%M:%S'), name, repr(address))
                logFile.write(serverPrint+'\n')
                logFile.flush()
                print(serverPrint)
                msgFiles[name].seek(0)
                msg = message('0',"Login Successful!\n\n-----Welcome to MMS!-----\n\n"+helpText+"\n\n")
                for line in msgFiles[name]:
                    msg.text = msg.text + '>>' + line +'\n'
                print(msgFiles[name].read())
                msgFiles[name].seek(0)
                msgFiles[name].truncate()
                user = userDB.getUser(address)
                #THREAD DELEGATION MAYBE
                
            elif(attempt == -1): #failure
                msg = message('-1',"Inocorrect username or password!")
            else:
                msg = message('-1',"User is already logged in!")
            
        elif(inMsg.type == '1'): #not a signin request
            if(userDB.getUser(address) != -1):
                serverPrint = "{}: {}: {}".format(datetime.now().strftime('%b %d %Y %H:%M:%S'), user, inMsg.text)
                logFile.write(serverPrint+'\n')
                logFile.flush()
                print(serverPrint)
                tokens = inMsg.text.lstrip().split(' ',2)
                if(tokens[0] == 'send'):
                    if(len(tokens) >= 3):
                        msg = message('1', 'sent!')
                        outMsg = message('1', user+': '+tokens[2])
                        outData = outMsg.toString().encode('ascii')
                        if tokens[1] in userDB.users.keys():
                            if(userDB.users[tokens[1]][2] == 1):
                                print("Sending Message to "+tokens[1])
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
                    msg = message('5', 'Thank you for using MMS!')
                    userDB.signOut(user)
                elif(tokens[0] == 'whoison'):
                    msg = message('1',userDB.whoison())
                else:
                    msg = message('1', helpText)
            else: #user is not recognized, server may have dropped, or user is malicious.
                serverPrint = "{}: Force signout of unauthorized user {}".format(datetime.now().strftime('%b %d %Y %H:%M:%S'), repr(address))
                logFile.write(serverPrint+'\n')
                logFile.flush()
                print(serverPrint)
                msg = message('5','force signout')
        
        #print("Sending out: '" + outMsg.text +"'")
        data = msg.toString().encode('ascii')
        sock.sendto(data, address)


##################################
def loginPrompt(sock, delay):
#Prompts user to login, returns login message from server
##################################
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

################################## 
def receiver(sock):
#Client thread for receiving messages from server
##################################
    while True:
        sock.setblocking(True)
        try:
            data = sock.recv(MAX_BYTES)
            rmsg = toMessage(data.decode('ascii'))
            print('>'+(rmsg.text))
            if(rmsg.type == '5'):   #terminate message. Exit program.
                os._exit(0)
            print('>',end='',flush=True)
        except ConnectionRefusedError:
            print("Problem connecting to server")
            
##################################
def sender(sock):
#Client thread for sending messages to server
##################################
     while True:
        delay = 0.1  # seconds
        text = input('>')
        msg = message('1',text)
        text = msg.toString()
        data = text.encode('ascii')
        sock.send(data)

##################################
def client(hostname, port):                                        #CLIENT
#Main Client
################################## 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))
    
    #login!
    login = message('','')
    while(login.type != '0'):
        login = loginPrompt(sock, 0.1)
        print(login.text)
            
    #begin threads
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
