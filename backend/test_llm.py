from llm import get_llm


llm = get_llm()


response = llm.invoke(
    "Explain deep learning in 50 words."
)


print(response)