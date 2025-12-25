import openai
from openai import OpenAI
from typing import List, Dict, Any, Optional
import logging
from ..database.config import settings


logger = logging.getLogger(__name__)


class OpenAIService:
    def __init__(self):
        # Initialize OpenAI client
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Default model to use
        self.default_model = "gpt-4-turbo"  # or "gpt-3.5-turbo" depending on availability and needs
    
    def generate_text(self, 
                     prompt: str, 
                     model: Optional[str] = None, 
                     max_tokens: int = 1000,
                     temperature: float = 0.7) -> Optional[str]:
        """Generate text based on the provided prompt"""
        try:
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            content = response.choices[0].message.content
            logger.info(f"Generated text using model {model or self.default_model}")
            return content
        except Exception as e:
            logger.error(f"Error generating text: {e}")
            return None
    
    def generate_embeddings(self, texts: List[str], model: str = "text-embedding-ada-002") -> Optional[List[List[float]]]:
        """Generate embeddings for the provided texts"""
        try:
            response = self.client.embeddings.create(
                input=texts,
                model=model
            )
            
            embeddings = [item.embedding for item in response.data]
            logger.info(f"Generated embeddings for {len(texts)} texts using model {model}")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return None
    
    def chat_completion(self, 
                       messages: List[Dict[str, str]], 
                       model: Optional[str] = None,
                       max_tokens: int = 1000,
                       temperature: float = 0.7) -> Optional[Dict[str, Any]]:
        """Perform a chat completion with the provided messages"""
        try:
            response = self.client.chat.completions.create(
                model=model or self.default_model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            result = {
                "content": response.choices[0].message.content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
            
            logger.info(f"Chat completion using model {model or self.default_model}")
            return result
        except Exception as e:
            logger.error(f"Error in chat completion: {e}")
            return None
    
    def validate_api_key(self) -> bool:
        """Validate if the API key is working properly"""
        try:
            # Try a simple completion to validate the API key
            self.client.chat.completions.create(
                model=self.default_model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
        except Exception as e:
            logger.error(f"API key validation failed: {e}")
            return False