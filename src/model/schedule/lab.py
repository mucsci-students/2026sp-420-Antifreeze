class lab():

    #initialize lab subclass
    def __init__(self):
        return

    def validate_entry(self, config: str, lab_name: str, operation: str) -> bool:
        """
        Validates lab entry based on operation type.
        
        Parameters:
        - config: Configuration object
        - lab_name: Name of the lab to validate
        - operation: 'add', 'modify', or 'delete'
        
        Returns:
        - True if validation passes, False otherwise
        """
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

    #Add Lab
    #Adds a lab to the configuration json
    #Parameters: Configuration file, Lab to add
    #Example usage: add_lab(example.json, Windows)
    def add_lab(self, config: str, lab_name: str):

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
    
    #Modify Lab
    #Modifies a lab from the configuration JSON
    #Parameters: Configuration file, old name for lab, new name for lab
    #Example usage: modify_lab(example.json, Linux, Linux_0)
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
    

    
    #Print Labs
    #Prints all labs currently stored in the configuration
    #Displays the name of each lab
    #Parameters: Configuration file
    def print_labs(self, config: str):
        labs = config.config.labs
        print("\nLabs:")
        for lab in labs:            
            print(f"Name: {lab}")

    #Get Lab IDs
    #Returns a list of lab names (IDs) from the configuration JSON
    #Parameters: Configuration file
    #Returns: List of lab name strings
    def get_lab_ids(self, config: str) -> list[str]:
        labs = config.config.labs
        return list(labs)

    #Get Lab Schedule
    #Returns a dictionary mapping each lab name to a list of course sections
    #that use that lab, parsed from a CSV schedule file
    #Each entry contains course ID, section, faculty, room, and meeting times
    #The lab session meeting is identified by a trailing '^' in the time field
    #Parameters: csv_path - path to the CSV schedule file
    #Returns: Dictionary mapping lab name (str) to list of course info dicts
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