from fileinput import filename
import json
from sched import scheduler
import sched
from tqdm import tqdm
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
        self.result = []

    #--------------#
    #FILE MANAGEMENT
    def loadConfig(self, fileName):
        try:
            self.config = load_config_from_file(CombinedConfig, fileName)
            print("Config loaded successfully.")
        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return


    def saveConfig(self):
        print("Enter the path of the file you would like to save to, including extension\n==> ",end="")
        fileName = input()
        try:
            with open(fileName, "w") as f:
                f.write(self.config.model_dump_json(indent=2))
                print("Config saved successfully.")
        except Exception as e:
            print("Could not save file, try again")
            print(e)
        return

    def printConfig(self):
        printable = self.config.model_dump_json(indent=2)
        print(printable)
        return
    
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
        
    
    def runScheduler(self):
        sched = Scheduler(self.config)
        print("Running scheduler, this may take a moment...")
        for model in sched.get_models():
            self.result.append(model)
            break
        print("Schedule found!")

    def printSchedule(self):
        if not self.result:
            print("No valid schedule found.")
            return

        for course in self.result[0]:
            print(course.as_csv())

    def saveSchedule(self):
        if not self.result:
            print("No valid schedule found, run the scheduler first1.")
            return
        print("Enter the path of the file you would like to save to, including extension\n==> ",end="")
        filename = input()
        if filename.endswith(".csv"):
            try:
                with open(filename, "w") as f:
                    for finSched in self.result:
                        for course in finSched:         
                            f.write(course.as_csv() + "\n")
                print("Schedule saved successfully.")
            except Exception as e:
                print("Could not save file, try again")
                print(e)
        else:  
            print("Invalid file type, please save as .csv")