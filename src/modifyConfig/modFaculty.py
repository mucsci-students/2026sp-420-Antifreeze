
def printModFacultyMenu():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Add faculty")
    print("2: Modify faculty")
    print("3: Remove faculty")
    print("r: return to main\n==> ",end="")

def ModFacultyMenuMain(sched):
    while(True):
        printModFacultyMenu()
        userCommand = input()
        if(userCommand == "1"):
            addFaculty(sched)
        elif(userCommand == "2"):
            modFaculty(sched)
        elif(userCommand == "3"):
            delFaculty(sched)
        elif(userCommand.lower() == "r"):
            return

def delFaculty(sched):
    while(True):
        print("press r and page through prompts to return to main")
        
        print("Enter Faculty name to delete\n==> ",end="")
        name = input()
        
        if (name.lower() == "r"):
            return
        sched.faculty.deleteFaculty(sched.config, name)


def addFaculty(sched):
    while(True):
        print("press r and page through prompts to return to main")
        print("Enter Faculty name to add\n==> ",end="")
        name = input()
        
        print("Enter maximum credits\n==> ",end="")        
        maximumCredits = input()

        print("Enter maximum days\n==> ",end="")        
        maximumDays = input()

        print("Enter minimum credits\n==> ",end="")
        minimumCredits = input()

        print("Enter unique course limit\n==> ",end="")        
        uniqueCourseLimit = input()

        print("Enter times\n==> ",end="")        
        times = input()

        print("Enter course preferences\n==> ",end="")        
        coursePreferences = input()

        print("Enter room preferences\n==> ",end="")        
        roomPreferences = input()

        print("Enter lab preferences\n==> ",end="")        
        labPreferences = input()

        print("Enter mandatory days\n==> ",end="")        
        mandatoryDays = input()
        
        fields = [
            name, maximumCredits, maximumDays, minimumCredits,
            uniqueCourseLimit, times, coursePreferences,
            roomPreferences, labPreferences, mandatoryDays
        ]

        if any(str(x).lower() == "r" for x in fields):
            return
        sched.faculty.addFaculty(sched.config, name, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit, times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)


def modFaculty(sched):
     while(True):
        print("press r and page through prompts to return to main")
        print("Enter Faculty name to modify\n==> ",end="")
        name = input()
        
        print("Enter new maximum credits\n==> ",end="")        
        maximumCredits = input()

        print("Enter new maximum days\n==> ",end="")        
        maximumDays = input()

        print("Enter new minimum credits\n==> ",end="")
        minimumCredits = input()

        print("Enter new unique course limit\n==> ",end="")        
        uniqueCourseLimit = input()

        print("Enter new times\n==> ",end="")        
        times = input()

        print("Enter new course preferences\n==> ",end="")        
        coursePreferences = input()

        print("Enter new room preferences\n==> ",end="")        
        roomPreferences = input()

        print("Enter new lab preferences\n==> ",end="")        
        labPreferences = input()

        print("Enter new mandatory days\n==> ",end="")        
        mandatoryDays = input()
        
        fields = [
            name, maximumCredits, maximumDays, minimumCredits,
            uniqueCourseLimit, times, coursePreferences,
            roomPreferences, labPreferences, mandatoryDays
        ]

        if any(str(x).lower() == "r" for x in fields):
            return
        sched.faculty.modifyFaculty(sched.config, name, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit, times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)
        
