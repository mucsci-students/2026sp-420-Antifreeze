from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig


class room():

    #initialize conflict subclass
    def __init__(self):
        return

    def validate_entry(self, config: str, room_name: str, operation: str) -> bool:
        """
        Validates room entry based on operation type.
        
        Parameters:
        - config: Configuration object
        - room_name: Name of the room to validate
        - operation: 'add', 'modify', or 'delete'
        
        Returns:
        - True if validation passes, False otherwise
        """
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

    def add_room(self, config: str, room_name: str):

        #Reference to rooms list in database
        rooms = config.config.rooms

        #Checking for empty input or duplicate room
        if room_name == "":
            print("Room must have a name — no changes made.")
            return
        elif room_name in rooms:
            print("Room already exists — no changes made.")
            return

        #Adding new room to rooms list
        rooms.append(room_name)

        #CLI outputs room added successfully
        print(f"Room '{room_name}' added successfully.")

    def delete_room(self, config: str, room_name: str):

        #Reference to rooms list in database
        rooms = config.config.rooms

        #Checking for empty input or nonexistent room
        if room_name == "":
            print("Room must have a name — no changes made.")
            return
        elif room_name not in rooms:
            print("Room does not exist — no changes made.")
            return

        #Removing room from rooms list
        rooms.remove(room_name)

        #CLI outputs room deleted successfully
        print(f"Room '{room_name}' deleted successfully.")

    def modify_room(self, config: str, old_name: str, new_name: str):

        #Reference to rooms list in database
        rooms = config.config.rooms

        #Checking for empty inputs, nonexistent rooms, or duplicate rooms
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

        #Replace old room with new room
        index = rooms.index(old_name)
        rooms[index] = new_name

        #CLI outputs room modified successfully
        print(f"Room renamed from '{old_name}' to '{new_name}' successfully.") 
    
    #Print Rooms
    #Prints all rooms currently stored in the configuration
    #Displays the name of each room
    #Parameters: Configuration file
    def print_rooms(self, config: str):
        rooms = config.config.rooms 
        print("\nRooms:")
        for room in rooms:            
            print(f"Name: {room}")

    #Get Room IDs
    #Returns a list of room names (IDs) from the configuration JSON
    #Parameters: Configuration file
    #Returns: List of room name strings
    def get_room_ids(self, config: str) -> list[str]:
        rooms = config.config.rooms
        return list(rooms)

    #Get Room Schedule
    #Returns a dictionary mapping each room name to a list of course sections
    #scheduled in that room, parsed from a CSV schedule file
    #Each entry contains course ID, section, faculty, lab, and meeting times
    #Parameters: csv_path - path to the CSV schedule file
    #Returns: Dictionary mapping room name (str) to list of course info dicts
    def get_room_schedule(self, csv_path: str) -> dict[str, list[dict]]:
        import csv

        room_schedule = {}

        with open(csv_path, newline='') as f:
            for line in f:
                line = line.strip()

                # Skip blank lines and schedule header lines
                if not line or line.startswith("Schedule"):
                    continue

                parts = [p.strip() for p in line.split(',')]

                # Expect at least: course_section, faculty, room, lab, and one meeting
                if len(parts) < 5:
                    continue

                course_section = parts[0]
                faculty        = parts[1]
                room_name      = parts[2]
                lab_name       = parts[3]
                meetings       = parts[4:]

                course_id, _, section = course_section.partition('.')

                entry = {
                    "course_id": course_id,
                    "section": section,
                    "faculty": faculty,
                    "lab": lab_name,
                    "meetings": meetings
                }

                if room_name not in room_schedule:
                    room_schedule[room_name] = []
                room_schedule[room_name].append(entry)

        return room_schedule