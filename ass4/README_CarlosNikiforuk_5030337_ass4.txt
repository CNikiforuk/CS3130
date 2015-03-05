Author: Carlos Nikiforuk
CS 3130 Ass #4
Date: March 2, 2015

https://github.com/CNikiforuk/CS3130/tree/master/ass4

--------------------Description---------------------

Python Client server messaging system

How to use the program:

1. python3 main.py <server/client> <ip>


--------------Additional Information----------------

-Server handles clients using threads, main thread listens for connections then delegates to workers.

-Semaphores are in place when writing to database to eliminate race conditions.

-A database log file is kept, and logs when an employee is added or removed.

