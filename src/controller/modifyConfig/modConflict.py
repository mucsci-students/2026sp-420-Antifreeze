from controller.modifyConfig.utilsCLI import prompt, end_prog

#Print Modify Conflict Menu
#Displays the conflict modification menu options to the user
def print_mod_conflict_menu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add conflict")
    print("2: Modify conflict")
    print("3: Remove conflict")
    print("4: Print conflicts")
    print("r: return to main")
    print("q: exit program\n==> ",end="")


#Modify Conflict Main
#Main control loop for conflict modification operations
#Routes user input to add, modify, delete, or print conflict actions
#Parameters: Scheduler object
def mod_conflict_main(sched):
    while(True):
        print_mod_conflict_menu()
        user_command = input()
        if(user_command == "1"):
            add_conflict(sched)
        elif(user_command == "2"):   
            mod_conflict(sched)
        elif(user_command == "3"):
            del_conflict(sched)
        elif(user_command == "4"):
            sched.conflict.print_conflicts(sched.config)
        elif(user_command.lower() == "r"):
            return
        elif(user_command.lower() == "q"):
            end_prog()
        else:
            print("Invalid command, try again.")


#Delete Conflict
#Removes an existing conflict between two courses
#Prompts the user for a course ID and conflicting course ID
#Parameters: Scheduler object
def del_conflict(sched):
    try:
        print("press r and enter at any time to return to main\n")

        course_id = prompt("Enter CourseID to remove conflict for\n==> ")
        
        # Validate course exists immediately
        if not sched.conflict.validate_entry(sched.config, course_id, "delete"):
            return
        
        conflicting_course_id = prompt("Enter conflicting course ID\n==> ")
        
        # Validate conflict exists immediately
        if not sched.conflict.validate_entry(sched.config, course_id, "delete", conflicting_course_id):
            return

        sched.conflict.delete_conflict(
            sched.config,
            course_id,
            conflicting_course_id
        )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return




#Add Conflict
#Adds a conflict between two courses in the configuration
#Prompts the user for a course ID and conflicting course ID
#Parameters: Scheduler object
def add_conflict(sched):
    try:
        print("press r and enter at any time to return to main\n")

        course_id = prompt("Enter CourseID to add conflict to\n==> ")
        
        # Validate course exists immediately
        if not sched.conflict.validate_entry(sched.config, course_id, "add"):
            return
        
        conflicting_course_id = prompt("Enter conflicting course ID\n==> ")
        
        # Validate conflict can be added immediately
        if not sched.conflict.validate_entry(sched.config, course_id, "add", conflicting_course_id):
            return

        sched.conflict.add_conflict(
            sched.config,
            course_id,
            conflicting_course_id
        )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return

        
#Modify Conflict
#Replaces an existing course conflict with a new conflicting course
#Prompts the user for a course ID, old conflict, and new conflict
#Parameters: Scheduler object
def mod_conflict(sched):
    try:
        print("press r and enter at any time to return to main\n")

        course_id = prompt("Enter CourseID to modify\n==> ")
        
        # Validate course exists immediately
        if not sched.conflict.validate_entry(sched.config, course_id, "modify"):
            return
        
        old_conf_course_id = prompt("Enter old conflicting course ID\n==> ")
        
        # Validate old conflict exists immediately
        if not sched.conflict.validate_entry(sched.config, course_id, "modify", old_conf_course_id):
            return
        
        new_conf_course_id = prompt("Enter new conflicting course ID\n==> ")
        
        # Validate new conflict can be added immediately
        if not sched.conflict.validate_entry(sched.config, course_id, "add", new_conf_course_id):
            return

        sched.conflict.modify_conflict(
            sched.config,
            course_id,
            old_conf_course_id,
            new_conf_course_id
        )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return