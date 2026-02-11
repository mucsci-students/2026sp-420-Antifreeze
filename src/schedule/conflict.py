from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

# TODO - create subclass details
class conflict():


    #initialize conflict subclass
    def __init__(self):
        return

  #Add Conflict
    #Adds a conflict between two courses
    #Parameters: courseID (the course to add conflict to), conflictingCourseID (the course that conflicts)
    #Example usage: addConflict("CMSC 140", "CMSC 161")
    # Note: This adds the conflict to the specified course. For bidirectional conflicts, call twice.
    def addConflict(self, config: str, courseID: str, conflictingCourseID: str):
        
        # Reference to courses list inside database
        courses = self.config.config.courses
        
        # Find the course to add conflict to
        courseFound = False
        for course in courses:
            if course.courseID == courseID:
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
        courses = self.config.config.courses
        
        #Find the course to remove conflict from
        courseFound = False
        for course in courses:
            if course.courseID == courseID:
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
        courses = self.config.config.courses
        
        #Find the course to modify conflict in
        courseFound = False
        for course in courses:
            if course.courseID == courseID:
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


   
    #Add/Remove/Modify Conflict tests
    def runConflictTests(self):
        print("\n" + "="*60)
        print("CONFLICT TESTS")
        print("="*60 + "\n")
        
        self.loadFile("example.json")
        
        # Display initial conflicts for a specific course
        print("Initial conflicts for CMSC 140:")
        for course in self.config.config.courses:
            if course.courseID == "CMSC 140":
                print(f"  {course.conflicts}")
                break
        
        print("\n--- Test 1: Add a new conflict ---")
        self.addConflict("CMSC 140", "CMSC 330")
        for course in self.config.config.courses:
            if course.courseID == "CMSC 140":
                print(f"Updated conflicts: {course.conflicts}")
                break
        
        print("\n--- Test 2: Try to add duplicate conflict ---")
        self.addConflict("CMSC 140", "CMSC 161")  # Already exists
        
        print("\n--- Test 3: Modify an existing conflict ---")
        self.modifyConflict("CMSC 140", "CMSC 161", "CMSC 340")
        for course in self.config.config.courses:
            if course.courseID == "CMSC 140":
                print(f"Updated conflicts: {course.conflicts}")
                break
        
        print("\n--- Test 4: Try to modify non-existent conflict ---")
        self.modifyConflict("CMSC 140", "CMSC 999", "CMSC 340")
        
        print("\n--- Test 5: Delete a conflict ---")
        self.deleteConflict("CMSC 140", "CMSC 162")
        for course in self.config.config.courses:
            if course.courseID == "CMSC 140":
                print(f"Updated conflicts: {course.conflicts}")
                break
        
        print("\n--- Test 6: Try to delete non-existent conflict ---")
        self.deleteConflict("CMSC 140", "CMSC 999")
        
        print("\n--- Test 7: Try to add conflict to non-existent course ---")
        self.addConflict("CMSC 999", "CMSC 140")
        
        print("\n" + "="*60)
        print("CONFLICT TESTS COMPLETED")
        print("="*60 + "\n")
    
