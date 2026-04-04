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
    name = name.lower().strip()
    name = name.replace(" lab", "")
    name = name.replace(" room", "")
    return name


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

    # ✅ defaults handled properly
    times = times or {}
    course_preferences = course_preferences or {}
    room_preferences = room_preferences or {}
    lab_preferences = lab_preferences or {}
    mandatory_days = mandatory_days or set()

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

    # ✅ defaults
    times = times or {}
    course_preferences = course_preferences or {}
    room_preferences = room_preferences or {}
    lab_preferences = lab_preferences or {}
    mandatory_days = mandatory_days or set()

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


# -------------------------
# COURSE (FIXED)
# -------------------------

def add_course(scheduler, course_id: str, credits: int, room, lab, conflicts, faculty):
    existing = [c.course_id.upper() for c in scheduler.config.config.courses]

    if course_id.upper() in existing:
        return {"error": f'"{course_id}" already exists.'}

    # 🔥 FIX: normalize structure
    room = _ensure_list(room)
    lab = _ensure_list(lab)
    conflicts = _ensure_list(conflicts)
    faculty = _ensure_list(faculty)

    # 🔥 FIX: clean
    room = _clean_list(room)
    lab = _clean_list(lab)
    conflicts = _clean_list(conflicts)
    faculty = _clean_list(faculty)

    # 🔥 FIX: semantic normalization
    room = [_normalize_name(r) for r in room]
    lab = [_normalize_name(lab) for lab in lab]

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


def delete_course(scheduler, course_id: str):
    existing = [c.course_id.upper() for c in scheduler.config.config.courses]

    if course_id.upper() not in existing:
        return {"error": f'"{course_id}" not found.'}

    scheduler.course.delete_course(scheduler.config, course_id)

    return {"status": "deleted", "course": course_id}


def modify_course(scheduler, index: int, course_id: str, credits: int, room, lab, conflicts, faculty):
    try:
        # 🔥 SAME FIXES HERE (important)
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

    name = _normalize_name(name)

    if name not in labs:
        return {"error": f'"{name}" not found.'}

    labs.remove(name)

    for course in scheduler.config.config.courses:
        course.lab = [lab for lab in course.lab if lab != name]

    return {"status": "deleted", "lab": name}


def modify_lab(scheduler, old_name: str, new_name: str):
    labs = scheduler.config.config.labs

    old_name = _normalize_name(old_name)
    new_name = _normalize_name(new_name)

    if old_name not in labs:
        return {"error": f'"{old_name}" not found.'}

    if new_name in labs:
        return {"error": f'"{new_name}" already exists.'}

    labs[labs.index(old_name)] = new_name

    for course in scheduler.config.config.courses:
        course.lab = [new_name if lab == old_name else lab for lab in course.lab]

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

    name = _normalize_name(name)

    if name not in rooms:
        return {"error": f'"{name}" not found.'}

    rooms.remove(name)

    for course in scheduler.config.config.courses:
        course.room = [r for r in course.room if r != name]

    return {"status": "deleted", "room": name}


def modify_room(scheduler, old_name: str, new_name: str):
    rooms = scheduler.config.config.rooms

    old_name = _normalize_name(old_name)
    new_name = _normalize_name(new_name)

    if old_name not in rooms:
        return {"error": f'"{old_name}" not found.'}

    if new_name in rooms:
        return {"error": f'"{new_name}" already exists.'}

    rooms[rooms.index(old_name)] = new_name

    for course in scheduler.config.config.courses:
        course.room = [new_name if r == old_name else r for r in course.room]

    return {"status": "modified", "room": new_name}


# -------------------------
# SCHEDULER
# -------------------------

def run_scheduler(scheduler, limit: int, optimize: bool):
    results = scheduler.run_scheduler(limit, optimize)
    return {"count": len(results)}


def get_schedule(scheduler, index: int):
    if not scheduler.result:
        return {"error": "No schedules generated"}

    if index >= len(scheduler.result):
        return {"error": "Index out of range"}

    model = scheduler.result[index]

    return {"schedule": [sch.as_csv() for sch in model]}
