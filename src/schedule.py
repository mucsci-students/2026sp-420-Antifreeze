from scheduler import (
    Scheduler,
    load_config_from_file,
)


from scheduler.config import CombinedConfig
import json
from pathlib import Path
import shutil

class schedule:
    def __init__(self):
        self.config = None
        self.configLoaded = False
        self.scheduler = None
        
    #TODO - wrap schedule into callable class
    #--------------#
    #FILE MANAGEMENT
    #TODO Implement feature
    def loadFile(self, fileName):
        try:
            self.config = load_config_from_file(CombinedConfig, fileName)
        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
        configLoaded = True
        scheduler = Scheduler(self.config)


    #TODO Implement feature
    def saveFile(self):
        return

    #TODO Implement feature
    def printFile(self):
        return


    #--------------#
    #LABS

    #Add Lab
    #Adds a lab to the configuration json
    #Parameters: Configuration file, Lab to add
    #Example usage: add_lab(example.json, Windows)
    def add_lab(self, lab_name: str):

        #Reference to labs list inside database
        labs = self.config.config.labs

        #Checking for duplicate lab
        if lab_name in labs:
            print("Lab already exists — no change made.")
            return

        labs.append(lab_name)

        #Convert back to JSON
        print(f"Lab '{lab_name}' added successfully.")

    #Delete Lab
    #Deletes a lab from the configuration JSON
    #Parameters: Configuration file, Lab to delete
    #Example usage: delete_lab(example.json, Linux)
    def delete_lab(self, lab_name: str):

        #Reference to labs list inside database
        labs = self.config.config.labs

        if lab_name not in labs:
            print("Lab not found — nothing deleted.")
            return

        labs.remove(lab_name)

        print(f"Lab '{lab_name}' deleted successfully.")
    
    #Modify Lab
    #Modifies a lab from the configuration JSON
    #Parameters: Configuration file, old name for lab, new name for lab
    #Example usage: modify_lab(example.json, Linux, Linux_0)
    def modify_lab(self, old_name: str, new_name: str):


        #Reference to labs list inside database
        labs = self.config.config.labs

        if old_name not in labs:
            print("Original lab not found — no changes made.")
            return

        if new_name in labs:
            print("New lab name already exists — choose a different name.")
            return

        #Replace so that order stays the same
        index = labs.index(old_name)
        labs[index] = new_name

        print(f"Lab renamed from '{old_name}' to '{new_name}'.") 
    
    #Add/Remove/Delete Lab tests
    def run_tests(self):
        source_file = "example.json"
        test_file = "example_test.json"
        self.loadFile("example.json")

       
        s = self

        self.loadFile("example.json")

        print("Initial labs:", self.config.config.labs)

        self.add_lab("Windows")
        print("After add:", self.config.config.labs)

        self.modify_lab("Mac", "MacOS")
        print("After modify:", self.config.config.labs)

        self.delete_lab("Linux")
        print("After delete:", self.config.config.labs)
        
    #--------------#
    #ROOMS
    #TODO Implement feature
    def addRoom(self):
        return

    #TODO Implement feature
    def deleteRoom(self):
        return

    #TODO Implement feature
    def modifyRoom(self):
        return

     #--------------#
    #CONFLICT
    
    #Add Conflict
    #Adds a conflict between two courses
    #Parameters: course_id (the course to add conflict to), conflicting_course_id (the course that conflicts)
    #Example usage: add_conflict("CMSC 140", "CMSC 161")
    # Note: This adds the conflict to the specified course. For bidirectional conflicts, call twice.
    def add_conflict(self, course_id: str, conflicting_course_id: str):
        
        # Reference to courses list inside database
        courses = self.config.config.courses
        
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
    def delete_conflict(self, course_id: str, conflicting_course_id: str):
        
        #Reference to courses list inside database
        courses = self.config.config.courses
        
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
    def modify_conflict(self, course_id: str, old_conflicting_course_id: str, new_conflicting_course_id: str):
        
        #Reference to courses list inside database
        courses = self.config.config.courses
        
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

   
    #Add/Remove/Modify Conflict tests
    def run_conflict_tests(self):
        print("\n" + "="*60)
        print("CONFLICT TESTS")
        print("="*60 + "\n")
        
        self.loadFile("example.json")
        
        # Display initial conflicts for a specific course
        print("Initial conflicts for CMSC 140:")
        for course in self.config.config.courses:
            if course.course_id == "CMSC 140":
                print(f"  {course.conflicts}")
                break
        
        print("\n--- Test 1: Add a new conflict ---")
        self.add_conflict("CMSC 140", "CMSC 330")
        for course in self.config.config.courses:
            if course.course_id == "CMSC 140":
                print(f"Updated conflicts: {course.conflicts}")
                break
        
        print("\n--- Test 2: Try to add duplicate conflict ---")
        self.add_conflict("CMSC 140", "CMSC 161")  # Already exists
        
        print("\n--- Test 3: Modify an existing conflict ---")
        self.modify_conflict("CMSC 140", "CMSC 161", "CMSC 340")
        for course in self.config.config.courses:
            if course.course_id == "CMSC 140":
                print(f"Updated conflicts: {course.conflicts}")
                break
        
        print("\n--- Test 4: Try to modify non-existent conflict ---")
        self.modify_conflict("CMSC 140", "CMSC 999", "CMSC 340")
        
        print("\n--- Test 5: Delete a conflict ---")
        self.delete_conflict("CMSC 140", "CMSC 162")
        for course in self.config.config.courses:
            if course.course_id == "CMSC 140":
                print(f"Updated conflicts: {course.conflicts}")
                break
        
        print("\n--- Test 6: Try to delete non-existent conflict ---")
        self.delete_conflict("CMSC 140", "CMSC 999")
        
        print("\n--- Test 7: Try to add conflict to non-existent course ---")
        self.add_conflict("CMSC 999", "CMSC 140")
        
        print("\n" + "="*60)
        print("CONFLICT TESTS COMPLETED")
        print("="*60 + "\n")

    #Read labs function to help testing
    def read_labs(self, file):
            return json.load(open(file))["config"]["labs"]

    #--------------#
    #FACULTY
    #TODO Implement feature
    def addFaculty(self):
        return

    #TODO Implement feature
    def deleteFaculty(self):
        return

    #TODO Implement feature
    def modifyFaculty(self):
        return

    #--------------#
    #COURSE
    #TODO Implement feature
    def addCourse(self):
        return

    #TODO Implement feature
    def deleteCourse(self):
        return

    #TODO Implement feature
    def modifyCourse(self):
        return


    #--------------#
    #SCHEDULER

    #TODO Implement feature
    def runScheduler(self):
        return

    #TODO Implement feature
    def displaySchedule(self):
        return
