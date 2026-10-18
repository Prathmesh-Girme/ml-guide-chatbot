
import streamlit as st
import requests

st.set_page_config(
    page_title="ML Guide",
    page_icon="🤖"
)

st.title("🤖 ML Guide")
st.caption("Your Machine Learning Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are ML Guide, a friendly Machine Learning "
                "teacher. Explain ML concepts simply with examples."
            )
        }
    ]

for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

question = st.chat_input("Ask me about Machine Learning...")

if question:
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("ML Guide is thinking..."):
            try:
                host = st.secrets["OLLAMA_HOST"].rstrip("/")
                token = st.secrets["OLLAMA_PROXY_TOKEN"]

                response = requests.post(
                    f"{host}/api/chat",
                    headers={
                        "Authorization": f"Bearer {token}"
                    },
                    json={
                        "model": "llama3.2:1b",
                        "messages": st.session_state.messages,
                        "stream": False
                    },
                    timeout=300
                )

                response.raise_for_status()
                answer = response.json()["message"]["content"]

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except KeyError:
                st.error(
                    "Missing OLLAMA_HOST or OLLAMA_PROXY_TOKEN "
                    "in Streamlit Secrets."
                )
                st.session_state.messages.pop()

            except (requests.RequestException, ValueError):
                st.error(
                    "Could not connect to ML Guide's local AI model. "
                    "Please check that your laptop and tunnel are running."
                )
                st.session_state.messages.pop()

st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        right: 18px;
        color: gray;
        font-size: 12px;
        opacity: 0.8;
        z-index: 999;
    }
    </style>

    <div class="footer">
        Developed by Prathmesh Girme
    </div>
    """,
    unsafe_allow_html=True
)
