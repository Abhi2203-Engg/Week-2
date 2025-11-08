# app.py
import streamlit as st
import pandas as pd

st.set_page_config(page_title="EV Vehicle Chatbot", page_icon="⚡", layout="wide")
st.title("⚡ EV Vehicle Chatbot ⚡")

# -------------------------------
# Load EV data safely
# -------------------------------
file_path = r"C:\EV Vehicle\ev_data.csv"  # change if needed

# Sample data if CSV is missing or empty
sample_data = pd.DataFrame({
    "Car": ["Tesla Model 3", "Nissan Leaf", "Chevy Bolt"],
    "Range": [353, 226, 259],
    "Price": [39999, 31999, 36999]
})

if pd.io.common.file_exists(file_path):
    try:
        ev_data = pd.read_csv(file_path)
        if ev_data.empty:
            st.warning("CSV is empty. Using sample EV data.")
            ev_data = sample_data
    except pd.errors.EmptyDataError:
        st.warning("CSV has no data. Using sample EV data.")
        ev_data = sample_data
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        ev_data = sample_data
else:
    st.info("CSV not found. Using sample EV data.")
    ev_data = sample_data

# -------------------------------
# Display EV data (optional)
# -------------------------------
st.subheader("Available EVs")
st.dataframe(ev_data)

# -------------------------------
# Chatbot functionality
# -------------------------------
st.subheader("Ask about EVs")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("Type your question here...")

def answer_question(question):
    question = question.lower()
    response = "Sorry, I don't understand. Try asking about 'range', 'price', or 'models'."
    
    if "range" in question:
        response = "Here are the ranges of available EVs:\n"
        for _, row in ev_data.iterrows():
            response += f"{row['Car']}: {row['Range']} km\n"
    elif "price" in question:
        response = "Here are the prices of available EVs:\n"
        for _, row in ev_data.iterrows():
            response += f"{row['Car']}: ${row['Price']}\n"
    elif "models" in question or "cars" in question:
        response = "Available EV models:\n" + ", ".join(ev_data['Car'].tolist())
    
    return response

if user_input:
    answer = answer_question(user_input)
    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("Bot", answer))

# Display chat history
for sender, message in st.session_state.chat_history:
    if sender == "You":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")
