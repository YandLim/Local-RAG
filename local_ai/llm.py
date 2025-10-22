import requests 
import json

def get_Ai_response(model, context, question):
    prompt = (
        "You are a factual assistant. Use ONLY the information from the context below to answer.\n"
        "If the answer is not explicitly stated, say: 'Not mentioned in the document.'\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n"
        "Answer:"
    )

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

    return "".join(answer_parts).strip()
