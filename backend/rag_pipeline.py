from llm import get_llm
from vector_store import get_retriever
from chat_memory import memory


class RAGPipeline:

    def __init__(self, k=5):
        """
        Initialize RAG components.
        """
        self.retriever = get_retriever(k)
        self.llm = get_llm()


    # ------------------------------
    # Retrieve relevant documents
    # ------------------------------

    def retrieve_context(self, question):
        """
        Retrieve relevant chunks from FAISS.
        """

        docs = self.retriever.invoke(question)

        context = ""
        sources = []

        for doc in docs:

            metadata = doc.metadata

            source = (
                f"{metadata.get('source')} "
                f"(page {metadata.get('page')})"
            )

            sources.append(source)

            context += (
                f"\nSOURCE: {source}\n"
                f"{doc.page_content}\n"
            )

        return context, list(set(sources))


    # ------------------------------
    # Get previous chat history
    # ------------------------------

    def get_chat_history(self, session_id):
        """
        Format previous conversation.
        """

        history = memory.get_history(session_id)

        formatted = ""

        for item in history:
            formatted += (
                f"{item['role']}: "
                f"{item['message']}\n"
            )

        return formatted


    # ------------------------------
    # Build optimized RAG prompt
    # ------------------------------

    def build_prompt(self,question, context, history):
        return f"""
You are an intelligent AI Document Assistant.

Your job is to answer questions using the provided DOCUMENT CONTEXT.

Instructions:

1. Carefully read all sections in DOCUMENT CONTEXT before answering.

2. If the user asks for:
   - a summary of the document,
   - an overview,
   - the main idea,
   - key points,
   - important topics,

   then combine all available information from DOCUMENT CONTEXT and create a well-structured summary.

3. For normal questions:
   - Give a precise answer using only the information available in DOCUMENT CONTEXT.
   - Include definitions, explanations, formulas, steps, examples, and important details whenever available.

4. If information is spread across multiple sections, combine those sections into one complete answer.

5. Format your answers professionally:
   - Use headings where appropriate.
   - Use bullet points for lists.
   - Keep explanations clear and easy to understand.

6. Do not say phrases such as:
   - "According to the document"
   - "Based on the provided context"
   - "The uploaded document states"

   Answer naturally.

7. If the relevant information is not available in DOCUMENT CONTEXT, reply exactly:
   "I could not find this information in the uploaded documents."

8. Use previous conversation only when it helps understand the current question. Do not use it to create facts.

--------------------------
PREVIOUS CONVERSATION:
{history}
--------------------------

DOCUMENT CONTEXT:
{context}

--------------------------

USER QUESTION:
{question}

--------------------------

FINAL ANSWER:
"""


    # ------------------------------
    # Generate RAG answer
    # ------------------------------

    def ask(self, question, session_id="default"):

    # Retrieve documents
        context, sources = self.retrieve_context(question)

        # Get chat history
        history = self.get_chat_history(session_id)

        # Create prompt
        prompt = self.build_prompt(
            question,
            context,
            history
        )

        # Generate response
        response = self.llm.invoke(prompt).content

        # Save memory
        memory.add_message(
            session_id,
            "User",
            question
        )

        memory.add_message(
            session_id,
            "Assistant",
            response
        )

        # Return response
        return {
            "answer": response,
            "sources": sources
        }

    # ------------------------------
    # Clear conversation history
    # ------------------------------

    def clear_chat(self, session_id="default"):
        """
        Delete chat history.
        """

        memory.clear(session_id)