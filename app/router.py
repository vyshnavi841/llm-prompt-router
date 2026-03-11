import json
import os
import google.generativeai as genai
from prompts import PROMPTS
from logger import log_route

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


CLASSIFIER_PROMPT = """
Your task is to classify the user's intent.

Choose ONE label from:
code, data, writing, career, unclear

Return ONLY JSON:

{
 "intent": "label",
 "confidence": 0.0
}
"""


def classify_intent(message: str):

    try:
        prompt = CLASSIFIER_PROMPT + "\nUser message:\n" + message

        response = model.generate_content(prompt)

        raw = response.text.strip()

        parsed = json.loads(raw)

        intent = parsed.get("intent", "unclear")
        confidence = float(parsed.get("confidence", 0))

        return {
            "intent": intent,
            "confidence": confidence
        }

    except Exception:
        return {
            "intent": "unclear",
            "confidence": 0.0
        }


def route_and_respond(message: str, intent_data: dict):

    intent = intent_data["intent"]
    confidence = intent_data["confidence"]

    if intent == "unclear":

        response = (
            "Could you clarify your request? "
            "Are you asking about coding, data analysis, writing feedback, "
            "or career advice?"
        )

        log_route(intent, confidence, message, response)

        return response

    system_prompt = PROMPTS.get(intent)

    prompt = system_prompt + "\n\nUser:\n" + message

    response = model.generate_content(prompt)

    final_response = response.text

    log_route(intent, confidence, message, final_response)

    return final_response