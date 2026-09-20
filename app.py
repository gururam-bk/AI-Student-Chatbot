import json
import random

import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from src.auth import register_user, login_user
from src.database import save_chat, get_chat_history


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Student Assistant",
    page_icon="AI",
    layout="centered"
)


# ============================================================
# LOAD DATASET
# ============================================================

with open(
    "data/intents.json",
    "r",
    encoding="utf-8"
) as file:

    data = json.load(file)


# ============================================================
# PREPARE TRAINING DATA
# ============================================================

texts = []
labels = []

for intent in data["intents"]:

    for pattern in intent["patterns"]:

        texts.append(pattern)
        labels.append(intent["tag"])


# ============================================================
# TF-IDF
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(texts)


# ============================================================
# TRAIN INTENT CLASSIFICATION MODEL
# ============================================================

model = LogisticRegression(
    max_iter=1000
)

model.fit(X, labels)


# ============================================================
# RESPONSE LOOKUP
# ============================================================

responses_by_intent = {}

for intent in data["intents"]:

    responses_by_intent[intent["tag"]] = intent["responses"]


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "username" not in st.session_state:

    st.session_state.username = None


if "messages" not in st.session_state:

    st.session_state.messages = []


if "selected_chat" not in st.session_state:

    st.session_state.selected_chat = None


if "last_intent" not in st.session_state:

    st.session_state.last_intent = None


# ============================================================
# LOGIN / REGISTER PAGE
# ============================================================

if not st.session_state.logged_in:

    st.title("AI Student Assistant")

    st.subheader("User Authentication")

    tab1, tab2 = st.tabs(
        [
            "Login",
            "Register"
        ]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with tab1:

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )


        if st.button(
            "Login",
            key="login_button"
        ):

            if not username or not password:

                st.warning(
                    "Please enter username and password."
                )

            elif login_user(
                username,
                password
            ):

                st.session_state.logged_in = True

                st.session_state.username = username

                st.session_state.messages = []

                st.session_state.selected_chat = None

                st.session_state.last_intent = None

                st.success(
                    "Login successful!"
                )

                st.rerun()

            else:

                st.error(
                    "Invalid username or password."
                )


    # ========================================================
    # REGISTER
    # ========================================================

    with tab2:

        new_username = st.text_input(
            "Create username",
            key="register_username"
        )

        new_password = st.text_input(
            "Create password",
            type="password",
            key="register_password"
        )

        confirm_password = st.text_input(
            "Confirm password",
            type="password",
            key="confirm_password"
        )


        if st.button(
            "Register",
            key="register_button"
        ):

            if not new_username or not new_password:

                st.warning(
                    "Please fill all fields."
                )

            elif new_password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            else:

                success, message = register_user(
                    new_username,
                    new_password
                )

                if success:

                    st.success(message)

                else:

                    st.error(message)


    st.stop()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("Chat History")


    # ========================================================
    # NEW CHAT
    # ========================================================

    if st.button(
        "＋ New Chat",
        key="new_chat_button",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.session_state.selected_chat = None

        st.session_state.last_intent = None

        st.rerun()


    st.divider()


    # ========================================================
    # LOAD USER CHAT HISTORY
    # ========================================================

    history = get_chat_history(
        st.session_state.username
    )


    if not history:

        st.caption(
            "No previous conversations."
        )

    else:

        st.subheader(
            "Previous Chats"
        )


        for index, chat in enumerate(
            reversed(history)
        ):

            previous_message = chat.get(
                "user_message",
                "Previous chat"
            )


            title = previous_message[:30]


            if len(previous_message) > 30:

                title += "..."


            if st.button(
                title,
                key=f"history_{index}",
                use_container_width=True
            ):

                st.session_state.selected_chat = chat

                st.session_state.messages = [

                    {
                        "role": "user",
                        "content": chat.get(
                            "user_message",
                            ""
                        )
                    },

                    {
                        "role": "assistant",
                        "content": chat.get(
                            "bot_response",
                            chat.get(
                                "response",
                                ""
                            )
                        )
                    }

                ]

                st.rerun()


    st.divider()


    # ========================================================
    # USER INFORMATION
    # ========================================================

    st.caption(
        f"Logged in as: {st.session_state.username}"
    )


    # ========================================================
    # LOGOUT
    # ========================================================

    if st.button(
        "Logout",
        key="sidebar_logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.username = None

        st.session_state.messages = []

        st.session_state.selected_chat = None

        st.session_state.last_intent = None

        st.rerun()


# ============================================================
# CHATBOT HEADER
# ============================================================

st.title("AI Student Assistant")

st.write(
    f"Welcome, **{st.session_state.username}**."
)

st.write(
    "Ask me about Python, AI, ML, Data Science and more."
)


# ============================================================
# DISPLAY CURRENT CHAT
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.write(
            message["content"]
        )


# ============================================================
# USER INPUT
# ============================================================

user_message = st.chat_input(
    "Type your message..."
)


if user_message:

    # ========================================================
    # DISPLAY USER MESSAGE
    # ========================================================

    with st.chat_message("user"):

        st.write(user_message)


    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )


    # ========================================================
    # CONVERT USER MESSAGE TO TF-IDF
    # ========================================================

    user_tfidf = vectorizer.transform(
        [user_message]
    )


    # ========================================================
    # INTENT PREDICTION
    # ========================================================

    prediction = model.predict(
        user_tfidf
    )

    predicted_intent = prediction[0]


    # ========================================================
    # CONFIDENCE
    # ========================================================

    probabilities = model.predict_proba(
        user_tfidf
    )

    confidence = probabilities.max()


    # ========================================================
    # SIMPLE CONTEXT AWARENESS
    # ========================================================

    follow_up_words = [
        "why",
        "how",
        "explain more",
        "tell me more",
        "more",
        "what about it",
        "can you explain"
    ]


    user_lower = user_message.lower().strip()


    is_follow_up = any(
        phrase in user_lower
        for phrase in follow_up_words
    )


    if (
        is_follow_up
        and st.session_state.last_intent is not None
    ):

        predicted_intent = (
            st.session_state.last_intent
        )


    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    confidence_threshold = 0.30


    if confidence < confidence_threshold:

        bot_response = (
            "I'm not sure I understand that yet. "
            "Please try asking in a different way."
        )

    else:

        responses = responses_by_intent.get(
            predicted_intent,
            []
        )


        if responses:

            bot_response = random.choice(
                responses
            )

        else:

            bot_response = (
                "I understood your question, "
                "but I don't have a response "
                "for it yet."
            )


    # ========================================================
    # UPDATE CONTEXT
    # ========================================================

    st.session_state.last_intent = predicted_intent


    # ========================================================
    # DISPLAY BOT RESPONSE
    # ========================================================

    with st.chat_message("assistant"):

        st.write(bot_response)


    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": bot_response
        }
    )


    # ========================================================
    # SAVE CHAT TO MONGODB
    # ========================================================

    save_chat(
        st.session_state.username,
        user_message,
        predicted_intent,
        confidence,
        bot_response
    )


    # ========================================================
    # REFRESH UI
    # ========================================================

    st.rerun()