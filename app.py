import streamlit as st
import requests
import json
import time
import datetime
import random
import os

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Definisi warna sesuai preferensi pengguna
COLORS = {
    "background": "#f4f3fa",
    "text_dark": "#000000",
    "text_medium": "#2b2b2b",
    "primary": "#75b2dd",
    "secondary": "#fcd116",
    "accent": "#0f2b5b"
}

# Daftar emoji yang akan digunakan secara acak
EMOJIS = ["😊", "🤔", "🧐", "💡", "✨", "🚀", "🎯", "🔍", "📚", "💭", "🌟", "🎨", "🎮", "🎵", "🌈"]

# Daftar model AI yang tersedia di OpenRouter
MODELS = {
    "Claude 3 Opus": "anthropic/claude-3-opus:beta",
    "Claude 3 Sonnet": "anthropic/claude-3-sonnet:beta",
    "Claude 3 Haiku": "anthropic/claude-3-haiku",
    "GPT-4o": "openai/gpt-4o",
    "GPT-4 Turbo": "openai/gpt-4-turbo",
    "Mistral Large": "mistralai/mistral-large",
    "Llama 3 70B": "meta-llama/llama-3-70b-instruct"
}

# Inisialisasi session state jika belum ada
if "messages" not in st.session_state:
    st.session_state.messages = []

if "selected_model" not in st.session_state:
    st.session_state.selected_model = "Claude 3 Haiku"

# Fungsi untuk mendapatkan respons dari OpenRouter API
def get_ai_response(prompt, model):
    api_key = "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"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": MODELS[model],
        "messages": [
            {"role": "system", "content": "Kamu adalah asisten AI yang ramah, membantu, dan informatif. Berikan jawaban yang jelas dan bermanfaat."},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(data)
        )
        response.raise_for_status()  # Raise exception for HTTP errors
        
        result = response.json()
        if "choices" in result and len(result["choices"]) > 0:
            return result["choices"][0]["message"]["content"]
        else:
            return "Maaf, saya tidak dapat memproses permintaan Anda saat ini. Silakan coba lagi."
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error saat menghubungi API: {str(e)}")
        return f"Terjadi kesalahan saat berkomunikasi dengan API: {str(e)}"
    
    except (KeyError, json.JSONDecodeError) as e:
        st.error(f"Error saat memproses respons API: {str(e)}")
        return "Terjadi kesalahan saat memproses respons dari API."

# Custom CSS untuk styling
def load_css():
    # Baca file CSS eksternal jika ada
    css_file = os.path.join(os.path.dirname(__file__), "styles.css")
    external_css = ""
    if os.path.exists(css_file):
        with open(css_file, "r") as f:
            external_css = f.read()
    
    # Gabungkan dengan CSS dasar
    st.markdown(f"""
    <style>
    .main {{
        background-color: {COLORS["background"]};
    }}
    
    .chat-container {{
        padding: 20px;
        border-radius: 15px;
        margin-bottom: 20px;
        max-height: 600px;
        overflow-y: auto;
    }}
    
    .user-bubble {{
        background-color: {COLORS["primary"]};
        color: white;
        border-radius: 18px 18px 0 18px;
        padding: 12px 18px;
        margin: 10px 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: relative;
        animation: slide-in-right 0.3s ease-out;
    }}
    
    .ai-bubble {{
        background-color: {COLORS["secondary"]};
        color: {COLORS["text_dark"]};
        border-radius: 18px 18px 18px 0;
        padding: 12px 18px;
        margin: 10px 0;
        max-width: 80%;
        float: left;
        clear: both;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: relative;
        animation: slide-in-left 0.3s ease-out;
    }}
    
    .timestamp {{
        font-size: 0.7em;
        color: rgba(255,255,255,0.7);
        margin-top: 5px;
        text-align: right;
    }}
    
    .ai-timestamp {{
        color: rgba(0,0,0,0.5);
    }}
    
    .emoji-prefix {{
        margin-right: 8px;
        font-size: 1.2em;
    }}
    
    @keyframes slide-in-right {{
        0% {{ transform: translateX(100px); opacity: 0; }}
        100% {{ transform: translateX(0); opacity: 1; }}
    }}
    
    @keyframes slide-in-left {{
        0% {{ transform: translateX(-100px); opacity: 0; }}
        100% {{ transform: translateX(0); opacity: 1; }}
    }}
    
    @keyframes thinking {{
        0% {{ opacity: 0.3; }}
        50% {{ opacity: 1; }}
        100% {{ opacity: 0.3; }}
    }}
    
    .thinking-animation {{
        display: flex;
        align-items: center;
        margin: 10px 0;
        float: left;
        clear: both;
        animation: slide-in-left 0.3s ease-out;
    }}
    
    .thinking-dot {{
        height: 12px;
        width: 12px;
        margin: 0 3px;
        background-color: {COLORS["accent"]};
        border-radius: 50%;
        display: inline-block;
        animation: thinking 1.5s infinite;
    }}
    
    .thinking-dot:nth-child(2) {{
        animation-delay: 0.2s;
    }}
    
    .thinking-dot:nth-child(3) {{
        animation-delay: 0.4s;
    }}
    
    .stTextInput input {{
        border-radius: 25px;
        border: 2px solid {COLORS["primary"]};
        padding: 10px 15px;
        font-size: 16px;
    }}
    
    .stButton > button {{
        border-radius: 25px;
        background-color: {COLORS["accent"]};
        color: white;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS["primary"]};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    
    .model-selector {{
        background-color: white;
        border-radius: 10px;
        padding: 10px;
        margin-bottom: 20px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    
    .clear-button {{
        background-color: #ff6b6b !important;
    }}
    
    .download-button {{
        background-color: #4caf50 !important;
    }}
    
    .stSelectbox {{
        margin-bottom: 0 !important;
    }}
    
    {external_css}
    </style>
    """, unsafe_allow_html=True)

# Fungsi untuk menampilkan animasi "thinking"
def show_thinking_animation():
    with st.container():
        st.markdown("""
        <div class="thinking-animation">
            <div class="ai-bubble" style="padding: 8px 15px;">
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
                <div class="thinking-dot"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Fungsi untuk menampilkan pesan dalam chat
def display_messages():
    for message in st.session_state.messages:
        if message["role"] == "user":
            emoji = random.choice(EMOJIS)
            st.markdown(f"""
            <div class="user-bubble">
                <span class="emoji-prefix">{emoji}</span>
                {message["content"]}
                <div class="timestamp">{message["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            emoji = random.choice(EMOJIS)
            st.markdown(f"""
            <div class="ai-bubble">
                <span class="emoji-prefix">{emoji}</span>
                {message["content"]}
                <div class="timestamp ai-timestamp">{message["timestamp"]}</div>
            </div>
            """, unsafe_allow_html=True)

# Fungsi untuk menyimpan riwayat chat ke file
def save_chat_history():
    if not st.session_state.messages:
        st.warning("Tidak ada riwayat chat untuk disimpan.")
        return
    
    chat_history = ""
    for message in st.session_state.messages:
        prefix = "Anda" if message["role"] == "user" else "AI"
        chat_history += f"{prefix} ({message['timestamp']}): {message['content']}\n\n"
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"chat_history_{timestamp}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write(chat_history)
    
    return filename

# Fungsi utama aplikasi
def main():
    load_css()
    
    st.title("🤖 AI Chatbot")
    st.markdown("Chat dengan AI menggunakan OpenRouter API")
    
    # Sidebar untuk pengaturan
    with st.sidebar:
        st.header("Pengaturan")
        
        # Pemilihan model
        st.markdown('<div class="model-selector">', unsafe_allow_html=True)
        selected_model = st.selectbox(
            "Pilih Model AI:",
            list(MODELS.keys()),
            index=list(MODELS.keys()).index(st.session_state.selected_model)
        )
        st.session_state.selected_model = selected_model
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tombol untuk mengunduh riwayat chat
        if st.button("💾 Unduh Riwayat Chat", key="download"):
            filename = save_chat_history()
            if filename:
                with open(filename, "r", encoding="utf-8") as f:
                    chat_content = f.read()
                st.download_button(
                    label="📥 Klik untuk Mengunduh",
                    data=chat_content,
                    file_name=filename,
                    mime="text/plain",
                    key="download_button"
                )
        
        # Tombol untuk menghapus riwayat chat
        if st.button("🗑️ Hapus Riwayat Chat", key="clear"):
            st.session_state.messages = []
            st.experimental_rerun()
    
    # Container untuk chat
    chat_container = st.container()
    
    # Input pengguna
    with st.container():
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input("Ketik pesan Anda di sini:", key="user_input")
        with col2:
            send_button = st.button("Kirim")
    
    # Menampilkan chat
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        display_messages()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Proses input pengguna
    if (user_input and send_button) or (user_input and st.session_state.get("user_input_submitted", False)):
        # Reset flag
        st.session_state.user_input_submitted = False
        
        # Tambahkan pesan pengguna ke riwayat
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
            "timestamp": timestamp
        })
        
        # Tampilkan animasi "thinking"
        with chat_container:
            thinking_placeholder = st.empty()
            with thinking_placeholder:
                show_thinking_animation()
        
        # Dapatkan respons dari AI
        ai_response = get_ai_response(user_input, st.session_state.selected_model)
        
        # Tambahkan respons AI ke riwayat
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        st.session_state.messages.append({
            "role": "assistant",
            "content": ai_response,
            "timestamp": timestamp
        })
        
        # Hapus animasi "thinking" dan refresh tampilan
        thinking_placeholder.empty()
        st.experimental_rerun()

if __name__ == "__main__":
    main()
