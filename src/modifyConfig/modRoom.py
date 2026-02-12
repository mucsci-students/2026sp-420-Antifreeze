def printModRoomMenu():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Add Room")
    print("2: Modify Room")
    print("3: Remove Room")
    print("r: return to main\n==> ",end="")

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
        elif(userCommand.lower() == "r"):
            return

def delRoom(sched):
    while(True):
            print("press r and page through prompts to return to main")
            
            print("Enter Room name to delete\n==> ",end="")
            name = input()
            
            if (name.lower() == "r"):
                return
            sched.room.deleteRoom(sched.config, name)


def addRoom(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter Room name to add\n==> ",end="")
        name = input()
        
        if (name.lower() == "r"):
                return
        sched.room.addRoom(sched.config, name)
        

def modRoom(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter Room name to change\n==> ",end="")
        oldName = input()
        
        print("Enter new Room name\n==> ",end="")
        
        newName = input()
        
        fields = [oldName, newName]
        
        if any(str(x).lower() == "r" for x in fields):
            return
        sched.room.modifyRoom(sched.config, oldName, newName)