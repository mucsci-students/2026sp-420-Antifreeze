from model.schedule import schedule
from controller.modifyConfig import configCli
from controller.modifyConfig.utilsCLI import endProg

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

#Check if Config is Loaded
#Validates that a configuration file has been loaded before running scheduler
#Returns True if config is loaded, False otherwise
def isConfigLoaded(sched):
    if sched.config is None or not sched.config.config.courses:
        sched.loadConfig("2026sp-420-Antifreeze\\src\\schedule\\empty.json")
    return True
            
#Run Scheduler Menu
#Handles user interaction for running and printing schedules
#Routes user input to scheduler execution or schedule display
#Parameters: Scheduler object
def runScheduler(sched):
    while(True):
        printRunSchedulerMenu()
        userCommand = input()
        if userCommand == "1":
            # Validate config is loaded before running scheduler
            if not isConfigLoaded(sched):
                return
            sched.runScheduler()
        elif userCommand == "2":
            # Validate config is loaded before printing schedule
            if not isConfigLoaded(sched):
                return
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
