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
import csv


# Manages course entries in the scheduler configuration.
class course():
     
    # Initializes course subclass.
    def __init__(self):
        return
    
    # Validates a course entry based on operation type.
    # For 'add': fails if course already exists.
    # For 'modify' or 'delete': fails if course does not exist.
    # Parameters: config, course_id, operation ('add'/'modify'/'delete')
    # Returns: True if validation passes, False otherwise
    def validate_entry(self, config: str, course_id: str, operation: str) -> bool:
        courses = [c.course_id.upper() for c in config.config.courses]
        
        if operation == "add":
            if course_id.upper() in courses:
                print(f"Error: Course '{course_id}' already exists — returning to menu.")
                return False
        
        elif operation in ["modify", "delete"]:
            if course_id.upper() not in courses:
                print(f"Error: Course '{course_id}' does not exist — returning to menu.")
                return False
        
        return True
    
    # Checks whether all referenced items (rooms, labs, conflicts, faculty) exist in the config.
    # Parameters: config, id (course_id), rms (rooms), lbs (labs), con (conflicts), fac (faculty)
    # Returns: True if all items exist, False if any are missing
    def existing_items(self, config: str, id: str, rms: list[str], lbs: list[str], con: list[str], fac: list[str]) -> bool:
            #variable being passed
            test = True
            # lists being tested against
            courses = [c.course_id.upper() for c in config.config.courses]
            labs = [l.upper() for l in config.config.labs]
            rooms = [r.upper() for r in config.config.rooms]
            fac_name = [f.name.upper() for f in config.config.faculty]
            
            #tests and error detection 
            for name in fac:
                if name.upper() not in fac_name:
                    test = False
                    print(f"the person '{name}' does not exist in the database\n")

            for rm in rms:
                if rm.upper() not in rooms:
                    test = False
                    print(f"the room '{rm}' does not exist in the database\n")

            for course_lab in lbs:
                if course_lab.upper() not in labs:
                    test = False
                    print(f"the lab '{course_lab}' does not exist in the database\n")

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
    
    # Adds a course to the config after validating all referenced items exist.
    # Parameters: config, id (course_id), creds (credits), rms (rooms),
    #             lbs (labs), con (conflicts), fac (faculty)
    def add_course(self, config: str, id: str, creds: int, rms: list[str], lbs: list[str], con: list[str], fac: list[str]):
            # calls existing_items to see if all values are able to be used.
            tests = self.existing_items(config, id, rms, lbs, con, fac)
            
            # if all values are good then we can finally add test to config   
            if tests is True:
                addition = CourseConfig(course_id=str(id), credits=int(creds), room=rms, lab=lbs, conflicts=con, faculty=fac)
                config.config.courses.append(addition)

    # Deletes a course from the config by ID.
    # Cascades removal to other course conflict lists and faculty course preferences.
    # Parameters: config, id (course_id)
    def delete_course(self, config, id: str):
        courses = config.config.courses
        target = None

        for course in courses:
            if course.course_id.upper() == id.upper():
                target = course
                break

        if target is None:
            print("Course does not exist — no changes made.")
            return

        # Remove the course
        courses.remove(target)

        # ---- Cascade: remove from other course conflicts ----
        for course in courses:
            if id in course.conflicts:
                course.conflicts = [c for c in course.conflicts if c.upper() != id.upper()]

        # ---- Cascade: remove from faculty course preferences ----
        for faculty in config.config.faculty:
            prefs = faculty.course_preferences
            if id in prefs:
                del prefs[id]

        print(f"Course '{id}' deleted successfully.")

    # Modifies an existing course in the config, including renaming.
    # Cascades the ID rename to other course conflict lists and faculty preferences.
    # Parameters: config, old_id, new_id, creds (credits), rms (rooms),
    #             lbs (labs), con (conflicts), fac (faculty)
    def modify_course(self, config, old_id: str, new_id: str,
                  creds: int, rms: list[str], lbs: list[str],
                  con: list[str], fac: list[str]):
        courses = config.config.courses
        target = None

        for course in courses:
            if course.course_id.upper() == old_id.upper():
                target = course
                break

        if target is None:
            print("Course not found.")
            return

        # ---- Rename course ----
        target.course_id = new_id

        # ---- Update other course conflicts ----
        for course in courses:
            course.conflicts = [
                new_id if c.upper() == old_id.upper() else c
                for c in course.conflicts
            ]

        # ---- Update faculty course preferences ----
        for faculty in config.config.faculty:
            prefs = faculty.course_preferences
            if old_id in prefs:
                prefs[new_id] = prefs.pop(old_id)

        # ---- Update remaining course fields ----
        target.credits = creds
        target.room = rms
        target.lab = lbs
        target.conflicts = con
        target.faculty = fac

        print(f"Course '{old_id}' modified to '{new_id}' successfully (cascade applied).")

    # Prints all courses in the config with their credits, rooms, labs, conflicts, and faculty.
    # Parameters: config
    def print_courses(self, config: str):
        courses = config.config.courses 
        print("\nCourses:")
        for course in courses:            
            print(f"Course ID: {course.course_id}, \n\tCredits: {course.credits}, \n\tRooms: {course.room}, \n\tLabs: {course.lab}, \n\tConflicts: {course.conflicts}, \n\tFaculty: {course.faculty}")
    
    # Returns a list of all course IDs from the config.
    # Parameters: config
    # Returns: List of course ID strings
    def get_course_id(self, config: str) -> list[str]:
            return [c.course_id for c in config.config.courses]

    # Parses the CSV schedule file and returns a list of all course entries,
    # sorted by course number then section.
    # Parameters: csv_path - path to the CSV schedule file
    # Returns: List of dicts with keys: course, faculty, room, lab, times
    def get_course_schedule(self, csv_path: str) -> list[dict]:
        courses = []
        
        with open(csv_path, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                
                course = {
                    "course": row[0].strip(),
                    "faculty": row[1].strip(),
                    "room": row[2].strip(),
                    "lab": row[3].strip(),
                    "times": [time.strip() for time in row[4:]]
                }
                courses.append(course)
        
        courses.sort(key=lambda c: (
            int(c["course"].split()[1].split(".")[0]),
            c["course"].split(".")[1]
        ))

        return courses