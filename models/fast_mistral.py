import requests
import json
import os
from dotenv import load_dotenv
from typing import Optional
import logging
import time

load_dotenv()

# Configure minimal logging
logging.basicConfig(level=logging.WARNING)  # Reduced logging
logger = logging.getLogger(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Ultra-fast configuration
ULTRA_FAST_TIMEOUT = 5  # 5 seconds max
MAX_TOKENS = 800  # Reduced for speed
TEMPERATURE = 0.3  # Lower for faster, more predictable responses

# Single persistent session
session = requests.Session()
session.headers.update({
    'Authorization': f'Bearer {OPENROUTER_API_KEY}',
    'Content-Type': 'application/json'
})

def ultra_fast_chat(prompt: str) -> str:
    """Ultra-fast chat with minimal processing"""
    
    if not OPENROUTER_API_KEY:
        return "Error: API key not configured"
    
    # Minimal system prompt for speed
    system_prompt = "You are a helpful ERP assistant. Provide concise, direct answers."
    
    # Streamlined request
    data = {
        "model": "mistralai/mistral-small-3.2-24b-instruct:free",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt[:1000]}  # Limit input length
        ],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "top_p": 0.7
    }
    
    try:
        response = session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=data,
            timeout=ULTRA_FAST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"]
        
        return f"Error: {response.status_code}"
        
    except requests.exceptions.Timeout:
        return "Response timeout - please try a shorter question"
    except Exception as e:
        return f"Error: {str(e)[:100]}"

def ultra_fast_image_chat(prompt: str, image_url: str) -> str:
    """Ultra-fast image chat"""
    
    if not OPENROUTER_API_KEY:
        return "Error: API key not configured"
    
    data = {
        "model": "mistralai/mistral-small-3.2-24b-instruct:free",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt[:500]},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        "temperature": TEMPERATURE,
        "max_tokens": 600,  # Even smaller for image responses
        "top_p": 0.7
    }
    
    try:
        response = session.post(
            "https://openrouter.ai/api/v1/chat/completions",
            json=data,
            timeout=ULTRA_FAST_TIMEOUT
        )
        
        if response.status_code == 200:
            result = response.json()
            if "choices" in result and result["choices"]:
                return result["choices"][0]["message"]["content"]
        
        return f"Error: {response.status_code}"
        
    except requests.exceptions.Timeout:
        return "Image analysis timeout - please try again"
    except Exception as e:
        return f"Error: {str(e)[:100]}"

# Backward compatibility
def chat_with_mistral(prompt: str, system_prompt: str = None) -> str:
    return ultra_fast_chat(prompt)

def chat_with_mistral_image(prompt: str, image_url: str, system_prompt: str = None) -> str:
    return ultra_fast_image_chat(prompt, image_url)
