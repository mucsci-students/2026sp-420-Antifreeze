from scheduler import CombinedConfig


# Manages room entries in the scheduler configuration.
class room:
    # Initializes room subclass.
    def __init__(self):
        return

    # Validates a room entry based on operation type.
    # For 'add': fails if room already exists or name is empty.
    # For 'modify' or 'delete': fails if room does not exist.
    # Parameters: config, room_name, operation ('add'/'modify'/'delete')
    # Returns: True if validation passes, False otherwise
    def validate_entry(
        self, config: "CombinedConfig", room_name: str, operation: str
    ) -> bool:
        rooms = config.config.rooms

        # Check for empty input
        if room_name == "":
            print("Error: Room must have a name — returning to menu.")
            return False

        if operation == "add":
            if room_name in rooms:
                print(f"Error: Room '{room_name}' already exists — returning to menu.")
                return False

        elif operation in ["modify", "delete"]:
            if room_name not in rooms:
                print(f"Error: Room '{room_name}' does not exist — returning to menu.")
                return False

        return True

    # Adds a room to the config.
    # Parameters: config, room_name
    def add_room(self, config: "CombinedConfig", room_name: str):

        # Reference to rooms list in database
        rooms = config.config.rooms

        # Checking for empty input or duplicate room
        if room_name == "":
            print("Room must have a name — no changes made.")
            return
        elif room_name in rooms:
            print("Room already exists — no changes made.")
            return

        # Adding new room to rooms list
        rooms.append(room_name)

        # CLI outputs room added successfully
        print(f"Room '{room_name}' added successfully.")

    # Deletes a room from the config.
    # Cascades removal to course room lists and faculty room preferences.
    # Parameters: config, room_name
    def delete_room(self, config: "CombinedConfig", room_name: str):

        rooms = config.config.rooms

        if room_name == "":
            print("Room must have a name — no changes made.")
            return
        elif room_name not in rooms:
            print("Room does not exist — no changes made.")
            return

        # Remove from master list
        rooms.remove(room_name)

        # ---- Cascade: Courses ----
        for course in config.config.courses:
            if room_name in course.room:
                course.room = [r for r in course.room if r != room_name]

        # ---- Cascade: Faculty Preferences ----
        for faculty in config.config.faculty:
            if room_name in faculty.room_preferences:
                del faculty.room_preferences[room_name]

        print(f"Room '{room_name}' deleted successfully.")

    # Renames a room in the config.
    # Cascades the rename to course room lists and faculty room preferences.
    # Parameters: config, old_name, new_name
    def modify_room(self, config: "CombinedConfig", old_name: str, new_name: str):

        rooms = config.config.rooms

        if old_name == "":
            print("Room must have a name — no changes made.")
            return
        elif old_name not in rooms:
            print("Original room not found — no changes made.")
            return
        elif new_name == "":
            print("Room must have a name — no changes made.")
            return
        elif new_name in rooms:
            print("New room already exists — choose a different room.")
            return

        # Rename in master list
        index = rooms.index(old_name)
        rooms[index] = new_name

        # ---- Cascade: Courses ----
        for course in config.config.courses:
            course.room = [new_name if r == old_name else r for r in course.room]

        # ---- Cascade: Faculty Preferences ----
        for faculty in config.config.faculty:
            prefs = faculty.room_preferences
            if old_name in prefs:
                prefs[new_name] = prefs.pop(old_name)

        print(f"Room renamed from '{old_name}' to '{new_name}' successfully.")

    # Prints all rooms in the config.
    # Parameters: config
    def print_rooms(self, config: "CombinedConfig"):
        rooms = config.config.rooms
        print("\nRooms:")
        for room in rooms:
            print(f"Name: {room}")

    # Returns a list of all room names from the config.
    # Parameters: config
    # Returns: List of room name strings
    def get_room_ids(self, config: "CombinedConfig") -> list[str]:
        rooms = config.config.rooms
        return list(rooms)

    # Parses the CSV schedule file and returns a dict mapping each room name
    # to a list of course sections scheduled in it.
    # Each entry contains: course_id, section, faculty, lab, meetings.
    # Parameters: csv_path - path to the CSV schedule file
    # Returns: Dict mapping room name (str) to list of course info dicts
    def get_room_schedule(self, csv_path: str) -> dict[str, list[dict]]:

        room_schedule = {}

        with open(csv_path, newline="") as f:
            for line in f:
                line = line.strip()

                # Skip blank lines and schedule header lines
                if not line or line.startswith("Schedule"):
                    continue

                parts = [p.strip() for p in line.split(",")]

                # Expect at least: course_section, faculty, room, lab, and one meeting
                if len(parts) < 5:
                    continue

                course_section = parts[0]
                faculty = parts[1]
                room_name = parts[2]
                lab_name = parts[3]
                meetings = parts[4:]

                course_id, _, section = course_section.partition(".")

                entry = {
                    "course_id": course_id,
                    "section": section,
                    "faculty": faculty,
                    "lab": lab_name,
                    "meetings": meetings,
                }

                if room_name not in room_schedule:
                    room_schedule[room_name] = []
                room_schedule[room_name].append(entry)

        return room_schedule
