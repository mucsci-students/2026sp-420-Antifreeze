def printModConflictMenu():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Add conflict")
    print("2: Modify conflict")
    print("3: Remove conflict")
    print("r: return to main\n==> ",end="")

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
        elif(userCommand.lower() == "r"):
            return

def delConflict(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter CourseID to remove conflict for\n==> ",end="")
        courseID = input()
    
        print("Enter conflicting course ID\n==> ",end="")
        conflictingCourseID = input()
        
        fields = [
            courseID, conflictingCourseID
        ]
        if any(str(x).lower() == "r" for x in fields):
            return
        
        sched.conflict.deleteConflict(sched.config, courseID, conflictingCourseID)



def addConflict(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter CourseID to add conflict to\n==> ",end="")
        courseID = input()
        
        print("Enter conflicting course ID\n==> ",end="")
        conflictingCourseID = input()
        
        fields = [
            courseID, conflictingCourseID
        ]
        if any(str(x).lower() == "r" for x in fields):
            return
        
        sched.conflict.addConflict(sched.config, courseID, conflictingCourseID)
        
    
def modConflict(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter CourseID to modify\n==> ",end="")
        courseID = input()
        
        print("Enter old conflicting course ID\n==> ",end="")
        oldConfCourseID = input()
            
        print("Enter new conflicting course ID\n==> ",end="")
        newConfCourseID = input()
        
        fields = [
            courseID, oldConfCourseID, newConfCourseID
        ]

        if any(str(x).lower() == "r" for x in fields):
            return
     
        sched.conflict.modifyConflict(sched.config, courseID, oldConfCourseID, newConfCourseID)        