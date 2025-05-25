from dotenv import load_dotenv
import os
load_dotenv()

DETECTOR_URL = os.getenv("DETECTOR_URL", "http://localhost:8000")
RECOGNIZER_URL = os.getenv("RECOGNIZER_URL", "http://localhost:8001")
API_KEY = os.getenv("API_KEY", "")
HEADERS = {
    'X-API-KEY': API_KEY,
    'Content-Type': 'application/json'
}
LLM_MODEL = os.getenv("LLM_MODEL", "llama3.1")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://localhost:11434")
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.1"))