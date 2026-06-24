from config import UPLOAD_FOLDER
from document_loader import (
    load_documents,
    split_documents
)

from vector_store import (
    create_vector_store,
    save_vector_store
)


def main():

    print("Loading documents...")

    docs = load_documents(
        UPLOAD_FOLDER
    )


    print("Creating chunks...")

    chunks = split_documents(
        docs
    )


    print("Creating vector database...")

    db = create_vector_store(
        chunks
    )


    save_vector_store(db)

    print("Index created successfully!")


if __name__ == "__main__":
    main()