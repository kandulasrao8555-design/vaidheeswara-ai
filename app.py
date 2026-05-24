import streamlit as st
import google.generativeai as genai
from PIL import Image
from duckduckgo_search import DDGS  # <--- New library for searching

# 1. Page Configuration
st.set_page_config(page_title="Code X AI", layout="centered")
st.title("⚡ Code X AI")
st.subheader("Executive Console")

# 2. Secure API Key Setup
api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("API Key not detected!")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 4. Sidebar Camera Input
with st.sidebar:
    st.header("📸 Visual Input")
    camera_file = st.camera_input("Take a photo")

# 5. Search Function
def search_for_image(query):
    with DDGS() as ddgs:
        # Search for images, get the first result
        results = list(ddgs.images(query, max_results=1))
        if results:
            return results[0]['image'] # Returns the URL
    return None

# 6. Chat Logic
prompt = st.chat_input("Ask for an image or code...")

if prompt or camera_file:
    # Check if user is asking for an image search
    is_image_search = "show me an image of" in prompt.lower()
    
    # Add User input to history
    user_text = prompt if prompt else "Analyze this image."
    st.session_state.messages.append({"role": "user", "content": user_text})
    
    with st.chat_message("user"):
        st.markdown(user_text)

    # Generate Response
    with st.chat_message("assistant"):
        if is_image_search:
            st.write("Searching the web for your image...")
            image_url = search_for_image(prompt.replace("show me an image of", "").strip())
            if image_url:
                st.image(image_url, caption="Found this for you!")
            else:
                st.write("Sorry, I couldn't find an image for that.")
        else:
            with st.spinner("Thinking..."):
                response = model.generate_content(user_text)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
