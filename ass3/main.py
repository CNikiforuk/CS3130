#!/usr/bin/env python3

#make message protocol to specify login, message, special, source user, etc.
#make client understand message and login, checking database.

import argparse, random, socket, sys, getpass, db
from datetime import datetime

infile = "users"
userDB = db.database(infile)

MAX_BYTES = 65535

class message:

    def __init__(self, type, text):
        self.type = type
        self.text = text
        
    def toString(self):
        return self.type+':'+self.text
        
def toMessage(text):
        fields = text.split(':',1)
        return message(fields[0], fields[1])

def loginPrompt(sock, delay):
    user = input('Enter username: ')
    password = getpass.getpass()
    
    msg = message('0',(user+':'+password))
    text = msg.toString()
    data = str(text).encode('ascii')
    
    while True:
        sock.send(data)
        print('Waiting up to {} seconds for a reply'.format(delay))
        sock.settimeout(delay)
        try:
            data = sock.recv(MAX_BYTES)
        except socket.timeout as exc:
            delay *= 2  # wait even longer for the next request
            if delay > 2.0:
                raise RuntimeError('I think the server is down') from exc
        else:
            break
            
    print('The server says {!r}'.format(data.decode('ascii')))
    

def server(interface, port):                                        #SERVER
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((interface, port))
    print('Listening at', sock.getsockname())
    while True:
        data, address = sock.recvfrom(MAX_BYTES)
        if random.random() < 0.5:
            print('Pretending to drop packet from {}'.format(address))
            continue
        text = data.decode('ascii')
        #print(text[0])
        msg = toMessage(text)
        if(msg.type == '0'):
            print("Attempt login!") #check database
            if(userDB.loginUser(msg.text) == 1):
                text = "Login Successful!"
            
        elif(msg.type == '1'):
            print('The client at {} says {!r}'.format(address, msg.text))
            text = str(msg.toString())
        
        print("Sending out: " + text)
        data = text.encode('ascii')
        
        #message = 'Your data was {} bytes long'.format(len(data))
        sock.sendto(data, address)

def client(hostname, port):                                         #CLIENT
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    hostname = sys.argv[2]
    sock.connect((hostname, port))
    print('Client socket name is {}'.format(sock.getsockname()))
    
    loginPrompt(sock, 0.1)
    
    while True:
        delay = 0.1  # seconds
        #t = "{}: ".format(datetime.now().strftime('%b %d %Y %H:%M:%S')); #nice format
        text = input('>')
        msg = message('1',(text))
        text = msg.toString()
        print("Sending out: "+text)
        data = text.encode('ascii')
        while True:
            sock.send(data)
            print('Waiting up to {} seconds for a reply'.format(delay))
            sock.settimeout(delay)
            try:
                data = sock.recv(MAX_BYTES)
            except socket.timeout as exc:
                delay *= 2  # wait even longer for the next request
                if delay > 2.0:
                    raise RuntimeError('I think the server is down') from exc
            else:
                break   # we are done, and can stop looping

        print('The server says {!r}'.format(data.decode('ascii')))

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
