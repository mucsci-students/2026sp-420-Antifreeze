# -------------------------
# HELPERS (ADD AT TOP)
# -------------------------


def _ensure_list(val):
    if val is None:
        return []
    if isinstance(val, list):
        return val
    return [val]


def _clean_list(values):
    return [v.strip() for v in values if isinstance(v, str) and v.strip()]


def _normalize_name(name: str):
    return name.strip()


def _to_set(val):
    """Coerce any value (list, set, None, str) into a set of strings."""
    if val is None:
        return set()
    if isinstance(val, set):
        return val
    if isinstance(val, str):
        return {val.strip()} if val.strip() else set()
    return {str(v).strip() for v in val if str(v).strip()}


def _find_in_list(name: str, lst: list):
    """Case-insensitive lookup — returns the actual stored value or None."""
    name = name.strip()
    for item in lst:
        if item.upper() == name.upper():
            return item
    return None


# -------------------------
# FACULTY
# -------------------------


def add_faculty(
    scheduler,
    name: str,
    maximum_credits: int,
    maximum_days: int,
    minimum_credits: int,
    unique_course_limit: int,
    times=None,
    course_preferences=None,
    room_preferences=None,
    lab_preferences=None,
    mandatory_days=None,
):
    fac_list = scheduler.config.config.faculty

    for prof in fac_list:
        if prof.name.upper() == name.upper():
            return {"error": f'"{name}" already exists.'}

    # defaults
    times = times or {}
    course_preferences = course_preferences or {}
    room_preferences = room_preferences or {}
    lab_preferences = lab_preferences or {}
    mandatory_days = _to_set(mandatory_days)

    try:
        scheduler.faculty.add_faculty(
            scheduler.config,
            name,
            maximum_credits,
            maximum_days,
            minimum_credits,
            unique_course_limit,
            times,
            course_preferences,
            room_preferences,
            lab_preferences,
            mandatory_days,
        )
    except Exception as e:
        msg = str(e)
        import re

        m = re.search(
            r"Mandatory days \[([^\]]+)\] must be present in the availability times",
            msg,
        )
        if m:
            missing = m.group(1)
            return {
                "error": f"Mandatory day(s) {missing} must have an availability time set. Please ask the user to provide time slots for those days (e.g. '09:00-09:50') before setting them as mandatory."
            }
        return {"error": msg}

    return {"status": "added", "faculty": name}


def modify_faculty(
    scheduler,
    old_name: str,
    new_name: str,
    maximum_credits: int,
    maximum_days: int,
    minimum_credits: int,
    unique_course_limit: int,
    times=None,
    course_preferences=None,
    room_preferences=None,
    lab_preferences=None,
    mandatory_days=None,
):
    fac_list = scheduler.config.config.faculty

    target = None
    for prof in fac_list:
        if prof.name.upper() == old_name.upper():
            target = prof
            break

    if target is None:
        return {"error": f'"{old_name}" not found.'}

    if new_name.upper() != old_name.upper():
        for prof in fac_list:
            if prof.name.upper() == new_name.upper():
                return {"error": f'"{new_name}" already exists.'}

    # defaults
    times = times or {}
    course_preferences = course_preferences or {}
    room_preferences = room_preferences or {}
    lab_preferences = lab_preferences or {}
    mandatory_days = _to_set(mandatory_days)

    try:
        scheduler.faculty.modify_faculty(
            scheduler.config,
            old_name,
            new_name,
            maximum_credits,
            maximum_days,
            minimum_credits,
            unique_course_limit,
            times,
            course_preferences,
            room_preferences,
            lab_preferences,
            mandatory_days,
        )
    except Exception as e:
        msg = str(e)
        import re

        m = re.search(
            r"Mandatory days \[([^\]]+)\] must be present in the availability times",
            msg,
        )
        if m:
            missing = m.group(1)
            return {
                "error": f"Mandatory day(s) {missing} must have an availability time set. Please ask the user to provide time slots for those days (e.g. '09:00-09:50') before setting them as mandatory."
            }
        return {"error": msg}

    return {"status": "modified", "faculty": new_name}


def delete_faculty(scheduler, name: str):
    fac_list = scheduler.config.config.faculty

    for prof in fac_list:
        if prof.name.upper() == name.upper():
            scheduler.faculty.delete_faculty(scheduler.config, name)
            return {"status": "deleted", "faculty": name}

    return {"error": f'"{name}" not found.'}


def list_faculty(scheduler):
    return {"faculty": [{"name": f.name} for f in scheduler.config.config.faculty]}


def get_faculty_details(scheduler, name: str):
    for f in scheduler.config.config.faculty:
        if f.name.upper() == name.upper():
            return {
                "name": f.name,
                "maximum_credits": f.maximum_credits,
                "minimum_credits": f.minimum_credits,
                "maximum_days": f.maximum_days,
                "unique_course_limit": f.unique_course_limit,
                "times": {
                    str(day): [str(t) for t in times] for day, times in f.times.items()
                },
                "course_preferences": {
                    str(k): v for k, v in f.course_preferences.items()
                },
                "room_preferences": {str(k): v for k, v in f.room_preferences.items()},
                "lab_preferences": {str(k): v for k, v in f.lab_preferences.items()},
                "mandatory_days": [str(d) for d in f.mandatory_days],
            }
    return {"error": f'"{name}" not found.'}


# -------------------------
# COURSE (FIXED)
# -------------------------


def add_course(scheduler, course_id: str, credits: int, room, lab, conflicts, faculty):
    existing = [c.course_id.upper() for c in scheduler.config.config.courses]

    if course_id.upper() in existing:
        return {"error": f'"{course_id}" already exists.'}

    # normalize structure
    room = _ensure_list(room)
    lab = _ensure_list(lab)
    conflicts = _ensure_list(conflicts)
    faculty = _ensure_list(faculty)

    # clean
    room = _clean_list(room)
    lab = _clean_list(lab)
    conflicts = _clean_list(conflicts)
    faculty = _clean_list(faculty)

    # semantic normalization
    room = [_normalize_name(r) for r in room]
    lab = [_normalize_name(lab) for lab in lab]

    scheduler.course.add_course(
        scheduler.config, course_id, credits, room, lab, conflicts, faculty
    )

    return {"status": "added", "course": course_id}


def get_course_details(scheduler, course_id: str):
    for i, c in enumerate(scheduler.config.config.courses):
        if c.course_id.upper() == course_id.upper():
            return {
                "index": i,
                "course_id": c.course_id,
                "credits": c.credits,
                "room": list(c.room),
                "lab": list(c.lab),
                "conflicts": list(c.conflicts),
                "faculty": list(c.faculty),
            }
    return {"error": f'"{course_id}" not found.'}


def delete_course(scheduler, course_id: str):
    existing = [c.course_id.upper() for c in scheduler.config.config.courses]

    if course_id.upper() not in existing:
        return {"error": f'"{course_id}" not found.'}

    scheduler.course.delete_course(scheduler.config, course_id)

    return {"status": "deleted", "course": course_id}


def modify_course(
    scheduler, index: int, course_id: str, credits: int, room, lab, conflicts, faculty
):
    try:
        # same normalization (important)
        room = _ensure_list(room)
        lab = _ensure_list(lab)
        conflicts = _ensure_list(conflicts)
        faculty = _ensure_list(faculty)

        room = _clean_list(room)
        lab = _clean_list(lab)
        conflicts = _clean_list(conflicts)
        faculty = _clean_list(faculty)

        room = [_normalize_name(r) for r in room]
        lab = [_normalize_name(lab) for lab in lab]

        course = scheduler.config.config.courses[index]

        course.course_id = course_id
        course.credits = credits
        course.room = room
        course.lab = lab
        course.conflicts = conflicts
        course.faculty = faculty

        return {"status": "modified", "course": course_id}

    except IndexError:
        return {"error": "Invalid course index"}


# -------------------------
# LAB
# -------------------------


def add_lab(scheduler, name: str):
    labs = scheduler.config.config.labs

    name = _normalize_name(name)

    if name.upper() in [lab.upper() for lab in labs]:
        return {"error": f'"{name}" already exists.'}

    labs.append(name)

    return {"status": "added", "lab": name}


def delete_lab(scheduler, name: str):
    labs = scheduler.config.config.labs

    actual = _find_in_list(name, labs)
    if actual is None:
        return {"error": f'"{name}" not found.'}

    labs.remove(actual)

    for course in scheduler.config.config.courses:
        course.lab = [lab for lab in course.lab if lab != actual]

    return {"status": "deleted", "lab": actual}


def modify_lab(scheduler, old_name: str, new_name: str):
    labs = scheduler.config.config.labs

    actual_old = _find_in_list(old_name, labs)
    if actual_old is None:
        return {"error": f'"{old_name}" not found.'}

    new_name = _normalize_name(new_name)

    if _find_in_list(new_name, labs) is not None:
        return {"error": f'"{new_name}" already exists.'}

    labs[labs.index(actual_old)] = new_name

    for course in scheduler.config.config.courses:
        course.lab = [new_name if lab == actual_old else lab for lab in course.lab]

    return {"status": "modified", "lab": new_name}


# -------------------------
# ROOM
# -------------------------


def add_room(scheduler, name: str):
    rooms = scheduler.config.config.rooms

    name = _normalize_name(name)

    if name.upper() in [r.upper() for r in rooms]:
        return {"error": f'"{name}" already exists.'}

    rooms.append(name)

    return {"status": "added", "room": name}


def delete_room(scheduler, name: str):
    rooms = scheduler.config.config.rooms

    actual = _find_in_list(name, rooms)
    if actual is None:
        return {"error": f'"{name}" not found.'}

    rooms.remove(actual)

    for course in scheduler.config.config.courses:
        course.room = [r for r in course.room if r != actual]

    return {"status": "deleted", "room": actual}


def modify_room(scheduler, old_name: str, new_name: str):
    rooms = scheduler.config.config.rooms

    actual_old = _find_in_list(old_name, rooms)
    if actual_old is None:
        return {"error": f'"{old_name}" not found.'}

    new_name = _normalize_name(new_name)

    if _find_in_list(new_name, rooms) is not None:
        return {"error": f'"{new_name}" already exists.'}

    rooms[rooms.index(actual_old)] = new_name

    for course in scheduler.config.config.courses:
        course.room = [new_name if r == actual_old else r for r in course.room]

    return {"status": "modified", "room": new_name}


# -------------------------
# TIME SLOTS
# -------------------------


# Serializes a time-range entry to a plain dict.
# Handles both dict entries (added at runtime) and pydantic TimeBlock objects
# (loaded from a config file).
def _ts_serialize_range(r):
    if isinstance(r, dict):
        return {
            "start": str(r.get("start", "")),
            "spacing": int(r.get("spacing", 0)),
            "end": str(r.get("end", "")),
        }
    return {
        "start": str(getattr(r, "start", "")),
        "spacing": int(getattr(r, "spacing", 0)),
        "end": str(getattr(r, "end", "")),
    }


# Serializes a meeting entry to a plain dict.
# Handles both dict entries and pydantic model objects.
def _ts_serialize_meeting(m):
    if isinstance(m, dict):
        return {
            "day": str(m.get("day", "")),
            "duration": int(m.get("duration", 0)),
            "lab": bool(m.get("lab", False)),
        }
    return {
        "day": str(getattr(m, "day", "")),
        "duration": int(getattr(m, "duration", 0)),
        "lab": bool(getattr(m, "lab", False)),
    }


# Serializes a class-pattern entry to a plain dict.
# Handles both dict entries and pydantic model objects.
# start_time is omitted from the result when absent.
def _ts_serialize_class(cls):
    if isinstance(cls, dict):
        credits = cls.get("credits", 0)
        meetings = cls.get("meetings", [])
        start_time = cls.get("start_time", None)
        disabled = cls.get("disabled", False)
    else:
        credits = getattr(cls, "credits", 0)
        meetings = getattr(cls, "meetings", [])
        start_time = getattr(cls, "start_time", None)
        disabled = getattr(cls, "disabled", False)
    result = {
        "credits": int(credits),
        "meetings": [_ts_serialize_meeting(m) for m in meetings],
        "disabled": bool(disabled),
    }
    if start_time is not None:
        result["start_time"] = str(start_time)
    return result


def get_time_slot_config(scheduler):
    times_raw = scheduler.time_slot.get_times(scheduler.config)
    classes_raw = scheduler.time_slot.get_classes(scheduler.config)
    times = {
        str(day): [_ts_serialize_range(r) for r in ranges]
        for day, ranges in times_raw.items()
    }
    classes = [_ts_serialize_class(cls) for cls in classes_raw]
    return {"times": times, "classes": classes}


def add_time_range(scheduler, day: str, start: str, spacing: int, end: str):
    day = day.upper()
    if day not in {"MON", "TUE", "WED", "THU", "FRI"}:
        return {"error": f"'{day}' is not a valid day."}
    scheduler.time_slot.add_time(scheduler.config, day, start, spacing, end)
    return {"status": "added", "day": day, "start": start, "end": end}


def modify_time_range(
    scheduler, day: str, index: int, start: str, spacing: int, end: str
):
    day = day.upper()
    if not scheduler.time_slot.validate_time_entry(
        scheduler.config, day, "modify", index
    ):
        return {"error": f"Time range index {index} for {day} not found."}
    scheduler.time_slot.modify_time(scheduler.config, day, index, start, spacing, end)
    return {"status": "modified"}


def delete_time_range(scheduler, day: str, index: int):
    day = day.upper()
    if not scheduler.time_slot.validate_time_entry(
        scheduler.config, day, "delete", index
    ):
        return {"error": f"Time range index {index} for {day} not found."}
    scheduler.time_slot.delete_time(scheduler.config, day, index)
    return {"status": "deleted"}


def add_class_pattern(
    scheduler,
    credits: int,
    meetings: list,
    start_time: str = None,
    disabled: bool = False,
):
    if not scheduler.time_slot.validate_class_entry(
        scheduler.config, "add", credits=credits, meetings=meetings
    ):
        return {"error": "Invalid class pattern — check day names and durations."}
    scheduler.time_slot.add_class(
        scheduler.config, credits, meetings, start_time, disabled
    )
    return {"status": "added"}


def modify_class_pattern(
    scheduler,
    index: int,
    credits: int,
    meetings: list,
    start_time: str = None,
    disabled: bool = False,
):
    if not scheduler.time_slot.validate_class_entry(
        scheduler.config, "modify", class_index=index
    ):
        return {"error": f"Class pattern index {index} not found."}
    scheduler.time_slot.modify_class(
        scheduler.config, index, credits, meetings, start_time, disabled
    )
    return {"status": "modified"}


def delete_class_pattern(scheduler, index: int):
    if not scheduler.time_slot.validate_class_entry(
        scheduler.config, "delete", class_index=index
    ):
        return {"error": f"Class pattern index {index} not found."}
    scheduler.time_slot.delete_class(scheduler.config, index)
    return {"status": "deleted"}


# -------------------------
# SCHEDULER
# -------------------------


# Runs the scheduling engine and returns the number of generated schedules
# along with a ui_action signal so the frontend opens the schedule viewer.
# Parameters: scheduler - shared Schedule instance
#             limit     - maximum number of schedules to generate
#             optimize  - whether to apply optimizer flags
# Returns: dict with ui_action "open_schedule" and count of generated schedules
def run_scheduler(scheduler, limit: int, optimize: bool):
    results = scheduler.run_scheduler(limit, optimize)
    count = len(results) if results else 0
    return {"ui_action": "open_schedule", "count": count}


def open_schedule_tool():
    return {"ui_action": "open_schedule"}
