from flask import request, jsonify
import os


def register_schedule_routes(app, scheduler):

    @app.route("/load_config", methods=["POST"])
    def load_config():
        file = request.files["file"]

        os.makedirs("uploads", exist_ok=True)

        path = os.path.join("uploads", file.filename)
        file.save(path)

        scheduler.load_config(path)

        return jsonify({"status": "loaded"})