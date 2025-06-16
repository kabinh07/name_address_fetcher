from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
import time
import os
from config import LLM_MODEL, LLM_BASE_URL, LLM_TEMPERATURE

def exec_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} executed in {elapsed_time:.4f} seconds")
        return result
    return wrapper

class Fetcher:
    def __init__(self):
        """
        Initialize the Fetcher instance.

        Loads the LLM model with the given config settings.
        """
        self.model = ChatOllama(model=LLM_MODEL, base_url=LLM_BASE_URL, temperature=LLM_TEMPERATURE, timeout=300)
        self.prompt_map = {
            "Salary Certificate": "prompts/salary_certificate.txt",
            "Pay Slip": "prompts/pay_slip.txt",
            "Job ID Card": "prompts/job_id_card.txt",
            "Trade License": "prompts/trade_license.txt",
            "Rental Deed": "prompts/rental_deed.txt",
            "Utility Bill": "prompts/utility_bill.txt"
        }

    def invoke_model(self, prompt, ocr_results):
        prompt = PromptTemplate.from_template(prompt)
        final_prompt = prompt.format(input=ocr_results)
        return self.model.invoke(final_prompt).content
    
    def get_document_type(self, ocr_results):
        """
        Use the LLM model to classify the document type given the OCR results.

        Args:
            ocr_results (list): List of OCR results

        Returns:
            str: The classified document type
        """
        prompt = None
        print(f"Prompt Path: {os.path.join(os.path.abspath(''), 'prompts/classifier.txt')}")
        with open(os.path.join(os.path.abspath(''), 'prompts/classifier.txt'), 'r') as f:
            prompt = f.read()
        if prompt is None:
            return "Prompt not found"
        prompt = PromptTemplate.from_template(prompt)
        final_prompt = prompt.format(input=ocr_results)
        response = self.model.invoke(final_prompt).content.split('</think>')[-1].strip()
        return response
        
    @exec_time
    def extract_text(self, ocr_results, document_type):
        """
        Use the LLM model to extract the relevant information from the OCR results.

        The prompt is read from the file specified by the LLM_PROMPT_PATH environment
        variable. The prompt is formatted with the OCR results and invoked on the
        LLM model. The response is then stripped of any newlines and returned.

        Args:
            ocr_results (list): List of OCR results

        Returns:
            str: The extracted information
        """
        print(f"LLM Prompt Path: {self.prompt_map.get(document_type, None)}")
        LLM_PROMPT_PATH = os.path.join(os.path.abspath(''), self.prompt_map.get(document_type, None))
        if LLM_PROMPT_PATH is None:
            raise ValueError(f"Document type '{document_type}' not supported.")
        with open(LLM_PROMPT_PATH, 'r') as f:
            prompt = f.read()
        prompt = PromptTemplate.from_template(prompt)
        final_prompt = prompt.format(input=ocr_results[:25])
        print("Invoking LLM...")
        response = self.model.invoke(final_prompt).content.split('</think>')[-1].strip()
        return response