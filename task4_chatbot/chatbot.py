import json
import os
import re

EXIT_WORDS = ["bye", "exit", "quit"]


def load_faq(filename):
    # loads intents from the json file, with error handling
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: faq.json not found")
    except json.JSONDecodeError:
        print("Error: faq.json is not valid JSON")
    return None


def clean(text):
    # lowercase, strip spaces, remove punctuation
    text = text.lower().strip()
    return re.sub(r"[^a-z0-9\s]", "", text)


def find_intents(text, faq):
    # returns every intent whose keyword appears in the text (multi-intent)
    matched = []
    for name, data in faq.items():
        for word in data["keywords"]:
            if re.search(r"\b" + re.escape(word) + r"(s|ed|ing)?\b", text):
                matched.append(name)
                break
    return matched


def chat(faq):
    state = "greeting"
    fails = 0
    topics = ", ".join(n for n in faq if n != "greeting")

    while state != "exit":
        if state == "greeting":
            print("Bot: Hi, I'm the TechMart assistant.")
            print("Bot: Ask me about", topics + ". Type 'bye' to exit.")
            state = "listening"
            continue

        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        text = clean(user)
        if not text:
            print("Bot: Please type something.")
            continue

        if set(text.split()) & set(EXIT_WORDS):
            print("Bot: Thanks for visiting TechMart. Goodbye!")
            state = "exit"
            continue

        intents = find_intents(text, faq)
        if intents:
            fails = 0
            for name in intents:
                print("Bot:", faq[name]["response"])
        else:
            fails += 1
            if fails >= 2:
                print("Bot: Sorry, I still didn't get that. I can help with:", topics)
            else:
                print("Bot: Sorry, I didn't understand. Can you rephrase?")


def main():
    faq = load_faq("faq.json")
    if faq is None:
        return
    chat(faq)


main()