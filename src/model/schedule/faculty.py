from scheduler import (
    FacultyConfig,
    Faculty,
    Day,
    TimeRange,
    Course,
    Preference,
    Room,
    Lab,
)


class faculty:
    # TODO - initialize conflict subclass
    def __init__(self):
        return

    # Add Faculty
    # Adds a new faculty to the configuration json
    # Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
    # limit, times, course preferences, room preferences, lab preferences, mandatory days
    def add_faculty(
        self,
        config,
        name: Faculty,
        maximum_credits: int,
        maximum_days: int,
        minimum_credits: int,
        unique_course_limit: int,
        times: dict[Day, list[TimeRange]],
        course_preferences: dict[Course, Preference],
        room_preferences: dict[Room, Preference],
        lab_preferences: dict[Lab, Preference],
        mandatory_days: set[Day],
    ):
        # Reference to faculty list inside database
        fac = config.config.faculty

        # Test if parameters are correct
        # test = self.testAddFaculty(name, config, maximum_credits, maximum_days, minimum_credits, unique_course_limit,
        # times, course_preferences, room_preferences, lab_preferences, mandatory_days)

        # Checking for duplicate faculty name
        for prof in fac:
            if prof.name.upper() == name.upper():
                print("Faculty already exists - no change made.")
                return

        new_member = FacultyConfig(
            name=name,
            maximum_credits=maximum_credits,
            maximum_days=maximum_days,
            minimum_credits=minimum_credits,
            unique_course_limit=unique_course_limit,
            times=times,
            course_preferences=course_preferences,
            room_preferences=room_preferences,
            lab_preferences=lab_preferences,
            mandatory_days=mandatory_days,
        )
        fac.append(new_member)
        print(f"Faculty member '{name}' added successfully")

    # Modify Faculty
    # Modifies the details of an existing faculty member in the configuration json
    # Parameters: Configuration file, scheduler, name of faculty, maximum credits, maximum days, minimum credits, unique course
    # limit, times, course preferences, room preferences, lab preferences, mandatory days
    def modify_faculty(
        self,
        config,
        old_name: Faculty,
        new_name: Faculty,
        maximum_credits: int,
        maximum_days: int,
        minimum_credits: int,
        unique_course_limit: int,
        times: dict[Day, list[TimeRange]],
        course_preferences: dict[Course, Preference],
        room_preferences: dict[Room, Preference],
        lab_preferences: dict[Lab, Preference],
        mandatory_days: set[Day],
    ):

        fac = config.config.faculty
        target = None

        for prof in fac:
            if prof.name.upper() == old_name.upper():
                target = prof
                break

        if target is None:
            print("No such faculty member exists.")
            return

        # Prevent duplicate names
        for prof in fac:
            if prof.name.upper() == new_name.upper() and prof != target:
                print("Faculty name already exists.")
                return

        # ---- Rename cascade ----
        if old_name.upper() != new_name.upper():
            for course in config.config.courses:
                course.faculty = [
                    new_name if f.upper() == old_name.upper() else f
                    for f in course.faculty
                ]

        # Update faculty fields
        target.name = new_name
        target.maximum_credits = maximum_credits
        target.maximum_days = maximum_days
        target.minimum_credits = minimum_credits
        target.unique_course_limit = unique_course_limit
        target.times = times
        target.course_preferences = course_preferences
        target.room_preferences = room_preferences
        target.lab_preferences = lab_preferences
        target.mandatory_days = mandatory_days

        print(f"Faculty member '{old_name}' modified successfully.")

    # Delete Faculty
    # Delete an existing faculty from the configuration json
    # Parameters: Configuration file, name of faculty
    def delete_faculty(self, config, name: Faculty):
        fac = config.config.faculty
        target = None

        for prof in fac:
            if prof.name.upper() == name.upper():
                target = prof
                break

        if target is None:
            print("No such faculty member exists.")
            return

        # Remove faculty from faculty list
        fac.remove(target)

        # ---- Cascade: remove from course assignments ----
        for course in config.config.courses:
            course.faculty = [f for f in course.faculty if f.upper() != name.upper()]

        print(f"Faculty member '{name}' deleted successfully (cascade applied)")

    # Print Faculty
    # Prints all faculty members currently stored in the configuration
    # Displays faculty attributes including credit limits, day limits, time availability,
    # course preferences, room preferences, lab preferences, and mandatory days
    # Parameters: Configuration file
    def print_faculty(self, config):
        faculty = config.config.faculty
        print("\nFaculty:")
        for prof in faculty:
            print(
                f"Name: {prof.name}, \n\tMax Credits: {prof.maximum_credits}, \n\tMax Days: {prof.maximum_days}, \n\tMin Credits: {prof.minimum_credits}, \n\tUnique Course Limit: {prof.unique_course_limit}, \n\tTimes: {prof.times}, \n\tCourse Preferences: {prof.course_preferences}, \n\tRoom Preferences: {prof.room_preferences}, \n\tLab Preferences: {prof.lab_preferences}, \n\tMandatory Days: {prof.mandatory_days}"
            )

    def validate_entry(self, config: str, faculty_name: str, operation: str) -> bool:

        # Validates faculty entry based on operation type.

        # Parameters:
        # config: Configuration object
        # faculty_name: Name of the faculty to validate
        # operation: 'add', 'modify', or 'delete'

        # Returns true if validation passes, False otherwise

        faculty_list = config.config.faculty

        # Check for empty input
        if faculty_name == "":
            print("Error: Faculty name cannot be empty — returning to menu.")
            return False

        # Check if faculty exists
        faculty_exists = False
        for fac in faculty_list:
            if fac.name.upper() == faculty_name.upper():
                faculty_exists = True
                break

        if operation == "add":
            if faculty_exists:
                print(
                    f"Error: Faculty '{faculty_name}' already exists — returning to menu."
                )
                return False

        elif operation in ["modify", "delete"]:
            if not faculty_exists:
                print(
                    f"Error: Faculty '{faculty_name}' does not exist — returning to menu."
                )
                return False

        return True

    # Get Faculty IDs
    # Returns a list of faculty names (IDs) from the configuration JSON
    # Parameters: Configuration file
    # Returns: List of faculty name strings
    def get_faculty_ids(self, config) -> list[str]:
        fac = config.config.faculty
        return [prof.name for prof in fac]

    # Get Faculty Schedule
    # Returns a dictionary mapping each faculty name to a list of course sections
    # assigned to them, parsed from a CSV schedule file
    # Each entry contains course ID, section, room, lab, and meeting times
    # The lab session meeting is identified by a trailing '^' in the time field
    # Parameters: csv_path - path to the CSV schedule file
    # Returns: Dictionary mapping faculty name (str) to list of course info dicts
    def get_faculty_schedule(self, csv_path: str) -> dict[str, list[dict]]:

        faculty_schedule = {}

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
                faculty_name = parts[1]
                room = parts[2]
                lab_name = parts[3]
                meetings = parts[4:]

                course_id, _, section = course_section.partition(".")

                entry = {
                    "course_id": course_id,
                    "section": section,
                    "room": room,
                    "lab": lab_name,
                    "meetings": meetings,
                }

                if faculty_name not in faculty_schedule:
                    faculty_schedule[faculty_name] = []
                faculty_schedule[faculty_name].append(entry)

        return faculty_schedule
