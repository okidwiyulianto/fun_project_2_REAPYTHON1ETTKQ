# 🤖✨ AI Chatbot dengan Streamlit dan OpenRouter API

Aplikasi chatbot AI ini dibuat menggunakan Streamlit dan OpenRouter API, dengan tampilan chat bubble yang unik dan lucu, dilengkapi emoji, timestamp, animasi saat proses respons dan hanya dapat digunakan dengan sistem API key pribadi anda sendiri. Aplikasi tetap fokus pada privasi dan keamanan.

## Fitur Utama

- 🔥 Menggunakan API Key pribadi (data tidak dikirim ke pihak ketiga!)
- 🤖 Integrasi dengan berbagai model AI melalui OpenRouter API
- 💬 Tampilan chat bubble yang unik dan lucu
- 😊 Emoji
- 🕒 Timestamp pada setiap pesan
- ✨ Animasi saat proses respons
- 🔄 Opsi untuk mengubah model AI yang digunakan
- 💾 Fitur untuk menyimpan dan mengunduh riwayat chat
- 🗑️ Fitur untuk menghapus riwayat chat
- 🛡️ Penanganan error yang komprehensif

## Persyaratan

- Python 3.6 atau lebih baru
- Ada di requirements.txt

## Instalasi

1. Pastikan Python sudah terinstal di komputer Anda
2. Clone atau download repository ini
```bash
git clone https://github.com/okidwiyulianto/fun_project_2_REAPYTHON1ETTKQ.git
```
3. Buka terminal dan navigasi ke direktori proyek
4. Instal dependensi yang diperlukan:

```bash
pip install requirements.txt
```

## Cara Penggunaan

1. Jalankan aplikasi dengan perintah:

```bash
streamlit run app.py
```

2. Aplikasi akan terbuka di browser Anda secara otomatis (biasanya di http://localhost:8501)
3. Ketik pesan Anda di kolom input di bagian bawah layar
4. Klik tombol "Kirim" atau tekan Enter untuk mengirim pesan
5. Tunggu respons dari AI
6. Gunakan sidebar untuk:
   - Mengubah model AI yang digunakan
   - Mengunduh riwayat chat
   - Menghapus riwayat chat

## Kustomisasi

### Mengubah Model AI

Anda dapat menambahkan atau mengubah pilihan model AI yang tersedia dengan mengedit variabel `MODELS`

```python
MODELS = {
    "Claude 3 Opus": "anthropic/claude-3-opus:beta",
    "Claude 3 Sonnet": "anthropic/claude-3-sonnet:beta",
    "Claude 3 Haiku": "anthropic/claude-3-haiku",
    "GPT-4o": "openai/gpt-4o",
    "GPT-4 Turbo": "openai/gpt-4-turbo",
    "Mistral Large": "mistralai/mistral-large",
    "Llama 3 70B": "meta-llama/llama-3-70b-instruct"
}
```

## Penanganan Error

Aplikasi ini dilengkapi dengan penanganan error yang komprehensif:

- Penanganan error untuk masalah koneksi API
- Penanganan error untuk respons API yang tidak valid
- Penanganan error untuk input yang tidak valid

## Struktur Kode

- `app.py`: File utama aplikasi
- `styles.css`: File CSS untuk styling tambahan
- `README.md`: Dokumentasi aplikasi

## Catatan Penting

- Aplikasi hanya dapat digunakan jika menggunakan API key AI, untuk itu gunakan API key anda pribadi masing-masing.
- Aplikasi ini dibuat dengan mengutamakan menggunakan OpenRouter API yang memungkinkan akses ke berbagai model AI dari berbagai penyedia.

## Troubleshooting

### Aplikasi tidak dapat terhubung ke API

- Pastikan Anda memiliki koneksi internet yang stabil
- Periksa apakah API key masih valid
- Periksa apakah model yang dipilih tersedia di OpenRouter

### Animasi atau styling tidak muncul

- Pastikan file `styles.css` berada di direktori yang sama dengan `app.py`
- Pastikan browser Anda mendukung CSS animations

### Error saat menjalankan aplikasi

- Pastikan semua dependensi terinstal dengan benar
- Periksa versi Python Anda (minimal 3.6)
- Periksa log error untuk informasi lebih lanjut

## Pengembangan Lebih Lanjut

Beberapa ide untuk pengembangan lebih lanjut:

- Menambahkan fitur text-to-speech untuk membacakan respons AI
- Menambahkan fitur speech-to-text untuk input suara
- Menambahkan fitur untuk mengunggah dan menganalisis file
- Menambahkan fitur untuk mengubah bahasa antarmuka
- Menambahkan fitur untuk menyimpan dan memuat sesi chat dari file

## Lisensi

Aplikasi ini bersifat open source dan dapat digunakan secara bebas.
