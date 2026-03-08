from flask import request, jsonify, send_file
import os
import json
import io


# Registers all schedule-level REST API routes on the Flask app.
# Covers config loading/saving, scheduler execution, result retrieval, and PDF export.
def register_schedule_routes(app, scheduler):

    # Accepts a uploaded JSON config file, saves it to /uploads, and loads it into the scheduler.
    # Expects a multipart file upload with key "file".
    @app.route("/load_config", methods=["POST"])
    def load_config():
        file = request.files["file"]

        os.makedirs("uploads", exist_ok=True)

        path = os.path.join("uploads", file.filename)
        file.save(path)

        scheduler.load_config(path)

        return jsonify({"status": "loaded"})

    # Serializes the current scheduler config to JSON and returns it as a downloadable file.
    @app.route("/save_config")
    def save_config():
        file_data = scheduler.config.model_dump_json(indent=2)

        return send_file(
            io.BytesIO(file_data.encode()),
            mimetype="application/json",
            as_attachment=True,
            download_name="schedule_config.json"
        )

    # Runs the scheduler with the given parameters.
    # Expects limit (int) and optimize (bool) in the JSON body.
    # Returns the count of generated schedules.
    @app.route("/run_scheduler", methods=["POST"])
    def run_scheduler_route():
        try:
            data = request.json

            limit = int(data["limit"])
            optimize = bool(data["optimize"])

            results = scheduler.run_scheduler(limit, optimize)

            return jsonify({
                "count": len(results)
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Returns a single generated schedule by index as a list of CSV row strings.
    # Returns 400 if no schedules exist, 400 if index is out of range.
    # Parameters: index - zero-based position in the results list
    @app.route("/schedule/<int:index>", methods=["GET"])
    def get_schedule(index):
        try:

            if not scheduler.result:
                return jsonify({"error": "No schedules generated"}), 400

            if index >= len(scheduler.result):
                return jsonify({"error": "Schedule index out of range"}), 400

            model = scheduler.result[index]

            rows = []

            for sch in model:
                rows.append(sch.as_csv())

            return jsonify({
                "schedule": rows
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Returns a single generated schedule grouped by day, with rows sorted by time.
    # Each day group contains a list of slot rows.  Every slot row has one entry per
    # meeting that falls on that day, with the time stripped of its day prefix.
    # Mode controls which secondary grouping label is shown as a sub-header within
    # each day: "course" (none), "faculty", "room", or "lab".
    # Returns 400 if no schedules exist or index is out of range.
    # Parameters: index - zero-based schedule index, mode - secondary grouping string
    @app.route("/schedule/<int:index>/view/<mode>", methods=["GET"])
    def get_schedule_grouped(index, mode):
        try:
            if not scheduler.result:
                return jsonify({"error": "No schedules generated"}), 400

            if index >= len(scheduler.result):
                return jsonify({"error": "Schedule index out of range"}), 400

            model = scheduler.result[index]

            DAY_ORDER = {"MON": 0, "TUE": 1, "WED": 2, "THU": 3, "FRI": 4}

            # Parse every CSV row and expand into one slot-entry per meeting day
            # A slot entry = one (day, time, course_row) triple
            slot_entries = []
            for sch in model:
                parts = [p.strip() for p in sch.as_csv().split(",")]
                if len(parts) < 4:
                    continue
                course_section = parts[0]
                faculty_name   = parts[1]
                room_name      = parts[2]
                lab_name       = parts[3]
                meetings       = parts[4:]
                course_id, _, section = course_section.partition(".")

                row = {
                    "course":  course_id,
                    "section": section,
                    "faculty": faculty_name,
                    "room":    room_name,
                    "lab":     lab_name,
                }

                for meeting in meetings:
                    meeting = meeting.strip()
                    if not meeting:
                        continue
                    # Strip the lab marker '^'
                    is_lab = meeting.endswith("^")
                    clean  = meeting.rstrip("^").strip()
                    # Expected format: "MON 09:00-09:50"
                    tokens = clean.split(" ", 1)
                    if len(tokens) != 2:
                        continue
                    day_abbr, time_range = tokens[0].upper(), tokens[1]
                    if day_abbr not in DAY_ORDER:
                        continue
                    slot_entries.append({
                        "day":      day_abbr,
                        "day_ord":  DAY_ORDER[day_abbr],
                        "time":     time_range,
                        "is_lab":   is_lab,
                        **row,
                    })

            # Sort all slot entries: day first, then start-time
            slot_entries.sort(key=lambda e: (e["day_ord"], e["time"]))

            # Determine secondary grouping key
            if mode == "faculty":
                group_key_fn = lambda e: e["faculty"]
            elif mode == "room":
                group_key_fn = lambda e: e["room"]
            elif mode == "lab":
                group_key_fn = lambda e: e["lab"]
            else:
                group_key_fn = None   # no sub-grouping for "course" mode

            # Build day → (optional sub-group →) list-of-slots structure
            DAY_NAMES = {"MON": "Monday", "TUE": "Tuesday", "WED": "Wednesday",
                         "THU": "Thursday", "FRI": "Friday"}

            days_dict = {}   # day_abbr -> { subkey -> [slot, ...] }
            for entry in slot_entries:
                day = entry["day"]
                sub = group_key_fn(entry) if group_key_fn else None
                days_dict.setdefault(day, {}).setdefault(sub, []).append({
                    "time":    entry["time"],
                    "is_lab":  entry["is_lab"],
                    "course":  entry["course"],
                    "section": entry["section"],
                    "faculty": entry["faculty"],
                    "room":    entry["room"],
                    "lab":     entry["lab"],
                })

            # Serialise into ordered list for JSON
            day_groups = []
            for day_abbr in ["MON", "TUE", "WED", "THU", "FRI"]:
                if day_abbr not in days_dict:
                    continue
                sub_groups = []
                for sub_key in (sorted(days_dict[day_abbr]) if group_key_fn else [None]):
                    sub_groups.append({
                        "sub_key": sub_key,
                        "slots":   days_dict[day_abbr][sub_key],
                    })
                day_groups.append({
                    "day":        day_abbr,
                    "day_name":   DAY_NAMES[day_abbr],
                    "sub_groups": sub_groups,
                })

            return jsonify({"mode": mode, "days": day_groups})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    from flask import send_file

    # Exports all generated schedules as a PDF and returns it as a downloadable file.
    # Returns 400 if no schedules have been generated yet.
    @app.route("/print_schedules", methods=["GET"])
    def print_schedules():

        pdf = scheduler.export_schedules_pdf()

        if not pdf:
            return jsonify({"error": "No schedules generated"}), 400

        return send_file(
            pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="schedules.pdf"
        )