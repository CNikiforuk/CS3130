################--Description--#################
#Main Module
#Python client server DB logging

###############-----Author-----#################
#Carlos Nikiforuk

from datetime import datetime

##################################
class log:
#Message class, contains message type and text
##################################
    
    def __init__(self, file):
        
        try:    
            self.logFile = open(file, 'r+')      #check if file exists. if not, create one.
        except FileNotFoundError:
            self.logFile = open(file, 'w+')

        self.logFile.seek(0,2)                   #seek to end of file.
        
    ##################################
    def makeEntry(self, string):
    #Converts message to its string representation
    ##################################
       self.logFile.write(datetime.now().strftime('%b %d %Y %H:%M:%S')+': '+string+'\n')
       self.logFile.flush()
