import logging
import os

import requests
import streamlit as st

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

CHATBOT_URL = os.getenv("CHATBOT_URL")

with st.sidebar:
    st.header("About")
    st.markdown(
        """
        This chatbot interfaces with a
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent designed to answer questions.
        """
    )

st.title("Chatbot")
st.info("Ask me questions and I will try to answer them.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("How was this generated", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("What do you want to know?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    with st.spinner("Searching for an answer..."):
        log.info(f"Sending request to {CHATBOT_URL} with data: {data}")
        response = requests.post(CHATBOT_URL, headers=headers, json=data)
        log.info(f"Received response: {response.text}")
        log.info(f"Response status code: {response.status_code}")

        if response.status_code == 200:
            output_text = response.json()["output"]
            try:
                explanation = response.json()["intermediate_steps"]
            except KeyError:
                explanation = "No explanation provided."

        else:
            output_text = """An error occurred while processing your message.
            Please try again or rephrase your message."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("How was this generated", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
