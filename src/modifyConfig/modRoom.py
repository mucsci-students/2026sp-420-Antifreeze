from modifyConfig.utilsCLI import prompt, endProg

#printModRoomMenu
#Displays the room modification menu options to the user
def printModRoomMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add Room")
    print("2: Modify Room")
    print("3: Remove Room")
    print("4: Print rooms")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

#modRoomMain
#Main control loop for room modification operations
#Routes user input to add, modify, delete, or print room actions
#Parameters: Scheduler object
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

#delRoom
#Removes an existing room from the configuration
#Prompts the user for a room name
#Parameters: Scheduler object
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

<<<<<<< HEAD

#addRoom
#Adds a new room to the configuration
#Prompts the user for a room name
#Parameters: Scheduler object
=======
>>>>>>> f18d85d7aabaf5bea8fe0bcd9815c7fd6fd7c1c4
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

<<<<<<< HEAD
        
#modRoom
#Replaces an existing room's name with a new name
#Prompts the user for a room name
#Parameters: Scheduler object
=======
>>>>>>> f18d85d7aabaf5bea8fe0bcd9815c7fd6fd7c1c4
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