class message:
    def __init__(self, type, text):
        self.type = type
        self.text = text
        
    def toString(self):
        return(self.type+':'+self.text)
        
def toMessage(string):
        fields = string.rstrip().split(":",1)[-1]
        return message(fields[0], fields[1])
        
def main():
    inp = input("Enter: ")
    print("wtf "+ inp)
    msg = message('0',inp)
    
    print(msg.toString())
    
main()