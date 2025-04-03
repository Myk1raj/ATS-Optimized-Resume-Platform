# backend/config.py

# Server configuration
HOST = "0.0.0.0"
PORT = 8081

# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "resume_db"
COLLECTION_NAME = "resumes"

# Gemini API configuration
GEMINI_API_KEY = "" #insert gemini api key
GEMINI_MODEL = "gemini-1.5-flash-latest"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"

# ChatGPT  API configuration
CHATGPT_API_KEY="" # insert chatgpt api key