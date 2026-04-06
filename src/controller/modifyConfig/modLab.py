from controller.modifyConfig.utilsCLI import prompt, end_prog
# print_mod_lab_menu
# Displays the lab modification menu options to the user


def print_mod_lab_menu():
    print(
        "\nPress the key associated with the command you would like to issue, then press enter."
    )
    print("1: Add Lab")
    print("2: Modify Lab")
    print("3: Remove Lab")
    print("4: Print labs")
    print("r: return to main")
    print("q: exit program\n==> ", end="")


# mod_lab_main
# Main control loop for lab modification operations
# Routes user input to add, modify, delete, or print lab actions
# Parameters: Scheduler object
def mod_lab_main(sched):
    while True:
        print_mod_lab_menu()
        user_command = input()
        if user_command == "1":
            add_lab(sched)
        elif user_command == "2":
            mod_lab(sched)
        elif user_command == "3":
            del_lab(sched)
        elif user_command == "4":
            sched.lab.print_labs(sched.config)
        elif user_command.lower() == "r":
            return
        elif user_command.lower() == "q":
            end_prog()
        else:
            print("Invalid command, try again.")


# del_lab
# Removes an existing lab from the configuration
# Prompts the user for a lab name
# Parameters: Scheduler object
def del_lab(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Lab name to delete\n==> ")

        # Validate immediately
        if not sched.lab.validate_entry(sched.config, name, "delete"):
            return

        sched.lab.delete_lab(sched.config, name)

    except KeyboardInterrupt:
        print("\nReturning to lab menu...")
        return


# add_lab
# Adds a new lab to the configuration
# Prompts the user for a lab name
# Parameters: Scheduler object
def add_lab(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter lab name to add\n==> ")

        # Validate immediately
        if not sched.lab.validate_entry(sched.config, name, "add"):
            return

        sched.lab.add_lab(sched.config, name)

    except KeyboardInterrupt:
        print("\nReturning to lab menu...")
        return


# mod_lab
# Replaces an existing lab's name with a new name
# Prompts the user for a lab name
# Parameters: Scheduler object
def mod_lab(sched):
    try:
        print("press r and enter at any time to return to main\n")

        old_name = prompt("Enter Lab name to change\n==> ")

        # Validate old name immediately
        if not sched.lab.validate_entry(sched.config, old_name, "modify"):
            return

        new_name = prompt("Enter new lab name\n==> ")

        # Validate new name doesn't already exist
        if not sched.lab.validate_entry(sched.config, new_name, "add"):
            return

        sched.lab.modify_lab(sched.config, old_name, new_name)

    except KeyboardInterrupt:
        print("\nReturning to lab menu...")
        return
