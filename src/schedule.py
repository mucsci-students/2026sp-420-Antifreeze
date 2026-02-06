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


    #Read labs function to help testing
    def read_labs(self, file):
            return json.load(open(file))["config"]["labs"]
        
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
    #TODO Implement feature
    def addConflict(self):
        return

    #TODO Implement feature
    def deleteConflict(self):
        return

    #TODO Implement feature
    def modifyConflict(self):
        return

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
if __name__ == "__main__":
    schedule().run_tests()