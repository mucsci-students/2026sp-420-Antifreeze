from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig, CourseConfig

from schedule import conflict
from schedule import course
from schedule import faculty
from schedule import lab
from schedule import room

class schedule:
    def __init__(self):
        self.schedConflict = conflict.conflict()
        # self.schedCourse = course.course()
        self.schedFaculty = faculty.faculty()
        self.schedLab = lab.lab()
        self.schedRoom = room.room()
        self.config = self.createEmptyConfig()
        self.configLoaded = False
        # scheduler = Scheduler(self.config)


    #--------------#
    #FILE MANAGEMENT
    #TODO Implement feature
    def loadFile(self, fileName):
        try:
            self.config = load_config_from_file(CombinedConfig, fileName)
        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
        configLoaded = True


    #TODO Implement feature
    def saveFile(self):
        return

    #TODO Implement feature
    def printFile(self):
        return

    #Creates an empty config file
    def createEmptyConfig(self):
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
        configLoaded = True
        
