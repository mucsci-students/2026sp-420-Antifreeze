from flask import request, jsonify


def register_lab_routes(app, scheduler):
    """Registers all lab REST API routes on the Flask app.

    All handlers close over `scheduler` for access to the config and lab list.
    """

    @app.route("/labs", methods=["GET"])
    def get_labs():
        """Return a JSON array of all lab names in the current config."""
        try:
            labs = []

            for lab in scheduler.config.config.labs:
                labs.append({"name": lab})

            return jsonify(labs)

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/labs", methods=["POST"])
    def add_lab():
        """Add a new lab. Expects JSON body with key 'name'.
        Returns 409 if the lab already exists (case-insensitive check).
        """
        try:
            data = request.json
            name = data["name"]

            labs = scheduler.config.config.labs

            # Converting to upper case to add case insensitivity
            upper_case_labs = [lab.upper() for lab in labs]

            if name.upper() in upper_case_labs:
                return jsonify({"error": f'"{name}" already exists.'}), 409

            labs.append(name)

            print(f"Lab '{name}' added successfully.")

            return jsonify({"status": "added"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/labs/<lab_name>", methods=["DELETE"])
    def delete_lab(lab_name):
        """Delete the named lab and cascade removal to course lab lists.
        Returns 404 if the lab does not exist.
        """
        try:
            labs = scheduler.config.config.labs

            if lab_name not in labs:
                return jsonify(
                    {
                        "error": f'"{lab_name}" was not found. Please check the name and try again.'
                    }
                ), 404

            labs.remove(lab_name)

            # cascade removal from courses
            for course in scheduler.config.config.courses:
                course.lab = [lab for lab in course.lab if lab != lab_name]

            print(f"Lab '{lab_name}' deleted successfully.")

            return jsonify({"status": "deleted"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/labs/<lab_name>", methods=["PUT"])
    def modify_lab(lab_name):
        """Rename a lab and cascade the change to all course lab lists.
        Expects JSON body with key 'name' (new name).
        Returns 404 if the old name is not found; 409 if the new name already exists.
        """
        try:
            data = request.json
            new_name = data["name"]

            labs = scheduler.config.config.labs

            # Converting to upper case to add case insensitivity
            upper_case_labs = [lab.upper() for lab in labs]

            if lab_name.upper() not in upper_case_labs:
                return jsonify(
                    {
                        "error": f'"{lab_name}" was not found. Please check the name and try again.'
                    }
                ), 404

            if new_name.upper() in upper_case_labs:
                return jsonify(
                    {"error": f'"{new_name}" already exists. Choose a different name.'}
                ), 409

            labs[labs.index(lab_name)] = new_name

            # cascade rename in courses
            for course in scheduler.config.config.courses:
                course.lab = [
                    new_name if lab == lab_name else lab for lab in course.lab
                ]

            return jsonify({"status": "modified"})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
