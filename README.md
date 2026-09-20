# AI Student Assistant Chatbot

An AI-powered student assistant chatbot built using **Natural Language Processing (NLP)** and **Machine Learning** to understand user queries, identify their intent, and provide relevant responses.

The project demonstrates an end-to-end NLP application using **TF-IDF, Logistic Regression, Streamlit, MongoDB, and bcrypt-based authentication**.

---

## Project Overview

The **AI Student Assistant Chatbot** is designed to answer student-oriented queries related to topics such as:

- Python
- Artificial Intelligence
- Machine Learning
- Data Science
- Data Analysis
- General student-related questions

The chatbot uses a supervised Machine Learning approach for **intent recognition**.

User messages are converted into numerical features using **TF-IDF**, and **Logistic Regression** is used to classify the message into a predefined intent.

The application also provides:

- Basic context-aware conversation
- User registration and login
- Password protection using bcrypt
- Persistent chat history using MongoDB
- Interactive web interface using Streamlit

---

## Key Features

### 1. Intent Recognition

The chatbot identifies the intent behind a user's message using a supervised Machine Learning model.

The overall processing flow is:

```text
User Message
      ↓
Text Processing
      ↓
TF-IDF Vectorization
      ↓
Logistic Regression
      ↓
Intent Prediction
      ↓
Response Selection
      ↓
Bot Response
```

The intent patterns and responses are stored in:

```text
data/intents.json
```

---

### 2. TF-IDF Feature Extraction

TF-IDF (Term Frequency-Inverse Document Frequency) is used to convert text into numerical feature vectors.

The implementation uses:

- **Unigrams** — individual words
- **Bigrams** — two-word combinations

Example configuration:

```python
TfidfVectorizer(ngram_range=(1, 2))
```

This allows the model to consider both individual terms and short word combinations when identifying an intent.

---

### 3. Logistic Regression Classification

**Logistic Regression** is used as the Machine Learning classifier for intent recognition.

The model learns the relationship between:

```text
User Text
    ↓
TF-IDF Features
    ↓
Intent Label
```

For a new user message, the trained classifier predicts the most likely intent and provides a confidence probability.

---

### 4. Basic Context-Aware Conversation

The chatbot maintains the previously detected intent during the current conversation to handle simple follow-up questions.

Example:

```text
User:
What is Python?

Bot:
Python is a high-level, general-purpose programming language
known for readable syntax and a large ecosystem of libraries.

User:
Who created it?

Bot:
Guido van Rossum is the creator of Python and served as its
original lead developer.
```

The current implementation provides **basic intent-based conversational context** and is not an LLM-based memory system.

---

### 5. User Authentication

The application provides user registration and login functionality.

Passwords are protected using **bcrypt hashing** instead of storing plain-text passwords.

Authentication allows users to access the chatbot and their stored chat history.

---

### 6. Persistent Chat History

MongoDB is used to store chatbot interactions.

Each interaction contains information such as:

```text
Username
User Message
Predicted Intent
Confidence
Bot Response
```

Users can access their previous chatbot interactions through the **Chat History** section.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Scikit-learn | Machine Learning and NLP |
| TF-IDF | Text feature extraction |
| Logistic Regression | Intent classification |
| Streamlit | Web application interface |
| MongoDB | Persistent chat history |
| PyMongo | MongoDB integration |
| bcrypt | Password hashing |
| JSON | Intent dataset |

---

## Project Architecture

```text
                    User Message
                         ↓
                  Text Processing
                         ↓
                  TF-IDF Vectorizer
                         ↓
                 Logistic Regression
                         ↓
                  Intent Prediction
                         ↓
                  Response Selection
                         ↓
                  Chatbot Response
                         ↓
                       MongoDB
                    Chat History
```

---

## Project Structure

```text
AI-Student-Chatbot/
│
├── data/
│   └── intents.json
│
├── src/
│   ├── auth.py
│   ├── chatbot.py
│   ├── database.py
│   ├── intent_engine.py
│   ├── processing.py
│   ├── main.py
│   └── test_database.py
│
├── app.py
├── train_model.py
├── train_2.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## NLP and Machine Learning Workflow

### Step 1: Intent Dataset

The chatbot uses predefined intent patterns and responses stored in:

```text
data/intents.json
```

Multiple example patterns are provided for each intent.

### Step 2: Text Feature Extraction

User text is converted into numerical features using TF-IDF.

```text
Text
 ↓
TF-IDF
 ↓
Numerical Feature Vector
```

### Step 3: Model Training

The intent classifier is trained using Logistic Regression.

```text
Training Patterns
       ↓
TF-IDF
       ↓
Logistic Regression
       ↓
Trained Classifier
```

### Step 4: Intent Prediction

When a new message is received:

```text
New User Message
       ↓
TF-IDF Transformation
       ↓
Model Prediction
       ↓
Predicted Intent
       ↓
Response Selection
```

### Step 5: Response Selection

An appropriate response associated with the predicted intent is selected and displayed to the user.

---

## Model Evaluation

The project includes a model training and evaluation script:

```text
train_model.py
```

The evaluation workflow includes:

- Train/test split
- TF-IDF feature extraction
- Logistic Regression
- Intent prediction
- Classification report

The classification report provides:

- Precision
- Recall
- F1-score
- Support

---

## Authentication Flow

```text
User
  ↓
Login / Register
  ↓
bcrypt Password Verification
  ↓
Authenticated User
  ↓
AI Student Assistant
```

---

## Database

MongoDB is used to persist chatbot interactions.

Chat history contains:

```text
username
user_message
intent
confidence
bot_response
```

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/gururam-bk/AI-Student-Chatbot.git
```

### 2. Navigate to the Project

```bash
cd AI-Student-Chatbot
```

### 3. Create a Virtual Environment

```bash
python -m venv .venv
```

### 4. Activate the Virtual Environment

For Windows:

```bash
.venv\Scripts\activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## MongoDB Configuration

The application requires a MongoDB connection for persistent data storage.

Configure the MongoDB connection according to your environment before running the application.

**Do not commit MongoDB credentials, passwords, API keys, or other sensitive information to GitHub.**

---

## Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will open in your web browser.

### Application Flow

```text
Register
   ↓
Login
   ↓
Ask a Question
   ↓
Intent Recognition
   ↓
Generate Response
   ↓
Save Chat History
```

---

## Example Conversation

```text
User:
What is Python?

Bot:
Python is a high-level, general-purpose programming language
known for readable syntax and a large ecosystem of libraries.

User:
Who created it?

Bot:
Guido van Rossum is the creator of Python and served as its
original lead developer.
```

---

## Learning Outcomes

This project provided practical experience with:

- Natural Language Processing
- Text classification
- TF-IDF
- Logistic Regression
- Intent recognition
- Machine Learning model evaluation
- Prediction confidence
- Basic conversational context
- Streamlit application development
- MongoDB integration
- User authentication
- Password hashing with bcrypt
- Building an end-to-end AI application

---

## Future Improvements

Potential future improvements include:

- Semantic embeddings
- Vector database integration
- Retrieval-Augmented Generation (RAG)
- Large Language Model integration
- Improved conversational memory
- More advanced intent detection
- Larger and more diverse training data
- Cloud deployment
- Improved conversation/session management

These are **future extensions** and are not part of the current implementation.

---

## Project Purpose

This project was developed as a practical implementation of NLP and Machine Learning concepts, with the goal of understanding how a traditional ML-based chatbot can be developed and integrated into a complete application.

---

## GitHub Repository

https://github.com/gururam-bk/AI-Student-Chatbot

---

## Author

**Guru Ram**

B.E. Computer Science and Engineering

### Interests

- Artificial Intelligence
- Machine Learning
- Natural Language Processing
- AI Engineering

---

## License

This project is intended for educational and learning purposes.
