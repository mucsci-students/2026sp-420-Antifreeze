from scheduler import (
    FacultyConfig,
    Faculty,
    Day,
    TimeRange,
    Course,
    Preference,
    Room,
    Lab
)


class faculty():
    #TODO - initialize conflict subclass
    def __init__(self):
        return

    #Add Faculty
    #Adds a new faculty to the configuration json
    #Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
                #limit, times, course preferences, room preferences, lab preferences, mandatory days
    def add_faculty(self, config, name: Faculty, maximum_credits: int, maximum_days: int, minimum_credits: int,
                   unique_course_limit: int, times: dict[Day, list[TimeRange]], course_preferences: dict[Course, Preference],
                   room_preferences: dict[Room, Preference], lab_preferences: dict[Lab, Preference], mandatory_days: set[Day]):
        #Reference to faculty list inside database
        fac = config.config.faculty

        #Test if parameters are correct
        #test = self.testAddFaculty(name, config, maximum_credits, maximum_days, minimum_credits, unique_course_limit,
                                  # times, course_preferences, room_preferences, lab_preferences, mandatory_days)

        #Checking for duplicate faculty name
        for prof in fac:
            if prof.name == name:
                print("Faculty already exists - no change made.")
        
        new_member = FacultyConfig(name = name, maximum_credits = maximum_credits, maximum_days = maximum_days, 
                                  minimum_credits = minimum_credits, unique_course_limit = unique_course_limit,
                                  times = times, course_preferences = course_preferences, room_preferences = room_preferences, 
                                  lab_preferences = lab_preferences, mandatory_days = mandatory_days)
        fac.append(new_member)
        print(f"Faculty member '{name}' added successfully")
    
    #Modify Faculty
    #Modifies the details of an existing faculty member in the configuration json
    #Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
                #limit, times, course preferences, room preferences, lab preferences, mandatory days
    def modify_faculty(self, config, name: Faculty, maximum_credits: int, maximum_days: int, minimum_credits: int,
                      unique_course_limit: int, times: dict[Day, list[TimeRange]], course_preferences: dict[Course, Preference],
                      room_preferences: dict[Room, Preference], lab_preferences: dict[Lab, Preference], mandatory_days: set[Day]):
        #Reference to faculty list inside database
        fac = config.config.faculty

        #Checking to see if faculty exists under provided name
        for prof in fac:
            if prof.name == name:
                fac.remove(prof)
                new_member = FacultyConfig(name = name, maximum_credits = maximum_credits, maximum_days = maximum_days, 
                                          minimum_credits = minimum_credits, unique_course_limit = unique_course_limit,
                                          times = times, course_preferences = course_preferences, room_preferences = room_preferences, 
                                          lab_preferences = lab_preferences, mandatory_days = mandatory_days)
                fac.append(new_member)
                print(f"Faculty member '{name}' modified successfully")
                return

        print("No such faculty member exists.")
        return
    

    #Delete Faculty
    #Delete an existing faculty from the configuration json
    #Parameters: Configuration file, name of faculty
    def delete_faculty(self, config, name: Faculty):
        
        #Reference to faculty list inside database
        fac = config.config.faculty

        #Checking to see if faculty exists under provided name
        for prof in fac:
            if prof.name == name:
                fac.remove(prof)
                print(f"Faculty member '{name}' deleted successfully")
                return
        print("No such faculty member exists.")

    #Print Faculty
    #Prints all faculty members currently stored in the configuration
    #Displays faculty attributes including credit limits, day limits, time availability,
    #course preferences, room preferences, lab preferences, and mandatory days
    #Parameters: Configuration file
    def print_faculty(self, config):
        faculty = config.config.faculty
        print("\nFaculty:")
        for prof in faculty:
            print(f"Name: {prof.name}, \n\tMax Credits: {prof.maximum_credits}, \n\tMax Days: {prof.maximum_days}, \n\tMin Credits: {prof.minimum_credits}, \n\tUnique Course Limit: {prof.unique_course_limit}, \n\tTimes: {prof.times}, \n\tCourse Preferences: {prof.course_preferences}, \n\tRoom Preferences: {prof.room_preferences}, \n\tLab Preferences: {prof.lab_preferences}, \n\tMandatory Days: {prof.mandatory_days}") 


    def validate_entry(self, config: str, faculty_name: str, operation: str) -> bool:
    
        #Validates faculty entry based on operation type.
        
        #Parameters:
        # config: Configuration object
        # faculty_name: Name of the faculty to validate
        # operation: 'add', 'modify', or 'delete'
        
        #Returns true if validation passes, False otherwise
    
        faculty_list = config.config.faculty
        
        # Check for empty input
        if faculty_name == "":
            print("Error: Faculty name cannot be empty — returning to menu.")
            return False
        
        # Check if faculty exists
        faculty_exists = False
        for fac in faculty_list:
            if fac.name.upper() == faculty_name.upper():
                faculty_exists = True
                break
        
        if operation == "add":
            if faculty_exists:
                print(f"Error: Faculty '{faculty_name}' already exists — returning to menu.")
                return False
        
        elif operation in ["modify", "delete"]:
            if not faculty_exists:
                print(f"Error: Faculty '{faculty_name}' does not exist — returning to menu.")
                return False
        
        return True