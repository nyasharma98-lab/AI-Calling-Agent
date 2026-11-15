import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("Gemini API key not found in .env file")

client = genai.Client(api_key=API_KEY)

conversation_history = []


def get_gemini_response(user_text):

    try:
        conversation_history.append({
            "role": "user",
            "parts": [{"text": user_text}]
        })

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=conversation_history,
            config=types.GenerateContentConfig(
                system_instruction=(
                    "You are a helpful AI Calling Agent. "
                    "Remember the conversation and use previous "
                    "messages when answering. "
                    "Keep answers short and natural for spoken conversation."
                ),
                temperature=0.7,
                max_output_tokens=200
            )
        )

        if response.text:
            answer = response.text.strip()

            conversation_history.append({
                "role": "model",
                "parts": [{"text": answer}]
            })

            return answer

        return "Sorry, I could not generate a response."

    except Exception as e:
        print("Gemini API error:", e)
        return "Sorry, I am having trouble generating a response."