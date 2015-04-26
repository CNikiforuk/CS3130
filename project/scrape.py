import argparse, requests, re, urllib, os, shutil, sys, httplib
from PIL import Image
from StringIO import StringIO
from urlparse import urlparse

#Author: Carlos Nikiforuk
#Description: Python script for retrieving images from input url and saving them to a folder.
#Date: April 24, 2015

##################################
def scrapeFiles(url, folder, quiet):
    """
    Scrapes files from passed in url, and saves them in specified folder.
    Quiet is a boolean that when true, will supress prompts for user input.
    """
##################################

    configFile = 'scrape.cfg'
    defaultConfig = {"extensions": ["jpg","png","gif","tif", "ico", "jpeg", "bmp"]}


    #attempt to load config from file
    try:
        config = loadConfig(configFile)
    except Exception as e:
        print("Error loading from config file. Will use default configuration")
        config = defaultConfig
    if (not quiet):
        print("Checking for files of type: "+repr(config["extensions"])+'\n')

    #generate extension string to use in regex
    extString = '\.'+config["extensions"][0] 
    for i in range(1,len(config["extensions"])):
        extString = extString+'|'+'\.'+config["extensions"][i]  

    #parse the url and attempt to connect
    parsedURL = urlparse(url)
    try:
        r = requests.get(parsedURL.geturl())
    except requests.exceptions.MissingSchema as e:
        print(e)
        return -1

    if(r.status_code != 200):
        print("Could not connect to url!")
        return -1

    #get the relevant HTML section
    string = r.text
    
    #generate regex
    regex = '[src|href|ref]=\"(http[s]?://|//|/)?([\w~&/$-_+!*\'(),?<>`;@:#]*?)({ext})\"'.format(ext = extString)
    #print(regex)

    #get all filenames
    tokens = re.findall(regex, string)
    
    #check to see if images have been found, if none, exit
    if (len(tokens) == 0):
        print("\nNo files of extension {} found at: \n{}\n\nExiting.".format(extensions, url))
        return(-1)
    else:
        print(repr(len(tokens)) + " files found.")
       
    #get statistics on file types, so user has a general idea of what would be downloaded.
    if(not quiet):
        eCount = {}  
        for i in range(0,len(tokens)):
            if(tokens[i][2] in eCount):
                eCount[tokens[i][2]] = eCount[tokens[i][2]]+1
            else:
                eCount[tokens[i][2]] =1
        for key, value in eCount.items():
            print(key[1:4]+": "+ repr(value))
        print('')
            


    #construct the url's from the scraped filenames
    files = []    
    for i in range(0, len(tokens)):
        if(tokens[i][0]=="//"):
            string = parsedURL.scheme+':'+tokens[i][0]+tokens[i][1]+tokens[i][2]      
            files.append((string, getFileName(tokens[i][1]), tokens[i][2]))
        elif(tokens[i][0]=="/"):
            string = parsedURL.scheme+'://'+parsedURL.netloc+tokens[i][0]+tokens[i][1]+tokens[i][2]
            files.append((string, getFileName(tokens[i][1]), tokens[i][2]))
        elif(tokens[i][0]==""):
            string = parsedURL.scheme+'://'+parsedURL.netloc+'/'+tokens[i][1]+tokens[i][2]
            files.append((string, getFileName(tokens[i][1]), tokens[i][2]))       
        else:
            string = tokens[i][0]+tokens[i][1]+tokens[i][2]
            files.append((string, getFileName(tokens[i][1]), tokens[i][2]))
        #print(string)
    

    #request to see if user wants to continue before beginning download
    inp = ''
    if(not quiet):
        while(inp != 'y' and inp != 'n'):
            inp = raw_input("Would you like to download them to {}?(y/n): ".format(folder))
    else:
        inp = 'y'
    if(inp=='n'):
        print("Exiting")
        return(0)
    

    #create folder if it does not exist
    if not os.path.isdir(folder):
        print("Creating folder...")        
        os.makedirs(folder)
    
    #clearFolder(folder)
    
    #begin downloading files
    print("Downloading Files...")
    for i in range(0, len(files)):
        file = urllib.URLopener()
        try:
            file.retrieve(files[i][0], folder+'/'+files[i][1]+files[i][2])
        except IOError as e:        
            print("error retrieving {} {}".format(i, files[i][0]))
    
    print("Done downloading!\n")

    #detect platform, and use appropriate means to open the download folder
    if(not quiet):
        try:
            if(re.search("linux", sys.platform)):
                os.system("xdg-open '{}'".format(folder))
            elif(re.search("darwin", sys.platform)):
                os.system("open '{}'".format(folder))
            elif(re.search("win", sys.platform)):
                os.system("explorer '{}'".format(folder))
        except Exception as e:
            print("Could not open download folder.")

    #now exit
    return(0)
            
##################################
def getFileName(path):
    """returns the filename string of a path to a file."""
##################################
    tokens = path.split('/')
    return tokens[len(tokens)-1]

##################################
def clearFolder(folder):
    """clears the contents of specified folder"""
##################################
    for tmpfile in os.listdir(folder):
        filepath = os.path.join(folder, tmpfile)
        try:
            if os.path.isfile(filepath):
                os.unlink(filepath)
        except Exception as e:
            print(e)

##################################
def loadConfig(configFile):
    """returns the program configuration after loading from specificied configFile"""
##################################

    config = {}
    fh = open(configFile, 'r')
    for line in fh.readlines():
        #print(line)
        fields = line.split('=')
        if(fields[0] == "extensions"):
            config[fields[0]] = []
            values = fields[1].split(',')
            for i in range(len(values)):
                config[fields[0]].append(values[i].lstrip().rstrip())

    return config

if __name__ == '__main__':   
    parser = argparse.ArgumentParser(description='Scraper')
    parser.add_argument('url', help='url to parse')
    parser.add_argument('-f', metavar='folder', default='./files', help='folder to output files')
    parser.add_argument('-q', dest='q', action='store_true', help='quietmode will suppress prompts and continue')
    args = parser.parse_args()
    print("\n----------File Scraper----------\n")    
    scrapeFiles(args.url, args.f, args.q)


