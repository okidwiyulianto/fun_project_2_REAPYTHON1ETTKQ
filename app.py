import streamlit as st
import requests
import datetime
import random

# --- Konfigurasi API ---
OPENROUTER_API_KEY = "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"
MODEL = "deepseek/deepseek-chat-v3-0324"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# --- Emoji Lucu ---
USER_EMOJIS = ["👨‍💻"]
BOT_EMOJIS = ["🤖"]
ERROR_EMOJIS = ["🙊", "🙈", "💔", "🌧️"]

# --- Custom CSS untuk Chat Bubbles ---
CSS = """
<style>
div.stTextInput > div > div > input {
    background-color: #f0f0f0;
}
.chat-row {
    display: flex;
    margin-bottom: 15px;
}
.chat-bubble {
    border-radius: 20px;
    padding: 15px;
    max-width: 75%;
    position: relative;
    font-size: 16px;
    line-height: 1.4;
}
.user-row {
    justify-content: flex-end;
}
.bot-row {
    justify-content: flex-start;
}
.user-bubble {
    background: rgb(220, 248, 198);
    color: black;
    border-bottom-right-radius: 5px;
}
.bot-bubble {
    background: #f4f3fa; 
    color: black;
    border-bottom-left-radius: 5px;
}
.timestamp {
    font-size: 12px;
    margin-top: 5px;
    opacity: 0.7;
    width: 100%;
    text-align: right;
    color: #000;
}
.avatar {
    font-size: 24px;
    margin: 0 8px;
    align-self: flex-end;
}
.typing-indicator {
    display: flex;
    align-items: center;
    margin-left: 40px;
    margin-bottom: 20px;
}
.typing-dot {
    width: 8px;
    height: 8px;
    margin: 0 2px;
    background: #8a8a8a;
    border-radius: 50%;
    opacity: 0.7;
    animation: typing 1.4s infinite ease-in-out;
}
.typing-dot:nth-child(1) { animation-delay: 0s; }
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes typing {
    0%, 60%, 100% { transform: translateY(0); }
    30% { transform: translateY(-10px); }
}
button.delete-button {
    background-color: #ff6b6b !important;
    color: white !important;
    border-radius: 12px !important;
    font-weight: bold !important;
}
button.delete-button:hover {
    background-color: #ff5252 !important;
}
</style>
"""

def get_random_emoji(emoji_list):
    """Mengambil emoji acak dari daftar."""
    return random.choice(emoji_list)

def get_timestamp():
    """Mengambil timestamp saat ini."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def get_ai_response(user_input, history):
    """Mengambil respons AI dari OpenRouter API."""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "http://localhost:8501",
            "X-Title": "AI Chatbot Streamlit"
        }
        
        # Membuat riwayat pesan untuk konteks
        messages = [
            {"role": "system", "content": "You are DeepSeek Chat, an AI assistant created by DeepSeek. Your purpose is to provide helpful, accurate, and engaging responses while adhering to ethical guidelines. You can assist with a wide range of topics, from general knowledge to technical support, but avoid harmful, illegal, or misleading content."}
        ]
        
        # Tambahkan riwayat pesan ke payload
        for msg in history:
            messages.append({"role": msg["role"], "content": msg["content"]})
            
        # Tambahkan pesan user terbaru
        messages.append({"role": "user", "content": user_input})
        
        payload = {
            "model": MODEL,
            "messages": messages
        }
        
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"{get_random_emoji(ERROR_EMOJIS)} Maaf, ada kesalahan. (Kode: {response.status_code})"
            
    except Exception as e:
        return f"{get_random_emoji(ERROR_EMOJIS)} Terjadi kesalahan: {str(e)}"

def clear_chat():
    """Menghapus seluruh riwayat chat"""
    st.session_state.messages = []
    st.session_state.waiting_for_response = False

# --- Setup UI ---
st.set_page_config(page_title="AI Chatbot", page_icon="🤖", layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

st.title("AI Chatbot Bubble Style")
st.markdown(f"Powered by {MODEL} via OpenRouter")

# Inisialisasi session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "waiting_for_response" not in st.session_state:
    st.session_state.waiting_for_response = False

# Tampilkan riwayat chat
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        if message["role"] == "user":
            # User message
            st.markdown(f"""
            <div class="chat-row user-row">
                <div class="chat-bubble user-bubble">
                    {message["content"]}
                    <div class="timestamp">{message["timestamp"]}</div>
                </div>
                <div class="avatar">{message["emoji"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            # Bot message
            st.markdown(f"""
            <div class="chat-row bot-row">
                <div class="avatar">{message["emoji"]}</div>
                <div class="chat-bubble bot-bubble">
                    {message["content"]}
                    <div class="timestamp">{message["timestamp"]}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Tampilkan indikator "typing" jika AI sedang memproses
    if st.session_state.waiting_for_response:
        st.markdown("""
        <div class="typing-indicator">
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        </div>
        """, unsafe_allow_html=True)

# Input dari user
user_input = st.chat_input("Tulis pesan di sini...")

# Proses input
if user_input:
    # Tambahkan pesan user ke history
    user_emoji = get_random_emoji(USER_EMOJIS)
    timestamp = get_timestamp()
    
    # Simpan ke session state
    st.session_state.messages.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp,
        "emoji": user_emoji
    })
    
    # Set status waiting
    st.session_state.waiting_for_response = True
    
    # Tampilkan pesan user dulu
    st.rerun()

# Cek apakah sedang menunggu respon AI
if st.session_state.waiting_for_response:
    # Buat salinan messages untuk konteks
    history = []
    if len(st.session_state.messages) > 1:
        history = [{"role": msg["role"], "content": msg["content"]} 
                  for msg in st.session_state.messages[:-1]]
    
    last_user_message = st.session_state.messages[-1]["content"]
    
    # Dapatkan respon AI
    ai_response = get_ai_response(last_user_message, history)
    
    # Tambahkan respon AI ke history
    bot_emoji = get_random_emoji(BOT_EMOJIS)
    ai_timestamp = get_timestamp()
    
    # Simpan ke session state
    st.session_state.messages.append({
        "role": "assistant",
        "content": ai_response,
        "timestamp": ai_timestamp,
        "emoji": bot_emoji
    })
    
    # Reset status waiting
    st.session_state.waiting_for_response = False
    
    # Refresh halaman untuk menampilkan chat baru
    st.rerun()
