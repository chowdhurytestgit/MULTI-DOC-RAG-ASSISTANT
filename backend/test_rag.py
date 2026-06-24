from rag_pipeline import RAGPipeline


rag = RAGPipeline(k=5)


while True:

    question = input("\nYou: ")

    if question.lower() == "exit":
        break


    response = rag.ask(
        question,
        session_id="akash"
    )


    print("\nAssistant:")
    print(response["answer"])


    print("\nSources:")

    for source in response["sources"]:
        print("-", source)