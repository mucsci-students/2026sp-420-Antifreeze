from modifyConfig.utilsCLI import prompt, endProg

def printModLabMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add Lab")
    print("2: Modify Lab")
    print("3: Remove Lab")
    print("4: Print labs")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

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
        elif(userCommand == "4"):
            sched.lab.printLabs(sched.config)   
        elif(userCommand.lower() == "r"):
            return
        elif(userCommand.lower() == "q"):
            endProg()
        else:
            print("Invalid command, try again.")

def delLab(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Lab name to delete\n==> ")
        
        # Validate immediately
        if not sched.lab.validateEntry(sched.config, name, "delete"):
            return

        sched.lab.deleteLab(
            sched.config,
            name
        )

    except KeyboardInterrupt:
        print("\nReturning to lab menu...")
        return

def addLab(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter lab name to add\n==> ")
        
        # Validate immediately
        if not sched.lab.validateEntry(sched.config, name, "add"):
            return

        sched.lab.addLab(
            sched.config,
            name
        )

    except KeyboardInterrupt:
        print("\nReturning to lab menu...")
        return

def modLab(sched):
    try:
        print("press r and enter at any time to return to main\n")

        oldName = prompt("Enter Lab name to change\n==> ")
        
        # Validate old name immediately
        if not sched.lab.validateEntry(sched.config, oldName, "modify"):
            return
        
        newName = prompt("Enter new lab name\n==> ")
        
        # Validate new name doesn't already exist
        if not sched.lab.validateEntry(sched.config, newName, "add"):
            return

        sched.lab.modifyLab(
            sched.config,
            oldName,
            newName
        )

    except KeyboardInterrupt:
        print("\nReturning to lab menu...")
        return