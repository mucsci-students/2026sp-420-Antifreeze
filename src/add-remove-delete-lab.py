import json
from pathlib import Path
import shutil

#Adds a lab to the configuration json
#Parameters: Configuration file, Lab to add
#Example usage: add_lab(example.json, Windows)
def add_lab(json_file: str, lab_name: str):

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



#Deletes a lab from the configuration JSON
#Parameters: Configuration file, Lab to delete
#Example usage: delete_lab(example.json, Linux)
def delete_lab(json_file: str, lab_name: str):
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


#Modifies a lab from the configuration JSON
#Parameters: Configuration file, old name for lab, new name for lab
#Example usage: modify_lab(example.json, Linux, Linux_0)
def modify_lab(json_file: str, old_name: str, new_name: str):
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




#tests
def run_tests():
    source_file = "example.json"
    test_file = "example_test.json"

    #copying the real config so we don't destroy it
    shutil.copy(source_file, test_file)

    print("Initial:", read_labs(test_file))

    add_lab(test_file, "Windows")
    print("After add:", read_labs(test_file))

    modify_lab(test_file, "Mac", "MacOS")
    print("After modify:", read_labs(test_file))

    delete_lab(test_file, "Linux")
    print("After delete:", read_labs(test_file))

def read_labs(file):
    with open(file) as f:
        return json.load(f)["config"]["labs"]


if __name__ == "__main__":
    run_tests()
