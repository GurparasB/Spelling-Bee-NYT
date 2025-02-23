import requests

API_KEY = "sk-97dd1e4b43f14e89bcb37da095b48ad4"
API_URL = "https://api.deepseek.com/v1/chat/completions"  # Replace with actual API URL

def chat_with_deepseek(prompt):
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "deepseek-chat",  # Replace with actual model name
        "messages": [{"role": "user", "content": prompt}]
    }
    
    response = requests.post(API_URL, headers=headers, json=data)
    return response.json()

# Example usage
response = chat_with_deepseek("Explain machine learning in simple terms.")
print(response)
