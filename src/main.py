# Entry point for the Scheduler Flask application.
# Creates the Flask app, instantiates the shared Schedule object, registers all
# REST API and static routes, then starts the development server when run directly.

from flask import Flask
from controller.flask.routes import register_routes
from model.schedule import schedule

app = Flask(__name__, template_folder="view/templates", static_folder="view/static")

scheduler = schedule.Schedule()

register_routes(app, scheduler)

if __name__ == "__main__":
    app.run(debug=True)
