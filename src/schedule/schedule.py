from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

from schedule.conflict import conflict
from schedule.course import course
from schedule.faculty import faculty
from schedule.lab import lab
from schedule.room import room



class Schedule():
    def __init__(self):
        self.conflict = conflict()
        self.course = course()
        self.faculty = faculty()
        self.lab = lab()
        self.room = room()
        self.config = self.createEmptyConfig()
        self.configLoaded = False
        self.loadFile("src\example.json")
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

    #Prints config in json format.
    def printFile(self):
        printable = self.config.model_dump_json(indent=2)
        print(printable)
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
        
    