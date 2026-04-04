from flask import request, jsonify


def register_room_routes(app, scheduler):

    @app.route("/rooms", methods=["GET"])
    def get_rooms():
        try:
            rooms = []

            for room in scheduler.config.config.rooms:
                rooms.append({"name": room})

            return jsonify(rooms)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/rooms", methods=["POST"])
    def add_room():
        try:
            data = request.json
            name = data["name"]

            rooms = scheduler.config.config.rooms

            # Converting to upper case to add case insensitivity
            upper_case_rooms = [room.upper() for room in rooms]

            if name.upper() in upper_case_rooms:
                return jsonify({"error": f'"{name}" already exists.'}), 409

            rooms.append(name)

            print(f"Room '{name}' added successfully.")

            return jsonify({"status": "added"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/rooms/<room_name>", methods=["DELETE"])
    def delete_room(room_name):
        try:
            rooms = scheduler.config.config.rooms

            if room_name not in rooms:
                return jsonify(
                    {
                        "error": f'"{room_name}" was not found. Please check the name and try again.'
                    }
                ), 404

            rooms.remove(room_name)

            # cascade removal from courses
            for course in scheduler.config.config.courses:
                course.room = [r for r in course.room if r != room_name]

            print(f"Room '{room_name}' deleted successfully.")

            return jsonify({"status": "deleted"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/rooms/<room_name>", methods=["PUT"])
    def modify_room(room_name):
        try:
            data = request.json
            new_name = data["name"]

            rooms = scheduler.config.config.rooms

            # Converting to upper case to add case insensitivity
            upper_case_rooms = [room.upper() for room in rooms]

            if room_name.upper() not in upper_case_rooms:
                return jsonify(
                    {
                        "error": f'"{room_name}" was not found. Please check the name and try again.'
                    }
                ), 404

            if new_name.upper() in upper_case_rooms:
                return jsonify(
                    {"error": f'"{new_name}" already exists. Choose a different name.'}
                ), 409

            rooms[rooms.index(room_name)] = new_name

            # cascade rename inside courses
            for course in scheduler.config.config.courses:
                course.room = [new_name if r == room_name else r for r in course.room]

            return jsonify({"status": "modified"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
