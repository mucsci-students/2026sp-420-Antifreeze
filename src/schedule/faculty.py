from scheduler import (
    Scheduler,
    load_config_from_file,
    FacultyConfig,
)
from scheduler.config import CombinedConfig


class faculty():

    #initialize conflict subclass
    def __init__(self):
        return

    #Add Faculty
    #Adds a new faculty to the configuration json
    #Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
                #limit, times, course preferences, room preferences, lab preferences, mandatory days
    #Example usage: addFaculty(example.json, )
    def addFaculty(self, config, name: str, maximumCredits: int, maximumDays: int, minimumCredits: int,
                   uniqueCourseLimit: int, times: dict, coursePreferences: dict, roomPreferences: dict,
                   labPreferences: dict, mandatoryDays: set):
        #Reference to faculty list inside database
        faculty = config.faculty

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
    def modifyFaculty(self, config, name: str, maximumCredits: int, maximumDays: int, minimumCredits: int,
                   uniqueCourseLimit: int, times: dict, coursePreferences: dict, roomPreferences: dict,
                   labPreferences: dict, mandatoryDays: set):
        #Reference to faculty list inside database
        faculty = config.faculty

        #Checking to see if faculty exists under provided name
        for name in faculty:
            if faculty.name == name:
                self.deleteFaculty(name, config)
                self.addFaculty(config, name, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit,
                                times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)
                print(f"Faculty member '{name}' modified successfully")
            else:
                print("No such faculty member exists.")
    
    #Delete Faculty
    #Delete an existing faculty from the configuration json
    #Parameters: Configuration file, name of faculty
    #Example usage: deleteFaculty(example.json, "Hogg")
    def deleteFaculty(self, config, name: str):
        
        #Reference to faculty list inside database
        faculty = config.faculty

        #Checking to see if faculty exists under provided name
        for name in faculty:
            if faculty.name == name:
                faculty.remove(name)
                print(f"Faculty member '{name}' deleted successfully")
            else:
                print("No such faculty member exists.")

    