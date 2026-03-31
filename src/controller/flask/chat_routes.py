from flask import request, jsonify
from model.AI.agent import run_agent

def register_chat_route(app, scheduler):

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        message = data.get("message", "")

        result = run_agent(scheduler, message)

        return jsonify({"result": result})