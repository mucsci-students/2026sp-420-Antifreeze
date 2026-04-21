from flask import request, jsonify
from model.AI.agent import run_agent
from faster_whisper import WhisperModel
import tempfile
import os

model = WhisperModel("tiny", device="cpu", compute_type="int8")

# Registers the AI chat REST API route on the Flask app.
# Parameters: app - Flask application instance, scheduler - shared Schedule object
def register_chat_route(app, scheduler):

    # Accepts a plain-text message from the user and passes it to the AI agent.
    # The agent has access to all scheduler tools and returns a natural-language reply.
    # Expects JSON body with key "message" (str).
    # Returns JSON with key "result" (str) containing the agent's response.
    @app.route("/chat", methods=["POST"])
    def chat():
        try:
            data = request.get_json()
            message = data.get("message", "")

            result = run_agent(scheduler, message)

            return jsonify({"result": result})
        except Exception as e:
            return jsonify({"result": f"Error: {str(e)}"}), 500
        
        
    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        try:
            audio = request.files["audio"]

            # save temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
                audio.save(tmp.name)
                tmp_path = tmp.name

            segments, info = model.transcribe(tmp_path)

            text = " ".join([seg.text for seg in segments]).strip()

            os.remove(tmp_path)

            return jsonify({"text": text})

        except Exception as e:
            return jsonify({"error": str(e)}), 500
