from controller.modifyConfig.utilsCLI import prompt, end_prog

import re

TIME_RANGE_RE = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}$")

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

#Checks if a new time slot overlaps with any existing time slots
def check_time_overlap(new_slot, existing_slots):
    """
    Checks if a new time slot overlaps with any existing time slots.
    Parameters:
    - new_slot: Time slot string in format HH:MM-HH:MM
    - existing_slots: List of existing time slot strings
    Returns:
    - (True, None) if no overlap
    - (False, overlapping_slot) if overlap detected
    """
    if not existing_slots:
        return True, None
    
    # Parse new slot
    new_start_time, new_end_time = new_slot.split('-')
    new_start_hour, new_start_min = map(int, new_start_time.split(':'))
    new_end_hour, new_end_min = map(int, new_end_time.split(':'))
    new_start_total = new_start_hour * 60 + new_start_min
    new_end_total = new_end_hour * 60 + new_end_min
    
    # Check against each existing slot
    for existing_slot in existing_slots:
        exist_start_time, exist_end_time = existing_slot.split('-')
        exist_start_hour, exist_start_min = map(int, exist_start_time.split(':'))
        exist_end_hour, exist_end_min = map(int, exist_end_time.split(':'))
        exist_start_total = exist_start_hour * 60 + exist_start_min
        exist_end_total = exist_end_hour * 60 + exist_end_min
        
        # Check for overlap
        # Overlap occurs if: new_start < exist_end AND new_end > exist_start
        if new_start_total < exist_end_total and new_end_total > exist_start_total:
            return False, existing_slot
    
    return True, None

#print_mod_faculty_menu
#Displays the faculty modification menu options to the user
def print_mod_faculty_menu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add faculty")
    print("2: Modify faculty")
    print("3: Remove faculty")
    print("4: Print faculty")
    print("r: return to main")
    print("q: exit program\n==> ",end= "")

#mod_faculty_main
#Main control loop for faculty modification operations
#Routes user input to add, modify, delete, or print faculty actions
#Parameters: Scheduler object
def mod_faculty_main(sched):
    while(True):
        print_mod_faculty_menu()
        user_command = input()
        if(user_command == "1"):
            add_faculty(sched)
        elif(user_command == "2"):
            mod_faculty(sched)
        elif(user_command == "3"):
            del_faculty(sched)
        elif(user_command == "4"):
            sched.faculty.print_faculty(sched.config)    
        elif(user_command.lower() == "r"):
            return
        elif(user_command.lower() == "q"):
            end_prog()
        else:
            print("Invalid command, try again.")
#del_faculty
#Removes an existing faculty from the configuration
#Prompts the user for a faculty name
#Parameters: Scheduler object
def del_faculty(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Faculty name to delete\n==> ")
        
        #Validate faculty exists immediately - if not, return to menu
        if not sched.faculty.validate_entry(sched.config, name, "delete"):
            return

        sched.faculty.delete_faculty(
            sched.config,
            name
        )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return

#add_faculty
#Adds a new faculty to the configuration
#Prompts the user for faculty name, max credits, max days, min credits, unique course limit, times, course preferences, room preferences, lab preferences, and mandatory days
#Parameters: Scheduler object
def add_faculty(sched):
    try:
        print("press r and enter at any time to return to main\n")

        while True:
            name = prompt("Enter faculty name to add\n==> ")
            if name == "":
                print("Error: Faculty name cannot be empty. Please try again.")
                continue
            
            #Validate faculty doesn't already exist - if it does, return to menu
            if not sched.faculty.validate_entry(sched.config, name, "add"):
                return
            break
        
        while True:
            maximum_credits = prompt("Enter maximum credits\n==> ")
            if not maximum_credits or not maximum_credits.isnumeric():
                print(f"Error: Maximum credits must be a positive integer, got '{maximum_credits}'. Please try again.")
                continue
            maximum_credits = int(maximum_credits)
            if maximum_credits <= 0:
                print("Error: Maximum credits must be greater than 0. Please try again.")
                continue
            break

        while True:
            minimum_credits = prompt("Enter minimum credits\n==> ")
            if not minimum_credits or not minimum_credits.isnumeric():
                print(f"Error: Minimum credits must be a non-negative integer, got '{minimum_credits}'. Please try again.")
                continue
            minimum_credits = int(minimum_credits)
            if minimum_credits < 0:
                print("Error: Minimum credits cannot be negative. Please try again.")
                continue
            if minimum_credits > maximum_credits:
                print(f"Error: Minimum credits ({minimum_credits}) cannot exceed maximum credits ({maximum_credits}). Please try again.")
                continue
            break

        while True:
            unique_course_limit = prompt("Enter unique course limit\n==> ")
            if not unique_course_limit or not unique_course_limit.isnumeric():
                print(f"Error: Unique course limit must be a positive integer, got '{unique_course_limit}'. Please try again.")
                continue
            unique_course_limit = int(unique_course_limit)
            if unique_course_limit <= 0:
                print("Error: Unique course limit must be greater than 0. Please try again.")
                continue
            break

        while True:
            maximum_days = prompt("Enter maximum days (1-5)\n==> ")
            if not maximum_days or not maximum_days.isnumeric():
                print(f"Error: Maximum days must be an integer between 1-5, got '{maximum_days}'. Please try again.")
                continue
            maximum_days = int(maximum_days)
            if maximum_days < 1 or maximum_days > 5:
                print(f"Error: Maximum days must be between 1 and 5, got {maximum_days}. Please try again.")
                continue
            break

        #Get existing courses, rooms, and labs for validation
        existing_courses = [course.course_id.upper() for course in sched.config.config.courses]
        existing_rooms = [rooms.upper() for rooms in sched.config.config.rooms]
        existing_labs = [lab.upper() for lab in sched.config.config.labs]

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
                
                #Check for overlapping time slots
                no_overlap, overlapping_slot = check_time_overlap(slot, slots)
                if not no_overlap:
                    print(f"Error: Time slot '{slot}' overlaps with existing slot '{overlapping_slot}'. Please try again.")
                    continue
                
                slots.append(slot)
                print(f"Current {day} slots: {slots}")
            times[day] = slots

        course_preferences = {}
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
            
            course_preferences[course] = weight
            print(f"Current Course Preferences: {course_preferences}")

        room_preferences = {}
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
            
            room_preferences[room] = weight
            print(f"Current Room Preferences: {room_preferences}")

        lab_preferences = {}
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
            
            lab_preferences[lab] = weight
            print(f"Current Lab Preferences: {lab_preferences}")
        
        mandatory_days = []
        days = {"MON", "TUE", "WED", "THU", "FRI"}
        while True:
            day = prompt("Enter mandatory day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
            if day == "d":
                break
            if day.upper() not in days:
                print(f"Error: Invalid day '{day}'. Must be MON/TUE/WED/THU/FRI. Please try again.")
                continue
            if day.upper() not in mandatory_days:
                mandatory_days.append(day.upper())
                print(f"Current Mandatory Days: {mandatory_days}")
            else:
                print(f"Day {day.upper()} already added.")
        
        sched.faculty.add_faculty(
            config = sched.config,
            name = name,
            maximum_credits = maximum_credits,
            maximum_days = maximum_days,
            minimum_credits = minimum_credits,
            unique_course_limit = unique_course_limit,
            times = times,
            course_preferences = course_preferences,
            room_preferences = room_preferences,
            lab_preferences = lab_preferences,
            mandatory_days = mandatory_days
        )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return

#mod_faculty
#Replaces an existing faculty's attributes with new values
#Prompts the user for faculty name, max credits, max days, min credits, unique course limit, times, course preferences, room preferences, lab preferences, and mandatory days
#Parameters: Scheduler object
def mod_faculty(sched):
    try:
        print("press r and enter at any time to return to main\n")

        while True:
            name = prompt("Enter faculty name to modify\n==> ")
            if name == "":
                print("Error: Faculty name cannot be empty. Please try again.")
                continue
            
            #Validate faculty exists - if not, return to menu
            if not sched.faculty.validate_entry(sched.config, name, "modify"):
                return
            break
        
        while True:
            maximum_credits = prompt("Enter new maximum credits\n==> ")
            if not maximum_credits or not maximum_credits.isnumeric():
                print(f"Error: Maximum credits must be a positive integer, got '{maximum_credits}'. Please try again.")
                continue
            maximum_credits = int(maximum_credits)
            if maximum_credits <= 0:
                print("Error: Maximum credits must be greater than 0. Please try again.")
                continue
            break

        while True:
            minimum_credits = prompt("Enter new minimum credits\n==> ")
            if not minimum_credits or not minimum_credits.isnumeric():
                print(f"Error: Minimum credits must be a non-negative integer, got '{minimum_credits}'. Please try again.")
                continue
            minimum_credits = int(minimum_credits)
            if minimum_credits < 0:
                print("Error: Minimum credits cannot be negative. Please try again.")
                continue
            if minimum_credits > maximum_credits:
                print(f"Error: Minimum credits ({minimum_credits}) cannot exceed maximum credits ({maximum_credits}). Please try again.")
                continue
            break

        while True:
            unique_course_limit = prompt("Enter new unique course limit\n==> ")
            if not unique_course_limit or not unique_course_limit.isnumeric():
                print(f"Error: Unique course limit must be a positive integer, got '{unique_course_limit}'. Please try again.")
                continue
            unique_course_limit = int(unique_course_limit)
            if unique_course_limit <= 0:
                print("Error: Unique course limit must be greater than 0. Please try again.")
                continue
            break

        while True:
            maximum_days = prompt("Enter new maximum days (1-5)\n==> ")
            if not maximum_days or not maximum_days.isnumeric():
                print(f"Error: Maximum days must be an integer between 1-5, got '{maximum_days}'. Please try again.")
                continue
            maximum_days = int(maximum_days)
            if maximum_days < 1 or maximum_days > 5:
                print(f"Error: Maximum days must be between 1 and 5, got {maximum_days}. Please try again.")
                continue
            break

        #Get existing courses, rooms, and labs for validation
        existing_courses = [course.course_id.upper() for course in sched.config.config.courses]
        existing_rooms = [rooms.upper() for rooms in sched.config.config.rooms]
        existing_labs = [lab.upper() for lab in sched.config.config.labs]

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
                
                #Check for overlapping time slots
                no_overlap, overlapping_slot = check_time_overlap(slot, slots)
                if not no_overlap:
                    print(f"Error: Time slot '{slot}' overlaps with existing slot '{overlapping_slot}'. Please try again.")
                    continue
                
                slots.append(slot)
                print(f"Current {day} slots: {slots}")
            times[day] = slots

        course_preferences = {}
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
            
            course_preferences[course] = weight
            print(f"Current Course Preferences: {course_preferences}")

        room_preferences = {}
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
            
            room_preferences[room] = weight
            print(f"Current Room Preferences: {room_preferences}")

        lab_preferences = {}
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
            
            lab_preferences[lab] = weight
            print(f"Current Lab Preferences: {lab_preferences}")

        mandatory_days = []
        days = {"MON", "TUE", "WED", "THU", "FRI"}
        while True:
            day = prompt("Enter new mandatory day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
            if day == "d":
                break
            if day.upper() not in days:
                print(f"Error: Invalid day '{day}'. Must be MON/TUE/WED/THU/FRI. Please try again.")
                continue
            if day.upper() not in mandatory_days:
                mandatory_days.append(day.upper())
                print(f"Current Mandatory Days: {mandatory_days}")
            else:
                print(f"Day {day.upper()} already added.")

        sched.faculty.modify_faculty(
            config = sched.config,
            name = name,
            maximum_credits = maximum_credits,
            maximum_days = maximum_days,
            minimum_credits = minimum_credits,
            unique_course_limit = unique_course_limit,
            times = times,
            course_preferences = course_preferences,
            room_preferences = room_preferences,
            lab_preferences = lab_preferences,
            mandatory_days = mandatory_days
        )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return
