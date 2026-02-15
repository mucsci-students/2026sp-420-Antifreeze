from modifyConfig.utilsCLI import prompt, endProg

import re

TIME_RANGE_RE = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}$")




def printModFacultyMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add faculty")
    print("2: Modify faculty")
    print("3: Remove faculty")
    print("4: Print faculty")
    print("r: return to main")
    print("q: exit program\n==> ",end= "")

def modFacultyMain(sched):
    while(True):
        printModFacultyMenu()
        userCommand = input()
        if(userCommand == "1"):
            addFaculty(sched)
        elif(userCommand == "2"):
            modFaculty(sched)
        elif(userCommand == "3"):
            delFaculty(sched)
        elif(userCommand == "4"):
            sched.faculty.printFaculty(sched.config)    
        elif(userCommand.lower() == "r"):
            return
        elif(userCommand.lower() == "q"):
            endProg()
        else:
            print("Invalid command, try again.")

def delFaculty(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Faculty name to delete\n==> ")
        
        #Validate faculty exists immediately - if not, return to menu
        if not sched.faculty.validateEntry(sched.config, name, "delete"):
            return

        sched.faculty.deleteFaculty(
            sched.config,
            name
        )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return


def addFaculty(sched):
    try:
        print("press r and enter at any time to return to main\n")

        while True:
            name = prompt("Enter faculty name to add\n==> ")
            if name == "":
                print("Error: Faculty name cannot be empty. Please try again.")
                continue
            
            #Validate faculty doesn't already exist - if it does, return to menu
            if not sched.faculty.validateEntry(sched.config, name, "add"):
                return
            break
        
        while True:
            maximumCredits = prompt("Enter maximum credits\n==> ")
            if not maximumCredits or not maximumCredits.isnumeric():
                print(f"Error: Maximum credits must be a positive integer, got '{maximumCredits}'. Please try again.")
                continue
            maximumCredits = int(maximumCredits)
            if maximumCredits <= 0:
                print("Error: Maximum credits must be greater than 0. Please try again.")
                continue
            break

        while True:
            minimumCredits = prompt("Enter minimum credits\n==> ")
            if not minimumCredits or not minimumCredits.isnumeric():
                print(f"Error: Minimum credits must be a non-negative integer, got '{minimumCredits}'. Please try again.")
                continue
            minimumCredits = int(minimumCredits)
            if minimumCredits < 0:
                print("Error: Minimum credits cannot be negative. Please try again.")
                continue
            if minimumCredits > maximumCredits:
                print(f"Error: Minimum credits ({minimumCredits}) cannot exceed maximum credits ({maximumCredits}). Please try again.")
                continue
            break

        while True:
            uniqueCourseLimit = prompt("Enter unique course limit\n==> ")
            if not uniqueCourseLimit or not uniqueCourseLimit.isnumeric():
                print(f"Error: Unique course limit must be a positive integer, got '{uniqueCourseLimit}'. Please try again.")
                continue
            uniqueCourseLimit = int(uniqueCourseLimit)
            if uniqueCourseLimit <= 0:
                print("Error: Unique course limit must be greater than 0. Please try again.")
                continue
            break

        while True:
            maximumDays = prompt("Enter maximum days (1-5)\n==> ")
            if not maximumDays or not maximumDays.isnumeric():
                print(f"Error: Maximum days must be an integer between 1-5, got '{maximumDays}'. Please try again.")
                continue
            maximumDays = int(maximumDays)
            if maximumDays < 1 or maximumDays > 5:
                print(f"Error: Maximum days must be between 1 and 5, got {maximumDays}. Please try again.")
                continue
            break

        #Get existing courses, rooms, and labs for validation
        existing_courses = [c.course_id.upper() for c in sched.config.config.courses]
        existing_rooms = [r.upper() for r in sched.config.config.rooms]
        existing_labs = [l.upper() for l in sched.config.config.labs]

        times = {}
        for day in ["MON", "TUE", "WED", "THU", "FRI"]:
            print(f"\nEnter time slots for {day} (send 'd' when finished)")
            slots = []
            while True:
                slot = prompt(f"{day} slot\n==> ")
                if slot == "d":
                    break
                
                #Validate time slot
                is_valid, error_msg = validate_time_slot(slot)
                if not is_valid:
                    print(f"Error: {error_msg}. Please try again.")
                    continue
                
                #Check for duplicate time slot
                if slot in slots:
                    print(f"Error: Time slot '{slot}' already added for {day}. Please try again.")
                    continue
                
                slots.append(slot)
                print(f"Current {day} slots: {slots}")
            times[day] = slots

        coursePreferences = {}
        while True:
            course = prompt("Enter course preference (or 'd')\n==> ")
            if course == "d":
                break
            #Validate course exists - if not, reprompt
            if course.upper() not in existing_courses:
                print(f"Error: Course '{course}' does not exist. Please try again.")
                continue
            
            while True:
                weight = prompt(f"Enter weight for {course}\n==> ")
                if not weight or not weight.isnumeric():
                    print(f"Error: Weight must be a positive integer, got '{weight}'. Please try again.")
                    continue
                weight = int(weight)
                break
            
            coursePreferences[course] = weight
            print(f"Current Course Preferences: {coursePreferences}")

        roomPreferences = {}
        while True:
            room = prompt("Enter room preference (or 'd')\n==> ")
            if room == "d":
                break
            #Validate room exists - if not, reprompt
            if room.upper() not in existing_rooms:
                print(f"Error: Room '{room}' does not exist. Please try again.")
                continue
            
            while True:
                weight = prompt(f"Enter weight for {room}\n==> ")
                if not weight or not weight.isnumeric():
                    print(f"Error: Weight must be a positive integer, got '{weight}'. Please try again.")
                    continue
                weight = int(weight)
                break
            
            roomPreferences[room] = weight
            print(f"Current Room Preferences: {roomPreferences}")

        labPreferences = {}
        while True:
            lab = prompt("Enter lab preference (or 'd')\n==> ")
            if lab == "d":
                break
            #Validate lab exists - if not, reprompt
            if lab.upper() not in existing_labs:
                print(f"Error: Lab '{lab}' does not exist. Please try again.")
                continue
            
            while True:
                weight = prompt(f"Enter weight for {lab}\n==> ")
                if not weight or not weight.isnumeric():
                    print(f"Error: Weight must be a positive integer, got '{weight}'. Please try again.")
                    continue
                weight = int(weight)
                break
            
            labPreferences[lab] = weight
            print(f"Current Lab Preferences: {labPreferences}")
        
        mandatoryDays = []
        days = {"MON", "TUE", "WED", "THU", "FRI"}
        while True:
            day = prompt("Enter mandatory day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
            if day == "d":
                break
            if day.upper() not in days:
                print(f"Error: Invalid day '{day}'. Must be MON/TUE/WED/THU/FRI. Please try again.")
                continue
            if day.upper() not in mandatoryDays:
                mandatoryDays.append(day.upper())
                print(f"Current Mandatory Days: {mandatoryDays}")
            else:
                print(f"Day {day.upper()} already added.")
        
        sched.faculty.addFaculty(
            config = sched.config,
            name = name,
            maximumCredits = maximumCredits,
            maximumDays = maximumDays,
            minimumCredits = minimumCredits,
            uniqueCourseLimit = uniqueCourseLimit,
            times = times,
            coursePreferences = coursePreferences,
            roomPreferences = roomPreferences,
            labPreferences = labPreferences,
            mandatoryDays = mandatoryDays
        )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return

def modFaculty(sched):
    try:
        print("press r and enter at any time to return to main\n")

        while True:
            name = prompt("Enter faculty name to modify\n==> ")
            if name == "":
                print("Error: Faculty name cannot be empty. Please try again.")
                continue
            
            #Validate faculty exists - if not, return to menu
            if not sched.faculty.validateEntry(sched.config, name, "modify"):
                return
            break
        
        while True:
            maximumCredits = prompt("Enter new maximum credits\n==> ")
            if not maximumCredits or not maximumCredits.isnumeric():
                print(f"Error: Maximum credits must be a positive integer, got '{maximumCredits}'. Please try again.")
                continue
            maximumCredits = int(maximumCredits)
            if maximumCredits <= 0:
                print("Error: Maximum credits must be greater than 0. Please try again.")
                continue
            break

        while True:
            minimumCredits = prompt("Enter new minimum credits\n==> ")
            if not minimumCredits or not minimumCredits.isnumeric():
                print(f"Error: Minimum credits must be a non-negative integer, got '{minimumCredits}'. Please try again.")
                continue
            minimumCredits = int(minimumCredits)
            if minimumCredits < 0:
                print("Error: Minimum credits cannot be negative. Please try again.")
                continue
            if minimumCredits > maximumCredits:
                print(f"Error: Minimum credits ({minimumCredits}) cannot exceed maximum credits ({maximumCredits}). Please try again.")
                continue
            break

        while True:
            uniqueCourseLimit = prompt("Enter new unique course limit\n==> ")
            if not uniqueCourseLimit or not uniqueCourseLimit.isnumeric():
                print(f"Error: Unique course limit must be a positive integer, got '{uniqueCourseLimit}'. Please try again.")
                continue
            uniqueCourseLimit = int(uniqueCourseLimit)
            if uniqueCourseLimit <= 0:
                print("Error: Unique course limit must be greater than 0. Please try again.")
                continue
            break

        while True:
            maximumDays = prompt("Enter new maximum days (1-5)\n==> ")
            if not maximumDays or not maximumDays.isnumeric():
                print(f"Error: Maximum days must be an integer between 1-5, got '{maximumDays}'. Please try again.")
                continue
            maximumDays = int(maximumDays)
            if maximumDays < 1 or maximumDays > 5:
                print(f"Error: Maximum days must be between 1 and 5, got {maximumDays}. Please try again.")
                continue
            break

        #Get existing courses, rooms, and labs for validation
        existing_courses = [c.course_id.upper() for c in sched.config.config.courses]
        existing_rooms = [r.upper() for r in sched.config.config.rooms]
        existing_labs = [l.upper() for l in sched.config.config.labs]

        times = {}
        for day in ["MON", "TUE", "WED", "THU", "FRI"]:
            print(f"\nEnter new time slots for {day} (send 'd' when finished)")
            slots = []
            while True:
                slot = prompt(f"{day} slot\n==> ")
                if slot == "d":
                    break
                
                #Validate time slot
                is_valid, error_msg = validate_time_slot(slot)
                if not is_valid:
                    print(f"Error: {error_msg}. Please try again.")
                    continue
                
                #Check for duplicate time slot
                if slot in slots:
                    print(f"Error: Time slot '{slot}' already added for {day}. Please try again.")
                    continue
                
                slots.append(slot)
                print(f"Current {day} slots: {slots}")
            times[day] = slots

        coursePreferences = {}
        while True:
            course = prompt("Enter new course preference (or 'd')\n==> ")
            if course == "d":
                break
            #Validate course exists - if not, reprompt
            if course.upper() not in existing_courses:
                print(f"Error: Course '{course}' does not exist. Please try again.")
                continue
            
            while True:
                weight = prompt(f"Enter weight for {course}\n==> ")
                if not weight or not weight.isnumeric():
                    print(f"Error: Weight must be a positive integer, got '{weight}'. Please try again.")
                    continue
                weight = int(weight)
                break
            
            coursePreferences[course] = weight
            print(f"Current Course Preferences: {coursePreferences}")

        roomPreferences = {}
        while True:
            room = prompt("Enter room preference (or 'd')\n==> ")
            if room == "d":
                break
            #Validate room exists - if not, reprompt
            if room.upper() not in existing_rooms:
                print(f"Error: Room '{room}' does not exist. Please try again.")
                continue
            
            while True:
                weight = prompt(f"Enter weight for {room}\n==> ")
                if not weight or not weight.isnumeric():
                    print(f"Error: Weight must be a positive integer, got '{weight}'. Please try again.")
                    continue
                weight = int(weight)
                break
            
            roomPreferences[room] = weight
            print(f"Current Room Preferences: {roomPreferences}")

        labPreferences = {}
        while True:
            lab = prompt("Enter lab preference (or 'd')\n==> ")
            if lab == "d":
                break
            #Validate lab exists - if not, reprompt
            if lab.upper() not in existing_labs:
                print(f"Error: Lab '{lab}' does not exist. Please try again.")
                continue
            
            while True:
                weight = prompt(f"Enter weight for {lab}\n==> ")
                if not weight or not weight.isnumeric():
                    print(f"Error: Weight must be a positive integer, got '{weight}'. Please try again.")
                    continue
                weight = int(weight)
                break
            
            labPreferences[lab] = weight
            print(f"Current Lab Preferences: {labPreferences}")

        mandatoryDays = []
        days = {"MON", "TUE", "WED", "THU", "FRI"}
        while True:
            day = prompt("Enter new mandatory day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
            if day == "d":
                break
            if day.upper() not in days:
                print(f"Error: Invalid day '{day}'. Must be MON/TUE/WED/THU/FRI. Please try again.")
                continue
            if day.upper() not in mandatoryDays:
                mandatoryDays.append(day.upper())
                print(f"Current Mandatory Days: {mandatoryDays}")
            else:
                print(f"Day {day.upper()} already added.")

        sched.faculty.modifyFaculty(
            config = sched.config,
            name = name,
            maximumCredits = maximumCredits,
            maximumDays = maximumDays,
            minimumCredits = minimumCredits,
            uniqueCourseLimit = uniqueCourseLimit,
            times = times,
            coursePreferences = coursePreferences,
            roomPreferences = roomPreferences,
            labPreferences = labPreferences,
            mandatoryDays = mandatoryDays
        )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return
    
#Validates that a time slot is in valid format and has valid time values.
def validate_time_slot(slot):

    if not TIME_RANGE_RE.match(slot):
        return False, "Invalid format. Use HH:MM-HH:MM"
    
    #Parse the times
    try:
        start_time, end_time = slot.split('-')
        start_hour, start_min = map(int, start_time.split(':'))
        end_hour, end_min = map(int, end_time.split(':'))
        
        #Validate hours (0-23)
        if not (0 <= start_hour <= 23):
            return False, f"Start hour {start_hour:02d} must be between 00-23"
        if not (0 <= end_hour <= 23):
            return False, f"End hour {end_hour:02d} must be between 00-23"
        
        #Validate minutes (0-59)
        if not (0 <= start_min <= 59):
            return False, f"Start minute {start_min:02d} must be between 00-59"
        if not (0 <= end_min <= 59):
            return False, f"End minute {end_min:02d} must be between 00-59"
        
        #Validate that end time is after start time
        start_total_mins = start_hour * 60 + start_min
        end_total_mins = end_hour * 60 + end_min
        if end_total_mins <= start_total_mins:
            return False, f"End time ({end_hour:02d}:{end_min:02d}) must be after start time ({start_hour:02d}:{start_min:02d})"
        
        return True, None
        
    except (ValueError, IndexError):
        return False, "Invalid time format"