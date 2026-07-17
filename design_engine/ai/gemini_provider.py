import os
import time
from abc import ABC, abstractmethod
import openai
from openai import OpenAI
from design_engine.config import CONFIG

class LLMServiceException(Exception):
    """Custom exception class for LLM service related issues."""
    pass

class BaseLLM(ABC):
    @abstractmethod
    def generate_layout_json(self, system_prompt: str, user_prompt: str) -> str:
        """
        Generates layout JSON string based on prompts.
        """
        pass

class MockLLM(BaseLLM):
    def __init__(self, mock_path: str = "mocks/mock_layout.json"):
        # Resolve mock path relative to the centralized workspace root directory
        self.mock_path = os.path.join(CONFIG.BASE_DIR, mock_path)
        os.makedirs(os.path.dirname(self.mock_path), exist_ok=True)

    def generate_layout_json(self, system_prompt: str, user_prompt: str) -> str:
        if not os.path.exists(self.mock_path):
            raise LLMServiceException(f"Mock layout file not found at: {self.mock_path}")
        try:
            with open(self.mock_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except Exception as e:
            raise LLMServiceException(f"Failed to read mock file: {e}")

class OpenAILLM(BaseLLM):
    def __init__(self):
        if not CONFIG.OPENAI_API_KEY:
            raise LLMServiceException("OpenAI API key is missing. Please set OPENAI_API_KEY environment variable.")
        self.client = OpenAI(api_key=CONFIG.OPENAI_API_KEY)

    def generate_layout_json(self, system_prompt: str, user_prompt: str, retries: int = 3) -> str:
        raise LLMServiceException(
            "OpenAI API call is temporarily disabled in this phase. "
            "Please instantiate MockLLM() instead."
        )

class GeminiLLM(BaseLLM):
    def __init__(self):
        self.api_key = CONFIG.GEMINI_API_KEY
        if not self.api_key:
            raise LLMServiceException(
                "Google Gemini API key is missing. "
                "Please configure GEMINI_API_KEY environment variable or verify secret_key.py."
            )
        
        try:
            import google.generativeai as genai
            self.genai = genai
            self.genai.configure(api_key=self.api_key)
        except ImportError:
            raise LLMServiceException(
                "Google Generative AI SDK is not installed. "
                "Please execute: pip install google-generativeai"
            )
        
        self.model_name = CONFIG.DEFAULT_GEMINI_MODEL

    def generate_layout_json(self, system_prompt: str, user_prompt: str) -> str:
        """
        Calls Google Generative AI (Gemini) endpoint with system instructions
        and enforces structured JSON returns.
        """
        try:
            # Instantiate model with system instructions
            model = self.genai.GenerativeModel(
                model_name=self.model_name,
                system_instruction=system_prompt
            )
            
            # Call generation configuration to return application/json format
            generation_config = {
                "response_mime_type": "application/json",
                "temperature": 0.7
            }
            
            response = model.generate_content(
                user_prompt,
                generation_config=generation_config
            )
            
            if not response.text:
                raise LLMServiceException("Received empty response text from Gemini API.")
                
            return response.text.strip()
            
        except Exception as e:
            raise LLMServiceException(f"Google Gemini API request failed: {e}")
