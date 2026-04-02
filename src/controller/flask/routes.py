from flask import render_template, send_from_directory
from .schedule_routes import register_schedule_routes
from .faculty_routes import register_faculty_routes
from .course_routes import register_course_routes
from .lab_routes import register_lab_routes
from .room_routes import register_room_routes
from .chat_routes import register_chat_route
from .time_slot_routes import register_time_slot_routes


# Registers all application routes on the Flask app.
# Mounts the index page, the controller JS static path, and all REST API
# route groups (schedule, faculty, course, lab, room, chat).
# Parameters: app - Flask application instance, scheduler - shared Schedule object
def register_routes(app, scheduler):

    # Serves the main single-page application HTML template.
    @app.route("/")
    def index():
        return render_template("index.html")

    # Serves controller JS files from the controller directory.
    # Required because Flask's default static folder is view/static.
    # Parameters: filename - relative path within the controller directory
    @app.route("/controller/<path:filename>")
    def custom_static(filename):
        return send_from_directory("controller/", filename)

    register_schedule_routes(app, scheduler)
    register_faculty_routes(app, scheduler)
    register_course_routes(app, scheduler)
    register_lab_routes(app, scheduler)
    register_room_routes(app, scheduler)
    register_chat_route(app, scheduler)
    register_time_slot_routes(app, scheduler)