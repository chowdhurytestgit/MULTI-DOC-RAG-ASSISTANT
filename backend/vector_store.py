import os

from langchain_community.vectorstores import FAISS

from embeddings import get_embedding_model
from config import FAISS_PATH


# -----------------------------------
# Create FAISS Vector Store
# -----------------------------------

def create_vector_store(documents):
    """
    Create a FAISS vector database
    from document chunks.
    """

    print("Creating embeddings...")

    embeddings = get_embedding_model()

    vector_store = FAISS.from_documents(
        documents=documents,
        embedding=embeddings
    )

    print("Vector database created.")

    return vector_store


# -----------------------------------
# Save FAISS Index
# -----------------------------------

def save_vector_store(vector_store):
    """
    Save FAISS index to disk.
    """

    os.makedirs(
        FAISS_PATH,
        exist_ok=True
    )

    vector_store.save_local(
        FAISS_PATH
    )

    print(
        f"FAISS index saved at: {FAISS_PATH}"
    )


# -----------------------------------
# Load Existing FAISS Index
# -----------------------------------

def load_vector_store():
    """
    Load previously saved FAISS index.
    """

    embeddings = get_embedding_model()

    vector_store = FAISS.load_local(
        folder_path=FAISS_PATH,
        embeddings=embeddings,
        allow_dangerous_deserialization=True
    )

    print("FAISS index loaded.")

    return vector_store


# -----------------------------------
# Check Whether Index Exists
# -----------------------------------

def vector_store_exists():
    """
    Check if a saved FAISS index exists.
    """

    return os.path.exists(
        os.path.join(
            FAISS_PATH,
            "index.faiss"
        )
    )


# -----------------------------------
# Similarity Search
# -----------------------------------

def search_documents(
    query,
    k=5
):
    """
    Retrieve top-k most relevant chunks.
    """

    vector_store = load_vector_store()

    results = vector_store.similarity_search(
        query=query,
        k=k
    )

    return results


# -----------------------------------
# Similarity Search With Scores
# -----------------------------------

def search_documents_with_scores(
    query,
    k=5
):
    """
    Retrieve chunks with similarity scores.
    """

    vector_store = load_vector_store()

    results = (
        vector_store
        .similarity_search_with_score(
            query=query,
            k=k
        )
    )

    return results


# -----------------------------------
# Convert Vector Store to Retriever
# -----------------------------------

def get_retriever(
    k=5
):
    """
    Create a retriever object for RAG.
    """

    vector_store = load_vector_store()

    retriever = vector_store.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 5,
        "fetch_k": 15
    }
    )

    return retriever


# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    query = "Explain machine learning."

    results = search_documents_with_scores(
        query=query,
        k=3
    )

    print("\nTop Results\n")

    for document, score in results:

        print("-" * 50)

        print(
            "Score:",
            score
        )

        print(
            "Source:",
            document.metadata
        )

        print(
            document.page_content[:300]
        )