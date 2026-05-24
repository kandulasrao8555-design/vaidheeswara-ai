import streamlit as st
from google import genai

# Page Configuration
st.set_page_config(page_title="Code X AI", page_icon="⚡")
st.title("⚡ Code X AI")
st.subheader("Executive Console")

# Secure API Key access (Linked via Streamlit Secrets)
api_key = st.secrets.get("AIzaSyDs3SGstUP9LH86zqLyfpMjhS2uWzIaH2o")

if not api_key:
    st.error("API Key not detected! Please configure it in Streamlit Cloud settings.")
    st.stop()

client = genai.Client(api_key=api_key)

# Manage Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("How can I assist you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
            )
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
