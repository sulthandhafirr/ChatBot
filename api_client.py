"""DeepSeek API client"""
import requests
from config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL, TEMPERATURE, MAX_TOKENS

def call_deepseek_api(messages):
    """Call DeepSeek Chat Completion API"""
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
        "stop": ["\n\n", "**"]  # Stop when markdown formatting appears
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, json=data, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error calling DeepSeek API: {e}")
        return f"Maaf, terjadi error saat menghubungi DeepSeek API: {str(e)}"
