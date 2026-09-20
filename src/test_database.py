from src.database import get_chat_history

history = get_chat_history()

print("\n==============================")
print("CHAT HISTORY")
print("==============================")

for chat in history:

    print("User:", chat.get("user_message"))
    print("Intent:", chat.get("intent", chat.get("predicted_intent")))
    print("Bot:", chat.get("bot_response", chat.get("response")))

    print("------------------------------")