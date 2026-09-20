import hashlib
import os

from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://localhost:27017/")

db = client["ai_student_chatbot"]

chat_history = db["chat_history"]

print("MongoDB connected successfully!")


def save_chat(
    username,
    user_message,
    intent,
    confidence,
    response
):

    chat_history.insert_one({
        "username": username,
        "user_message": user_message,
        "intent": intent,
        "confidence": confidence,
        "bot_response": response
    })

    print("Chat history saved to MongoDB.")

def get_chat_history(username):

    history = chat_history.find(
        {"username": username}
    ).sort("_id", 1)

    return list(history)
# ============================================================
# USER AUTHENTICATION
# ============================================================

users = db["users"]


def hash_password(password):
    """
    Convert a password into a secure hash.
    """

    salt = os.urandom(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return salt.hex(), password_hash.hex()


def verify_password(password, salt_hex, stored_hash):
    """
    Check whether the entered password matches
    the stored password hash.
    """

    salt = bytes.fromhex(salt_hex)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        100000
    )

    return password_hash.hex() == stored_hash


def register_user(username, password):
    """
    Register a new user.
    """

    existing_user = users.find_one(
        {"username": username}
    )

    if existing_user:
        return False, "Username already exists."

    salt, password_hash = hash_password(password)

    users.insert_one(
        {
            "username": username,
            "password_hash": password_hash,
            "salt": salt
        }
    )

    return True, "Registration successful."


def authenticate_user(username, password):
    """
    Authenticate an existing user.
    """

    user = users.find_one(
        {"username": username}
    )

    if not user:
        return False

    return verify_password(
        password,
        user["salt"],
        user["password_hash"]
    )