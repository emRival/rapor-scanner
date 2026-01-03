# 📊 Rapor Scanner

Aplikasi untuk mengekstrak nilai dari PDF Rapor K13 (Kurikulum 2013) secara otomatis.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Fitur

- 📄 **Extract PDF Digital** - Ekstrak nilai dari PDF rapor digital
- 🔬 **OCR Support** - Support PDF scan dengan EasyOCR (eksperimental)
- 📊 **Tabel Rekap** - Tampilan tabel dengan Total, Rata-rata, Ranking
- 📈 **Grafik Perkembangan** - Analisis trend nilai antar semester
- 📥 **Export Excel** - Download rekap dalam format Excel

## 🚀 Quick Install (Ubuntu/Debian)

### One-Click Installation
```bash
curl -sSL https://raw.githubusercontent.com/emRival/rapor-scanner/main/install.sh | sudo bash
```

### Manual Installation
```bash
# Clone repository
git clone https://github.com/emRival/rapor-scanner.git
cd rapor-scanner

# Install dependencies
sudo apt install python3 python3-pip python3-venv poppler-utils
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
streamlit run app.py
```

## 🖥️ Access

Setelah instalasi, akses aplikasi di:
- **Local:** http://localhost:8501
- **Network:** http://YOUR_IP:8501

## 📁 Struktur Project

```
rapor-scanner/
├── app.py              # Entry point
├── config.py           # Konfigurasi
├── requirements.txt    # Dependencies
├── install.sh          # Installation script
│
├── core/               # Core logic
│   ├── extractor.py    # PDF digital extraction
│   ├── ocr.py          # EasyOCR extraction
│   └── parser.py       # Text parsing
│
├── utils/              # Utilities
│   ├── formatting.py   # Format nilai
│   └── excel.py        # Excel export
│
└── ui/                 # User Interface
    ├── styles.py       # CSS styling
    ├── tab_tabel.py    # Tab Tabel Rekap
    └── tab_grafik.py   # Tab Grafik
```

## 🔧 Manage Service

```bash
# Status
sudo systemctl status rapor-scanner

# Stop
sudo systemctl stop rapor-scanner

# Start
sudo systemctl start rapor-scanner

# Restart
sudo systemctl restart rapor-scanner

# View logs
sudo journalctl -u rapor-scanner -f
```

## 📝 Requirements

- Python 3.9+
- Ubuntu/Debian (untuk auto-install)
- poppler-utils (untuk pdf2image)

## 👨‍💻 Author

**@em_rival** - PMJ IT Team

## 📄 License

MIT License
