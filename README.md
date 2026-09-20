# AI Student Assistant Chatbot

An AI-powered student assistant chatbot built using Natural Language Processing (NLP) and Machine Learning to understand user queries and provide relevant responses.

## Project Overview

The AI Student Assistant Chatbot is a machine-learning-based chatbot designed to answer questions related to Python, Artificial Intelligence, Machine Learning, Data Science, Data Analysis, and other student-oriented topics.

The application uses TF-IDF for text feature extraction and Logistic Regression for intent classification. It also provides basic context-aware conversation, user authentication, and persistent chat history using MongoDB.

## Features

### 1. Intent Recognition

The chatbot identifies the intent behind a user's message using a supervised machine learning model.

**Pipeline:**

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
