import google.generativeai as genai

from config import GEMINI_API_KEY


genai.configure(
    api_key=GEMINI_API_KEY
)


model = genai.GenerativeModel(
    "gemini-2.0-flash"
)


def ask_ai(messages):

    conversation = ""

    for msg in messages:
        role = msg["role"]
        content = msg["content"]

        conversation += f"{role}: {content}\n"


    response = model.generate_content(
        conversation
    )

    return response.text