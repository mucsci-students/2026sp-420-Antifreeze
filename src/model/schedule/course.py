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
from scheduler.config import CombinedConfig, CourseConfig


class course():
     
    #initialize course subclass
    def __init__(self):
        return
    
    def validateEntry(self, config: str, courseID: str, operation: str) -> bool:
        """
        Validates course entry based on operation type.
        
        Parameters:
        - config: Configuration object
        - courseID: ID of the course to validate
        - operation: 'add', 'modify', or 'delete'
        
        Returns:
        - True if validation passes, False otherwise
        """
        courses = [c.course_id.upper() for c in config.config.courses]
        
        if operation == "add":
            if courseID.upper() in courses:
                print(f"Error: Course '{courseID}' already exists — returning to menu.")
                return False
        
        elif operation in ["modify", "delete"]:
            if courseID.upper() not in courses:
                print(f"Error: Course '{courseID}' does not exist — returning to menu.")
                return False
        
        return True
    
    # Existing Item
    # Tests to see if params passed exist in the config
    # params: Config with data, course_id, list of rooms, list of labs, list fo conflicts, list of faculty
    def existingItems(self,config:str, id:str, rms:list[str], lbs:list[str],con: list[str], fac:list[str]) ->bool:
            #variable being passed
            test = True
            # lists being tested against
            courses = [c.course_id.upper() for c in config.config.courses]
            labs = [l.upper() for l in config.config.labs]
            rooms = [r.upper() for r in config.config.rooms]
            facName =[f.name.upper() for f in config.config.faculty]
            
        
            #tests and error detection 
            for name in fac:
                if name.upper() not in facName:
                    test = False
                    print(f"the person '{name}' does not exist in the database\n")


            for rm in rms:
                if rm.upper() not in rooms:
                    test = False
                    print(f"the room '{rm}' does not exist in the database\n")
                
                
                
            for courseLab in lbs:
                if courseLab.upper() not in labs:
                    test = False
                    print(f"the lab '{courseLab}' does not exist in the database\n")

            for c in con:
                if c.upper() not in courses:
                    test = False
                    print(f"the course '{c}' does not exist in the list of courses\n")
            
                    
        
            for course in courses:
                if course == id.upper():
                    test = False
                    print("course already exists")
            # Returns bool
            return test
    
    # add Courses
    # Adds a Course to Config
    #Params: data to parse in config,course_id, list of room names, list of lab names, list of conflicts, list of faculty
    def addCourse(self,config: str,id: str, creds: int, rms: list[str], lbs: list[str], con: list[str], fac: list[str]):
            # calls existingItems to see if all values are able to be used.
            tests = self.existingItems(config,id,rms,lbs,con,fac)
            
            
            # if all values are good then we can finally add test to config   
            if tests is True :
                addition = CourseConfig( course_id= str(id), credits= int(creds), room= rms, lab= lbs, conflicts= con,faculty= fac)
                config.config.courses.append(addition)
            

    # Delete Course
    # Deletes a course already in the Config
    # Params: id of course
    def deleteCourse(self,config, id: str):
            courses = config.config.courses
            for course in courses:
                if course.course_id.upper() == id.upper():
                    config.config.courses.remove(course)
                    print('Deleted data')
                    return
            print("course DOES NOT already exists")
            
            

    # Modifys Course
    # Modifys a Course already present in configs 
    #Params: course_id, list of room names, list of lab names, list of conflicts, list of faculty
    def modifyCourse(self,config,id: str, creds: int, rms: list[str], lbs: list[str], con: list[str], fac: list[str]):
            
            courses = config.config.courses

            for course in courses:
                if course.course_id.upper() == id.upper():
                    self.deleteCourse(config=config, id=id)
                    self.addCourse(config=config,id=id,creds=creds,rms=rms,lbs=lbs,con=con,fac=fac)
                    print("Modified successfully. ")
                    return
            print("dont have it.")
        
    #Print Courses
    #Prints all courses currently stored in the configuration
    #Displays course details including credits, assigned rooms, labs,
    #conflicts, and associated faculty
    #Parameters: Configuration file
    def printCourses(self, config: str):
        courses = config.config.courses 
        print("\nCourses:")
        for course in courses:            
            print(f"Course ID: {course.course_id}, \n\tCredits: {course.credits}, \n\tRooms: {course.room}, \n\tLabs: {course.lab}, \n\tConflicts: {course.conflicts}, \n\tFaculty: {course.faculty}")
