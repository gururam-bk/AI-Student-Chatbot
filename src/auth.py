import bcrypt
from pymongo import MongoClient


# ============================================================
# MONGODB CONNECTION
# ============================================================

client = MongoClient("mongodb://localhost:27017/")

db = client["ai_student_chatbot"]

users_collection = db["users"]


# ============================================================
# REGISTER USER
# ============================================================

def register_user(username, password):

    # Check whether username already exists
    existing_user = users_collection.find_one(
        {"username": username}
    )

    if existing_user:
        return False, "Username already exists."

    # Convert password into bytes
    password_bytes = password.encode("utf-8")

    # Generate secure password hash
    hashed_password = bcrypt.hashpw(
        password_bytes,
        bcrypt.gensalt()
    )

    # Store user
    users_collection.insert_one({
        "username": username,
        "password": hashed_password
    })

    return True, "Registration successful."


# ============================================================
# LOGIN USER
# ============================================================

def login_user(username, password):

    # Find user by username
    user = users_collection.find_one(
        {"username": username}
    )

    # User does not exist
    if not user:
        return False

    # Convert entered password into bytes
    password_bytes = password.encode("utf-8")


    # --------------------------------------------------------
    # Get stored password hash safely
    # --------------------------------------------------------

    stored_password = user.get("password")


    # If old database record does not contain password
    if stored_password is None:

        return False


    # --------------------------------------------------------
    # Convert MongoDB Binary value to bytes if necessary
    # --------------------------------------------------------

    stored_password = bytes(stored_password)


    # --------------------------------------------------------
    # Compare entered password with stored hash
    # --------------------------------------------------------

    if bcrypt.checkpw(
        password_bytes,
        stored_password
    ):

        return True


    return False