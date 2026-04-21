from controller.modifyConfig.utilsCLI import prompt, end_prog


# Print Modify Room Menu
# Displays the room modification menu options to the user
def print_mod_room_menu():
    print(
        "\nPress the key associated with the command you would like to issue, then press enter."
    )
    print("1: Add Room")
    print("2: Modify Room")
    print("3: Remove Room")
    print("4: Print rooms")
    print("r: return to main")
    print("q: exit program\n==> ", end="")


# Modify Room Main
# Main control loop for room modification operations
# Routes user input to add, modify, delete, or print room actions
# Parameters: Scheduler object
def mod_room_main(sched):
    while True:
        print_mod_room_menu()
        user_command = input()
        if user_command == "1":
            add_room(sched)
        elif user_command == "2":
            mod_room(sched)
        elif user_command == "3":
            del_room(sched)
        elif user_command == "4":
            sched.room.print_rooms(sched.config)
        elif user_command.lower() == "r":
            return
        elif user_command.lower() == "q":
            end_prog()
        else:
            print("Invalid command, try again.")


# Delete Room
# Removes an existing room from the configuration
# Prompts the user for a room name
# Parameters: Scheduler object
def del_room(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Room name to delete\n==> ")

        # Validate immediately
        if not sched.room.validate_entry(sched.config, name, "delete"):
            return

        sched.room.delete_room(sched.config, name)

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return


# Add Room
# Adds a new room to the configuration
# Prompts the user for a room name
# Parameters: Scheduler object
def add_room(sched):
    try:
        print("press r and enter at any time to return to main\n")

        name = prompt("Enter Room name to add\n==> ")

        # Validate immediately
        if not sched.room.validate_entry(sched.config, name, "add"):
            return

        sched.room.add_room(sched.config, name)

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return


# Modify Room
# Replaces an existing room's name with a new name
# Prompts the user for old and new room names
# Parameters: Scheduler object
def mod_room(sched):
    try:
        print("press r and enter at any time to return to main\n")

        old_name = prompt("Enter Room name to change\n==> ")

        # Validate old name immediately
        if not sched.room.validate_entry(sched.config, old_name, "modify"):
            return

        new_name = prompt("Enter new Room name\n==> ")

        # Validate new name doesn't already exist
        if not sched.room.validate_entry(sched.config, new_name, "add"):
            return

        sched.room.modify_room(sched.config, old_name, new_name)

    except KeyboardInterrupt:
        print("\nReturning to room menu...")
        return
