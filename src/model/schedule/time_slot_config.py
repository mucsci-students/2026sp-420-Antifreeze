from scheduler import (
    Scheduler,
    load_config_from_file,
)
from scheduler.config import CombinedConfig


# Manages time slot configuration entries in the scheduler configuration.
# Covers two sub-sections:
#   - times:   per-day time grids  (start, spacing, end)
#   - classes: meeting patterns    (credits, meetings, start_time, disabled)
class time_slot_config():

    VALID_DAYS = {"MON", "TUE", "WED", "THU", "FRI"}

    # Initializes time_slot_config subclass.
    def __init__(self):
        return

 
    
 
    # TIME-GRID HELPERS
    # Validates a time-grid entry based on operation type.
    # For 'add': fails if the exact (start, spacing, end) range already
    #            exists for the given day, or if the day is invalid.
    # For 'modify' or 'delete': fails if the range at `range_index` does
    #            not exist for the given day.
    # Parameters: config, day (e.g. "MON"), operation ('add'/'modify'/'delete'),
    #             range_index (int, required for modify/delete)
    # Returns: True if validation passes, False otherwise
    def validate_time_entry(self, config, day: str, operation: str,
                            range_index: int = None) -> bool:
        day = day.upper()

        if day not in self.VALID_DAYS:
            print(f"Error: '{day}' is not a valid day — expected one of {sorted(self.VALID_DAYS)}.")
            return False

        times = config.time_slot_config.times

        if operation == "add":
            # Day may not yet have an entry — that's fine for add.
            return True

        elif operation in ["modify", "delete"]:
            if day not in times or not times[day]:
                print(f"Error: No time ranges exist for '{day}' — returning to menu.")
                return False

            if range_index is None:
                print("Error: A range index is required for modify/delete.")
                return False

            if range_index < 0 or range_index >= len(times[day]):
                print(f"Error: Range index {range_index} is out of bounds for '{day}' "
                      f"(0–{len(times[day]) - 1}).")
                return False

        return True

    # Adds a new time range to a day's grid.
    # Parameters: config, day (e.g. "MON"),
    #             start (str "HH:MM"), spacing (int minutes), end (str "HH:MM")
    def add_time(self, config, day: str, start: str, spacing: int, end: str):
        day = day.upper()

        if day not in self.VALID_DAYS:
            print(f"'{day}' is not a valid day — no changes made.")
            return

        times = config.time_slot_config.times

        new_range = {"start": start, "spacing": spacing, "end": end}

        # Initialise day list if absent
        if day not in times:
            times[day] = []

        # Check for exact duplicate
        for existing in times[day]:
            if (existing.get("start") == start and
                    existing.get("spacing") == spacing and
                    existing.get("end") == end):
                print(f"Identical time range already exists for '{day}' — no change made.")
                return

        times[day].append(new_range)
        print(f"Time range {start}–{end} (spacing {spacing} min) added to {day}.")

    # Modifies an existing time range for a day by index.
    # Parameters: config, day (e.g. "MON"), range_index (int),
    #             start (str "HH:MM"), spacing (int minutes), end (str "HH:MM")
    def modify_time(self, config, day: str, range_index: int,
                    start: str, spacing: int, end: str):
        day = day.upper()
        times = config.time_slot_config.times

        if day not in times or range_index < 0 or range_index >= len(times[day]):
            print("Time range not found — no changes made.")
            return

        times[day][range_index] = {"start": start, "spacing": spacing, "end": end}
        print(f"Time range at index {range_index} for {day} updated to {start}–{end} "
              f"(spacing {spacing} min).")

    # Deletes a time range from a day by index.
    # Parameters: config, day (e.g. "MON"), range_index (int)
    def delete_time(self, config, day: str, range_index: int):
        day = day.upper()
        times = config.time_slot_config.times

        if day not in times or range_index < 0 or range_index >= len(times[day]):
            print("Time range not found — nothing deleted.")
            return

        removed = times[day].pop(range_index)
        print(f"Time range {removed.get('start')}–{removed.get('end')} removed from {day}.")

    # Prints all time ranges for every day.
    # Parameters: config
    def print_times(self, config):
        times = config.time_slot_config.times
        print("\nTime Slot Grid:")
        for day in ["MON", "TUE", "WED", "THU", "FRI"]:
            ranges = times.get(day, [])
            if not ranges:
                print(f"  {day}: (none)")
                continue
            for i, r in enumerate(ranges):
                start = r.get("start", r) if isinstance(r, dict) else r
                spacing = r.get("spacing", "") if isinstance(r, dict) else ""
                end = r.get("end", "") if isinstance(r, dict) else ""
                print(f"  {day} [{i}]: {start} – {end}  (spacing {spacing} min)")

    # Returns the time ranges dict from the config.
    # Parameters: config
    # Returns: dict[str, list]
    def get_times(self, config) -> dict:
        return config.time_slot_config.times

  
    

    #CLASS-PATTERN HELPERS
    # Validates a class-pattern entry based on operation type.
    # For 'add': basic sanity checks only (credits > 0, meetings non-empty).
    # For 'modify' or 'delete': fails if class_index is out of range.
    # Parameters: config, operation ('add'/'modify'/'delete'),
    #             class_index (int, required for modify/delete),
    #             credits (int, used for add validation),
    #             meetings (list, used for add validation)
    # Returns: True if validation passes, False otherwise
    def validate_class_entry(self, config, operation: str,
                             class_index: int = None,
                             credits: int = None,
                             meetings: list = None) -> bool:
        classes = config.time_slot_config.classes

        if operation == "add":
            if credits is None or credits <= 0:
                print("Error: Credits must be a positive integer.")
                return False
            if not meetings:
                print("Error: At least one meeting is required.")
                return False
            for m in meetings:
                day = m.get("day", "").upper()
                if day not in self.VALID_DAYS:
                    print(f"Error: '{day}' is not a valid day in a meeting entry.")
                    return False
                if m.get("duration", 0) <= 0:
                    print("Error: Meeting duration must be a positive integer.")
                    return False
            return True

        elif operation in ["modify", "delete"]:
            if class_index is None:
                print("Error: A class index is required for modify/delete.")
                return False
            if class_index < 0 or class_index >= len(classes):
                print(f"Error: Class index {class_index} is out of bounds "
                      f"(0–{len(classes) - 1}).")
                return False
            return True

        return True

    # Adds a new class meeting pattern.
    # Parameters: config, credits (int),
    #             meetings (list of dicts with day, duration, and optional lab bool),
    #             start_time (str "HH:MM", optional),
    #             disabled (bool, optional — defaults to False)
    def add_class(self, config, credits: int, meetings: list,
                  start_time: str = None, disabled: bool = False):
        classes = config.time_slot_config.classes

        new_class = {"credits": credits, "meetings": meetings}

        if start_time is not None:
            new_class["start_time"] = start_time

        if disabled:
            new_class["disabled"] = True

        classes.append(new_class)
        days = ", ".join(m.get("day", "?") for m in meetings)
        print(f"Class pattern added ({credits} credits, meets {days}).")

    # Modifies an existing class meeting pattern by index.
    # Parameters: config, class_index (int), credits (int),
    #             meetings (list of dicts), start_time (str or None),
    #             disabled (bool)
    def modify_class(self, config, class_index: int, credits: int,
                     meetings: list, start_time: str = None,
                     disabled: bool = False):
        classes = config.time_slot_config.classes

        if class_index < 0 or class_index >= len(classes):
            print("Class pattern not found — no changes made.")
            return

        updated = {"credits": credits, "meetings": meetings}

        if start_time is not None:
            updated["start_time"] = start_time

        if disabled:
            updated["disabled"] = True

        classes[class_index] = updated
        print(f"Class pattern at index {class_index} updated.")

    # Deletes a class meeting pattern by index.
    # Parameters: config, class_index (int)
    def delete_class(self, config, class_index: int):
        classes = config.time_slot_config.classes

        if class_index < 0 or class_index >= len(classes):
            print("Class pattern not found — nothing deleted.")
            return

        removed = classes.pop(class_index)
        days = ", ".join(m.get("day", "?") for m in removed.get("meetings", []))
        print(f"Class pattern removed ({removed.get('credits', '?')} credits, met {days}).")

    # Prints all class meeting patterns in the config.
    # Parameters: config
    def print_classes(self, config):
        classes = config.time_slot_config.classes
        print("\nClass Meeting Patterns:")
        for i, cls in enumerate(classes):
            credits = cls.get("credits", cls.credits if hasattr(cls, "credits") else "?")
            meetings = cls.get("meetings", cls.meetings if hasattr(cls, "meetings") else [])
            start_time = cls.get("start_time", getattr(cls, "start_time", None))
            disabled = cls.get("disabled", getattr(cls, "disabled", False))

            meeting_strs = []
            for m in meetings:
                day = m.get("day", m.day if hasattr(m, "day") else "?")
                dur = m.get("duration", m.duration if hasattr(m, "duration") else "?")
                lab = m.get("lab", getattr(m, "lab", False))
                tag = " (lab)" if lab else ""
                meeting_strs.append(f"{day} {dur}min{tag}")

            extras = []
            if start_time:
                extras.append(f"start_time={start_time}")
            if disabled:
                extras.append("DISABLED")
            extra_str = f"  [{', '.join(extras)}]" if extras else ""

            print(f"  [{i}] {credits} credits — {', '.join(meeting_strs)}{extra_str}")

    # Returns the classes list from the config.
    # Parameters: config
    # Returns: list
    def get_classes(self, config) -> list:
        return config.time_slot_config.classes


 
  
    # CONVENIENCE / PRINT ALL
    # Prints the full time slot configuration (times + classes).
    # Parameters: config
    def print_time_slot_config(self, config):
        self.print_times(config)
        self.print_classes(config)