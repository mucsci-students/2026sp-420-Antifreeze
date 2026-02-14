from modifyConfig.utilsCLI import prompt, endProg

def printModConflictMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add conflict")
    print("2: Modify conflict")
    print("3: Remove conflict")
    print("4: Print conflicts")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

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

def delConflict(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            courseID = prompt("Enter CourseID to remove conflict for\n==> ")
            conflictingCourseID = prompt("Enter conflicting course ID\n==> ")

            sched.conflict.deleteConflict(
                sched.config,
                courseID,
                conflictingCourseID
            )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return





def addConflict(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            courseID = prompt("Enter CourseID to add conflict to\n==> ")
            conflictingCourseID = prompt("Enter conflicting course ID\n==> ")

            sched.conflict.addConflict(
                sched.config,
                courseID,
                conflictingCourseID
            )

    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return

        
    
def modConflict(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            courseID = prompt("Enter CourseID to modify\n==> ")
            oldConfCourseID = prompt("Enter old conflicting course ID\n==> ")
            newConfCourseID = prompt("Enter new conflicting course ID\n==> ")

            sched.conflict.modifyConflict(
                sched.config,
                courseID,
                oldConfCourseID,
                newConfCourseID
            )


    except KeyboardInterrupt:
        print("\nReturning to conflict menu...")
        return
