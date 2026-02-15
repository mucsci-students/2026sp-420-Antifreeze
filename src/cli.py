from schedule import schedule
from modifyConfig import configCli
from modifyConfig.utilsCLI import endProg

#Print Main Menu
#Displays the main program menu options
def printMain():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Load/Modify/Save config")
    print("2: Run/Print Scheduler")
    print("q: exit program\n==> ",end="")
    
#Print Run Scheduler Menu
#Displays the scheduler execution and display options
def printRunSchedulerMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Run Scheduler")
    print("2: Print Schedule")
    print("r: return to main")
    print("q: exit program\n==> ",end="")
            
#Run Scheduler Menu
#Handles user interaction for running and printing schedules
#Routes user input to scheduler execution or schedule display
#Parameters: Scheduler object
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

#Main CLI
#Primary command-line interface control loop
#Routes user input to configuration or scheduler menus
#Parameters: Scheduler object
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
        
