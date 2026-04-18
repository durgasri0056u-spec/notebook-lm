from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime
import os


def process_pdf(file_path):
    try:
        # Load PDF
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        # Initialize splitter
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        # Split into chunks
        chunks = splitter.split_documents(documents)

        # Extract filename
        filename = os.path.basename(file_path)

        # Add metadata
        for chunk in chunks:
            chunk.metadata["filename"] = filename
            chunk.metadata["upload_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Ensure page number exists
            if "page" in chunk.metadata:
                chunk.metadata["page_number"] = chunk.metadata["page"]
            else:
                chunk.metadata["page_number"] = "unknown"

        return chunks

    except Exception as e:
        print(f"Error processing PDF: {e}")
        return []