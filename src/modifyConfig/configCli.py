from schedule import schedule
from modifyConfig import modConflict
from modifyConfig import modCourse
from modifyConfig import modFaculty
from modifyConfig import modLab
from modifyConfig import modRoom


def printConfigMain():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Load Config")
    print("2: Modify Config")
    print("3: Save Config")
    print("r: return to main\n==> ",end="")
    
def printModConfig():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Conflict Config")
    print("2: Course Config")
    print("3: Faculty Config")
    print("4: Lab Config")
    print("5: Room Config")
    print("r: return to main\n==> ",end="")

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


def config(sched):
    while(True):
        printConfigMain()
        userCommand = input()
        if(userCommand == "1"):
            print ("Type the name of the file you would like to load from, including extension\n==> ",end="")
            fileName = input()
            sched.loadFile(fileName)
        elif(userCommand == "2"):
            confLoop(sched)
        elif(userCommand == "3"):
            sched.saveFile()
        elif(userCommand.lower() == "r"):
            break
