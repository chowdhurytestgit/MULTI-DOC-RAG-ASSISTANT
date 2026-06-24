import streamlit as st
import requests
import uuid


# ===============================
# Configuration
# ===============================

API_URL = "http://127.0.0.1:8000"


# ===============================
# Page Settings
# ===============================

st.set_page_config(
    page_title="Multi-Document RAG Assistant",
    page_icon="🤖",
    layout="wide"
)


# ===============================
# Custom CSS
# ===============================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    text-align: center;
    color: #00FFAA;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ===============================
# Session Initialization
# ===============================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


if "messages" not in st.session_state:
    st.session_state.messages = []


# ===============================
# Sidebar
# ===============================

with st.sidebar:

    st.title("📂 Document Manager")

    uploaded_file = st.file_uploader(
        "Upload PDF / DOCX / TXT",
        type=["pdf", "docx", "txt"]
    )


    if uploaded_file:

        if st.button("Upload Document"):

            with st.spinner("Uploading and indexing document..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue()
                    )
                }


                response = requests.post(
                    f"{API_URL}/upload",
                    files=files
                )


                if response.status_code == 200:

                    st.success(
                        response.json()["message"]
                    )

                else:

                    st.error(
                        response.text
                    )


    st.divider()


    if st.button("🗑️ Clear Chat"):

        response = requests.post(
            f"{API_URL}/clear-chat",
            json={
                "session_id":
                st.session_state.session_id
            }
        )


        st.session_state.messages = []


        st.success(
            "Chat cleared successfully!"
        )


    st.divider()


    st.info(
        f"""
Session ID:

{st.session_state.session_id[:8]}
        """
    )


# ===============================
# Main Chat UI
# ===============================


st.title(
    "🧠 DocuMind AI"
)


st.caption(
    "Your Intelligent Document Companion. Ask questions from your uploaded documents"
)


# Display old messages

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# Chat input

question = st.chat_input(
    "Ask something from your documents..."
)


if question:

    # User message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    with st.chat_message("user"):

        st.markdown(question)


    # Assistant response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = requests.post(
                f"{API_URL}/chat",
                json={
                    "question": question,
                    "session_id":
                    st.session_state.session_id
                }
            )


            if response.status_code == 200:

                data = response.json()


                answer = data["answer"]


                sources = data["sources"]


                st.markdown(answer)


                if sources:

                    st.markdown(
                        "### 📄 Sources"
                    )


                    for source in sources:

                        st.write(
                            f"• {source}"
                        )


                final_message = (
                    answer +
                    "\n\nSources:\n" +
                    "\n".join(
                        [
                            f"- {s}"
                            for s in sources
                        ]
                    )
                )


                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": final_message
                    }
                )


            else:

                st.error(
                    "Failed to get response from API"
                )