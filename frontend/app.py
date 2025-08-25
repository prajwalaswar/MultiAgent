import streamlit as st
import requests

API_URL = "http://127.0.0.1:9999/api/chat"

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Chatbot Agents")
st.write("Create and Interact with the AI Agents!")

system_prompt = st.text_area("Define your AI Agent:", height=70, placeholder="Type your system prompt here...")

MODEL_NAMES_GROQ = ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
MODEL_NAMES_OPENAI = ["gpt-4o-mini"]

provider = st.radio("Select Provider:", ("Groq", "OpenAI"))

if provider == "Groq":
    selected_model = st.selectbox("Select Groq Model:", MODEL_NAMES_GROQ)
else:
    selected_model = st.selectbox("Select OpenAI Model:", MODEL_NAMES_OPENAI)

allow_web_search = st.checkbox("Allow Web Search")

user_query = st.text_area("Enter your query:", height=150, placeholder="Ask Anything!")

if st.button("Ask Agent!"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search,
        }
        try:
            r = requests.post(API_URL, json=payload, timeout=30)
            r.raise_for_status()
            data = r.json()
            if isinstance(data, dict) and "response" in data:
                st.subheader("Agent Response")
                st.markdown(f"**Final Response:** {data['response']}")
            else:
                st.error(str(data))
        except requests.exceptions.ConnectionError:
            st.error("❌ Backend server is not running at 127.0.0.1:9999. Please start it.")
        except requests.HTTPError as e:
            st.error(f"HTTP error: {e.response.status_code} {e.response.text}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
    else:
        st.warning("Please enter a query before asking the agent!")
