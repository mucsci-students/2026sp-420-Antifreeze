from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

class conflict():

    #initialize conflict subclass
    def __init__(self):
        return

    def validateEntry(self, config: str, courseID: str, operation: str, conflictingCourseID: str = None) -> bool:
        """
        Validates conflict entry based on operation type.
        
        Parameters:
        - config: Configuration object
        - courseID: ID of the course
        - operation: 'add', 'modify', or 'delete'
        - conflictingCourseID: ID of the conflicting course (optional)
        
        Returns:
        - True if validation passes, False otherwise
        """
        courses = config.config.courses
        
        # Check if main course exists
        courseFound = False
        targetCourse = None
        for course in courses:
            if course.course_id == courseID:
                courseFound = True
                targetCourse = course
                break
        
        if not courseFound:
            print(f"Error: Course '{courseID}' not found — returning to menu.")
            return False
        
        # For operations that need a conflicting course
        if conflictingCourseID:
            # Check if conflicting course exists in system
            conflictingCourseExists = False
            for course in courses:
                if course.course_id == conflictingCourseID:
                    conflictingCourseExists = True
                    break
            
            if not conflictingCourseExists:
                print(f"Error: Conflicting course '{conflictingCourseID}' not found — returning to menu.")
                return False
            
            if operation == "add":
                if conflictingCourseID in targetCourse.conflicts:
                    print(f"Error: Conflict already exists between '{courseID}' and '{conflictingCourseID}' — returning to menu.")
                    return False
            
            elif operation in ["modify", "delete"]:
                if conflictingCourseID not in targetCourse.conflicts:
                    print(f"Error: Conflict not found between '{courseID}' and '{conflictingCourseID}' — returning to menu.")
                    return False
        
        return True

    #Add Conflict
    #Adds a conflict between two courses
    #Parameters: courseID (the course to add conflict to), conflictingCourseID (the course that conflicts)
    #Example usage: addConflict("CMSC 140", "CMSC 161")
    # Note: This adds the conflict to the specified course. For bidirectional conflicts, call twice.
    def addConflict(self, config: str, courseID: str, conflictingCourseID: str):
        
        # Reference to courses list inside database
        courses = config.config.courses
        
        # Find the course to add conflict to
        courseFound = False
        for course in courses:
            if course.course_id == courseID:
                courseFound = True
                
                # Check if conflict already exists
                if conflictingCourseID in course.conflicts:
                    print(f"Conflict already exists between '{courseID}' and '{conflictingCourseID}' — no change made.")
                    return
                
                # Add the conflict
                course.conflicts.append(conflictingCourseID)
                print(f"Conflict added: '{courseID}' now conflicts with '{conflictingCourseID}'.")
                return
        
        if not courseFound:
            print(f"Course '{courseID}' not found — no changes made.")

    #Delete Conflict
    #Removes a conflict between two courses
    #Parameters: courseID (the course to remove conflict from), conflictingCourseID (the conflicting course to remove)
    #Example usage: deleteConflict("CMSC 140", "CMSC 161")
    def deleteConflict(self, config: str, courseID: str, conflictingCourseID: str):
        
        #Reference to courses list inside database
        courses = config.config.courses
        
        #Find the course to remove conflict from
        courseFound = False
        for course in courses:
            if course.course_id == courseID:
                courseFound = True
                
                # Check if conflict exists
                if conflictingCourseID not in course.conflicts:
                    print(f"Conflict not found between '{courseID}' and '{conflictingCourseID}' — nothing deleted.")
                    return
                
                # Remove the conflict
                course.conflicts.remove(conflictingCourseID)
                print(f"Conflict removed: '{courseID}' no longer conflicts with '{conflictingCourseID}'.")
                return
        
        if not courseFound:
            print(f"Course '{courseID}' not found — no changes made.")

    #Modify Conflict
    #Modifies an existing conflict by replacing the conflicting course
    #Parameters: courseID, oldConflictingCourseID, newConflictingCourseID
    #Example usage: modifyConflict("CMSC 140", "CMSC 161", "CMSC 162")
    def modifyConflict(self, config: str, courseID: str, oldConflictingCourseID: str, newConflictingCourseID: str):
        
        #Reference to courses list inside database
        courses = config.config.courses
        
        #Find the course to modify conflict in
        courseFound = False
        for course in courses:
            if course.course_id == courseID:
                courseFound = True
                
                #Check if old conflict exists
                if oldConflictingCourseID not in course.conflicts:
                    print(f"Original conflict not found between '{courseID}' and '{oldConflictingCourseID}' — no changes made.")
                    return
                
                #Check if new conflict already exists
                if newConflictingCourseID in course.conflicts:
                    print(f"New conflict already exists between '{courseID}' and '{newConflictingCourseID}' — choose a different course.")
                    return
                
                #Replace the conflict (maintain order)
                index = course.conflicts.index(oldConflictingCourseID)
                course.conflicts[index] = newConflictingCourseID
                print(f"Conflict modified: '{courseID}' now conflicts with '{newConflictingCourseID}' instead of '{oldConflictingCourseID}'.")
                return
        
        if not courseFound:
            print(f"Course '{courseID}' not found — no changes made.")

    def printConflicts(self, config: str):
        courses = config.config.courses
        print("\nCourse Conflicts:")
        for course in courses:            
            print(f"Course ID: {course.course_id}, \n\tConflicts: {course.conflicts}")