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


def modConfig(sched):
    printModConfig()
    userCommand = input()
    if(userCommand == "1"):
        modConflict.modConflict(sched)
    elif(userCommand == "2"):
        modCourse.modCourse(sched)
    elif(userCommand == "3"):
        modFaculty.modFaculty(sched)
    elif(userCommand == "4"):
        modLab.modLab(sched)
    elif(userCommand == "5"):
        modRoom.modRoom(sched)
    elif(userCommand == "r"):
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
            modConfig(sched)
        elif(userCommand == "3"):
            sched.saveFile()
        elif(userCommand == "r"):
            return


