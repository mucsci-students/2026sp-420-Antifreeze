from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig


# Manages lab entries in the scheduler configuration.
class lab():

    # Initializes lab subclass.
    def __init__(self):
        return

    # Validates a lab entry based on operation type.
    # For 'add': fails if lab already exists or name is empty.
    # For 'modify' or 'delete': fails if lab does not exist.
    # Parameters: config, lab_name, operation ('add'/'modify'/'delete')
    # Returns: True if validation passes, False otherwise
    def validate_entry(self, config: str, lab_name: str, operation: str) -> bool:
        labs = config.config.labs
        
        # Check for empty input
        if lab_name == "":
            print("Error: Lab must have a name — returning to menu.")
            return False
        
        if operation == "add":
            if lab_name in labs:
                print(f"Error: Lab '{lab_name}' already exists — returning to menu.")
                return False
        
        elif operation in ["modify", "delete"]:
            if lab_name not in labs:
                print(f"Error: Lab '{lab_name}' does not exist — returning to menu.")
                return False
        
        return True

    # Adds a lab to the config.
    # Parameters: config, lab_name
    # Example: add_lab(config, "Windows")
    def add_lab(self, config: str, lab_name: str):

        # Reference to labs list inside database
        labs = config.config.labs

        # Checking for duplicate lab
        if lab_name in labs:
            print("Lab already exists — no change made.")
            return

        labs.append(lab_name)

        # Convert back to JSON
        print(f"Lab '{lab_name}' added successfully.")

    # Deletes a lab from the config.
    # Cascades removal to course lab lists and faculty lab preferences.
    # Parameters: config, lab_name
    # Example: delete_lab(config, "Linux")
    def delete_lab(self, config: str, lab_name: str):

        labs = config.config.labs

        if lab_name not in labs:
            print("Lab not found — nothing deleted.")
            return

        # Remove from labs list
        labs.remove(lab_name)

        # ---- Cascade: Courses ----
        for course in config.config.courses:
            if lab_name in course.lab:
                course.lab = [l for l in course.lab if l != lab_name]

        # ---- Cascade: Faculty Preferences ----
        for faculty in config.config.faculty:
            if lab_name in faculty.lab_preferences:
                del faculty.lab_preferences[lab_name]

        print(f"Lab '{lab_name}' deleted successfully.")
    
    # Renames a lab in the config.
    # Cascades the rename to course lab lists and faculty lab preferences.
    # Parameters: config, old_name, new_name
    # Example: modify_lab(config, "Linux", "Linux_0")
    def modify_lab(self, config: str, old_name: str, new_name: str):

        labs = config.config.labs

        if old_name not in labs:
            print("Original lab not found — no changes made.")
            return

        if new_name in labs:
            print("New lab name already exists — choose a different name.")
            return

        # Rename in labs list
        index = labs.index(old_name)
        labs[index] = new_name

        # ---- Cascade: Courses ----
        for course in config.config.courses:
            course.lab = [
                new_name if lab == old_name else lab
                for lab in course.lab
            ]

        # ---- Cascade: Faculty Preferences ----
        for faculty in config.config.faculty:
            prefs = faculty.lab_preferences
            if old_name in prefs:
                prefs[new_name] = prefs.pop(old_name)

        print(f"Lab renamed from '{old_name}' to '{new_name}'.")

    # Prints all labs in the config.
    # Parameters: config
    def print_labs(self, config: str):
        labs = config.config.labs
        print("\nLabs:")
        for lab in labs:            
            print(f"Name: {lab}")

    # Returns a list of all lab names from the config.
    # Parameters: config
    # Returns: List of lab name strings
    def get_lab_ids(self, config: str) -> list[str]:
        labs = config.config.labs
        return list(labs)

    # Parses the CSV schedule file and returns a dict mapping each lab name
    # to a list of course sections that use it. Skips rows with no assigned lab.
    # Each entry contains: course_id, section, faculty, room, meetings.
    # Parameters: csv_path - path to the CSV schedule file
    # Returns: Dict mapping lab name (str) to list of course info dicts
    def get_lab_schedule(self, csv_path: str) -> dict[str, list[dict]]:
        import csv

        lab_schedule = {}

        with open(csv_path, newline='') as f:
            for line in f:
                line = line.strip()

                # Skip blank lines and schedule header lines
                if not line or line.startswith("Schedule"):
                    continue

                parts = [p.strip() for p in line.split(',')]

                # Expect at least: course_section, faculty, room, lab, and one meeting
                if len(parts) < 5:
                    continue

                course_section = parts[0]
                faculty        = parts[1]
                room           = parts[2]
                lab_name       = parts[3]
                meetings       = parts[4:]

                # Only include rows that have an assigned lab
                if lab_name == "None" or lab_name == "":
                    continue

                course_id, _, section = course_section.partition('.')

                entry = {
                    "course_id": course_id,
                    "section": section,
                    "faculty": faculty,
                    "room": room,
                    "meetings": meetings
                }

                if lab_name not in lab_schedule:
                    lab_schedule[lab_name] = []
                lab_schedule[lab_name].append(entry)

        return lab_schedule