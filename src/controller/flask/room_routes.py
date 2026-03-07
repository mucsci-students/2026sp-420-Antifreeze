from flask import request, jsonify


# Registers all room REST API routes on the Flask app.
# All handlers close over `scheduler` for access to the config directly.
def register_room_routes(app, scheduler):

    # Returns a JSON array of all room names.
    @app.route("/rooms", methods=["GET"])
    def get_rooms():
        try:
            rooms = []

            for room in scheduler.config.config.rooms:
                rooms.append({
                    "name": room
                })

            return jsonify(rooms)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Adds a new room. Expects name in the JSON body.
    # Returns "exists" status if the room already exists.
    @app.route("/rooms", methods=["POST"])
    def add_room():
        try:
            data = request.json
            name = data["name"]

            rooms = scheduler.config.config.rooms

            if name in rooms:
                print("Room already exists.")
                return jsonify({"status": "exists"})

            rooms.append(name)

            print(f"Room '{name}' added successfully.")

            return jsonify({"status": "added"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Deletes a room by name. Cascades removal from all course room lists.
    # Returns "not_found" status if the room does not exist.
    # Parameters: room_name - taken from the URL path
    @app.route("/rooms/<room_name>", methods=["DELETE"])
    def delete_room(room_name):
        try:
            rooms = scheduler.config.config.rooms

            if room_name not in rooms:
                print("Room not found.")
                return jsonify({"status": "not_found"})

            rooms.remove(room_name)

            # cascade removal from courses
            for course in scheduler.config.config.courses:
                course.room = [
                    r for r in course.room
                    if r != room_name
                ]

            print(f"Room '{room_name}' deleted successfully.")

            return jsonify({"status": "deleted"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Renames a room. Cascades the rename to all course room lists.
    # Expects new name in the JSON body. Returns 404 if room not found.
    # Parameters: room_name - current room name taken from the URL path
    @app.route("/rooms/<room_name>", methods=["PUT"])
    def modify_room(room_name):
        try:
            data = request.json
            new_name = data["name"]

            rooms = scheduler.config.config.rooms

            if room_name not in rooms:
                return jsonify({"error": "Room not found"}), 404

            rooms[rooms.index(room_name)] = new_name

            # cascade rename inside courses
            for course in scheduler.config.config.courses:
                course.room = [
                    new_name if r == room_name else r
                    for r in course.room
                ]

            return jsonify({"status": "modified"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500