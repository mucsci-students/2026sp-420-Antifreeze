from schedule import schedule
from modifyConfig import configCli
from modifyConfig.utilsCLI import endProg
def printMain():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Load/Modify/Save config")
    print("2: Run/Print Scheduler")
    print("q: exit program\n==> ",end="")
    
def printRunSchedulerMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Run Scheduler")
    print("2: Print Schedule")
    print("r: return to main")
    print("q: exit program\n==> ",end="")
            
def runScheduler(sched):
    while(True):
        printRunSchedulerMenu()
        userCommand = input()
        if userCommand == "1":
            sched.runScheduler()
        elif userCommand == "2":
            sched.printSchedule()
        elif userCommand.lower() == "r":
            return 
        elif userCommand.lower() == "q":
            endProg()


def cli(sched):
    while(True):
        printMain()
        userCommand = input()
        if(userCommand.lower() == "q"):
            endProg()
        elif(userCommand == "1"):
            configCli.config(sched)
        elif(userCommand == "2"):
            runScheduler(sched)
        
