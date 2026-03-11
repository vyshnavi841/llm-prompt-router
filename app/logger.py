import json

LOG_FILE = "route_log.jsonl"

def log_route(intent, confidence, user_message, final_response):

    entry = {
        "intent": intent,
        "confidence": confidence,
        "user_message": user_message,
        "final_response": final_response
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")