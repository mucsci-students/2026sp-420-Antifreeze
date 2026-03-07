from flask import request, jsonify


# Registers all course REST API routes on the Flask app.
# All handlers close over `scheduler` for access to the config and course model.
def register_course_routes(app, scheduler):

    # Returns a JSON array of all courses with their course_id and credits.
    @app.route("/courses", methods=["GET"])
    def get_courses():
        try:
            courses = []

            for c in scheduler.config.config.courses:
                courses.append({
                    "course_id": c.course_id,
                    "credits": c.credits
                })

            return jsonify(courses)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Adds a new course. Expects course_id, credits, room, lab, conflicts,
    # and faculty in the JSON body.
    @app.route("/courses", methods=["POST"])
    def add_course():
        try:
            data = request.json

            scheduler.course.add_course(
                scheduler.config,
                data["course_id"],
                data["credits"],
                data["room"],
                data["lab"],
                data["conflicts"],
                data["faculty"]
            )

            return jsonify({"status": "added"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Deletes a course by course_id from the scheduler config.
    # Parameters: course_id - taken from the URL path
    @app.route("/courses/<course_id>", methods=["DELETE"])
    def delete_course(course_id):
        try:
            scheduler.course.delete_course(
                scheduler.config,
                course_id
            )

            return jsonify({"status": "deleted"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Modifies an existing course. The URL course_id is the old ID.
    # Expects new course_id, credits, room, lab, conflicts, and faculty in the JSON body.
    # Parameters: course_id - old course ID taken from the URL path
    @app.route("/courses/<course_id>", methods=["PUT"])
    def modify_course(course_id):
        try:
            data = request.json

            scheduler.course.modify_course(
                scheduler.config,
                course_id,          # old id
                data["course_id"],  # new id
                data["credits"],
                data["room"],
                data["lab"],
                data["conflicts"],
                data["faculty"]
            )

            return jsonify({"status": "modified"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500