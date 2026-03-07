from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig

class conflict():

    #initialize conflict subclass
    def __init__(self):
        return

    def validate_entry(self, config, course_id: str, operation: str, conflicting_course_id: str = None) -> bool:
        """
        Validates conflict entry based on operation type.
        
        Parameters:
        - config: Configuration object
        - course_id: ID of the course
        - operation: 'add', 'modify', or 'delete'
        - conflicting_course_id: ID of the conflicting course (optional)
        
        Returns:
        - True if validation passes, False otherwise
        """
        if not course_id.strip():
            print(f"Error: Course ID cannot be empty.")
            return False
        courses = config.config.courses
        
        # Check if main course exists
        course_found = False
        target_course = None
        for course in courses:
            if course.course_id == course_id:
                course_found = True
                target_course = course
                break
        
        if not course_found:
            print(f"Error: Course '{course_id}' not found — returning to menu.")
            return False
        
        # For operations that need a conflicting course
        if conflicting_course_id:
            # Check if conflicting course exists in system
            conflicting_course_exists = False
            for course in courses:
                if course.course_id == conflicting_course_id:
                    conflicting_course_exists = True
                    break
            
            if not conflicting_course_exists:
                print(f"Error: Conflicting course '{conflicting_course_id}' not found — returning to menu.")
                return False
            
            if operation == "add":
                if conflicting_course_id in target_course.conflicts:
                    print(f"Error: Conflict already exists between '{course_id}' and '{conflicting_course_id}' — returning to menu.")
                    return False
            
            elif operation in ["modify", "delete"]:
                if conflicting_course_id not in target_course.conflicts:
                    print(f"Error: Conflict not found between '{course_id}' and '{conflicting_course_id}' — returning to menu.")
                    return False
        
        return True

    #Add Conflict
    #Adds a conflict between two courses
    #Parameters: course_id (the course to add conflict to), conflicting_course_id (the course that conflicts)
    #Example usage: add_conflict("CMSC 140", "CMSC 161")
    # Note: This adds the conflict to the specified course. For bidirectional conflicts, call twice.
    def add_conflict(self, config: str, course_id: str, conflicting_course_id: str):
        
        # Reference to courses list inside database
        courses = config.config.courses
        
        # Find the course to add conflict to
        course_found = False
        for course in courses:
            if course.course_id == course_id:
                course_found = True
                
                # Check if conflict already exists
                if conflicting_course_id in course.conflicts:
                    print(f"Conflict already exists between '{course_id}' and '{conflicting_course_id}' — no change made.")
                    return
                
                # Add the conflict
                course.conflicts.append(conflicting_course_id)
                print(f"Conflict added: '{course_id}' now conflicts with '{conflicting_course_id}'.")
                return
        
        if not course_found:
            print(f"Course '{course_id}' not found — no changes made.")

    #Delete Conflict
    #Removes a conflict between two courses
    #Parameters: course_id (the course to remove conflict from), conflicting_course_id (the conflicting course to remove)
    #Example usage: delete_conflict("CMSC 140", "CMSC 161")
    def delete_conflict(self, config: str, course_id: str, conflicting_course_id: str):
        
        #Reference to courses list inside database
        courses = config.config.courses
        
        #Find the course to remove conflict from
        course_found = False
        for course in courses:
            if course.course_id == course_id:
                course_found = True
                
                # Check if conflict exists
                if conflicting_course_id not in course.conflicts:
                    print(f"Conflict not found between '{course_id}' and '{conflicting_course_id}' — nothing deleted.")
                    return
                
                # Remove the conflict
                course.conflicts.remove(conflicting_course_id)
                print(f"Conflict removed: '{course_id}' no longer conflicts with '{conflicting_course_id}'.")
                return
        
        if not course_found:
            print(f"Course '{course_id}' not found — no changes made.")

    #Modify Conflict
    #Modifies an existing conflict by replacing the conflicting course
    #Parameters: course_id, old_conflicting_course_id, new_conflicting_course_id
    #Example usage: modify_conflict("CMSC 140", "CMSC 161", "CMSC 162")
    def modify_conflict(self, config: str, course_id: str, old_conflicting_course_id: str, new_conflicting_course_id: str):
        
        #Reference to courses list inside database
        courses = config.config.courses
        
        #Find the course to modify conflict in
        course_found = False
        for course in courses:
            if course.course_id == course_id:
                course_found = True
                
                #Check if old conflict exists
                if old_conflicting_course_id not in course.conflicts:
                    print(f"Original conflict not found between '{course_id}' and '{old_conflicting_course_id}' — no changes made.")
                    return
                
                #Check if new conflict already exists
                if new_conflicting_course_id in course.conflicts:
                    print(f"New conflict already exists between '{course_id}' and '{new_conflicting_course_id}' — choose a different course.")
                    return
                
                #Replace the conflict (maintain order)
                index = course.conflicts.index(old_conflicting_course_id)
                course.conflicts[index] = new_conflicting_course_id
                print(f"Conflict modified: '{course_id}' now conflicts with '{new_conflicting_course_id}' instead of '{old_conflicting_course_id}'.")
                return
        
        if not course_found:
            print(f"Course '{course_id}' not found — no changes made.")

    #Print Conflicts
    #Prints all course conflicts currently stored in the configuration
    #Displays each course ID along with its associated conflict list
    #Parameters: Configuration file
    def print_conflicts(self, config: str):
        courses = config.config.courses
        print("\nCourse Conflicts:")
        for course in courses:            
            print(f"Course ID: {course.course_id}, \n\tConflicts: {course.conflicts}")