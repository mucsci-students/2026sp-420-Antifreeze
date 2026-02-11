from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig


class room():

    #initialize conflict subclass
    def __init__(self, config: str = None):
        if config:
            self.config = load_config_from_file(config)
        else:
            self.config = None


        return


    def addRoom(self, roomName: str):

        #Reference to rooms list in database
        rooms = self.config.config.rooms

        #Checking for empty input or duplicate room
        if roomName == "":
            print("Room must have a name — no changes made.")
            return
        elif roomName in rooms:
            print("Room already exists — no changes made.")
            return

        #Adding new room to rooms list
        rooms.append(roomName)

        #CLI outputs room added successfully
        print(f"Room '{roomName}' added successfully.")

    #TODO Implement feature
    def deleteRoom(self, roomName: str):

        #Reference to rooms list in database
        rooms = self.config.config.rooms

        #Checking for empty input or nonexistent room
        if roomName == "":
            print("Room must have a name — no changes made.")
            return
        elif roomName not in rooms:
            print("Room does not exist — no changes made.")
            return

        #Removing room from rooms list
        rooms.remove(roomName)

        #CLI outputs room deleted successfully
        print(f"Room '{roomName}' deleted successfully.")

    #TODO Implement feature
    def modifyRoom(self, oldName: str, newName: str):

        #Reference to rooms list in database
        rooms = self.config.config.rooms

        #Checking for empty inputs, nonexistent rooms, or duplicate rooms
        if oldName == "":
            print("Room must have a name — no changes made.")
            return
        elif oldName not in rooms:
            print("Original room not found — no changes made.")
            return
        elif newName == "":
            print("Room must have a name — no changes made.")
            return
        elif newName in rooms:
            print("New room already exists — choose a different room.")
            return

        #Replace old room with new room
        index = rooms.index(oldName)
        rooms[index] = newName

        #CLI outputs room modified successfully
        print(f"Room renamed from '{oldName}' to '{newName}' successfully.") 
    
    #Add/Delete/Modify Room tests
    def runTests(self):
        self.loadFile("example.json")

        print("Initial rooms:", self.config.config.rooms)

        ###### Adding tests ######
        #1. Empty string
        self.addRoom("")
        print("After add:", self.config.config.rooms)

        #2. Room that exists
        self.addRoom("Roddy 136")
        print("After add:", self.config.config.rooms)

        #3. Room that doesn't exist
        self.addRoom("Roddy 143")
        print("After add:", self.config.config.rooms)

        ###### Deleting tests ######
        #1. Empty string
        self.deleteRoom("")
        print("After delete:", self.config.config.rooms)

        #2. Room that exists
        self.deleteRoom("Roddy 136")
        print("After delete:", self.config.config.rooms)

        #3. Room that doesn't exist
        self.deleteRoom("Roddy 200")
        print("After delete:", self.config.config.rooms)

        ###### Modifying tests ######
        #1. Empty strings
        self.modifyRoom("", "Roddy 140")
        print("After modify:", self.config.config.rooms)

        self.modifyRoom("Roddy 140", "")
        print("After modify:", self.config.config.rooms)

        #2. Room that exists
        self.modifyRoom("Roddy 140", "Roddy 147")
        print("After modify:", self.config.config.rooms)

        self.modifyRoom("Roddy 140", "Roddy 340")
        print("After modify:", self.config.config.rooms)

        self.modifyRoom("Roddy 340", "Roddy 340")
        print("After modify:", self.config.config.rooms)

        #3. Room that doesn't exist
        self.modifyRoom("Roddy 300", "Roddy 340")
        print("After modify:", self.config.config.rooms)
