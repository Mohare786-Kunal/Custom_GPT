import streamlit as st
import os
import base64
from datetime import datetime
from main import process_file, get_answer, initialize_vector_store, load_conversation, save_conversation

# Set page config
st.set_page_config(page_title="AI Custom Botwa", layout="wide")

# Initialize session state
if 'vector_store' not in st.session_state:
    st.session_state.vector_store = initialize_vector_store()
if 'conversation' not in st.session_state:
    st.session_state.conversation = load_conversation()

# Title
st.title("RAG AI Custom Bot")

# File uploader
uploaded_file = st.file_uploader("Upload a document (PDF, TXT, or Image)", type=["pdf", "txt", "png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Save the file
    save_path = os.path.join("dataset", uploaded_file.name)
    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Process the file
    success = process_file(save_path)
    if success:
        st.success(f"File {uploaded_file.name} uploaded and processed successfully!")
    else:
        st.error(f"Error processing file {uploaded_file.name}")

# Query input
query = st.text_input("Enter your question:")

# GPT-4 checkbox
use_gpt4 = st.checkbox("Use GPT-4")

# Get answer button
if st.button("Get Answer"):
    if query:
        answer = get_answer(query, use_gpt4)
        st.write("Answer:")
        st.write(answer)

        # Add to conversation history
        st.session_state.conversation.append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "answer": answer
        })
        save_conversation(st.session_state.conversation)
    else:
        st.warning("Please enter a question.")

# Display conversation history
st.subheader("Conversation History")
for entry in st.session_state.conversation:
    st.text(f"Q: {entry['query']}")
    st.text(f"A: {entry['answer']}")
    st.text(f"Timestamp: {entry['timestamp']}")
    st.text("---")

# Display uploaded files
st.subheader("Uploaded Files")
for file in os.listdir("dataset"):
    st.text(file)
    
    # Add download button for each file
    with open(os.path.join("dataset", file), "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{file}">Download {file}</a>'
        st.markdown(href, unsafe_allow_html=True)