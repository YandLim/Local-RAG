# Import Libraries
from tkinter import Tk, filedialog
from PyPDF2 import PdfReader

# Call tkinter to open file picker window
def pick_file():
    root = Tk()
    root.withdraw()

    print("Choose a pdf file")

    file_path = filedialog.askopenfilename(
        title="Select your PDF file",
        filetypes=[("PDF file", "*.pdf")] # PDF only file
    )

    # Make sure the file is valid
    if file_path:
        print(f"✅ Selected file: {file_path}")
        return file_path
    else:
        print("❌ No file selected.")
        return None
    

# Open and read the PDF file from pick_file() function
def read_file(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text
