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
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Course name to delete\n==> ")
        
        # Validate immediately
        if not sched.course.validateEntry(sched.config, name, "delete"):
            return

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
        
        # Validate immediately
        if not sched.course.validateEntry(sched.config, name, "add"):
            return
        
        credits = prompt("Enter credits\n==> ")
        
        # Validate credits is an integer
        try:
            credits_int = int(credits)
            if credits_int <= 0:
                print("Error: Credits must be a positive integer — returning to menu.")
                return
        except ValueError:
            print(f"Error: Credits must be an integer, got '{credits}' — returning to menu.")
            return

        # Get existing rooms, labs, courses, and faculty for validation
        existing_rooms = [r.upper() for r in sched.config.config.rooms]
        existing_labs = [l.upper() for l in sched.config.config.labs]
        existing_courses = [c.course_id.upper() for c in sched.config.config.courses]
        existing_faculty = [f.name.upper() for f in sched.config.config.faculty]

        rooms = []
        while True:
            room = prompt("Enter rooms, one at a time. when finished, send 'd'\n==> ")
            if room == "d":
                break
            # Validate room exists
            if room.upper() not in existing_rooms:
                print(f"Error: Room '{room}' does not exist — returning to menu.")
                return
            rooms.append(room)
            print(f"Current Rooms: {rooms}")

        labs = []
        while True:
            lab = prompt("Enter labs, one at a time. when finished, send 'd'\n==> ")
            if lab == "d":
                break
            # Validate lab exists
            if lab.upper() not in existing_labs:
                print(f"Error: Lab '{lab}' does not exist — returning to menu.")
                return
            labs.append(lab)
            print(f"Current Labs: {labs}")

        conflicts = []
        while True:
            conflict = prompt("Enter conflicts, one at a time. when finished, send 'd'\n==> ")
            if conflict == "d":
                break
            # Validate conflict course exists
            if conflict.upper() not in existing_courses:
                print(f"Error: Course '{conflict}' does not exist — returning to menu.")
                return
            conflicts.append(conflict)
            print(f"Current Conflicts: {conflicts}")

        faculty = []
        while True:
            prof = prompt("Enter faculty, one at a time. when finished, send 'd'\n==> ")
            if prof == "d":
                break
            # Validate faculty exists
            if prof.upper() not in existing_faculty:
                print(f"Error: Faculty '{prof}' does not exist — returning to menu.")
                return
            faculty.append(prof)
            print(f"Current Faculty: {faculty}")

        sched.course.addCourse(
            config=sched.config,
            id=name,
            creds=credits_int,
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
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Course ID to modify\n==> ")
        
        # Validate immediately
        if not sched.course.validateEntry(sched.config, name, "modify"):
            return
        
        credits = prompt("Enter new credits\n==> ")
        
        # Validate credits is an integer
        try:
            credits_int = int(credits)
            if credits_int <= 0:
                print("Error: Credits must be a positive integer — returning to menu.")
                return
        except ValueError:
            print(f"Error: Credits must be an integer, got '{credits}' — returning to menu.")
            return

        # Get existing rooms, labs, courses, and faculty for validation
        existing_rooms = [r.upper() for r in sched.config.config.rooms]
        existing_labs = [l.upper() for l in sched.config.config.labs]
        existing_courses = [c.course_id.upper() for c in sched.config.config.courses]
        existing_faculty = [f.name.upper() for f in sched.config.config.faculty]

        rooms = []
        while True:
            room = prompt("Enter new rooms, one at a time. when finished, send 'd'\n==> ")
            if room == "d":
                break
            # Validate room exists
            if room.upper() not in existing_rooms:
                print(f"Error: Room '{room}' does not exist — returning to menu.")
                return
            rooms.append(room)
            print(f"Current Rooms: {rooms}")

        labs = []
        while True:
            lab = prompt("Enter new labs, one at a time. when finished, send 'd'\n==> ")
            if lab == "d":
                break
            # Validate lab exists
            if lab.upper() not in existing_labs:
                print(f"Error: Lab '{lab}' does not exist — returning to menu.")
                return
            labs.append(lab)
            print(f"Current Labs: {labs}")

        conflicts = []
        while True:
            conflict = prompt("Enter new conflicts, one at a time. when finished, send 'd'\n==> ")
            if conflict == "d":
                break
            # Validate conflict course exists
            if conflict.upper() not in existing_courses:
                print(f"Error: Course '{conflict}' does not exist — returning to menu.")
                return
            conflicts.append(conflict)
            print(f"Current Conflicts: {conflicts}")

        faculty = []
        while True:
            prof = prompt("Enter new faculty, one at a time. when finished, send 'd'\n==> ")
            if prof == "d":
                break
            # Validate faculty exists
            if prof.upper() not in existing_faculty:
                print(f"Error: Faculty '{prof}' does not exist — returning to menu.")
                return
            faculty.append(prof)
            print(f"Current Faculty: {faculty}")

        sched.course.modifyCourse(
            config=sched.config,
            id=name,
            creds=credits_int,
            rms=rooms,
            lbs=labs,
            con=conflicts,
            fac=faculty
        )

    except KeyboardInterrupt:
        print("\nReturning to course menu...")
        return