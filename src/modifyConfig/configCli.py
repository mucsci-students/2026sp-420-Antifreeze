from modifyConfig.utilsCLI import prompt, endProg
from modifyConfig import modLab, modRoom, modCourse, modConflict, modFaculty

def printConfigMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Load config")
    print("2: Modify config")
    print("3: Save config")
    print("4: Print config")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

def printModConfigMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Modify Labs")
    print("2: Modify Rooms")
    print("3: Modify Courses")
    print("4: Modify Conflicts")
    print("5: Modify Faculty")
    print("r: return to config menu")
    print("q: exit program\n==> ",end="")

#Check if Config is Loaded
#Validates that a configuration file has been loaded before modifying/saving/printing
#Returns True if config is loaded, False otherwise
def isConfigLoaded(sched):
    if sched.config is None or not hasattr(sched.config, 'config'):
        print("Error: No configuration loaded. Please load a config file first — returning to config menu.")
        return False
    return True

def confLoop(sched):
    while(True):
        printModConfigMenu()
        userCommand = input()
        if(userCommand == "1"):
            modLab.modLabMain(sched)
        elif(userCommand == "2"):
            modRoom.modRoomMain(sched)
        elif(userCommand == "3"):
            modCourse.modCourseMain(sched)
        elif(userCommand == "4"):
            modConflict.modConflictMain(sched)
        elif(userCommand == "5"):
            modFaculty.modFacultyMain(sched)
        elif(userCommand.lower() == "r"):
            return
        elif(userCommand.lower() == "q"):
            endProg()
        else:
            print("Invalid command, try again.")

def config(sched):
    while(True):
        printConfigMenu()
        userCommand = input()
        if(userCommand == "1"):
            print("Enter the path of the file you would like to load, including extension\n==> ",end="")
            fileName = input()
            sched.loadConfig(fileName)
        elif(userCommand == "2"):
            # Validate config is loaded before modifying
            if not isConfigLoaded(sched):
                continue
            confLoop(sched)
        elif(userCommand == "3"):
            # Validate config is loaded before saving
            if not isConfigLoaded(sched):
                continue
            sched.saveConfig()
        elif(userCommand == "4"):
            # Validate config is loaded before printing
            if not isConfigLoaded(sched):
                continue
            sched.printConfig()
        elif(userCommand.lower() == "r"):
            return
        elif(userCommand.lower() == "q"):
            endProg()
        else:
            print("Invalid command, try again.")