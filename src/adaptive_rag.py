import os
import streamlit as st
from dotenv import load_dotenv
from utils.query_analysis import determine_query_complexity
from utils.retrieval import initialize_vector_store
from utils.response_generation import handle_simple_query, handle_complex_query
from PyPDF2 import PdfReader
from PIL import Image
import fitz  # PyMuPDF for PDF image extraction
import io

# Load environment variables
load_dotenv()

# Initialize OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")

def extract_images_from_pdf(file_path):
    """Extracts images from a PDF and returns them as a list of PIL Images."""
    images = []
    with fitz.open(file_path) as pdf:
        for page_index in range(len(pdf)):
            page = pdf[page_index]
            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = pdf.extract_image(xref)
                image_bytes = base_image["image"]
                pil_image = Image.open(io.BytesIO(image_bytes))
                images.append(pil_image)
    return images

def preview_pdf(file_path):
    """Displays the PDF text content and any images in the file."""
    st.write("**Extracted Text:**")
    reader = PdfReader(file_path)
    for page_num, page in enumerate(reader.pages, start=1):
        st.write(f"Page {page_num}: {page.extract_text()}")

    st.write("**Extracted Images:**")
    images = extract_images_from_pdf(file_path)
    if images:
        for idx, image in enumerate(images, start=1):
            st.image(image, caption=f"Image {idx}", )
    else:
        st.write("No images found in the PDF.")

# Streamlit app
def main():
    st.title("Adaptive RAG System")
    st.write("This system dynamically adjusts retrieval strategies based on query complexity.")
    
    # File uploader for PDF
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    col1, col2 = st.columns([6,6])
    with col1:
        if uploaded_file is not None:
            # Save the uploaded file temporarily
            file_path = os.path.join("data", uploaded_file.name)
            os.makedirs("data", exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Preview the uploaded file
            preview_pdf(file_path)

            # Load the vector store
            vector_store = initialize_vector_store(file_path, openai_api_key)
    with col2:
        # Chat interface
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        

        # Get user input (chat message)
        user_message = st.chat_input("Ask your question:")

        if user_message:
            # Add user message to the chat
            st.session_state.messages.append({"role": "user", "content": user_message})

            # Determine query complexity
            complexity = determine_query_complexity(user_message)
            st.write(f"Query Complexity: {complexity.capitalize()}")

            # Handle query based on complexity
            if complexity == "simple":
                response = handle_simple_query(user_message, openai_api_key)
            else:
                response = handle_complex_query(user_message, vector_store, openai_api_key)

            # Add LLM response to the chat
            st.session_state.messages.append({"role": "assistant", "content": response})

            # Display assistant's response
            # st.chat_message("assistant").markdown(response)

            # Display existing messages
            for msg in st.session_state.messages:
                st.chat_message(msg["role"]).markdown(msg["content"])

if __name__ == "__main__":
    main()
