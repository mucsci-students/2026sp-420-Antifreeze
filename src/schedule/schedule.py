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
        self.config = createEmptyConfig()
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
def createEmptyConfig():
    emptyConfig = {
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
    return emptyConfig