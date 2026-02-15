from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig


class lab():

    #initialize lab subclass
    def __init__(self):
        return

     #Add Lab
    #Adds a lab to the configuration json
    #Parameters: Configuration file, Lab to add
    #Example usage: add_lab(example.json, Windows)
    def addLab(self, config: str, lab_name: str):

        #Reference to labs list inside database
        labs = config.config.labs

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
    def deleteLab(self, config: str, lab_name: str):

        #Reference to labs list inside database
        labs = config.config.labs

        if lab_name not in labs:
            print("Lab not found — nothing deleted.")
            return

        labs.remove(lab_name)

        print(f"Lab '{lab_name}' deleted successfully.")
    
    #Modify Lab
    #Modifies a lab from the configuration JSON
    #Parameters: Configuration file, old name for lab, new name for lab
    #Example usage: modify_lab(example.json, Linux, Linux_0)
    def modifyLab(self, config: str, old_name: str, new_name: str):


        #Reference to labs list inside database
        labs = config.config.labs

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
    def runTests(self):
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
    
    #Print Labs
    #Prints all labs currently stored in the configuration
    #Displays the name of each lab
    #Parameters: Configuration file
    def printLabs(self, config: str):
        labs = config.config.labs
        print("\nLabs:")
        for lab in labs:            
            print(f"Name: {lab}")   




   
