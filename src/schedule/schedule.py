from scheduler import (
    Scheduler,
    load_config_from_file,
)



from scheduler.config import CombinedConfig
import json
from pathlib import Path
import shutil

class schedule:
    def __init__(self):
        self.config = create_empty_config()
        self.configLoaded = False
        self.scheduler = None

from scheduler.config import CombinedConfig

class schedule:
    def __init__(self):
        config = ""
        configLoaded = False
        scheduler = ""

        
    #TODO - wrap schedule into callable class
    #--------------#
    #FILE MANAGEMENT
    #TODO Implement feature
    def loadFile(self, fileName):
        try:

            self.config = load_config_from_file(CombinedConfig, fileName)

            config = load_config_from_file(CombinedConfig, fileName)

        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
        configLoaded = True
        scheduler = Scheduler(self.config)


    #TODO Implement feature
    def saveFile(self):
        return

    #TODO Implement feature
    def printFile(self):
        return


    #--------------#

    #--------------#
    #ROOMS
    #TODO Implement feature
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
    def run_tests(self):
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

    
    #--------------#
    #FACULTY
    #TODO Implement feature
    def addFaculty(self):
        return

    #TODO Implement feature
    def deleteFaculty(self):
        return

    #TODO Implement feature
    def modifyFaculty(self):
        return

    #--------------#
    #COURSE
    #TODO Implement feature
    def addCourse(self):
        return

    #TODO Implement feature
    def deleteCourse(self):
        return

    #TODO Implement feature
    def modifyCourse(self):
        return


    #--------------#
    #SCHEDULER

    #TODO Implement feature
    def runScheduler(self):
        return

    #TODO Implement feature
    def displaySchedule(self):
        return






#Creates an empty config file
def create_empty_config():
    empty_config = {
        "config": {
            "rooms": [],
            "labs": [],
            "courses": [],
            "faculty": []
        },
        "time_slot_config": {
            "times": {
                "MON": [],
                "TUE": [],
                "WED": [],
                "THU": [],
                "FRI": []
            },
            "classes": []
        },
        "limit": 100,
        "optimizer_flags": []
    }
    return empty_config