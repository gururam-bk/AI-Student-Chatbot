import json
import re
import random
from src.database import save_chat
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. CONVERSATION MEMORY
# ============================================================

last_intent = None
last_topic = None


# Map intents to their conversation topics
topic_map = {
    "python_information": "Python",
    "python_creator": "Python",
    "python_uses": "Python",

    "ai_information": "Artificial Intelligence",

    "ml_information": "Machine Learning",

    "data_science": "Data Science",
    "data_analysis": "Data Analysis"
}


# ============================================================
# 2. LOAD DATASET
# ============================================================

with open("data/intents.json", "r", encoding="utf-8") as file:
    data = json.load(file)


# ============================================================
# 3. EXTRACT PATTERNS AND INTENT LABELS
# ============================================================

texts = []
labels = []

for i, intent in enumerate(data["intents"]):

    # Validate dataset structure
    if "tag" not in intent:
        raise ValueError(
            f"Intent {i} is missing the 'tag' field."
        )

    if "patterns" not in intent:
        raise ValueError(
            f"Intent {i} ({intent['tag']}) is missing the 'patterns' field."
        )

    if "responses" not in intent:
        raise ValueError(
            f"Intent {i} ({intent['tag']}) is missing the 'responses' field."
        )

    # Add every training sentence
    for pattern in intent["patterns"]:

        # Ignore empty patterns
        if not pattern.strip():
            continue

        texts.append(pattern)
        labels.append(intent["tag"])


print("Total training examples:", len(texts))
print("Total intents:", len(set(labels)))


# ============================================================
# 4. CREATE RESPONSE LOOKUP
# ============================================================

responses_by_intent = {}

for intent in data["intents"]:
    responses_by_intent[intent["tag"]] = intent["responses"]


# ============================================================
# 5. SPLIT DATA INTO TRAINING AND TESTING
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    texts,
    labels,
    test_size=0.20,
    random_state=42,
    stratify=labels
)


print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))


# ============================================================
# 6. CONVERT TEXT INTO TF-IDF FEATURES
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)


# Learn vocabulary + calculate TF-IDF for training data
X_train_tfidf = vectorizer.fit_transform(X_train)


# Convert testing data using the SAME vocabulary
X_test_tfidf = vectorizer.transform(X_test)


print("TF-IDF features:", X_train_tfidf.shape[1])


# ============================================================
# 7. CREATE MACHINE LEARNING MODEL
# ============================================================

model = LogisticRegression(
    max_iter=1000
)


# ============================================================
# 8. TRAIN THE MODEL
# ============================================================

model.fit(X_train_tfidf, y_train)

print("\nModel training completed.")


# ============================================================
# 9. EVALUATE THE MODEL
# ============================================================

y_pred = model.predict(X_test_tfidf)

accuracy = accuracy_score(y_test, y_pred)

print("\n==============================")
print("MODEL EVALUATION")
print("==============================")

print("Accuracy:", accuracy)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred,
        zero_division=0
    )
)


# ============================================================
# 10. TEST WITH A NEW SENTENCE
# ============================================================

test_message = "What is Python?"

test_message_tfidf = vectorizer.transform(
    [test_message]
)

test_prediction = model.predict(
    test_message_tfidf
)

test_probabilities = model.predict_proba(
    test_message_tfidf
)

test_confidence = test_probabilities.max()

print("\n==============================")
print("TEST PREDICTION")
print("==============================")

print("User:", test_message)
print("Predicted Intent:", test_prediction[0])
print("Confidence:", test_confidence)


# ============================================================
# 11. START CHATBOT
# ============================================================

print("\n==============================")
print("AI STUDENT ASSISTANT")
print("==============================")

print("Type 'quit' to exit.\n")


while True:

    # --------------------------------------------------------
    # Get user input
    # --------------------------------------------------------

    user_message = input("You: ").strip()


    # --------------------------------------------------------
    # Ignore empty messages
    # --------------------------------------------------------

    if not user_message:
        print("Chatbot: Please enter a message.")
        continue


    # --------------------------------------------------------
    # Exit chatbot
    # --------------------------------------------------------

    if user_message.lower() == "quit":
        print("Chatbot: Goodbye!")
        break


    # --------------------------------------------------------
    # Detect follow-up question
    # --------------------------------------------------------

    user_message_lower = user_message.lower()

    follow_up_words = [
        "it",
        "this",
        "that",
        "its"
    ]

    words = re.findall(
        r"\b\w+\b",
        user_message_lower
    )

    is_follow_up = any(
        word in words
        for word in follow_up_words
    )


    print("Is follow-up:", is_follow_up)


    # --------------------------------------------------------
    # Add previous topic for context
    # --------------------------------------------------------

    message_for_model = user_message

    if is_follow_up and last_topic is not None:

        message_for_model = (
            user_message
            + " "
            + last_topic
        )


    print(
        "Message sent to model:",
        message_for_model
    )


    # --------------------------------------------------------
    # Convert user message to TF-IDF
    # --------------------------------------------------------

    user_message_tfidf = vectorizer.transform(
        [message_for_model]
    )


    # --------------------------------------------------------
    # Predict intent
    # --------------------------------------------------------

    prediction = model.predict(
        user_message_tfidf
    )

    predicted_intent = prediction[0]


    # --------------------------------------------------------
    # Calculate confidence
    # --------------------------------------------------------

    probabilities = model.predict_proba(
        user_message_tfidf
    )

    confidence = probabilities.max()


    print(
        "Predicted Intent:",
        predicted_intent
    )

    print(
        "Confidence:",
        round(confidence, 4)
    )


    # --------------------------------------------------------
    # Confidence threshold
    # --------------------------------------------------------

    confidence_threshold = 0.3


    if confidence < confidence_threshold:

        print(
            "Chatbot: I'm not sure I understand "
            "that yet."
        )

        continue


    # --------------------------------------------------------
    # Remember the detected intent
    # --------------------------------------------------------

    last_intent = predicted_intent


    # --------------------------------------------------------
    # Remember the conversation topic
    # --------------------------------------------------------

    if predicted_intent in topic_map:

        last_topic = topic_map[
            predicted_intent
        ]


    # --------------------------------------------------------
    # Select an appropriate response
    # --------------------------------------------------------

    responses = responses_by_intent.get(
        predicted_intent,
        []
    )


    if responses:

        response = random.choice(
            responses
        )

        print(
            "Chatbot:",
            response
        )

        # ----------------------------------------------------
        # SAVE CHAT TO MONGODB
        # ----------------------------------------------------

        save_chat(
            user_message,
            predicted_intent,
            response
        )

        print("Chat history saved to MongoDB.")

    else:

        response = (
            "I understood your question, "
            "but I don't have a response for it yet."
        )

        print(
            "Chatbot:",
            response
        )

        # Save even when a fallback response is used
        save_chat(
            user_message,
            predicted_intent,
            response
        )

        print("Chat history saved to MongoDB.")