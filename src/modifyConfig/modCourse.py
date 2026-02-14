from modifyConfig.utilsCLI import prompt, endProg

def printModCourseMenu():
    print("\nPress the key associated with the command you would like to issue, then press enter.")
    print("1: Add Course")
    print("2: Modify Course")
    print("3: Remove Course")
    print("4: Print courses")
    print("r: return to main")
    print("q: exit program\n==> ",end="")

def modCourseMain(sched):
    while(True):
        printModCourseMenu()
        userCommand = input()
        if(userCommand == "1"):
            addCourse(sched)
        elif(userCommand == "2"):
            modCourse(sched)
        elif(userCommand == "3"):
            delCourse(sched)
        elif(userCommand == "4"):
            sched.course.printCourses(sched.config) 
        elif(userCommand.lower() == "r"):
            return
        elif(userCommand.lower() == "q"):   
            endProg()
        else:
            print("Invalid command, try again.")

def delCourse(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            name = prompt("Enter Course name to delete\n==> ")

            sched.course.deleteCourse(
                sched.config,
                name
            )

    except KeyboardInterrupt:
        print("\nReturning to course menu...")
        return



def addCourse(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Course ID\n==> ")
        credits = prompt("Enter credits\n==> ")

        rooms = []
        while True:
            room = prompt("Enter rooms, one at a time. when finished, send 'd'\n==> ")
            if room == "d":
                break
            rooms.append(room)
            print(f"Current Rooms: {rooms}")

        labs = []
        while True:
            lab = prompt("Enter labs, one at a time. when finished, send 'd'\n==> ")
            if lab == "d":
                break
            labs.append(lab)
            print(f"Current Labs: {labs}")

        conflicts = []
        while True:
            conflict = prompt("Enter conflicts, one at a time. when finished, send 'd'\n==> ")
            if conflict == "d":
                break
            conflicts.append(conflict)
            print(f"Current Conflicts: {conflicts}")

        faculty = []
        while True:
            prof = prompt("Enter faculty, one at a time. when finished, send 'd'\n==> ")
            if prof == "d":
                break
            faculty.append(prof)
            print(f"Current Faculty: {faculty}")

        sched.course.addCourse(
            config=sched.config,
            id=name,
            creds=credits,
            rms=rooms,
            lbs=labs,
            con=conflicts,
            fac=faculty
        )

    except KeyboardInterrupt:
        print("\nReturning to course menu...")
        return




def modCourse(sched):
    try:
        while True:
            print("press r and enter at any time to return to main\n")

            name = prompt("Enter Course ID to modify\n==> ")
            credits = prompt("Enter new credits\n==> ")

            rooms = []
            while True:
                room = prompt("Enter new rooms, one at a time. when finished, send 'd'\n==> ")
                if room == "d":
                    break
                rooms.append(room)
                print(f"Current Rooms: {rooms}")

            labs = []
            while True:
                lab = prompt("Enter new labs, one at a time. when finished, send 'd'\n==> ")
                if lab == "d":
                    break
                labs.append(lab)
                print(f"Current Labs: {labs}")

            conflicts = []
            while True:
                conflict = prompt("Enter new conflicts, one at a time. when finished, send 'd'\n==> ")
                if conflict == "d":
                    break
                conflicts.append(conflict)
                print(f"Current Conflicts: {conflicts}")

            faculty = []
            while True:
                prof = prompt("Enter new faculty, one at a time. when finished, send 'd'\n==> ")
                if prof == "d":
                    break
                faculty.append(prof)
                print(f"Current Faculty: {faculty}")

            sched.course.modifyCourse(
                config=sched.config,
                id=name,
                creds=int(credits),
                rms=rooms,
                lbs=labs,
                con=conflicts,
                fac=faculty
            )

    except KeyboardInterrupt:
        print("\nReturning to course menu...")
        return
