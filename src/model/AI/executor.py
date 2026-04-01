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
    mandatory_days=None
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
            mandatory_days
        )
    except Exception as e:
        msg = str(e)
        import re
        m = re.search(r"Mandatory days \[([^\]]+)\] must be present in the availability times", msg)
        if m:
            missing = m.group(1)
            return {"error": f"Mandatory day(s) {missing} must have an availability time set. Please ask the user to provide time slots for those days (e.g. '09:00-09:50') before setting them as mandatory."}
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
    mandatory_days=None
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
            mandatory_days
        )
    except Exception as e:
        msg = str(e)
        import re
        m = re.search(r"Mandatory days \[([^\]]+)\] must be present in the availability times", msg)
        if m:
            missing = m.group(1)
            return {"error": f"Mandatory day(s) {missing} must have an availability time set. Please ask the user to provide time slots for those days (e.g. '09:00-09:50') before setting them as mandatory."}
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
    return {
        "faculty": [{"name": f.name} for f in scheduler.config.config.faculty]
    }


def get_faculty_details(scheduler, name: str):
    for f in scheduler.config.config.faculty:
        if f.name.upper() == name.upper():
            return {
                "name": f.name,
                "maximum_credits": f.maximum_credits,
                "minimum_credits": f.minimum_credits,
                "maximum_days": f.maximum_days,
                "unique_course_limit": f.unique_course_limit,
                "times": {str(day): [str(t) for t in times] for day, times in f.times.items()},
                "course_preferences": {str(k): v for k, v in f.course_preferences.items()},
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
    lab = [_normalize_name(l) for l in lab]

    scheduler.course.add_course(
        scheduler.config,
        course_id,
        credits,
        room,
        lab,
        conflicts,
        faculty
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


def modify_course(scheduler, index: int, course_id: str, credits: int, room, lab, conflicts, faculty):
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
        lab = [_normalize_name(l) for l in lab]

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

    if name.upper() in [l.upper() for l in labs]:
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
        course.lab = [l for l in course.lab if l != actual]

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
        course.lab = [new_name if l == actual_old else l for l in course.lab]

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
# SCHEDULER
# -------------------------
def open_schedule_tool():
    return {"ui_action": "open_schedule"}