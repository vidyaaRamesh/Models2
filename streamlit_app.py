import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit's secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Title of the app
st.title("VR Health Symptom Checker2")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    role, content = message["role"], message["content"]
    with st.chat_message(role):
        st.markdown(content)

# Function to check if the input is health-related
def is_health_related(text):
    health_keywords = [
        "fever", "pain", "headache", "cough", "symptom", "nausea",
        "vomiting", "dizziness", "sore", "infection", "cold", "flu",
        "diarrhea", "allergy", "rash", "fatigue", "breathing", "illness",
        "disease", "health", "swelling", "injury", "wound", "cramp", "burn"
    ]
    return any(keyword in text.lower() for keyword in health_keywords)

# Function to get a response from OpenAI with health advice
def get_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ] + [{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Collect user input for symptoms
user_input = st.chat_input("Describe your symptoms here...")

# Process and display response if there's input
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if is_health_related(user_input):
        assistant_prompt = f"User has reported the following symptoms: {user_input}. Provide a general remedy or advice."
        assistant_response = get_response(assistant_prompt)
    else:
        assistant_response = "Sorry, I can only help with health or symptom-related questions."

    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
