from fileinput import filename
import json
from sched import scheduler
import sched
from modifyConfig.utilsCLI import prompt
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

        limit = int(prompt("How many schedules to generate?\n==> "))

        while True:
            fmt = prompt("Output format? (csv/json)\n==> ").lower()
            if fmt in {"csv", "json"}:
                break
            print("Please enter 'csv' or 'json'.")

        outfile = prompt("Output file name, including extensions\n==> ")

        while True:
            opt = prompt("Optimize schedules? (y/n)\n==> ").lower()
            if opt in {"y", "n"}:
                optimize = (opt == "y")
                break
            print("Please enter 'y' or 'n'.")
        if opt == "y":
            self.config.optimizer_flags = [
                "faculty_course",
                "faculty_room",
                "faculty_lab",
                "same_room",
                "same_lab",
                "pack_rooms"
            ]
        else:
            self.config.optimizer_flags = []
        print("Running scheduler, this may take a moment...\n")
        sched = Scheduler(self.config)

        self.result = []
        for model in sched.get_models():
            self.result.append(model)
            if len(self.result) >= limit:
                break
            print

        if not self.result:
            print("No valid schedules found.")
            return

        model = self.result[0]

        if fmt == "csv":
            try:
                with open(outfile, "w") as f:
                    i = 1
                    for model in self.result:
                        f.write(f"Schedule {i}:\n")
                        for sch in model:
                            f.write(sch.as_csv() + "\n\n")
                        i += 1
                        f.write("\n")

            except Exception as e:
                print("Could not save file, try again")
                print(e)
        else:
            try:
                with open(outfile, "w") as f:
                    for model in self.result:
                        for course in model:
                            json.dump([course.model_dump()], f, indent=4)
            except Exception as e:
                print("Could not save file, try again")
                print(e)
        print("Schedule generated and saved.")


    def printSchedule(self):
            if not self.result:
                print("No valid schedule found, please run the scheduler first.")
                return

            for course in self.result[0]:
                print(course.as_csv())
