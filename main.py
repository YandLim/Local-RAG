# Importing libaries
from sentence_transformers import SentenceTransformer
from document_ingestion import file_reader, embedder
from dotenv import load_dotenv
from local_ai import llm
import faiss
import os

# Make sure the function only work when run the main.py directly
if __name__ == "__main__":
    # Load env that contains local ai model and local embed model
    load_dotenv()

    # Call the local models
    EMBEDMODEL = os.getenv("EMBEDMODEL")
    LOCALMODEL = os.getenv("LOCALMODEL")

    model = SentenceTransformer(EMBEDMODEL)

    # Proccesing the file
    file_path = file_reader.pick_file() # Call tkinter for filedialog function
    text = file_reader.read_file(file_path) # Get the full pdf text from file_path
    splited_text, text_embedding = embedder.convert_to_vectors(text, model) # Embed and split the text sentence by sentence

    # Store the splited text into vector database
    f_index = faiss.IndexFlatL2(text_embedding.shape[1])
    f_index.add(text_embedding)

    # Asking the user for question
    question = input("What do you want to know?(type 'quit' to end)\n=> ")

    # Make sure the question is valid
    while True:
        if question.strip():
            print("Proccessing the question . . .\n")

            question_embedding = model.encode([question]).astype("float32") # Convert the question into vector
            D, I = f_index.search(question_embedding, 3) # Finding the chunks that relevant with the question from vector database
            relevant_chunks = [splited_text[i] for i in I[0]] # Take the found chunks

            # Send the question and chunks to local AI
            response = llm.get_Ai_response(LOCALMODEL, relevant_chunks, question)
            print(response) # Print the output
            break

        # type 'quit' to exit the program
        elif question == "quit":
            print("Farewell")
            break
        # Asking again, if the question is not valid
        else:
            print("No question found. Try again")