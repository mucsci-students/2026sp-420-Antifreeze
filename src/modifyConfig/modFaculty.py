from modifyConfig.utilsCLI import prompt, endProg

import re

TIME_RANGE_RE = re.compile(r"^\d{2}:\d{2}-\d{2}:\d{2}$")

def printModFacultyMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add faculty")
    print("2: Modify faculty")
    print("3: Remove faculty")
    print("4: Print faculty")
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
        elif(userCommand == "4"):
            sched.faculty.printFaculty(sched.config)    
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

            while True:
                name = prompt("Enter faculty name to add\n==> ")
                if (name != ""):
                    break
                print("Invalid input for faculty name, try again.")
            
            while True:
                maximumCredits = prompt("Enter maximum credits\n==> ")
                if maximumCredits and maximumCredits.isnumeric():
                    maximumCredits = int(maximumCredits)
                    break
                print("Invalid input for maximum credits, try again.")

            while True:
                minimumCredits = prompt("Enter minimum credits\n==> ")
                if minimumCredits and minimumCredits.isnumeric():
                    minimumCredits = int(minimumCredits)
                    break
                print("Invalid input for minimum credits, try again.")

            while True:
                uniqueCourseLimit = prompt("Enter unique course limit\n==> ")
                if uniqueCourseLimit and uniqueCourseLimit.isnumeric():
                    uniqueCourseLimit = int(uniqueCourseLimit)
                    break
                print("Invalid input for unique course limit, try again.")

            while True:
                maximumDays = prompt("Enter maximum days\n==> ")
                if maximumDays and maximumDays.isnumeric():
                    maximumDays = int(maximumDays)
                    break
                print("Invalid input for maximum days, try again.")

            times = {}
            for day in ["MON", "TUE", "WED", "THU", "FRI"]:
                print(f"\nEnter time slots for {day} (send 'd' when finished)")
                slots = []
                while True:
                    slot = prompt(f"{day} slot\n==> ")
                    if slot == "d":
                        break
                    if not TIME_RANGE_RE.match(slot):
                        print("Invalid time format. Use HH:MM-HH:MM")
                        continue
                    slots.append(slot)
                    print(f"Current {day} slots: {slots}")
                times[day] = slots

            coursePreferences = {}
            while True:
                course = prompt("Enter course preference (or 'd')\n==> ")
                if course == "d":
                    break
                while True:
                    weight = prompt(f"Enter weight for {course}\n==> ")
                    if weight and weight.isnumeric():
                        weight = int(weight)
                        break
                    print("Invalid input for weight, try again.")
                coursePreferences[course] = weight
                print(f"Current Course Preferences: {coursePreferences}")

            roomPreferences = {}
            while True:
                room = prompt("Enter room preference (or 'd')\n==> ")
                if room == "d":
                    break
                while True:
                    weight = prompt(f"Enter weight for {room}\n==> ")
                    if weight and weight.isnumeric():
                        weight = int(weight)
                        break
                    print("Invalid input for weight, try again.")
                roomPreferences[room] = weight
                print(f"Current Room Preferences: {roomPreferences}")

            labPreferences = {}
            while True:
                lab = prompt("Enter lab preference (or 'd')\n==> ")
                if lab == "d":
                    break
                while True:
                    weight = prompt(f"Enter weight for {lab}\n==> ")
                    if weight and weight.isnumeric():
                        weight = int(weight)
                        break
                    print("Invalid input for weight, try again.")
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
                config = sched.config,
                name = name,
                maximumCredits = maximumCredits,
                maximumDays = maximumDays,
                minimumCredits = minimumCredits,
                uniqueCourseLimit = uniqueCourseLimit,
                times = times,
                coursePreferences = coursePreferences,
                roomPreferences = roomPreferences,
                labPreferences = labPreferences,
                mandatoryDays = mandatoryDays
            )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return

def modFaculty(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            while True:
                name = prompt("Enter faculty name to modify\n==> ")
                if (name != ""):
                    break
                print("Invalid input for faculty name, try again.")
            
            while True:
                maximumCredits = prompt("Enter new maximum credits\n==> ")
                if maximumCredits and maximumCredits.isnumeric():
                    maximumCredits = int(maximumCredits)
                    break
                print("Invalid input for maximum credits, try again.")

            while True:
                minimumCredits = prompt("Enter new minimum credits\n==> ")
                if minimumCredits and minimumCredits.isnumeric():
                    minimumCredits = int(minimumCredits)
                    break
                print("Invalid input for minimum credits, try again.")

            while True:
                uniqueCourseLimit = prompt("Enter new unique course limit\n==> ")
                if uniqueCourseLimit and uniqueCourseLimit.isnumeric():
                    uniqueCourseLimit = int(uniqueCourseLimit)
                    break
                print("Invalid input for unique course limit, try again.")

            while True:
                maximumDays = prompt("Enter new maximum days\n==> ")
                if maximumDays and maximumDays.isnumeric():
                    maximumDays = int(maximumDays)
                    break
                print("Invalid input for maximum days, try again.")

            times = {}
            for day in ["MON", "TUE", "WED", "THU", "FRI"]:
                print(f"\nEnter new time slots for {day} (send 'd' when finished)")
                slots = []
                while True:
                    slot = prompt(f"{day} slot\n==> ")
                    if slot == "d":
                        break
                    if not TIME_RANGE_RE.match(slot):
                        print("Invalid time format. Use HH:MM-HH:MM")
                        continue
                    slots.append(slot)
                    print(f"Current {day} slots: {slots}")
                times[day] = slots

            coursePreferences = {}
            while True:
                course = prompt("Enter new course preference (or 'd')\n==> ")
                if course == "d":
                    break
                while True:
                    weight = prompt(f"Enter weight for {course}\n==> ")
                    if weight and weight.isnumeric():
                        weight = int(weight)
                        break
                    print("Invalid input for weight, try again.")
                coursePreferences[course] = weight
                print(f"Current Course Preferences: {coursePreferences}")

            roomPreferences = {}
            while True:
                room = prompt("Enter room preference (or 'd')\n==> ")
                if room == "d":
                    break
                while True:
                    weight = prompt(f"Enter weight for {room}\n==> ")
                    if weight and weight.isnumeric():
                        weight = int(weight)
                        break
                    print("Invalid input for weight, try again.")
                roomPreferences[room] = weight
                print(f"Current Room Preferences: {roomPreferences}")

            labPreferences = {}
            while True:
                lab = prompt("Enter lab preference (or 'd')\n==> ")
                if lab == "d":
                    break
                while True:
                    weight = prompt(f"Enter weight for {lab}\n==> ")
                    if weight and weight.isnumeric():
                        weight = int(weight)
                        break
                    print("Invalid input for weight, try again.")
                labPreferences[lab] = weight
                print(f"Current Lab Preferences: {labPreferences}")

            mandatoryDays = []
            days = {"MON", "TUE", "WED", "THU", "FRI"}
            while True:
                day = prompt("Enter new mandatory day (MON/TUE/WED/THU/FRI) or 'd'\n==> ")
                if day == "d":
                    break
                if day.upper() in days:
                    mandatoryDays.append(day.upper())
                    print(f"Current Mandatory Days: {mandatoryDays}")
                else:
                    print("Invalid day, try again.")

            sched.faculty.modifyFaculty(
                config = sched.config,
                name = name,
                maximumCredits = maximumCredits,
                maximumDays = maximumDays,
                minimumCredits = minimumCredits,
                uniqueCourseLimit = uniqueCourseLimit,
                times = times,
                coursePreferences = coursePreferences,
                roomPreferences = roomPreferences,
                labPreferences = labPreferences,
                mandatoryDays = mandatoryDays
            )

    except KeyboardInterrupt:
        print("\nReturning to faculty menu...")
        return
