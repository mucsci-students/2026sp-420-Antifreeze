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
        self.conflict = conflict.conflict()
        # self.course = course.course()
        self.faculty = faculty.faculty()
        self.lab = lab.lab()
        self.room = room.room()
        self.config = None  # Don't create empty config yet
        self.configLoaded = False


    #--------------#
    #FILE MANAGEMENT
    def loadFile(self, fileName):
        try:
            self.config = load_config_from_file(CombinedConfig, fileName)
            self.configLoaded = True
            print(f"Successfully loaded: {fileName}\n")
        except Exception as e:
            print("Could not load file, try again")
            print(e)
            self.configLoaded = False
            return


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
        

    #Displays the schedule in a human-readable format    
    def displaySchedule(self):
        if not self.configLoaded or self.config is None:
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