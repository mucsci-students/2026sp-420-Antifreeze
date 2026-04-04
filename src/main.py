from flask import Flask
from controller.flask.routes import register_routes
from model.schedule import schedule

app = Flask(__name__, template_folder="view/templates", static_folder="view/static")

scheduler = schedule.Schedule()

register_routes(app, scheduler)

if __name__ == "__main__":
    app.run(debug=True)
