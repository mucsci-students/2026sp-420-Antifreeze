from modifyConfig.utilsCLI import prompt, endProg

def printModFacultyMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add faculty")
    print("2: Modify faculty")
    print("3: Remove faculty")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

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
        elif(userCommand.lower() == "q"):
            endProg()
        else:
            print("Invalid command, try again.")

def delFaculty(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            name = prompt("Enter Faculty name to delete\n==> ")

            sched.faculty.deleteFaculty(
                sched.config,
                name
            )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return


def addFaculty(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            name = prompt("Enter Faculty name to add\n==> ")

            maximumCredits = int(prompt("Enter maximum credits\n==> "))
            minimumCredits = int(prompt("Enter minimum credits\n==> "))
            uniqueCourseLimit = int(prompt("Enter unique course limit\n==> "))
            maximumDays = int(prompt("Enter maximum days\n==> "))

            times = {}
            for day in ["MON", "TUE", "WED", "THU", "FRI"]:
                print(f"\nEnter time slots for {day} (send 'd' when finished)")
                slots = []
                while True:
                    slot = prompt(f"{day} slot\n==> ")
                    if slot == "d":
                        break
                    slots.append(slot)
                    print(f"Current {day} slots: {slots}")
                times[day] = slots

            coursePreferences = {}
            while True:
                course = prompt("Enter course preference (or 'd')\n==> ")
                if course == "d":
                    break
                weight = int(prompt(f"Enter weight for {course}\n==> "))
                coursePreferences[course] = weight
                print(f"Current Course Preferences: {coursePreferences}")

            roomPreferences = {}
            while True:
                room = prompt("Enter room preference (or 'd')\n==> ")
                if room == "d":
                    break
                weight = int(prompt(f"Enter weight for {room}\n==> "))
                roomPreferences[room] = weight
                print(f"Current Room Preferences: {roomPreferences}")

            labPreferences = {}
            while True:
                lab = prompt("Enter lab preference (or 'd')\n==> ")
                if lab == "d":
                    break
                weight = int(prompt(f"Enter weight for {lab}\n==> "))
                labPreferences[lab] = weight
                print(f"Current Lab Preferences: {labPreferences}")
            
            mandatoryDays = []
            days = {"MON", "TUE", "WED", "THU", "FRI"}
            while True:
                day = prompt("Enter mandatory day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
                if day == "d":
                    break
                if day.upper() in days:
                    mandatoryDays.append(day.upper())
                    print(f"Current Mandatory Days: {mandatoryDays}")
                else:
                    print("Invalid day, try again.")
            
            sched.faculty.addFaculty(
                config=sched.config,
                name=name,
                maximumCredits=maximumCredits,
                maximumDays=maximumDays,
                minimumCredits=minimumCredits,
                uniqueCourseLimit=uniqueCourseLimit,
                times=times,
                coursePreferences=coursePreferences,
                roomPreferences=roomPreferences,
                labPreferences=labPreferences, mandatoryDays=mandatoryDays
            )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return

def modFaculty(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            name = prompt("Enter Faculty name to modify\n==> ")

            maximumCredits = int(prompt("Enter new maximum credits\n==> "))
            minimumCredits = int(prompt("Enter new minimum credits\n==> "))
            uniqueCourseLimit = int(prompt("Enter new unique course limit\n==> "))
            maximumDays = int(prompt("Enter new maximum days\n==> "))

            # TIMES (per day)
            times = {}
            for day in ["MON", "TUE", "WED", "THU", "FRI"]:
                print(f"\nEnter time slots for {day} (send 'd' when finished)")
                slots = []
                while True:
                    slot = prompt(f"{day} slot\n==> ")
                    if slot == "d":
                        break
                    slots.append(slot)
                    print(f"Current {day} slots: {slots}")
                times[day] = slots

            mandatoryDays = []
            days = {"MON", "TUE", "WED", "THU", "FRI"}
            while True:
                day = prompt("Enter mandatory day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
                if day == "d":
                    break
                if day.upper() in days:
                    mandatoryDays.append(day.upper())
                    print(f"Current Mandatory Days: {mandatoryDays}")
                else:
                    print("Invalid day, try again.")

            coursePreferences = {}
            while True:
                course = prompt("Enter course preference (or 'd')\n==> ")
                if course == "d":
                    break
                weight = int(prompt(f"Enter weight for {course}\n==> "))
                coursePreferences[course] = weight
                print(f"Current Course Preferences: {coursePreferences}")

            roomPreferences = {}
            while True:
                room = prompt("Enter room preference (or 'd')\n==> ")
                if room == "d":
                    break
                weight = int(prompt(f"Enter weight for {room}\n==> "))
                roomPreferences[room] = weight
                print(f"Current Room Preferences: {roomPreferences}")

            labPreferences = {}
            while True:
                lab = prompt("Enter lab preference (or 'd')\n==> ")
                if lab == "d":
                    break
                weight = int(prompt(f"Enter weight for {lab}\n==> "))
                labPreferences[lab] = weight
                print(f"Current Lab Preferences: {labPreferences}")

            sched.faculty.modifyFaculty(
                sched.config,
                name,
                maximumCredits,
                maximumDays,
                minimumCredits,
                uniqueCourseLimit,
                times,
                coursePreferences,
                roomPreferences,
                labPreferences,
                mandatoryDays
            )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return

