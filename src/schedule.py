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
        config = ""
        configLoaded = False
        scheduler = ""
        
    #TODO - wrap schedule into callable class
    #--------------#
    #FILE MANAGEMENT
    #TODO Implement feature
    def loadFile(self, fileName):
        try:
            config = load_config_from_file(CombinedConfig, fileName)
        except Exception as e:
            if(e):
                print("Could not load file, try again")
                print(e)
                return
        configLoaded = True
        scheduler = Scheduler(config)


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
    def add_lab(self, json_file: str, lab_name: str):

        path = Path(json_file)

        #Reads and parses JSON into a Python dict
        data = json.loads(path.read_text())

        #Reference to labs list inside data
        labs = data["config"]["labs"]

        #Checking for duplicate lab
        if lab_name in labs:
            print("Lab already exists — no change made.")
            return

        labs.append(lab_name)

        #Convert back to JSON
        path.write_text(json.dumps(data))
        print(f"Lab '{lab_name}' added successfully.")

    #Delete Lab
    #Deletes a lab from the configuration JSON
    #Parameters: Configuration file, Lab to delete
    #Example usage: delete_lab(example.json, Linux)
    def delete_lab(self, json_file: str, lab_name: str):
        path = Path(json_file)

        #Reads and parses JSON into a Python dict
        data = json.loads(path.read_text())

        #Reference to labs list inside data
        labs = data["config"]["labs"]

        if lab_name not in labs:
            print("Lab not found — nothing deleted.")
            return

        labs.remove(lab_name)

        #Convert back to JSON
        path.write_text(json.dumps(data))
        print(f"Lab '{lab_name}' deleted successfully.")
    
    #Modify Lab
    #Modifies a lab from the configuration JSON
    #Parameters: Configuration file, old name for lab, new name for lab
    #Example usage: modify_lab(example.json, Linux, Linux_0)
    def modify_lab(self, json_file: str, old_name: str, new_name: str):
        path = Path(json_file)

        #Reads and parses JSON into a Python dict
        data = json.loads(path.read_text())

        #Reference to labs list inside data
        labs = data["config"]["labs"]

        if old_name not in labs:
            print("Original lab not found — no changes made.")
            return

        if new_name in labs:
            print("New lab name already exists — choose a different name.")
            return


        #Replace so that order stays the same
        index = labs.index(old_name)
        labs[index] = new_name


        #Convert back to JSON
        path.write_text(json.dumps(data, indent=2))
        print(f"Lab renamed from '{old_name}' to '{new_name}'.") 
    
    #Add/Remove/Delete Lab tests
    def run_tests(self):
        source_file = "example.json"
        test_file = "example_test.json"

       
        s = self

        #copy example json so original isn't modified
        shutil.copy(source_file, test_file)

        print("Initial:", s.read_labs(test_file))

        s.add_lab(test_file, "Windows")
        print("After add:", s.read_labs(test_file))

        s.modify_lab(test_file, "Mac", "MacOS")
        print("After modify:", s.read_labs(test_file))

        s.delete_lab(test_file, "Linux")
        print("After delete:", s.read_labs(test_file))

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
