from flask import request, jsonify
from model.AI.agent import run_agent

def register_chat_route(app, scheduler):

    @app.route("/chat", methods=["POST"])
    def chat():
        data = request.get_json()
        message = data.get("message", "")

        result = run_agent(scheduler, message)

        # 🔥 UI actions pass through directly
        if isinstance(result, dict) and "ui_action" in result:
            return jsonify(result)

        # ✅ everything else unchanged
        return jsonify({"result": result})