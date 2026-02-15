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
    #Initialize Schedule
    #Initializes all scheduling submodules and creates an empty configuration
    #Sets up conflict, course, faculty, lab, and room handlers
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
    
    #Create Empty Configuration
    #Generates and returns a default empty configuration structure
    #Used to initialize the scheduler before loading a file
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


       #Print Schedule
    
    #Displays the current schedule in a human-readable, formatted layout
    #Prints courses, faculty assignments, classes, time slots, and misc settings
    #Requires a loaded configuration   
    def printSchedule(self):
        if self.config is None or not self.config.config.courses:
            print("No configuration loaded. Please load a file first.")
            return
        
        #=============================================================================
        #COURSES SECTION
        #=============================================================================
        print("\n" + "="*125)
        print("Courses")
        print("="*125)
        print(f"{'Course #':<15} {'Credits':<10} {'Room(s)':<35} {'Lab(s)':<20} {'Conflicts':<20}")
        print("-"*125)
        
        for course in self.config.config.courses:
            rooms = ", ".join(course.room) if course.room else ""
            labs = ", ".join(course.lab) if course.lab else ""
            conflicts = ", ".join(course.conflicts) if course.conflicts else ""
            
            #Column widths
            print(f"{course.course_id:<15} {course.credits:<10} {rooms:<35} {labs:<20} {conflicts:<20}")
        
        #=============================================================================
        #FACULTY SECTION
        #=============================================================================
        print("\n" + "="*125)
        print("Faculty")
        print("="*125)
        print(f"{'Name':<15} {'Max Credits':<15} {'Min Credits':<15} {'Unique Courses':<20} {'Timeslots'}")
        print("-"*125)
        
        facultyList = self.config.config.faculty
        for idx, fac in enumerate(facultyList):
            timeslots = []
            for day, times in fac.times.items():
                if times:
                    for timeRange in times:
                        timeslots.append(f"{day[:3]} : {timeRange}")
            
            #First row: faculty info + first timeslot
            firstPart = f"{fac.name:<15} {fac.maximum_credits:<15} {fac.minimum_credits:<15} {fac.unique_course_limit:<20} "
            firstTimeslot = timeslots[0] if timeslots else ""
            print(f"{firstPart}{firstTimeslot}")
            
            #Continuation lines: match the spacing of firstPart exactly
            indent = len(firstPart)
            for i in range(1, len(timeslots)):
                print(f"{' '*indent}{timeslots[i]}")
            
            #Add separator line after each faculty member except the last one
            if idx < len(facultyList) - 1:
                print("-"*125)
        
        #=============================================================================
        #CLASSES SECTION
        #=============================================================================
        print("\n" + "="*125)
        print("Classes")
        print("="*125)
        print(f"{'Credits':<20} {'Meetings':<30} {'Lab':<15}")
        print("-"*125)
        
        #Get all non-disabled classes first
        enabledClasses = [c for c in self.config.time_slot_config.classes 
                          if not (hasattr(c, 'disabled') and c.disabled)]
        
        for idx, classConfig in enumerate(enabledClasses):
            meetings = []
            hasLab = False
            for meeting in classConfig.meetings:
                labMarker = ""
                if hasattr(meeting, 'lab') and meeting.lab:
                    hasLab = True
                meetings.append(f"{meeting.day[:3]} - {meeting.duration} min")
            
            #First row: credits + first meeting + lab status
            #Build the first part with exact spacing
            firstPart = f"{classConfig.credits:<20} "
            firstMeeting = meetings[0] if meetings else ""
            print(f"{firstPart}{firstMeeting:<30} {str(hasLab):<15}")
            
            #Continuation lines: match the spacing of firstPart exactly
            indent = len(firstPart)
            for i in range(1, len(meetings)):
                print(f"{' '*indent}{meetings[i]:<30}")
            
            #Add separator line after each class except the last one
            if idx < len(enabledClasses) - 1:
                print("-"*125)
        
        #=============================================================================
        # TIME SLOT CONFIG SECTION
        #=============================================================================
        print("\n" + "="*125)
        print("Time Slot Config")
        print("="*125)
        
        days = ["Mon", "Tue", "Wed", "Thu", "Fri"]
        dayKeys = ["MON", "TUE", "WED", "THU", "FRI"]
        
        #Print header
        header = ""
        for day in days:
            header += f"{day:<25}"
        print(header)
        print("-"*125)
        
        #Get max number of time blocks across all days
        maxBlocks = 0
        dayBlocks = {}
        for dayKey in dayKeys:
            if dayKey in self.config.time_slot_config.times:
                dayBlocks[dayKey] = self.config.time_slot_config.times[dayKey]
                maxBlocks = max(maxBlocks, len(dayBlocks[dayKey]))
        
        #Print time blocks
        for i in range(maxBlocks):
            #Create formatted strings for each day
            dayStrs = []
            for dayKey in dayKeys:
                if dayKey in dayBlocks and i < len(dayBlocks[dayKey]):
                    block = dayBlocks[dayKey][i]
                    # Access as object attributes, not dictionary keys
                    blockLines = [
                        f"Start  : {block.start}",
                        f"spacing: {block.spacing}",
                        f"End    : {block.end}"
                    ]
                    dayStrs.append(blockLines)
                else:
                    dayStrs.append(["", "", ""])
            
            #Print 3 lines for each time block
            for lineIdx in range(3):
                line = ""
                for dayLines in dayStrs:
                    line += f"{dayLines[lineIdx]:<25}"
                print(line)
            
            #Add blank line between blocks if not last block
            if i < maxBlocks - 1:
                print()
        
        #=============================================================================
        #MISC SECTION
        #=============================================================================
        print("\n" + "="*125)
        print("Misc")
        print("="*125)
        print(f"Limit: {self.config.limit}")
        flagsStr = ", ".join(self.config.optimizer_flags) if self.config.optimizer_flags else "None"
        print(f"Flags: {flagsStr}")
        print("="*125 + "\n")

