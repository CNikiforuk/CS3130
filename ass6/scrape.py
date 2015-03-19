import requests, re, urllib

#TODO Format Output. Update before printing. Ask to continue. error checking

def main():

    #get the relevant HTML section
    r = requests.get("http://www.theglobeandmail.com/globe-investor/")
    a = r.text.split('MiniMarketsDashboardModule')
    b = a[2].split('\n')
    string = b[0]
    
    
    #parse through it
    names = re.findall('(class="positive">(.*?)<)|(class="negative">(.*?)<)|(<th>(.*?)</th>)', string)
    values = re.findall('(\$</span>(.*?)<)|(chars9">(.*?)<)|(chars8">(.*?)<)', string)
    changes = re.findall('class="(neg color ">(.*?)</span>)|(pos color ">(.*?)</span>)', string)
    times = re.findall('class="timing update-info" data=" (EDT|CDT)">(.*?)</span>', string)
    
    #filter out empty lines
    filterRE(names)    
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
        
     #Request input
    print("\n-----------Market Information-----------\n")
    print("Select one of the following:\n")
 
    for i in range(0, len(names)):
        print("    {}) {}".format(i+1, names[i][1]))
        
    inp = input('Option? ')
    key = names[int(inp)-1][1]
    
    print("\n    "+key, data[key])
    

def filterRE(m):
    if m:    
        for i in range(0,len(m)):
            m[i] = list(filter(None, m[i]))
            #print(m[i]) for debugging
        return m
    else:
        return 0
        
def printAll(data):
    for key in data.keys():
        print("{}: {} {} {} {}".format(key, data[key][0], data[key][1], data[key][2], data[key][3]))

main()


