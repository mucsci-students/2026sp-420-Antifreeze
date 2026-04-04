from controller.modifyConfig.utilsCLI import prompt, end_prog


# print_mod_course_menu
# Displays the course modification menu options to the user
def print_mod_course_menu():
    print(
        "\nPress the key associated with the command you would like to issue, then press enter."
    )
    print("1: Add Course")
    print("2: Modify Course")
    print("3: Remove Course")
    print("4: Print courses")
    print("r: return to main")
    print("q: exit program\n==> ", end="")


# mod_course_main
# Main control loop for course modification operations
# Routes user input to add, modify, delete, or print course actions
# Parameters: Scheduler object
def mod_course_main(sched):
    while True:
        print_mod_course_menu()
        user_command = input()
        if user_command == "1":
            add_course(sched)
        elif user_command == "2":
            mod_course(sched)
        elif user_command == "3":
            del_course(sched)
        elif user_command == "4":
            sched.course.print_courses(sched.config)
        elif user_command.lower() == "r":
            return
        elif user_command.lower() == "q":
            end_prog()
        else:
            print("Invalid command, try again.")


# del_course
# Removes an existing course from the configuration
# Prompts the user for a course ID
# Parameters: Scheduler object
def del_course(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Course name to delete\n==> ")

        # Validate immediately
        if not sched.course.validate_entry(sched.config, name, "delete"):
            return

        sched.course.delete_course(sched.config, name)

    except KeyboardInterrupt:
        print("\nReturning to course menu...")
        return


# add_course
# Adds a new course to the configuration
# Prompts the user for course ID, credits, rooms, labs, conflicts, and faculty
# Parameters: Scheduler object
def add_course(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Course ID\n==> ")

        # Validate immediately
        if not sched.course.validate_entry(sched.config, name, "add"):
            return

        credits = prompt("Enter credits\n==> ")

        # Validate credits is an integer
        try:
            credits_int = int(credits)
            if credits_int <= 0:
                print("Error: Credits must be a positive integer — returning to menu.")
                return
        except ValueError:
            print(
                f"Error: Credits must be an integer, got '{credits}' — returning to menu."
            )
            return

        # Get existing rooms, labs, courses, and faculty for validation
        existing_rooms = [rooms.upper() for rooms in sched.config.config.rooms]
        existing_labs = [lab.upper() for lab in sched.config.config.labs]
        existing_courses = [
            courses.course_id.upper() for courses in sched.config.config.courses
        ]
        existing_faculty = [
            faculty.name.upper() for faculty in sched.config.config.faculty
        ]

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
            conflict = prompt(
                "Enter conflicts, one at a time. when finished, send 'd'\n==> "
            )
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

        sched.course.add_course(
            config=sched.config,
            id=name,
            creds=credits_int,
            rms=rooms,
            lbs=labs,
            con=conflicts,
            fac=faculty,
        )

    except KeyboardInterrupt:
        print("\nReturning to course menu...")
        return


# mod_course
# Replaces an existing course's attributes with new values
# Prompts the user for course ID, credits, rooms, labs, conflicts, and faculty
# Parameters: Scheduler object


def mod_course(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Course ID to modify\n==> ")

        # Validate immediately
        if not sched.course.validate_entry(sched.config, name, "modify"):
            return

        new_name = prompt("Enter new Course ID\n==> ")

        credits = prompt("Enter new credits\n==> ")

        # Validate credits is an integer
        try:
            credits_int = int(credits)
            if credits_int <= 0:
                print("Error: Credits must be a positive integer — returning to menu.")
                return
        except ValueError:
            print(
                f"Error: Credits must be an integer, got '{credits}' — returning to menu."
            )
            return

        # Get existing rooms, labs, courses, and faculty for validation
        existing_rooms = [rooms.upper() for rooms in sched.config.config.rooms]
        existing_labs = [lab.upper() for lab in sched.config.config.labs]
        existing_courses = [
            course.course_id.upper() for course in sched.config.config.courses
        ]
        existing_faculty = [
            faculty.name.upper() for faculty in sched.config.config.faculty
        ]

        rooms = []
        while True:
            room = prompt(
                "Enter new rooms, one at a time. when finished, send 'd'\n==> "
            )
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
            conflict = prompt(
                "Enter new conflicts, one at a time. when finished, send 'd'\n==> "
            )
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
            prof = prompt(
                "Enter new faculty, one at a time. when finished, send 'd'\n==> "
            )
            if prof == "d":
                break
            # Validate faculty exists
            if prof.upper() not in existing_faculty:
                print(f"Error: Faculty '{prof}' does not exist — returning to menu.")
                return
            faculty.append(prof)
            print(f"Current Faculty: {faculty}")

        sched.course.modify_course(
            old_id=name,
            new_id=new_name,
            config=sched.config,
            id=name,
            creds=credits_int,
            rms=rooms,
            lbs=labs,
            con=conflicts,
            fac=faculty,
        )

    except KeyboardInterrupt:
        print("\nReturning to course menu...")
        return
