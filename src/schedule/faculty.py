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
    def addFaculty(self, config, name: Faculty, maximumCredits: int, maximumDays: int, minimumCredits: int,
                   uniqueCourseLimit: int, times: dict[Day, list[TimeRange]], coursePreferences: dict[Course, Preference],
                   roomPreferences: dict[Room, Preference], labPreferences: dict[Lab, Preference], mandatoryDays: set[Day]):
        #Reference to faculty list inside database
        fac = config.config.faculty

        #Test if parameters are correct
        #test = self.testAddFaculty(name, config, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit,
                                  # times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)

        #Checking for duplicate faculty name
        for prof in fac:
            if prof.name == name:
                print("Faculty already exists - no change made.")
        
        newMember = FacultyConfig(name = name, maximum_credits = maximumCredits, maximum_days = maximumDays, 
                                  minimum_credits = minimumCredits, unique_course_limit = uniqueCourseLimit,
                                  times = times, course_preferences = coursePreferences, room_preferences = roomPreferences, 
                                  lab_preferences = labPreferences, mandatory_days = mandatoryDays)
        fac.append(newMember)
        print(f"Faculty member '{name}' added successfully")
    
    #Modify Faculty
    #Modifies the details of an existing faculty member in the configuration json
    #Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
                #limit, times, course preferences, room preferences, lab preferences, mandatory days
    def modifyFaculty(self, config, name: Faculty, maximumCredits: int, maximumDays: int, minimumCredits: int,
                      uniqueCourseLimit: int, times: dict[Day, list[TimeRange]], coursePreferences: dict[Course, Preference],
                      roomPreferences: dict[Room, Preference], labPreferences: dict[Lab, Preference], mandatoryDays: set[Day]):
        #Reference to faculty list inside database
        fac = config.config.faculty

        #Checking to see if faculty exists under provided name
        for prof in fac:
            if prof.name == name:
                fac.remove(prof)
                newMember = FacultyConfig(name = name, maximum_credits = maximumCredits, maximum_days = maximumDays, 
                                          minimum_credits = minimumCredits, unique_course_limit = uniqueCourseLimit,
                                          times = times, course_preferences = coursePreferences, room_preferences = roomPreferences, 
                                          lab_preferences = labPreferences, mandatory_days = mandatoryDays)
                fac.append(newMember)
                print(f"Faculty member '{name}' modified successfully")
                return

        print("No such faculty member exists.")
        return
    

    #Delete Faculty
    #Delete an existing faculty from the configuration json
    #Parameters: Configuration file, name of faculty
    def deleteFaculty(self, config, name: Faculty):
        
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
    def printFaculty(self, config):
        faculty = config.config.faculty
        print("\nFaculty:")
        for prof in faculty:
            print(f"Name: {prof.name}, \n\tMax Credits: {prof.maximum_credits}, \n\tMax Days: {prof.maximum_days}, \n\tMin Credits: {prof.minimum_credits}, \n\tUnique Course Limit: {prof.unique_course_limit}, \n\tTimes: {prof.times}, \n\tCourse Preferences: {prof.course_preferences}, \n\tRoom Preferences: {prof.room_preferences}, \n\tLab Preferences: {prof.lab_preferences}, \n\tMandatory Days: {prof.mandatory_days}") 


    def validateEntry(self, config: str, facultyName: str, operation: str) -> bool:
    
        #Validates faculty entry based on operation type.
        
        #Parameters:
        # config: Configuration object
        # facultyName: Name of the faculty to validate
        # operation: 'add', 'modify', or 'delete'
        
        #Returns true if validation passes, False otherwise
    
        faculty_list = config.config.faculty
        
        # Check for empty input
        if facultyName == "":
            print("Error: Faculty name cannot be empty — returning to menu.")
            return False
        
        # Check if faculty exists
        facultyExists = False
        for fac in faculty_list:
            if fac.name.upper() == facultyName.upper():
                facultyExists = True
                break
        
        if operation == "add":
            if facultyExists:
                print(f"Error: Faculty '{facultyName}' already exists — returning to menu.")
                return False
        
        elif operation in ["modify", "delete"]:
            if not facultyExists:
                print(f"Error: Faculty '{facultyName}' does not exist — returning to menu.")
                return False
        
        return True