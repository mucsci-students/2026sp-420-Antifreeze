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
