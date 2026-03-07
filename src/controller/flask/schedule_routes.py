from flask import request, jsonify, send_file
import os
import json
import io


# Registers all schedule-level REST API routes on the Flask app.
# Covers config loading/saving, scheduler execution, result retrieval, and PDF export.
def register_schedule_routes(app, scheduler):

    # Accepts a uploaded JSON config file, saves it to /uploads, and loads it into the scheduler.
    # Expects a multipart file upload with key "file".
    @app.route("/load_config", methods=["POST"])
    def load_config():
        file = request.files["file"]

        os.makedirs("uploads", exist_ok=True)

        path = os.path.join("uploads", file.filename)
        file.save(path)

        scheduler.load_config(path)

        return jsonify({"status": "loaded"})

    # Serializes the current scheduler config to JSON and returns it as a downloadable file.
    @app.route("/save_config")
    def save_config():
        file_data = scheduler.config.model_dump_json(indent=2)

        return send_file(
            io.BytesIO(file_data.encode()),
            mimetype="application/json",
            as_attachment=True,
            download_name="schedule_config.json"
        )

    # Runs the scheduler with the given parameters.
    # Expects limit (int) and optimize (bool) in the JSON body.
    # Returns the count of generated schedules.
    @app.route("/run_scheduler", methods=["POST"])
    def run_scheduler_route():
        try:
            data = request.json

            limit = int(data["limit"])
            optimize = bool(data["optimize"])

            results = scheduler.run_scheduler(limit, optimize)

            return jsonify({
                "count": len(results)
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Returns a single generated schedule by index as a list of CSV row strings.
    # Returns 400 if no schedules exist, 400 if index is out of range.
    # Parameters: index - zero-based position in the results list
    @app.route("/schedule/<int:index>", methods=["GET"])
    def get_schedule(index):
        try:

            if not scheduler.result:
                return jsonify({"error": "No schedules generated"}), 400

            if index >= len(scheduler.result):
                return jsonify({"error": "Schedule index out of range"}), 400

            model = scheduler.result[index]

            rows = []

            for sch in model:
                rows.append(sch.as_csv())

            return jsonify({
                "schedule": rows
            })

        except Exception as e:
            return jsonify({"error": str(e)}), 500

    from flask import send_file

    # Exports all generated schedules as a PDF and returns it as a downloadable file.
    # Returns 400 if no schedules have been generated yet.
    @app.route("/print_schedules", methods=["GET"])
    def print_schedules():

        pdf = scheduler.export_schedules_pdf()

        if not pdf:
            return jsonify({"error": "No schedules generated"}), 400

        return send_file(
            pdf,
            mimetype="application/pdf",
            as_attachment=True,
            download_name="schedules.pdf"
        )