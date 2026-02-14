from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig


class room():

    #initialize conflict subclass
    def __init__(self):
        return

    def validateEntry(self, config: str, roomName: str, operation: str) -> bool:
        """
        Validates room entry based on operation type.
        
        Parameters:
        - config: Configuration object
        - roomName: Name of the room to validate
        - operation: 'add', 'modify', or 'delete'
        
        Returns:
        - True if validation passes, False otherwise
        """
        rooms = config.config.rooms
        
        # Check for empty input
        if roomName == "":
            print("Error: Room must have a name — returning to menu.")
            return False
        
        if operation == "add":
            if roomName in rooms:
                print(f"Error: Room '{roomName}' already exists — returning to menu.")
                return False
        
        elif operation in ["modify", "delete"]:
            if roomName not in rooms:
                print(f"Error: Room '{roomName}' does not exist — returning to menu.")
                return False
        
        return True

    def addRoom(self, config: str, roomName: str):

        #Reference to rooms list in database
        rooms = config.config.rooms

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

    def deleteRoom(self, config: str, roomName: str):

        #Reference to rooms list in database
        rooms = config.config.rooms

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

    def modifyRoom(self, config: str, oldName: str, newName: str):

        #Reference to rooms list in database
        rooms = config.config.rooms

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
    
    def printRooms(self, config: str):
        rooms = config.config.rooms 
        print("\nRooms:")
        for room in rooms:            
            print(f"Name: {room}")