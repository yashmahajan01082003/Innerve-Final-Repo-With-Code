import ollama

response = ollama.chat(model="mistral", messages=[{"role": "user", "content": "Hello"}])
print(response["message"]["content"])
