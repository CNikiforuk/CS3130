import re

################--Description--#################
#Regular Expression phone number formatting

################-----Author-----#################
#Carlos Nikiforuk

def main():
    print("\n-----Phone Number formatting----\nTo quit, type quit or exit.\n")
    while(True):
        good = False
        new = ""     
        alpha = False           
        inp = input("Enter a phone number: ")
        if(inp.lower() not in ['quit', 'exit']):
            format = re.match("([\d]{10})|(\([\d]{3}\)( |)[\d]{3}( |-)[\d]{4})|([\d]{3}(-| )[\d]{3}(-| )[\d]{4})",inp)
            if(format):
                num = re.sub('\D+','',inp)
                print("({}) {}-{}".format(num[0:3],num[3:6],num[6:10]))
            else:
                print("Bad Phone Number")
        else:
            exit()
    

main()
