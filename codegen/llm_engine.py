# codegen/llm_engine.py

import requests

def generate_code_with_llm(prompt: str) -> str:
    url = "https://0f4be692acc8.ngrok-free.app/generate"  # URL du backend LLM
    
    try:
        response = requests.post(url, json={"prompt": prompt}, timeout=60)
        response.raise_for_status()  # Soulève une erreur si HTTP != 200

        data = response.json()
        return data.get("code", "Aucune réponse 'code' reçue dans le JSON.")
    
    except requests.exceptions.RequestException as e:
        return f"Erreur réseau : {e}"
    
    except ValueError:
        return "⚠️ Erreur : réponse non au format JSON."








