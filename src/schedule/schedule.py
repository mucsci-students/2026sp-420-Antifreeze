from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

import conflict
import course
import faculty
import lab
import room

class schedule:
    def __init__(self):
        self.config = None
        self.configLoaded = False
        self.scheduler = None
        self.schedConflict = conflict.conflict()
        self.schedCourse = course.course()
        self.schedFaculty = faculty.faculty()
        self.schedLab = lab.lab()
        self.schedRoom = room.room()

    #--------------#
    #FILE MANAGEMENT
    #TODO Implement feature
    def loadFile(self, fileName):
        try:
            config = load_config_from_file(CombinedConfig, fileName)
        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
        configLoaded = True
        scheduler = Scheduler(config)


    #TODO Implement feature
    def saveFile(self):
        return

    #TODO Implement feature
    def printFile(self):
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