from sentence_transformers import SentenceTransformer
from document_ingestion import file_reader, embedder
from dotenv import load_dotenv
from local_ai import llm
import faiss
import os

if __name__ == "__main__":
    load_dotenv()

    EMBEDMODEL = os.getenv("EMBEDMODEL")
    LOCALMODEL = os.getenv("LOCALMODEL")

    model = SentenceTransformer(EMBEDMODEL)

    file_path = file_reader.pick_file()
    text = file_reader.read_file(file_path)
    splited_text, text_embedding = embedder.convert_to_vectors(text, model)

    f_index = faiss.IndexFlatL2(text_embedding.shape[1])
    f_index.add(text_embedding)

    question = input("What do you want to know?(type 'quit' to end)\n=> ")

    while True:
        if question.strip():
            print("Proccessing the question . . .\n")

            question_embedding = model.encode([question]).astype("float32")
            D, I = f_index.search(question_embedding, 3)
            relevant_chunks = [splited_text[i] for i in I[0]]

            response = llm.get_Ai_response(LOCALMODEL, relevant_chunks, question)
            print(response)
            break
        elif question == "quit":
            print("Farewell")
            break
        else:
            print("No question found. Try again")