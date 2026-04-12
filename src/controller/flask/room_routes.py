from flask import request, jsonify


def register_room_routes(app, scheduler):
    """Registers all room REST API routes on the Flask app.

    All handlers close over `scheduler` for access to the config and room list.
    """

    @app.route("/rooms", methods=["GET"])
    def get_rooms():
        """Return a JSON array of all room names in the current config."""
        try:
            rooms = []

            for room in scheduler.config.config.rooms:
                rooms.append({"name": room})

            return jsonify(rooms)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/rooms", methods=["POST"])
    def add_room():
        """Add a new room. Expects JSON body with key 'name'.
        Returns 409 if the room already exists (case-insensitive check).
        """
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
        """Delete the named room and cascade removal to course room lists.
        Returns 404 if the room does not exist.
        """
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
        """Rename a room and cascade the change to all course room lists.
        Expects JSON body with key 'name' (new name).
        Returns 404 if the old name is not found; 409 if the new name already exists.
        """
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
