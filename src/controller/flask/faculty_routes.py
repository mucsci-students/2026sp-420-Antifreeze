from flask import request, jsonify


# Registers all faculty REST API routes on the Flask app.
# All handlers close over `scheduler` for access to the config and faculty model.
def register_faculty_routes(app, scheduler):

    # Returns a JSON array of all faculty names from the scheduler config.
    @app.route("/faculty", methods=["GET"])
    def get_faculty():
        faculty_list = []

        try:
            for f in scheduler.config.config.faculty:
                faculty_list.append({
                    "name": f.name
                })

            return jsonify(faculty_list)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Adds a new faculty member. Requires name, maximum_credits, maximum_days,
    # minimum_credits in the JSON body. Optional: unique_course_limit, times,
    # course/room/lab_preferences, mandatory_days.
    @app.route("/faculty", methods=["POST"])
    def add_faculty():
        try:
            print("ADD FACULTY ROUTE HIT")

            data = request.json

            required = [
                "name",
                "maximum_credits",
                "maximum_days",
                "minimum_credits",
            ]

            for field in required:
                if field not in data:
                    return jsonify({"error": f"Missing {field}"}), 400

            scheduler.faculty.add_faculty(
                scheduler.config,
                data["name"],
                data["maximum_credits"],
                data["maximum_days"],
                data["minimum_credits"],
                data["unique_course_limit"],
                data["times"],
                data["course_preferences"],
                data["room_preferences"],
                data["lab_preferences"],
                set(data["mandatory_days"])
            )

            return jsonify({"status": "added"})

        except KeyError as e:
            print("Missing field:", e)
            return jsonify({"error": f"Missing field {str(e)}"}), 400

        except Exception as e:
            print("Faculty add error:", e)
            return jsonify({"error": str(e)}), 500

    # Deletes the faculty member matching `name` from the scheduler config.
    @app.route("/faculty/<name>", methods=["DELETE"])
    def delete_faculty(name):
        try:
            scheduler.faculty.delete_faculty(
                scheduler.config,
                name
            )

            return jsonify({"status": "deleted"})

        except Exception as e:
            print("Faculty delete error:", e)
            return jsonify({"error": str(e)}), 500

    # Returns details for a single faculty member. Search is case-insensitive.
    # Returns 404 if not found.
    @app.route("/faculty/<name>", methods=["GET"])
    def get_single_faculty(name):
        try:
            for f in scheduler.config.config.faculty:
                if f.name.upper() == name.upper():
                    return jsonify({
                        "name": f.name,
                        "maximum_credits": f.maximum_credits,
                        "maximum_days": f.maximum_days,
                        "minimum_credits": f.minimum_credits,
                        "unique_course_limit": f.unique_course_limit
                    })

            return jsonify({"error": "Faculty not found"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500