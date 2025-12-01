# Personal Chatbot with AI API (DeepSeek / Gemini)

Chatbot pribadi sederhana yang menggunakan RAG (Retrieval-Augmented Generation) untuk menjawab pertanyaan tentang diri Anda. Project ini mendukung **dua pilihan AI provider**: **DeepSeek API** atau **Google Gemini API** untuk generate response, dan menggunakan ChromaDB sebagai vector database untuk knowledge base.

## 🚀 Fitur

- ✅ RAG (Retrieval-Augmented Generation) untuk jawaban yang akurat
- ✅ Vector database menggunakan ChromaDB
- ✅ Semantic search untuk mencari informasi relevan
- ✅ Chat interface yang user-friendly
- ✅ **Dual AI Provider Support**: Pilih antara DeepSeek atau Gemini
- ✅ Easy switching antara AI providers via environment variable
- ✅ Knowledge base yang mudah dikustomisasi

## 📋 Prerequisites

- Python 3.8 atau lebih tinggi
- **Pilih salah satu atau kedua API key**:
  - DeepSeek API Key (dapatkan di https://platform.deepseek.com/)
  - Gemini API Key (dapatkan di https://makersuite.google.com/app/apikey)

## 🛠️ Installation

### 1. Clone atau Download Repository

```bash
cd "c:\Users\SulthanDR\Documents\Materi Univ\Code\On\Chatbot"
```

### 2. Buat Virtual Environment

```powershell
python -m venv venv
```

### 3. Aktifkan Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

Jika muncul error execution policy, jalankan:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

### 5. Setup Environment Variables

Buat file `.env` dari template:
```powershell
Copy-Item .env.example .env
```

Edit file `.env` dan pilih AI provider yang ingin digunakan:

**Untuk menggunakan DeepSeek:**
```env
AI_PROVIDER=deepseek
DEEPSEEK_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```

**Untuk menggunakan Gemini:**
```env
AI_PROVIDER=gemini
GEMINI_API_KEY=AIzaSyxxxxxxxxxxxxxxxxxxxxxxxx
```

**Atau isi keduanya** (bisa switch kapan saja dengan mengubah `AI_PROVIDER`)

### 6. Kustomisasi Knowledge Base

Edit file-file di folder `knowledge_base/` sesuai dengan informasi pribadi Anda:
- `bio.txt` - Biodata dan informasi tentang diri Anda
- `skills.txt` - Skill dan keahlian Anda
- `projects.txt` - Project-project yang pernah Anda kerjakan

## 🎯 Cara Menjalankan

### 1. Jalankan Aplikasi

```powershell
python app.py
```

### 2. Pilih AI Provider

Saat aplikasi dijalankan, Anda akan diminta memilih AI provider:

```
==================================================
   PERSONAL CHATBOT - AI PROVIDER SELECTION
==================================================

Pilih AI Provider yang ingin digunakan:

  [1] DeepSeek API
  [2] Google Gemini API

--------------------------------------------------

Masukkan pilihan (1/2): _
```

Ketik **1** untuk DeepSeek atau **2** untuk Gemini, lalu tekan Enter.

### 3. Buka Browser

Setelah server berjalan, buka browser dan akses:
```
http://localhost:5000
```

## 💬 Cara Menggunakan

1. Ketik pertanyaan di input box
2. Klik tombol "Kirim" atau tekan Enter
3. Bot akan menjawab berdasarkan knowledge base yang telah Anda buat

Contoh pertanyaan:
- "Siapa kamu?"
- "Apa skill yang kamu kuasai?"
- "Ceritakan tentang project yang pernah kamu buat"
- "Apa pendidikan terakhir kamu?"

## 📁 Struktur Project

```
Chatbot/
├── app.py                  # Backend Flask server
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (buat sendiri)
├── .env.example           # Template environment variables
├── .gitignore             # Git ignore file
├── README.md              # Dokumentasi
├── knowledge_base/        # Knowledge base files
│   ├── bio.txt           # Biodata
│   ├── skills.txt        # Skills
│   └── projects.txt      # Projects
├── frontend/              # Frontend files
│   ├── index.html        # HTML structure
│   ├── styles.css        # Styling
│   └── script.js         # JavaScript logic
└── chroma_db/            # ChromaDB database (auto-generated)
```

## 🔧 Konfigurasi Lanjutan

### Switching AI Provider

Untuk beralih provider, cukup stop server (Ctrl+C) dan jalankan lagi:

```powershell
python app.py
```

Lalu pilih provider yang berbeda saat diminta.

### Mengubah Model atau Parameter AI

**Untuk DeepSeek**, edit file `app.py` pada bagian `call_deepseek_api()`:
```python
data = {
    "model": "deepseek-chat",  # Ganti dengan model lain jika perlu
    "temperature": 0.7,        # Adjust creativity (0.0 - 1.0)
    "max_tokens": 1000         # Maximum response length
}
```

**Untuk Gemini**, edit file `app.py` pada bagian `call_gemini_api()`:
```python
"generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 1000,
}
```

### Mengubah Jumlah Context

Edit file `app.py` pada bagian endpoint `/api/chat`:
```python
context_chunks = query_knowledge_base(user_message, n_results=3)  # Ubah angka 3
```

## 🐛 Troubleshooting

### Error: "API key not configured"
- Pastikan file `.env` sudah dibuat dan berisi API key yang valid
- Check `AI_PROVIDER` di `.env` sesuai dengan API key yang Anda isi
- Restart server setelah menambahkan API key

### Error: "Knowledge base directory not found"
- Pastikan folder `knowledge_base/` ada dan berisi file `.txt`

### Server tidak bisa diakses
- Pastikan tidak ada aplikasi lain yang menggunakan port 5000
- Coba ubah port di `app.py`: `app.run(port=8000)`

### ChromaDB Error
- Hapus folder `chroma_db/` dan restart server untuk rebuild database

### NumPy Compatibility Error
- Install NumPy versi yang kompatibel: `pip install "numpy<2.0.0" --force-reinstall`

### Gemini API Error
- Pastikan API key valid dan aktif
- Cek quota API di Google AI Studio: https://makersuite.google.com/
- Pastikan `AI_PROVIDER=gemini` di file `.env`

## 🚢 Deployment

### Backend (Railway/Render)
1. Push code ke GitHub
2. Connect repository ke Railway/Render
3. Set environment variables:
   - `AI_PROVIDER` (pilih: `deepseek` atau `gemini`)
   - `DEEPSEEK_API_KEY` (jika pakai DeepSeek)
   - `GEMINI_API_KEY` (jika pakai Gemini)
4. Deploy

### Frontend (Vercel/Netlify)
1. Update `API_URL` di `frontend/script.js` dengan URL backend production
2. Deploy folder `frontend/` ke Vercel/Netlify

## 📝 Lisensi

Free to use untuk keperluan personal dan educational.

## 🤝 Kontribusi

Feel free to fork dan improve project ini!

## 📧 Kontak

Jika ada pertanyaan, silakan buat issue di repository ini.

---

**Happy Coding!** 🎉
