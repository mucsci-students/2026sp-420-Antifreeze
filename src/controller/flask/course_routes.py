from flask import request, jsonify


# Registers all course REST API routes on the Flask app.
# All handlers close over `scheduler` for access to the config and course model.
def register_course_routes(app, scheduler):

    # Returns a JSON array of all courses with their full configuration.
    @app.route("/courses", methods=["GET"])
    def get_courses():
        try:
            courses = []

            for c in scheduler.config.config.courses:
                courses.append(
                    {
                        "course_id": c.course_id,
                        "credits": c.credits,
                        "room": list(c.room),
                        "lab": list(c.lab),
                        "conflicts": list(c.conflicts),
                        "faculty": list(c.faculty),
                    }
                )

            return jsonify(courses)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Adds a new course. Expects course_id, credits, room, lab, conflicts,
    # and faculty in the JSON body.
    # Returns 409 if a course with that ID already exists.
    @app.route("/courses", methods=["POST"])
    def add_course():
        try:
            data = request.json
            course_id = data["course_id"]

            # Check for duplicate before delegating to model
            existing = [c.course_id.upper() for c in scheduler.config.config.courses]
            if course_id.upper() in existing:
                return jsonify({"error": f'"{course_id}" already exists.'}), 409

            scheduler.course.add_course(
                scheduler.config,
                course_id,
                data["credits"],
                data["room"],
                data["lab"],
                data["conflicts"],
                data["faculty"],
            )

            return jsonify({"status": "added"})

        except KeyError as e:
            return jsonify({"error": f"Missing field: {str(e)}"}), 400

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Deletes a course by course_id from the scheduler config.
    # Returns 404 if the course does not exist.
    # Parameters: course_id - taken from the URL path
    @app.route("/courses/<course_id>", methods=["DELETE"])
    def delete_course(course_id):
        try:
            existing = [c.course_id.upper() for c in scheduler.config.config.courses]

            if course_id.upper() not in existing:
                return jsonify(
                    {
                        "error": f'"{course_id}" was not found. Please check the course ID and try again.'
                    }
                ), 404

            scheduler.course.delete_course(scheduler.config, course_id)

            return jsonify({"status": "deleted"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Modifies an existing course. The URL course_id is the old ID.
    # Expects new course_id, credits, room, lab, conflicts, and faculty in the JSON body.
    # Returns 404 if the old course_id does not exist.
    # Returns 409 if the new course_id already belongs to a different course.
    # Parameters: course_id - old course ID taken from the URL path
    @app.route("/courses/<int:index>", methods=["PUT"])
    def modify_course(index):
        try:
            data = request.json
            print(data)
            course = scheduler.config.config.courses[index]

            course.course_id = data["course_id"]
            course.credits = data["credits"]
            course.room = data["room"]
            course.lab = data["lab"]
            course.conflicts = data["conflicts"]
            course.faculty = data["faculty"]

            return jsonify({"status": "modified"})

        except IndexError:
            return jsonify({"error": "Invalid course index"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/courses/<int:index>", methods=["GET"])
    def get_course(index):
        """Return the full details of a single course by its 0-based list index.
        Returns 404 if the index is out of range.
        """
        try:
            course = scheduler.config.config.courses[index]

            return jsonify(
                {
                    "course_id": course.course_id,
                    "credits": course.credits,
                    "room": course.room,
                    "lab": course.lab,
                    "conflicts": course.conflicts,
                    "faculty": course.faculty,
                }
            )

        except IndexError:
            return jsonify({"error": "Invalid course index"}), 404

        except Exception as e:
            return jsonify({"error": str(e)}), 500
