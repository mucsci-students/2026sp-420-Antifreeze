from schedule import schedule
from modifyConfig import configCli
def printMain():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Load/Modify/Save config")
    print("2: Run/Print Scheduler")
    print("q: exit program\n==> ",end="")


    
def endProg():
    quit()
    

            
def runScheduler():
    return

def cli(sched):
    while(True):
        printMain()
        userCommand = input()
        if(userCommand == "q"):
            endProg()
        elif(userCommand == "1"):
            configCli.config(sched)
        elif(userCommand == "2"):
            runScheduler()
        
