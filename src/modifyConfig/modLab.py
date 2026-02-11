
def printModLabMenu():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Add Lab")
    print("2: Modify Lab")
    print("3: Remove Lab")
    print("r: return to main\n==> ",end="")

def modLabMain(sched):
    while(True):
        printModLabMenu()
        userCommand = input()
        if(userCommand == "1"):
            addLab(sched)
        elif(userCommand == "2"):
            modLab(sched)
        elif(userCommand == "3"):
            delLab(sched)
        elif(userCommand.lower() == "r"):
            return

def delLab(sched):
    while(True):
            print("press r and page through prompts to return to main")
            
            print("Enter Lab name to delete\n==> ",end="")
            name = input()
            
            if (name.lower() == "r"):
                return
            sched.lab.deleteLab(sched.config, name)


def addLab(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter lab name to add\n==> ",end="")
        name = input()
        
        if (name.lower() == "r"):
                return
        sched.lab.addLab(sched.config, name)
    
def modLab(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter Lab name to change\n==> ",end="")
        oldName = input()
        
        print("Enter new lab name\n==> ",end="")
        
        newName = input()
        
        fields = [oldName, newName]
        
        if any(str(x).lower() == "r" for x in fields):
            return
        sched.lab.modifyLab(sched.config, oldName, newName)