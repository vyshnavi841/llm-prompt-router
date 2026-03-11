from dotenv import load_dotenv
load_dotenv()
from router import classify_intent, route_and_respond

def main():

    print("LLM Prompt Router")
    print("Type 'exit' to quit")

    while True:

        message = input("\nUser: ")

        if message.lower() == "exit":
            break

        intent = classify_intent(message)

        print(f"\nDetected Intent: {intent}")

        response = route_and_respond(message, intent)

        print("\nAssistant:", response)


if __name__ == "__main__":
    main()