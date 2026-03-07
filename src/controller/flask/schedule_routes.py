from flask import request, jsonify, send_file
import os
import json
import io

def register_schedule_routes(app, scheduler):

    @app.route("/load_config", methods=["POST"])
    def load_config():
        file = request.files["file"]

        os.makedirs("uploads", exist_ok=True)

        path = os.path.join("uploads", file.filename)
        file.save(path)

        scheduler.load_config(path)

        return jsonify({"status": "loaded"})
    
    @app.route("/save_config")
    def save_config():
        file_data = scheduler.config.model_dump_json(indent=2)

        return send_file(
            io.BytesIO(file_data.encode()),
            mimetype="application/json",
            as_attachment=True,
            download_name="schedule_config.json"
        )
        
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