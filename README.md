# ⚡ Corent — Auto-Discussion AI Builder

Corent adalah CLI/Web tool untuk membuat **AI Agent mandiri (offline-ready)** tanpa training manual. Menggunakan teknik **Synthetic Data Generation** melalui dual-model conversation (OpenRouter/Groq). Data otomatis dikategorikan dan disimpan sebagai JSON di folder `data/`.

## 📁 Struktur Proyek

```
Corent/
├── main.py                 # Entry point CLI
├── setup.py                # Python package installer
├── requirements.txt        # Python dependencies
├── .env.example            # Template environment
├── config.json             # Auto-generated config
├── core/
│   ├── installer.py        # Fase 1: Install wizard
│   ├── config.py           # Config manager
│   ├── provider.py         # Fase 3: Provider selection
│   ├── json_store.py       # JSON storage engine
│   └── offline_compiler.py # Fase 6: RAG prep
├── ai/
│   ├── models.py           # API wrappers
│   ├── prompts.py          # Prompt templates
│   └── discussion.py       # Fase 5: Auto-discussion
├── web/
│   ├── server.js           # Express dashboard
│   └── public/             # Frontend assets
├── data/
│   ├── conversations/      # Per-turn JSON files
│   └── categories/         # Per-category JSONL files
└── output/                 # Compiled datasets
```

## 🚀 Cara Pakai

```bash
# 1. Install & jalankan
python main.py

# 2. Ikuti wizard 6 fase:
#    - Install dependencies otomatis
#    - Masukkan nama agent
#    - Pilih provider (OpenRouter / Groq)
#    - Masukkan API Key & pilih model
#    - Auto-discussion berjalan
#    - Dataset siap di /output

# 3. Buka web dashboard (setelah wizard selesai)
cd web && npm start
# Buka http://localhost:3000
```

## 🔧 Requirements

- Python >= 3.8
- Node.js >= 16
- API Key dari OpenRouter (https://openrouter.ai) atau Groq (https://console.groq.com)
