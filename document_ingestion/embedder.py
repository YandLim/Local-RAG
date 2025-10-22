import numpy as np

def convert_to_vectors(text, model):
    chunks = text.split(".")
    embedding = model.encode(chunks)
    vectored_text = np.array(embedding).astype("float32")

    return chunks, vectored_text
