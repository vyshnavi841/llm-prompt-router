import os
from google import genai
from prompts import PROMPTS
from logger import log_route

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def classify_intent(message: str):

    try:
        message_lower = message.lower()

        # 🔹 Local fallback (for demo safety)
        if "python" in message_lower or "code" in message_lower or "bug" in message_lower:
            return {"intent": "code", "confidence": 0.95}

        if "writing" in message_lower or "sentence" in message_lower or "verbose" in message_lower:
            return {"intent": "writing", "confidence": 0.95}

        if "career" in message_lower or "job" in message_lower:
            return {"intent": "career", "confidence": 0.95}

        if "data" in message_lower or "average" in message_lower:
            return {"intent": "data", "confidence": 0.95}

        # 🔹 Try Gemini (optional)
        prompt = f"""
Classify intent: code, data, writing, career, unclear.

Message: {message}

Return only one word.
"""

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        intent = response.text.strip().lower()

        if intent not in ["code", "data", "writing", "career"]:
            intent = "unclear"

        return {"intent": intent, "confidence": 0.9}

    except Exception as e:
        print("Classifier Error:", e)
        return {"intent": "unclear", "confidence": 0.0}


def route_and_respond(message: str, intent_data: dict):

    intent = intent_data["intent"]
    confidence = intent_data["confidence"]

    if intent == "unclear":
        response = (
            "Could you clarify your request? "
            "Are you asking about coding, data analysis, writing feedback, or career advice?"
        )
        log_route(intent, confidence, message, response)
        return response

    system_prompt = PROMPTS.get(intent)
    prompt = system_prompt + "\n\nUser:\n" + message

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        final_response = response.text

    except Exception as e:
        print("LLM Error:", e)

        # 🔹 fallback responses
        if intent == "code":
            final_response = "You can sort a list in Python using sorted() or list.sort()."

        elif intent == "writing":
            final_response = "Try reducing sentence length and removing unnecessary words."

        elif intent == "career":
            final_response = "Can you share your skills and interests so I can guide you better?"

        elif intent == "data":
            final_response = "Average = sum of values / number of values."

        else:
            final_response = "I'm not sure how to help."

    log_route(intent, confidence, message, final_response)

    return final_response
