
def printModFacultyMenu():
    print("Press the key associated with the command you would like to issue, then press enter.")
    print("1: Add faculty")
    print("2: Modify faculty")
    print("3: Remove faculty")
    print("r: return to main\n==> ",end="")

def modFacultyMain(sched):
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

        # ----- TIMES ----- #
        print("Enter time for MON\n==> ",end="")        
        timeMon = input()

        print("Enter time for TUE\n==> ",end="")        
        timeTue = input()

        print("Enter time for WED\n==> ",end="")        
        timeWed = input()

        print("Enter time for THU\n==> ",end="")        
        timeThu = input()

        print("Enter time for FRI\n==> ",end="")        
        timeFri = input()

        times = {"MON": [timeMon], "TUE": [timeTue], "WED": [timeWed], "THU": [timeThu], "FRI": [timeFri]}

        # ----- COURSE PREFERENCES ----- #
        print("Enter number of courses preferred\n==> ",end="")   
        numCourses = int(input())

        coursePreferences = {}
        while (numCourses > 0):
            print("Enter course preference\n==> ",end="")
            course = input()
            print("Enter weight preference\n==> ",end="")
            courseWeight = input()
            coursePreferences.update({course: courseWeight})
            numCourses -= 1

        # ----- ROOM PREFERENCES ----- #
        print("Enter number of rooms preferred\n==> ",end="")   
        numRooms = int(input())

        roomPreferences = {}
        while (numRooms > 0):
            print("Enter room preference\n==> ",end="")
            room = input()
            print("Enter weight preference\n==> ",end="")
            roomWeight = input()
            roomPreferences.update({room: roomWeight})
            numRooms -= 1

        # ----- LAB PREFERENCES ----- #
        print("Enter number of labs preferred\n==> ",end="")   
        numLabs = int(input())

        labPreferences = {}
        while (numLabs > 0):
            print("Enter lab preference\n==> ",end="")
            lab = input()
            print("Enter weight preference\n==> ",end="")
            labWeight = input()
            labPreferences.update({lab: labWeight})
            numLabs -= 1

        # ----- MANDATORY DAYS ----- #
        print("Enter mandatory days (MON, TUE, WED, THU, FRI)\n==> ",end="")
        daysInput = input()
        if (daysInput == ""):
            mandatoryDays = []
        mandatoryDays = daysInput.split(", ")
        
        fields = [
            name, maximumCredits, maximumDays, minimumCredits,
            uniqueCourseLimit, times, coursePreferences,
            roomPreferences, labPreferences, mandatoryDays
        ]

        if any(str(x).lower() == "r" for x in fields):
            return
        sched.faculty.addFaculty(sched.config, name, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit, 
                                 times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)


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

        # ----- TIMES ----- #
        print("Enter new time for MON\n==> ",end="")        
        timeMon = input()

        print("Enter new time for TUE\n==> ",end="")        
        timeTue = input()

        print("Enter new time for WED\n==> ",end="")        
        timeWed = input()

        print("Enter new time for THU\n==> ",end="")        
        timeThu = input()

        print("Enter new time for FRI\n==> ",end="")        
        timeFri = input()

        times = {"MON": [timeMon], "TUE": [timeTue], "WED": [timeWed], "THU": [timeThu], "FRI": [timeFri]}

        # ----- COURSE PREFERENCES ----- #
        print("Enter number of courses preferred\n==> ",end="")   
        numCourses = int(input())

        coursePreferences = {}
        while (numCourses > 0):
            print("Enter new course preference\n==> ",end="")
            course = input()
            print("Enter new weight preference\n==> ",end="")
            courseWeight = input()
            coursePreferences.update({course: courseWeight})
            numCourses -= 1

        # ----- ROOM PREFERENCES ----- #
        print("Enter number of rooms preferred\n==> ",end="")   
        numRooms = int(input())

        roomPreferences = {}
        while (numRooms > 0):
            print("Enter new room preference\n==> ",end="")
            room = input()
            print("Enter new weight preference\n==> ",end="")
            roomWeight = input()
            roomPreferences.update({room: roomWeight})
            numRooms -= 1

        # ----- LAB PREFERENCES ----- #
        print("Enter number of labs preferred\n==> ",end="")   
        numLabs = int(input())

        labPreferences = {}
        while (numLabs > 0):
            print("Enter new lab preference\n==> ",end="")
            lab = input()
            print("Enter new weight preference\n==> ",end="")
            labWeight = input()
            labPreferences.update({lab: labWeight})
            numLabs -= 1

        # ----- MANDATORY DAYS ----- #
        print("Enter new mandatory days (MON, TUE, WED, THU, FRI)\n==> ",end="")
        daysInput = input()
        if (daysInput == ""):
            mandatoryDays = []
        mandatoryDays = daysInput.split(", ")
        
        fields = [
            name, maximumCredits, maximumDays, minimumCredits,
            uniqueCourseLimit, times, coursePreferences,
            roomPreferences, labPreferences, mandatoryDays
        ]

        if any(str(x).lower() == "r" for x in fields):
            return
        sched.faculty.modifyFaculty(sched.config, name, maximumCredits, maximumDays, minimumCredits, uniqueCourseLimit, 
                                    times, coursePreferences, roomPreferences, labPreferences, mandatoryDays)
        
