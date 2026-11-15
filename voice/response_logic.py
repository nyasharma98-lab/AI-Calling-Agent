def get_agent_response(user_text):

    text = user_text.lower().strip()

    if "hello" in text or "hi" in text:
        return "Hello! How can I help you today?"

    elif "how are you" in text:
        return "I'm doing great! Thanks for asking. How can I help you?"

    elif "your name" in text or "who are you" in text:
        return "I am your AI Calling Agent. How can I assist you?"

    elif "thank you" in text or "thanks" in text:
        return "You're welcome! Happy to help."

    elif "bye" in text or "goodbye" in text:
        return "Goodbye! Have a great day."

    elif "help" in text:
        return "Of course! Please tell me what you need help with."

    else:
        return "I understand. Could you please tell me a little more?"