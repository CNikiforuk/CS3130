Author: Carlos Nikiforuk
CS 3130 Ass #3
Date: Feb 12, 2015

https://github.com/CNikiforuk/CS3130/tree/master/ass3

--------------------Description---------------------

Python Client server messaging system

How to use the program:

1. python3 main.py <server/client> <ip>
2. Login with username and password. User info located in file 'users'


--------------------Example Run---------------------

****SERVER****
$ python3 main.py server localhost
Listening at ('127.0.0.1', 1060)
Feb 12 2015 12:24:41: Login attempt by: ('127.0.0.1', 54954)
Feb 12 2015 12:24:41: francoc logged in. Address:  ('127.0.0.1', 54954)

Feb 12 2015 12:24:44: francoc: whoison
Feb 12 2015 12:24:53: francoc: send hello hey hello!
Feb 12 2015 12:25:05: francoc: signout


****CLIENT****
$ python3 main.py client localhost
Client socket name is ('127.0.0.1', 53803)

-----Signin to MMS!-----

Enter username: francoc
Password: 
Login Successful!

-----Welcome to MMS!-----

The following commands are supported:

whoIsOn
send <user> <message>
signout


>whoison
>>francoc
>>
>send hello hey hello!
>>User is offline, message will be sent when they signin.
>signout
>Thank you for using MMS!


----------------Additional Information-----------------
-A server logfile is kept and is called server.log

-Undelivered messages are kept in file located at messages/<username>

-The users logged on is kept in memory, rather than a file. This means if the server restarts the users logged on at that time will need to sign in and authorize themselves again.

-You cannot sign in if the server detects you are already online. I chose this option over kicking someone off.
This does raise the issue where if the client terminates without signing out, the server will think you are online.
The simple solution is to restart the server, future implementations could check every so often to see if client is alive.

-You CAN send messages to yourself, much like how people talk to themselves






