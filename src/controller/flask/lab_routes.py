from flask import request, jsonify


def register_lab_routes(app, scheduler):

    @app.route("/labs", methods=["GET"])
    def get_labs():
        try:
            labs = []

            for lab in scheduler.config.config.labs:
                labs.append({
                    "name": lab
                })

            return jsonify(labs)

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route("/labs", methods=["POST"])
    def add_lab():
        try:
            data = request.json
            name = data["name"]

            labs = scheduler.config.config.labs

            if name in labs:
                print("Lab already exists.")
                return jsonify({"status": "exists"})

            labs.append(name)

            print(f"Lab '{name}' added successfully.")

            return jsonify({"status": "added"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route("/labs/<lab_name>", methods=["DELETE"])
    def delete_lab(lab_name):
        try:
            labs = scheduler.config.config.labs

            if lab_name not in labs:
                print("Lab not found.")
                return jsonify({"status": "not_found"})

            labs.remove(lab_name)

            # cascade removal from courses
            for course in scheduler.config.config.courses:
                course.lab = [
                    l for l in course.lab
                    if l != lab_name
                ]

            print(f"Lab '{lab_name}' deleted successfully.")

            return jsonify({"status": "deleted"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    @app.route("/labs/<lab_name>", methods=["PUT"])
    def modify_lab(lab_name):
        try:
            data = request.json
            new_name = data["name"]

            labs = scheduler.config.config.labs

            if lab_name not in labs:
                return jsonify({"error": "Lab not found"}), 404

            labs[labs.index(lab_name)] = new_name

            # cascade rename in courses
            for course in scheduler.config.config.courses:
                course.lab = [
                    new_name if l == lab_name else l
                    for l in course.lab
                ]

            return jsonify({"status": "modified"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500