from schedule import schedule

def printMain():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Load/Modify/Save config")
    print("2: Run/Print Scheduler")
    print("q: exit program\n==> ",end="")
    
def printConfigMain():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Load Config")
    print("2: Modify Config")
    print("3: Save Config")
    print("r: return to main\n==> ",end="")


    
def endProg():
    quit()
    
def config(sched):
    while(True):
        printConfigMain()
        userCommand = input()
        if(userCommand == "1"):
            print ("Type the name of the file you would like to load from, including extension\n==> ",end="")
            fileName = input()
            sched.loadFile(fileName)
        elif(userCommand == "2"):
            #TODO
            print()
        elif(userCommand == "3"):
            sched.saveFile()
        elif(userCommand == "r"):
            break
            
def runScheduler():
    return

def cli(sched):
    while(True):
        printMain()
        userCommand = input()
        if(userCommand == "q"):
            endProg()
        elif(userCommand == "1"):
            config(sched)
        elif(userCommand == "2"):
            runScheduler()
        
