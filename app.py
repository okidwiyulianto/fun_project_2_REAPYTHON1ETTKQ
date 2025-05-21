import streamlit as st
import requests
import json
import pandas as pd
import time
import datetime
import os
import csv
import base64
from io import StringIO

# Set page configuration
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="👽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "current_chat_name" not in st.session_state:
    st.session_state.current_chat_name = f"Chat {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
if "pinned_messages" not in st.session_state:
    st.session_state.pinned_messages = []
if "chat_histories" not in st.session_state:
    st.session_state.chat_histories = {}
if "api_key" not in st.session_state:
    st.session_state.api_key = "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"
if "user_message" not in st.session_state:
    st.session_state.user_message = ""

# Define available models
MODELS = {
    "Claude": "anthropic/claude-3-opus",
    "GPT-4": "openai/gpt-4-turbo",
    "DeepSeek": "deepseek/deepseek-coder"
}

# Custom CSS for styling
def load_css():
    st.markdown("""
    <style>
    /* Main background color */
    .stApp {
        background-color: #f4f3fa;
    }
    
    /* User message styling */
    .user-message {
        background-color: #0f2b5b;
        color: #ffffff;
        border-radius: 20px 20px 5px 20px;
        padding: 15px;
        margin: 10px 0;
        max-width: 80%;
        float: right;
        position: relative;
        animation: fadeIn 0.5s;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* AI message styling */
    .ai-message {
        background-color: #fcd116;
        color: #000000;
        border-radius: 20px 20px 20px 5px;
        padding: 15px;
        margin: 10px 0;
        max-width: 80%;
        float: left;
        position: relative;
        animation: fadeIn 0.5s;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Timestamp styling */
    .timestamp {
        font-size: 0.7em;
        opacity: 0.7;
        margin-top: 5px;
        text-align: right;
    }
    
    /* Message container */
    .message-container {
        display: flex;
        flex-direction: column;
        width: 100%;
        overflow: hidden;
        margin-bottom: 15px;
    }
    
    /* User message container */
    .user-container {
        display: flex;
        justify-content: flex-end;
        width: 100%;
    }
    
    /* AI message container */
    .ai-container {
        display: flex;
        justify-content: flex-start;
        width: 100%;
    }
    
    /* Emoji styling */
    .emoji {
        font-size: 1.5em;
        margin-right: 10px;
        margin-left: 10px;
        align-self: flex-end;
    }
    
    /* Animation for messages */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Animation for typing indicator */
    .typing-indicator {
        display: flex;
        padding: 10px;
        background-color: #fcd116;
        border-radius: 20px;
        margin: 10px 0;
        width: fit-content;
    }
    
    .typing-indicator span {
        height: 10px;
        width: 10px;
        background-color: #333;
        border-radius: 50%;
        display: inline-block;
        margin: 0 2px;
        animation: bounce 1.5s infinite ease-in-out;
    }
    
    .typing-indicator span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-indicator span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes bounce {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-5px); }
    }
    
    /* Pin button styling */
    .pin-button {
        background-color: transparent;
        border: none;
        color: #555;
        cursor: pointer;
        float: right;
        margin-left: 10px;
    }
    
    .pin-button:hover {
        color: #000;
    }
    
    /* Pinned message styling */
    .pinned-message {
        border-left: 4px solid #fcd116;
        padding-left: 10px;
        margin: 10px 0;
        background-color: rgba(252, 209, 22, 0.1);
    }
    
    /* Clear button styling */
    .stButton button {
        background-color: #0f2b5b;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 20px;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #0a1f42;
        transform: scale(1.05);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f0f0f8;
    }
    
    /* Input box styling */
    .stTextInput input {
        border-radius: 20px;
        border: 1px solid #ddd;
        padding: 10px 15px;
    }
    
    /* Selectbox styling */
    .stSelectbox div[data-baseweb="select"] {
        border-radius: 20px;
    }
    
    /* Download button styling */
    .download-button {
        display: inline-block;
        background-color: #0f2b5b;
        color: white;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 20px;
        margin-top: 10px;
        text-align: center;
    }
    
    .download-button:hover {
        background-color: #0a1f42;
    }
    </style>
    """, unsafe_allow_html=True)

# Function to call OpenRouter API
def get_ai_response(messages, model):
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {st.session_state.api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": messages
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise exception for HTTP errors
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling OpenRouter API: {str(e)}")
        return "Sorry, I encountered an error while processing your request. Please try again."

# Function to save chat history to CSV
def save_chat_to_csv(messages, filename="chat_history.csv"):
    try:
        with open(os.path.join("assets", filename), 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Role", "Content", "Timestamp"])
            for msg in messages:
                writer.writerow([msg["role"], msg["content"], msg.get("timestamp", "")])
        return os.path.join("assets", filename)
    except Exception as e:
        st.error(f"Error saving chat history: {str(e)}")
        return None

# Function to download chat history
def get_csv_download_link(messages, filename="chat_history.csv"):
    # Create a CSV string from messages
    csv_string = StringIO()
    writer = csv.writer(csv_string)
    writer.writerow(["Role", "Content", "Timestamp"])
    for msg in messages:
        writer.writerow([msg["role"], msg["content"], msg.get("timestamp", "")])
    
    # Encode the CSV string to base64
    b64 = base64.b64encode(csv_string.getvalue().encode()).decode()
    
    # Create download link
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-button">Download Chat History</a>'
    return href

# Function to display messages with custom styling
def display_messages():
    for i, message in enumerate(st.session_state.messages):
        role = message["role"]
        content = message["content"]
        timestamp = message.get("timestamp", "")
        
        if role == "user":
            st.markdown(f"""
            <div class="message-container">
                <div class="user-container">
                    <div class="user-message">
                        {content}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                    <div class="emoji">🧑‍💻</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-container">
                <div class="ai-container">
                    <div class="emoji">👽</div>
                    <div class="ai-message">
                        {content}
                        <div class="timestamp">{timestamp}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# Function to display typing indicator
def display_typing_indicator():
    st.markdown("""
    <div class="message-container">
        <div class="ai-container">
            <div class="emoji">👽</div>
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Function to display pinned messages
def display_pinned_messages():
    if st.session_state.pinned_messages:
        st.sidebar.markdown("### Pinned Messages")
        for i, pinned in enumerate(st.session_state.pinned_messages):
            st.sidebar.markdown(f"""
            <div class="pinned-message">
                <strong>{pinned['role'].capitalize()}:</strong> {pinned['content'][:50]}...
                <button class="pin-button" onclick="unpin({i})">📌</button>
            </div>
            """, unsafe_allow_html=True)

# Callback function for message submission
def handle_message_submit():
    if st.session_state.user_message:
        # Get the message from session state
        user_input = st.session_state.user_message
        
        # Add user message to chat
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        user_message = {"role": "user", "content": user_input, "timestamp": timestamp}
        st.session_state.messages.append(user_message)
        
        # Clear the input field by setting the session state variable
        st.session_state.user_message = ""
        
        # Force a rerun to update the UI and process the AI response
        st.experimental_rerun()

# Main function
def main():
    # Load custom CSS
    load_css()
    
    # Sidebar for settings and options
    with st.sidebar:
        st.title("AI Chatbot Settings")
        
        # Model selection
        selected_model = st.selectbox(
            "Select AI Model",
            list(MODELS.keys()),
            index=0
        )
        
        # Theme selection (simplified for now)
        st.subheader("Theme")
        st.write("Current theme: Default (#f4f3fa background)")
        
        # Chat history management
        st.subheader("Chat Management")
        
        # Rename current chat
        new_chat_name = st.text_input("Rename Current Chat", st.session_state.current_chat_name)
        if new_chat_name != st.session_state.current_chat_name:
            st.session_state.current_chat_name = new_chat_name
        
        # Save current chat
        if st.button("Save Current Chat"):
            if st.session_state.messages:
                st.session_state.chat_histories[st.session_state.current_chat_name] = st.session_state.messages.copy()
                st.success(f"Chat '{st.session_state.current_chat_name}' saved!")
        
        # Load saved chat
        if st.session_state.chat_histories:
            selected_chat = st.selectbox(
                "Load Saved Chat",
                list(st.session_state.chat_histories.keys())
            )
            
            if st.button("Load Selected Chat"):
                st.session_state.messages = st.session_state.chat_histories[selected_chat].copy()
                st.session_state.current_chat_name = selected_chat
                st.experimental_rerun()
        
        # Download chat history
        if st.session_state.messages:
            st.markdown(get_csv_download_link(st.session_state.messages), unsafe_allow_html=True)
        
        # Clear chat
        if st.button("Clear Current Chat"):
            st.session_state.messages = []
            st.experimental_rerun()
    
    # Main chat interface
    st.title("AI Chatbot")
    st.write("Chat with AI using different models from OpenRouter.ai")
    
    # Display chat messages
    display_messages()
    
    # Process AI response if there are messages and the last one is from the user
    if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
        # Display typing indicator
        with st.empty():
            display_typing_indicator()
            
            # Get AI response
            api_messages = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ai_response = get_ai_response(api_messages, MODELS[selected_model])
            
            # Add AI response to chat
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            ai_message = {"role": "assistant", "content": ai_response, "timestamp": timestamp}
            st.session_state.messages.append(ai_message)
            
            # Refresh display
            time.sleep(0.5)  # Small delay for animation effect
            st.experimental_rerun()
    
    # Input for new message - using on_change callback to handle submission
    st.text_input(
        "Type your message here...", 
        key="user_message",
        on_change=handle_message_submit
    )
    
    # JavaScript for keyboard shortcuts and interactivity
    st.markdown("""
    <script>
    // Enter key to submit
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            const inputElement = document.querySelector('input[aria-label="Type your message here..."]');
            if (document.activeElement === inputElement && inputElement.value.trim() !== '') {
                // Trigger the change event to activate the on_change callback
                const event = new Event('change', { bubbles: true });
                inputElement.dispatchEvent(event);
            }
        }
    });
    
    // Function to unpin messages
    function unpin(index) {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            value: {action: 'unpin', index: index}
        }, '*');
    }
    </script>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Create assets directory if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Run the app
    main()
