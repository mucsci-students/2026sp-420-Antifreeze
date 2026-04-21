from controller.modifyConfig.utilsCLI import end_prog
from controller.modifyConfig import (
    modLab,
    modRoom,
    modCourse,
    modConflict,
    modFaculty,
    modTimeSlot,
)


# Print Config Menu
# Displays the top-level configuration management menu options
def print_config_menu():
    print(
        "\nPress the key associated with the command you would like to issue, then press enter."
    )
    print("1: Load config")
    print("2: Modify config")
    print("3: Save config")
    print("4: Print config")
    print("r: return to main")
    print("q: exit program\n==> ", end="")


# Print Modify Config Menu
# Displays the sub-menu for selecting which config entity to modify
def print_mod_config_menu():
    print(
        "\nPress the key associated with the command you would like to issue, then press enter."
    )
    print("1: Modify Labs")
    print("2: Modify Rooms")
    print("3: Modify Courses")
    print("4: Modify Conflicts")
    print("5: Modify Faculty")
    print("6: Modify Time Slot")
    print("r: return to config menu")
    print("q: exit program\n==> ", end="")


# Check if Config is Loaded
# Validates that a configuration file has been loaded before modifying/saving/printing
# Returns True if config is loaded, False otherwise
def is_config_loaded(sched):
    if sched.config is None or not hasattr(sched.config, "config"):
        sched.load_config("2026sp-420-Antifreeze\\src\\schedule\\empty.json")
    return True


# Config Modification Loop
# Interactive loop for selecting and executing config modification operations
# Routes user input to the appropriate entity modifier (lab, room, course, conflict, faculty, time slot)
# Parameters: Scheduler object
def conf_loop(sched):
    while True:
        print_mod_config_menu()
        user_command = input()
        if user_command == "1":
            modLab.mod_lab_main(sched)
        elif user_command == "2":
            modRoom.mod_room_main(sched)
        elif user_command == "3":
            modCourse.mod_course_main(sched)
        elif user_command == "4":
            modConflict.mod_conflict_main(sched)
        elif user_command == "5":
            modFaculty.mod_faculty_main(sched)
        elif user_command == "6":
            modTimeSlot.mod_time_slot(sched)
        elif user_command.lower() == "r":
            return
        elif user_command.lower() == "q":
            end_prog()
        else:
            print("Invalid command, try again.")


# Config
# Main configuration management loop
# Handles loading, modifying, saving, and printing the scheduler configuration
# Parameters: Scheduler object
def config(sched):
    while True:
        print_config_menu()
        user_command = input()
        if user_command == "1":
            print(
                "Enter the path of the file you would like to load, including extension\n==> ",
                end="",
            )
            file_name = input()
            print(repr(file_name))
            sched.load_config(file_name)
        elif user_command == "2":
            # Validate config is loaded before modifying
            if not is_config_loaded(sched):
                continue
            conf_loop(sched)
        elif user_command == "3":
            # Validate config is loaded before saving
            if not is_config_loaded(sched):
                continue
            sched.save_config()
        elif user_command == "4":
            # Validate config is loaded before printing
            if not is_config_loaded(sched):
                continue
            sched.print_config()
        elif user_command.lower() == "r":
            return
        elif user_command.lower() == "q":
            end_prog()
        else:
            print("Invalid command, try again.")
