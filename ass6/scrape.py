import requests, re
#Author: Carlos Nikiforuk
#Description: Python script for retrieving market info from mail and globe.
#Date: March 26, 2015

#TODO HMM

def main():

    url = "http://www.theglobeandmail.com/globe-investor/"
    
    #connect to url
    r = requests.get(url)
    while(r.status_code != 200):
        print("Failed to connect to Globe and Mail. Press any key to try again.")
        input()
        r = requests.get(url)
        
    #get the relevant HTML section
    a = r.text.split('MiniMarketsDashboardModule')
    b = a[2].split('\n')
    string = b[0]
    
    #get names and filter empty lines
    names = re.findall('(class="positive">(.*?)<)|(class="negative">(.*?)<)|(<th>(.*?)</th>)', string)
    filterRE(names)   
    
    #request input
    print("\n-----------Market Information-----------\n")
    print("Select one of the following:\n")
 
    for i in range(0, len(names)):
        print("    {}) {}".format(i+1, names[i][1]))
        
    inp = input('\nOption? ')
    while(inp < '1' or ord(inp) > len(names)+48):
        inp = input('\nOption? ')
    
    
    #parse information
    values = re.findall('(\$</span>(.*?)<)|(chars9">(.*?)<)|(chars8">(.*?)<)', string)
    changes = re.findall('class="(neg color ">(.*?)</span>)|(pos color ">(.*?)</span>)', string)
    times = re.findall('class="timing update-info" data=" (EDT|CDT)">(.*?)</span>', string)
    
    #filter out empty lines
    filterRE(values)
    filterRE(changes)
    filterRE(times)
    
    #store it in a dictionary
    data = {}
    for i in range(0,len(names)):
        data[names[i][1]] = []
        data[names[i][1]].append(values[i][1])
        data[names[i][1]].append(changes[i*2][1])
        data[names[i][1]].append(changes[i*2+1][1])
        data[names[i][1]].append(times[i][1])
        
    #format and output
    key = names[int(inp)-1][1]
    print("\n{0:<{m}}{1:<{m}}{2:<{m}}{3:<{m}}".format('Name', 'Value', 'Change', 'Time', m=15))
    print("{0:-<{m}}".format("", m=15*4))
    print("{0:<{m}}{1:<{m}}{2:<{m}}{3:<{m}}\n".format(key, '$'+data[key][0], data[key][1]+' '+data[key][2], data[key][3], m=15))
    
    
    

def filterRE(m):
#remove empty lines
    if m:    
        for i in range(0,len(m)):
            m[i] = list(filter(None, m[i]))
            #print(m[i]) for debugging
        return m
    else:
        return 0
        
def printAll(data):
#output all data gathered
    for key in data.keys():
        print("{}: {} {} {} {}".format(key, data[key][0], data[key][1], data[key][2], data[key][3]))

main()


