
import streamlit as st
from ollama import chat

# Page settings
st.set_page_config(
    page_title="ML Guide",
    page_icon="🤖"
)

# GUI title
st.title("🤖 ML Guide")
st.caption("Your Machine Learning Assistant")

# Initialize conversation history
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

# Display previous messages
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept a new question
question = st.chat_input("Ask me about Machine Learning...")

if question:
    # Save and display the user question
    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    # Generate the AI response
    with st.chat_message("assistant"):
        with st.spinner("ML Guide is thinking..."):
            response = chat(
                model="llama3.2:1b",
                messages=st.session_state.messages
            )

            answer = response.message.content
            st.markdown(answer)

    # Save the assistant response
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# Footer credit
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
