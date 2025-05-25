from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import time
from config import LLM_MODEL, LLM_BASE_URL, LLM_TEMPERATURE

def exec_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"{func.__name__} executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper

class Fetcher:
    def __init__(self):
        self.model = ChatOllama(model=LLM_MODEL, base_url=LLM_BASE_URL, temperature=LLM_TEMPERATURE)
        print(f"MODEL CONFIGURATION: {self.model}")
    
    @exec_time
    def extract_text(self, ocr_results):
        with open("prompt.txt", 'r') as f:
            prompt = f.read()
        prompt = PromptTemplate.from_template(prompt)
        final_prompt = prompt.format(input=ocr_results[:20])
        print("Invoking LLM...")
        response = self.model.invoke(final_prompt).content.split('</think>')[0].strip()
        return response
    
    
    