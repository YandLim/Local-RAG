"""
Fetches a response from a locally running AI model (Ollama) based on a given question and context.

This function:
- Builds a factual prompt with strict context limits
- Sends it to a local Ollama model via REST API
- Streams and aggregates the model’s response
"""

# Import libraries
import requests 
import json

# Main local AI function
def get_Ai_response(model, context, question):
    # Custom prompt for Local AI
    prompt = (
        "You are a factual assistant. Use ONLY the information from the context below to answer.\n"
        "If the answer is not explicitly stated, say: 'Not mentioned in the document.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )

    # Post the prompt to Ollama Local AI
    response = requests.post(
        url="http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "options": {"temprature": 0.3}
        },
        stream=True,
        timeout=120
    )

    # Cleaning up the answer given by Local AI
    answer_parts = []
    for line in response.iter_lines():
        if not line:
            continue
        try:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                answer_parts.append(data["response"])
            if data.get("done"):
                break
        except json.JSONDecodeError:
            continue

    # Return the answer text
    return "".join(answer_parts).strip()
