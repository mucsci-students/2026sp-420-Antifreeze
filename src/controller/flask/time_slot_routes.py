import re as _re
from flask import request, jsonify


_VALID_DAYS = {"MON", "TUE", "WED", "THU", "FRI"}
_TIME_PATTERN = r"^([01]\d|2[0-3]):[0-5]\d$"


# Serializes a single time-range entry to a plain dict.
# Handles both dict entries (added at runtime) and pydantic TimeBlock
# objects (loaded from a config file).
# Parameters: r - time range entry (dict or TimeBlock pydantic model)
# Returns: dict with keys start (str), spacing (int), end (str)
def _serialize_range(r):
    if isinstance(r, dict):
        return {
            "start":   str(r.get("start",   "")),
            "spacing": int(r.get("spacing", 0)),
            "end":     str(r.get("end",     ""))
        }
    return {
        "start":   str(getattr(r, "start",   "")),
        "spacing": int(getattr(r, "spacing", 0)),
        "end":     str(getattr(r, "end",     ""))
    }


# Serializes a single meeting entry to a plain dict.
# Handles both dict entries and pydantic model objects.
# Parameters: m - meeting entry (dict or pydantic model)
# Returns: dict with keys day (str), duration (int), lab (bool)
def _serialize_meeting(m):
    if isinstance(m, dict):
        return {
            "day":      str(m.get("day",      "")),
            "duration": int(m.get("duration", 0)),
            "lab":      bool(m.get("lab",     False))
        }
    return {
        "day":      str(getattr(m, "day",      "")),
        "duration": int(getattr(m, "duration", 0)),
        "lab":      bool(getattr(m, "lab",     False))
    }


# Serializes a single class-pattern entry to a plain dict.
# Handles both dict entries and pydantic model objects.
# start_time is omitted from the result when absent.
# Parameters: cls - class pattern entry (dict or pydantic model)
# Returns: dict with keys credits (int), meetings (list), disabled (bool),
#          and optionally start_time (str)
def _serialize_class(cls):
    if isinstance(cls, dict):
        credits    = cls.get("credits",    0)
        meetings   = cls.get("meetings",   [])
        start_time = cls.get("start_time", None)
        disabled   = cls.get("disabled",   False)
    else:
        credits    = getattr(cls, "credits",    0)
        meetings   = getattr(cls, "meetings",   [])
        start_time = getattr(cls, "start_time", None)
        disabled   = getattr(cls, "disabled",   False)

    result = {
        "credits":  int(credits),
        "meetings": [_serialize_meeting(m) for m in meetings],
        "disabled": bool(disabled)
    }
    if start_time is not None:
        result["start_time"] = str(start_time)
    return result


# Registers all time slot REST API routes on the Flask app.
# Covers both time-grid ranges and class meeting patterns.
# All handlers close over `scheduler` for access to the config.
def register_time_slot_routes(app, scheduler):

    # Returns the full time slot configuration as JSON.
    # Response: { "times": { DAY: [{start, spacing, end}, ...] }, "classes": [{...}, ...] }
    @app.route("/time_slots", methods=["GET"])
    def get_time_slots():
        try:
            times_raw   = scheduler.time_slot.get_times(scheduler.config)
            classes_raw = scheduler.time_slot.get_classes(scheduler.config)

            times = {
                str(day): [_serialize_range(r) for r in ranges]
                for day, ranges in times_raw.items()
            }
            classes = [_serialize_class(cls) for cls in classes_raw]

            return jsonify({"times": times, "classes": classes})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Adds a new time range to a day's grid.
    # Expects JSON body: { day, start (HH:MM), spacing (int min), end (HH:MM) }
    @app.route("/time_slots/times", methods=["POST"])
    def add_time_range():
        try:
            data    = request.json
            day     = str(data.get("day", "")).upper()
            start   = str(data.get("start",   ""))
            end     = str(data.get("end",     ""))
            spacing = data.get("spacing")

            if day not in _VALID_DAYS:
                return jsonify({"error": f"'{day}' is not a valid day. Use MON, TUE, WED, THU, or FRI."}), 400
            if not _re.match(_TIME_PATTERN, start):
                return jsonify({"error": "Start time must be in HH:MM format (e.g. 08:00)."}), 400
            if not _re.match(_TIME_PATTERN, end):
                return jsonify({"error": "End time must be in HH:MM format (e.g. 17:00)."}), 400
            if spacing is None or int(spacing) <= 0:
                return jsonify({"error": "Spacing must be a positive integer (minutes)."}), 400

            scheduler.time_slot.add_time(scheduler.config, day, start, int(spacing), end)
            return jsonify({"status": "added"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Modifies a time range within a day by index.
    # Expects JSON body: { start (HH:MM), spacing (int min), end (HH:MM) }
    # Parameters: day - weekday string (MON-FRI), index - 0-based position
    @app.route("/time_slots/times/<day>/<int:index>", methods=["PUT"])
    def modify_time_range(day, index):
        try:
            day   = day.upper()
            data  = request.json
            start   = str(data.get("start",   ""))
            end     = str(data.get("end",     ""))
            spacing = data.get("spacing")

            if day not in _VALID_DAYS:
                return jsonify({"error": f"'{day}' is not a valid day."}), 400
            if not _re.match(_TIME_PATTERN, start):
                return jsonify({"error": "Start time must be in HH:MM format (e.g. 08:00)."}), 400
            if not _re.match(_TIME_PATTERN, end):
                return jsonify({"error": "End time must be in HH:MM format (e.g. 17:00)."}), 400
            if spacing is None or int(spacing) <= 0:
                return jsonify({"error": "Spacing must be a positive integer (minutes)."}), 400

            if not scheduler.time_slot.validate_time_entry(scheduler.config, day, "modify", index):
                return jsonify({"error": f"Time range index {index} for {day} not found."}), 404

            scheduler.time_slot.modify_time(scheduler.config, day, index, start, int(spacing), end)
            return jsonify({"status": "modified"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Deletes a time range from a day by index.
    # Parameters: day - weekday string (MON-FRI), index - 0-based position
    @app.route("/time_slots/times/<day>/<int:index>", methods=["DELETE"])
    def delete_time_range(day, index):
        try:
            day = day.upper()
            if not scheduler.time_slot.validate_time_entry(scheduler.config, day, "delete", index):
                return jsonify({"error": f"Time range index {index} for {day} not found."}), 404
            scheduler.time_slot.delete_time(scheduler.config, day, index)
            return jsonify({"status": "deleted"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Adds a new class meeting pattern.
    # Expects JSON body: { credits (int), meetings ([{day, duration, lab?},...]),
    #                      start_time? (HH:MM), disabled? (bool) }
    @app.route("/time_slots/classes", methods=["POST"])
    def add_class_pattern():
        try:
            data       = request.json
            credits    = data.get("credits")
            meetings   = data.get("meetings", [])
            start_time = data.get("start_time") or None
            disabled   = bool(data.get("disabled", False))

            if credits is None or int(credits) <= 0:
                return jsonify({"error": "Credits must be a positive integer."}), 400
            if not meetings:
                return jsonify({"error": "At least one meeting is required."}), 400

            credits = int(credits)

            if not scheduler.time_slot.validate_class_entry(
                    scheduler.config, "add", credits=credits, meetings=meetings):
                return jsonify({"error": "Invalid class pattern — check day names and durations."}), 400

            scheduler.time_slot.add_class(scheduler.config, credits, meetings, start_time, disabled)
            return jsonify({"status": "added"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Modifies an existing class meeting pattern by index.
    # Expects JSON body: { credits, meetings, start_time?, disabled? }
    # Parameters: index - 0-based position in the classes list
    @app.route("/time_slots/classes/<int:index>", methods=["PUT"])
    def modify_class_pattern(index):
        try:
            data       = request.json
            credits    = data.get("credits")
            meetings   = data.get("meetings", [])
            start_time = data.get("start_time") or None
            disabled   = bool(data.get("disabled", False))

            if credits is None or int(credits) <= 0:
                return jsonify({"error": "Credits must be a positive integer."}), 400
            if not meetings:
                return jsonify({"error": "At least one meeting is required."}), 400

            credits = int(credits)

            if not scheduler.time_slot.validate_class_entry(
                    scheduler.config, "modify", class_index=index):
                return jsonify({"error": f"Class pattern index {index} not found."}), 404

            scheduler.time_slot.modify_class(scheduler.config, index, credits, meetings, start_time, disabled)
            return jsonify({"status": "modified"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500


    # Deletes a class meeting pattern by index.
    # Parameters: index - 0-based position in the classes list
    @app.route("/time_slots/classes/<int:index>", methods=["DELETE"])
    def delete_class_pattern(index):
        try:
            if not scheduler.time_slot.validate_class_entry(
                    scheduler.config, "delete", class_index=index):
                return jsonify({"error": f"Class pattern index {index} not found."}), 404
            scheduler.time_slot.delete_class(scheduler.config, index)
            return jsonify({"status": "deleted"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
