from schedule import schedule
from modifyConfig import modConflict
from modifyConfig import modCourse
from modifyConfig import modFaculty
from modifyConfig import modLab
from modifyConfig import modRoom
from modifyConfig.utilsCLI import endProg

#printConfigMain
#Displays the main configuration menu options to the user
def printConfigMain():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Load Config")
    print("2: Modify Config")
    print("3: Print Config")
    print("4: Save Config")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

#printModConfig
#Displays the configuration modification menu options to the user
def printModConfig():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Conflict Config")
    print("2: Course Config")
    print("3: Faculty Config")
    print("4: Lab Config")
    print("5: Room Config")
    print("r: return to main")
    print("q: exit program\n==> ",end="")


#confLoop
#Main control loop for configuration modification operations
#Routes user input to conflict, course, faculty, lab, or room modification
#Parameters: Scheduler object
def confLoop(sched):
    while(True):
        printModConfig()
        userCommand = input()
        if userCommand == "1":
            modConflict.modConflictMain(sched)
        elif userCommand == "2":
            modCourse.modCourseMain(sched)
        elif userCommand == "3":
            modFaculty.modFacultyMain(sched)
        elif userCommand == "4":
            modLab.modLabMain(sched)
        elif userCommand == "5":
            modRoom.modRoomMain(sched)
        elif userCommand.lower() == "r":
            return
        elif userCommand.lower() == "q":
            endProg()
        else:
            print("Invalid command, try again.")

#config
#Main control loop for configuration operations
#Routes user input to load, modify, print, or save configuration
#Parameters: Scheduler object
def config(sched):
    while(True):
        printConfigMain()
        userCommand = input()
        if(userCommand == "1"):
            print ("Type the name of the file you would like to load from, including extension\n==> ",end="")
            fileName = input()
            sched.loadConfig(fileName)
        elif(userCommand == "2"):
            confLoop(sched)
        elif(userCommand == "3"):
            sched.printConfig()
        elif(userCommand == "4"):
            sched.saveConfig()
        elif(userCommand.lower() == "r"):
            break
        elif(userCommand.lower() == "q"):
            endProg()
