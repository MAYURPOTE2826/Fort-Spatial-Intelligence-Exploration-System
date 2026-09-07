import os
from typing import List, Dict, Any, Optional
from google import genai
from google.genai import types

class LLMService:
    def __init__(self):
        self.api_key = os.environ.get("GEMINI_API_KEY")
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    def generate_response(self, system_instruction: str, user_prompt: str) -> str:
        if not self.client:
            return "Error: LLM API key not configured."
            
        try:
            response = self.client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.3,
                )
            )
            return response.text
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"

llm_service = LLMService()
