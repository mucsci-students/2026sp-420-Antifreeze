from fileinput import filename
import json
from sched import scheduler
import sched
from controller.modifyConfig.utilsCLI import prompt
from scheduler import (
    Scheduler,
    load_config_from_file,
    CourseConfig,
    CombinedConfig,
    FacultyConfig,
    TimeSlotConfig,
    OptimizerFlags
    
)


from model.schedule.conflict import conflict
from model.schedule.course import course
from model.schedule.faculty import faculty
from model.schedule.lab import lab
from model.schedule.room import room



class Schedule():
    #Initialize Schedule
    #Initializes all scheduling submodules and creates an empty configuration
    #Sets up conflict, course, faculty, lab, and room handlers
    def __init__(self):
        self.conflict = conflict()
        self.course = course()
        self.faculty = faculty()
        self.lab = lab()
        self.room = room()
        self.config = self.loadConfig("2026sp-420-Antifreeze\\src\\schedule\\empty.json")
        self.result = []

    #--------------#
    #FILE MANAGEMENT

    #Load Configuration
    #Loads a configuration file into the scheduler
    #Replaces the current configuration with the loaded file
    #Parameters: Configuration file path
    def loadConfig(self, fileName):
        try:
            self.config = load_config_from_file(CombinedConfig, fileName)
            print("Config loaded successfully.")

        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return

    #Save Configuration
    #Saves the current configuration to a file
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

    #Print Configuration
    #Prints the current configuration in a human-readable format
    def printConfig(self):
        self.conflict.printConflicts(self.config)
        self.course.printCourses(self.config)
        self.faculty.printFaculty(self.config)
        self.lab.printLabs(self.config)
        self.room.printRooms(self.config)
        return

    #Run Scheduler
    #Executes the scheduling engine using the current configuration
    #Prompts the user for generation limits, output format, and optimization options
    #Generates schedules and writes results to a file
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
        try:
            sched = Scheduler(self.config)
        except Exception as e:
            print("Scheduler error:", e)
            return

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


    #Print Schedule
    #Displays the current schedule in a human-readable, formatted layout
    #Prints courses, faculty assignments, classes, time slots, and misc settings
    #Requires a loaded configuration   
    def printSchedule(self):
        if not self.result:
            print("No schedules available to print.")
            return

        total = len(self.result)

        while True:
            try:
                n = int(input(f"How many schedules would you like to print? (1–{total}): "))

                if n < 1 or n > total:
                    print("Invalid number. Please try again.")
                    continue

                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        print(f"\nPrinting first {n} schedule(s):\n")

        for i in range(n):
            print(f"\nSchedule {i + 1}:")

            for sch in self.result[i]:
                print(sch.as_csv())

