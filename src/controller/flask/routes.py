from flask import render_template, send_from_directory
from .schedule_routes import register_schedule_routes
from .faculty_routes import register_faculty_routes

def register_routes(app, scheduler):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/controller/<path:filename>")
    def custom_static(filename):
        return send_from_directory("controller/", filename)

    register_schedule_routes(app, scheduler)
    register_faculty_routes(app, scheduler)