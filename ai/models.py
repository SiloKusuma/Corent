import requests, json, time
from typing import Optional

API_URLS = {
    "openrouter": "https://openrouter.ai/api/v1/chat/completions",
    "groq": "https://api.groq.com/openai/v1/chat/completions"
}

HEADERS_TEMPLATE = {
    "openrouter": {
        "Authorization": "Bearer {key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://corent.app",
        "X-Title": "Corent AI"
    },
    "groq": {
        "Authorization": "Bearer {key}",
        "Content-Type": "application/json"
    }
}

def chat_completion(
    provider: str,
    api_key: str,
    model: str,
    messages: list,
    temperature: float = 0.8,
    max_tokens: int = 512,
    retries: int = 3
) -> Optional[str]:
    provider_key = provider.lower()
    url = API_URLS.get(provider_key)
    if not url:
        raise ValueError(f"Provider tidak dikenal: {provider}")

    headers = {}
    for k, v in HEADERS_TEMPLATE.get(provider_key, {}).items():
        headers[k] = v.replace("{key}", api_key)

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    for attempt in range(retries):
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=60)
            resp.raise_for_status()
            data = resp.json()
            choice = data["choices"][0]
            content = choice["message"]["content"].strip()
            return content
        except requests.exceptions.Timeout:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return "[TIMEOUT]"
        except (requests.RequestException, KeyError, IndexError) as e:
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
                continue
            return f"[ERROR: {str(e)[:80]}]"
    return "[FAILED]"
