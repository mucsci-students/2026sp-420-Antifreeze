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

def existingItems(self, id:str, rms:list[str], lbs:list[str],con: list[str], fac:list[str]) ->bool:
        #variable being passed
        test = True
        # lists being tested against
        courses = self.config.config.courses
        labs = [l.upper() for l in self.config.config.labs]
        rooms = [r.upper() for r in self.config.config.rooms]
       
        #tests and error detection 
        for rm in rms:
            if rm.upper() not in rooms:
                test = False
                print(f"the Room '{rm}' does not exist in the database\n")
               
            
            
        for courseLab in lbs:
            if courseLab.upper() not in labs:
                test = False
                print(f"the lab '{courseLab}' does not exist in the database\n")

        for c in con:
             if c.upper() not in courses:
                  test = False
                  print(f"the course '{c}' does not exist in the list of courses\n")
        
                
       
        for course in courses:
            if course.course_id.upper() == id.upper():
                test = False
                print("course already exists")
                
        return test
# add Courses
# Adds a Course to Config
#Params: course_id, list of room names, list of lab names, list of conflicts, list of faculty
def addCourse(self,id: str, creds: int, rms: list[str], lbs: list[str], con: list[str], fac: list[str]):
        # calls existingItems to see if all values are able to be used.
        tests = self.existingItems(id,rms,lbs,con,fac)
        
        
         # if all values are good then we can finally add test to config   
        if tests is True :
            addition = CourseConfig( course_id= str(id), credits= int(creds), room= rms, lab= lbs, conflicts= con,faculty= fac)
            self.config.config.courses.append(addition)
        

# Delete Course
# Deletes a course already in the Config
# Params: id of course
def deleteCourse(self, id: str):
        courses = self.config.config.courses
        for course in courses:
            if course.course_id.upper() == id.upper():
                self.config.config.courses.remove(course)
                print('deleted')
                return
        print("course DOES NOT already exists")
        
        

# Modifys Course
# Modifys a Course already present in configs 
#Params: course_id, list of room names, list of lab names, list of conflicts, list of faculty
def modifyCourse(self,id: str, creds: int, rms: list[str], lbs: list[str], con: list[str], fac: list[str]):
        
        courses = self.config.config.courses

        for course in courses:
            if course.course_id.upper() == id.upper():
                self.deleteCourse(id)
                self.addCourse(id,creds,rms,lbs,con,fac)
                return
        print("dont have it.")
    
    
def returnConfig(self):
        print(self.config.config.courses)
        print('\n')

