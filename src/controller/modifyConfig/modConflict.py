from controller.modifyConfig.utilsCLI import prompt, endProg

#Print Modify Conflict Menu
#Displays the conflict modification menu options to the user
def printModConflictMenu():
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
def modConflictMain(sched):
    while(True):
        printModConflictMenu()
        userCommand = input()
        if(userCommand == "1"):
            addConflict(sched)
        elif(userCommand == "2"):   
            modConflict(sched)
        elif(userCommand == "3"):
            delConflict(sched)
        elif(userCommand == "4"):
            sched.conflict.printConflicts(sched.config)
        elif(userCommand.lower() == "r"):
            return
        elif(userCommand.lower() == "q"):
            endProg()
        else:
            print("Invalid command, try again.")


#Delete Conflict
#Removes an existing conflict between two courses
#Prompts the user for a course ID and conflicting course ID
#Parameters: Scheduler object
def delConflict(sched):
    try:
        print("press r and enter at any time to return to main\n")

        courseID = prompt("Enter CourseID to remove conflict for\n==> ")
        
        # Validate course exists immediately
        if not sched.conflict.validateEntry(sched.config, courseID, "delete"):
            return
        
        conflictingCourseID = prompt("Enter conflicting course ID\n==> ")
        
        # Validate conflict exists immediately
        if not sched.conflict.validateEntry(sched.config, courseID, "delete", conflictingCourseID):
            return

        sched.conflict.deleteConflict(
            sched.config,
            courseID,
            conflictingCourseID
        )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return




#Add Conflict
#Adds a conflict between two courses in the configuration
#Prompts the user for a course ID and conflicting course ID
#Parameters: Scheduler object
def addConflict(sched):
    try:
        print("press r and enter at any time to return to main\n")

        courseID = prompt("Enter CourseID to add conflict to\n==> ")
        
        # Validate course exists immediately
        if not sched.conflict.validateEntry(sched.config, courseID, "add"):
            return
        
        conflictingCourseID = prompt("Enter conflicting course ID\n==> ")
        
        # Validate conflict can be added immediately
        if not sched.conflict.validateEntry(sched.config, courseID, "add", conflictingCourseID):
            return

        sched.conflict.addConflict(
            sched.config,
            courseID,
            conflictingCourseID
        )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return

        
#Modify Conflict
#Replaces an existing course conflict with a new conflicting course
#Prompts the user for a course ID, old conflict, and new conflict
#Parameters: Scheduler object
def modConflict(sched):
    try:
        print("press r and enter at any time to return to main\n")

        courseID = prompt("Enter CourseID to modify\n==> ")
        
        # Validate course exists immediately
        if not sched.conflict.validateEntry(sched.config, courseID, "modify"):
            return
        
        oldConfCourseID = prompt("Enter old conflicting course ID\n==> ")
        
        # Validate old conflict exists immediately
        if not sched.conflict.validateEntry(sched.config, courseID, "modify", oldConfCourseID):
            return
        
        newConfCourseID = prompt("Enter new conflicting course ID\n==> ")
        
        # Validate new conflict can be added immediately
        if not sched.conflict.validateEntry(sched.config, courseID, "add", newConfCourseID):
            return

        sched.conflict.modifyConflict(
            sched.config,
            courseID,
            oldConfCourseID,
            newConfCourseID
        )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return