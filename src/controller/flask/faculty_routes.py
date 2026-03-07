from flask import request, jsonify


def register_faculty_routes(app, scheduler):

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
    