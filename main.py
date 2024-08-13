import os
from dotenv import load_dotenv
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import Chroma
import warnings
from openai import OpenAI
import fitz  # PyMuPDF for PDF processing
import pytesseract  # Tesseract OCR
from PIL import Image
import json
from datetime import datetime

warnings.filterwarnings("ignore")

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

dataset_path = "dataset"
HISTORY_FILE = "conversation_history.json"
VECTOR_STORE_PATH = "vector_store"

def extract_text_from_pdf(file_path):
    text = ""
    try:
        doc = fitz.open(file_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            images = page.get_images()
            for image in images:
                xref = image[0]
                pix = fitz.Pixmap(doc, xref)
                if pix.n < 5:  # this is GRAY or RGB
                    pix = fitz.Pixmap(fitz.csRGB, pix)
                img_bytes = pix.tobytes("ppm")
                text += pytesseract.image_to_string(Image.frombytes("RGB", [pix.width, pix.height], img_bytes))
            text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from {file_path}: {e}")
        text = "OCR extraction failed for this document."
    return text

def initialize_vector_store():
    embeddings = OpenAIEmbeddings()
    if os.path.exists(VECTOR_STORE_PATH):
        vector_store = Chroma(persist_directory=VECTOR_STORE_PATH, embedding_function=embeddings)
        print("Loaded existing vector store")
    else:
        documents = []
        for file in os.listdir(dataset_path):
            file_path = os.path.join(dataset_path, file)
            if file.endswith(".pdf"):
                text = extract_text_from_pdf(file_path)
                documents.append(Document(page_content=text))
        
        if not documents:
            print("No documents were loaded. Check your dataset path and file contents.")
            return None

        vector_store = Chroma.from_documents(documents, embeddings, persist_directory=VECTOR_STORE_PATH)
        vector_store.persist()
        print("Created new vector store")
    
    return vector_store

def process_file(file_path):
    vector_store = initialize_vector_store()
    if vector_store is None:
        return False

    try:
        if file_path.endswith(".pdf"):
            text = extract_text_from_pdf(file_path)
        elif file_path.endswith(".txt"):
            with open(file_path, "r") as f:
                text = f.read()
        elif file_path.endswith((".png", ".jpg", ".jpeg")):
            text = pytesseract.image_to_string(Image.open(file_path))
        else:
            return False

        document = Document(page_content=text)
        vector_store.add_documents([document])
        vector_store.persist()
        return True
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False

def get_answer(query, use_gpt4=False):
    vector_store = initialize_vector_store()
    if vector_store is None:
        return "Error: Vector store not initialized"

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    if use_gpt4:
        response = client.chat.completions.create(
            model="gpt-4",  # Make sure you have access to GPT-4
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": query}
            ]
        )
        answer = response.choices[0].message.content.strip()
    else:
        retrieval_qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(), chain_type="stuff", retriever=retriever)
        answer = retrieval_qa.run(query)
    
    new_doc = Document(page_content=f"Q: {query}\nA: {answer}")
    vector_store.add_documents([new_doc])
    vector_store.persist()
    
    return answer

def save_conversation(conversation):
    with open(HISTORY_FILE, "w") as f:
        json.dump(conversation, f, indent=2)

def load_conversation():
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No previous conversation history found. Starting a new one.")
        return []