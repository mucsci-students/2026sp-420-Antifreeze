def cli():
    while(True):
        printMain()
        userCommand = input()
        if(userCommand == "q"):
            endProg()
        
        
def printMain():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Load/Modify/Save config")
    print("2: Run Scheduler")
    print("q: exit program")
    print("\n==> ",end="")
    
def endProg():
    quit()