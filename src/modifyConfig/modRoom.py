from modifyConfig.utilsCLI import prompt, endProg

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
        while True:
            print("press r and enter at any time to return to main\n")

            name = prompt("Enter Room name to delete\n==> ")

            sched.room.deleteRoom(
                sched.config,
                name
            )

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return



def addRoom(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            name = prompt("Enter Room name to add\n==> ")

            sched.room.addRoom(
                sched.config,
                name
            )

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return

        

def modRoom(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            oldName = prompt("Enter Room name to change\n==> ")
            newName = prompt("Enter new Room name\n==> ")

            sched.room.modifyRoom(
                sched.config,
                oldName,
                newName
            )

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return
