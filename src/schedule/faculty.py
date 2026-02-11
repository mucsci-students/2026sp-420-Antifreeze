from scheduler import (
    Scheduler,
    load_config_from_file,
    FacultyConfig,
    Faculty,
    Day,
    TimeRange,
    Course,
    Preference,
    Room,
    Lab
)
from scheduler.config import CombinedConfig

# TODO - create subclass details
class faculty():
    #TODO - initialize conflict subclass
    def __init__(self):
        return
    
    #Test Add Faculty
    #A temporary test to check if addFaculty works
    def testAddFaculty(self, config, name: Faculty, maximumCredits: int, maximumDays: int, minimumCredits: int,
                       uniqueCourseLimit: int, times: dict[Day, list[TimeRange]], coursePreferences: dict[Course, Preference],
                       roomPreferences: dict[Room, Preference], labPreferences: dict[Lab, Preference], 
                       mandatoryDays: set[Day]) -> bool:
        
        #Boolean test
        test = True

        #Some of the parameters that are being tested against
        courses = [c.upper() for c in config.courses]
        rooms = [r.upper() for r in config.rooms]
        labs = [l.upper() for l in config.rooms]

        #Testing parameters
        if type(times) != dict[Day, list[TimeRange]]:
            test = False
            print("Wrong input for times.")
        return test

    #Add Faculty
    #Adds a new faculty to the configuration json
    #Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
                #limit, times, course preferences, room preferences, lab preferences, mandatory days
    #Example usage: addFaculty(example.json, )
    def addFaculty(self, config, name: Faculty, maximumCredits: int, maximumDays: int, minimumCredits: int,
                   uniqueCourseLimit: int, times: dict[Day, list[TimeRange]], coursePreferences: dict[Course, Preference],
                   roomPreferences: dict[Room, Preference], labPreferences: dict[Lab, Preference], mandatoryDays: set[Day]):
        #Reference to faculty list inside database
        faculty = config.faculty

        #Test if parameters are correct
        test = self.testAddFaculty(name, config, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit,
                                   times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)

        #Checking for duplicate faculty name
        if name in faculty:
            print("Faculty already exists - no change made.")
        
        newMember = FacultyConfig(name, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit,
                                   times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)
        faculty.append(newMember)
        print(f"Faculty member '{name}' added successfully")
    
    #Modify Faculty
    #Modifies the details of an existing faculty member in the configuration json
    #Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
                #limit, times, course preferences, room preferences, lab preferences, mandatory days
    #Example usage: addFaculty(example.json, )
    def modifyFaculty(self, config, name: Faculty, maximumCredits: int, maximumDays: int, minimumCredits: int,
                      uniqueCourseLimit: int, times: dict[Day, list[TimeRange]], coursePreferences: dict[Course, Preference],
                      roomPreferences: dict[Room, Preference], labPreferences: dict[Lab, Preference], mandatoryDays: set[Day]):
        #Reference to faculty list inside database
        faculty = config.faculty

        #Checking to see if faculty exists under provided name
        for name in faculty:
            if faculty.name == name:
                self.deleteFaculty(name)
                self.addCourse(name, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit,
                                times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)
                print(f"Faculty member '{name}' modified successfully")
            else:
                print("No such faculty member exists.")
    
    #Delete Faculty
    #Delete an existing faculty from the configuration json
    #Parameters: Configuration file, name of faculty
    #Example usage: deleteFaculty(example.json, "Hogg")
    def deleteFaculty(self, config, name: Faculty):
        
        #Reference to faculty list inside database
        faculty = config.faculty

        #Checking to see if faculty exists under provided name
        for name in faculty:
            if faculty.name == name:
                faculty.remove(name)
                print(f"Faculty member '{name}' deleted successfully")
            else:
                print("No such faculty member exists.")