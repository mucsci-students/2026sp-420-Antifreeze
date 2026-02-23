from controller.modifyConfig.utilsCLI import prompt, endProg

def printModRoomMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add Room")
    print("2: Modify Room")
    print("3: Remove Room")
    print("4: Print rooms")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

def modRoomMain(sched):
    while(True):
        printModRoomMenu()
        userCommand = input()
        if(userCommand == "1"):
            addRoom(sched)
        elif(userCommand == "2"):
            modRoom(sched)
        elif(userCommand == "3"):
            delRoom(sched)
        elif(userCommand == "4"):
            sched.room.printRooms(sched.config)
        elif(userCommand.lower() == "r"):
            return
        elif(userCommand.lower() == "q"):
            endProg()
        else:
            print("Invalid command, try again.")

def delRoom(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Room name to delete\n==> ")
        
        # Validate immediately
        if not sched.room.validateEntry(sched.config, name, "delete"):
            return

        sched.room.deleteRoom(
            sched.config,
            name
        )

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return

def addRoom(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Room name to add\n==> ")
        
        # Validate immediately
        if not sched.room.validateEntry(sched.config, name, "add"):
            return

        sched.room.addRoom(
            sched.config,
            name
        )

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return

def modRoom(sched):
    try:
        print("press r and enter at any time to return to main\n")

        oldName = prompt("Enter Room name to change\n==> ")
        
        # Validate old name immediately
        if not sched.room.validateEntry(sched.config, oldName, "modify"):
            return
        
        newName = prompt("Enter new Room name\n==> ")
        
        # Validate new name doesn't already exist
        if not sched.room.validateEntry(sched.config, newName, "add"):
            return

        sched.room.modifyRoom(
            sched.config,
            oldName,
            newName
        )

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return