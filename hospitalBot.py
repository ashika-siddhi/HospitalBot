import os
from google.cloud import dialogflow_v2 as dialogflow

# 1. Set path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "hospitalBot-key.json"  # use your exact filename

# 2. Dialogflow setup
PROJECT_ID = "pizzabot-nedk"  # we'll find this in a moment
SESSION_ID = "test-session"  # you can keep this as it is
LANGUAGE_CODE = "en"

# Create a session
session_client = dialogflow.SessionsClient()
session = session_client.session_path(PROJECT_ID, SESSION_ID)

print("Chat with your Dialogflow chatbot! Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    text_input = dialogflow.types.TextInput(text=user_input, language_code=LANGUAGE_CODE)
    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    print("Bot:", response.query_result.fulfillment_text)

