import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google.cloud import dialogflow_v2 as dialogflow
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "hospitalBot-key.json"

# --- CONFIG ---
PROJECT_ID = "pizzabot-nedk"   # use your existing project id
LANGUAGE_CODE = "en"

app = Flask(__name__, static_folder=".")
CORS(app)

# Dialogflow session client
session_client = dialogflow.SessionsClient()

@app.route("/detect_intent", methods=["POST"])
def detect_intent():
    data = request.get_json(force=True)
    user_message = data.get("message", "")
    session_id = data.get("session_id", "web-session")

    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=user_message, language_code=LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)
    fulfillment_text = response.query_result.fulfillment_text

    return jsonify({"reply": fulfillment_text})

# Serve the chatbot UI HTML
@app.route("/")
def index():
    return send_from_directory(".", "dialogflow_chatbot_ui.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
