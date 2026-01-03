# 📊 Rapor Scanner

Aplikasi untuk mengekstrak nilai dari PDF Rapor K13 (Kurikulum 2013) secara otomatis.

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Fitur

- 📄 **Extract PDF Digital** - Ekstrak nilai dari PDF rapor digital
- 🔬 **OCR Support** - Support PDF scan dengan EasyOCR (eksperimental)
- 📊 **Tabel Rekap** - Tampilan tabel dengan Total, Rata-rata, Ranking
- 📈 **Grafik Perkembangan** - Analisis trend nilai antar semester
- 📥 **Export Excel** - Download rekap dalam format Excel
- ⚙️ **OCR Settings** - Atur DPI, Confidence, Preprocessing via UI

## 🚀 Installation

### 🐧 Ubuntu 22.04 LTS (Recommended)
```bash
curl -sSL https://raw.githubusercontent.com/emRival/rapor-scanner/main/install.sh | sudo bash
```

### 🍎 macOS
```bash
curl -sSL https://raw.githubusercontent.com/emRival/rapor-scanner/main/install_mac.sh | bash
```

### 🪟 Windows
1. Download `install_windows.bat` dari [Release](https://github.com/emRival/rapor-scanner/releases)
2. Right-click → Run as Administrator
3. Install [Poppler](https://github.com/oschwartz10612/poppler-windows/releases) untuk OCR

### 📦 Manual Install
```bash
git clone https://github.com/emRival/rapor-scanner.git
cd rapor-scanner
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## 💻 System Requirements

| Spesifikasi | Minimum | Recommended |
|-------------|---------|-------------|
| **OS** | Ubuntu 20.04+ | Ubuntu 22.04 LTS |
| **RAM** | 2GB | 4GB |
| **CPU** | 2 cores | 4 cores |
| **Storage** | 5GB | 10GB |
| **Python** | 3.9+ | 3.10-3.11 |

> ⚠️ **Note:** Debian Trixie (Python 3.13) tidak disarankan karena banyak package belum ada wheel.

## 🖥️ Access

Setelah instalasi, akses aplikasi di:
- **Local:** http://localhost:8501
- **Network:** http://YOUR_IP:8501

## 📁 Project Structure

```
rapor-scanner/
├── app.py              # Entry point (~200 lines)
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── install.sh          # Ubuntu/Debian installer
├── install_mac.sh      # macOS installer
├── install_windows.bat # Windows installer
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
    └── tab_grafik.py   # Tab Grafik Perkembangan
```

## 🔧 Manage Service (Ubuntu/Debian)

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

# Update
cd /opt/rapor-scanner && git pull && sudo systemctl restart rapor-scanner
```

## ⚙️ OCR Settings

Akses di sidebar aplikasi:
- **DPI (150-400)** - Resolusi scan
- **Confidence (0.1-0.9)** - Filter akurasi
- **Preprocessing** - Grayscale, Contrast, Sharpness, Denoise, Binarize

## 📝 Changelog

### v1.0.0
- Initial release
- PDF digital & OCR extraction
- Tabel rekap dengan ranking
- Grafik perkembangan
- Export Excel
- Multi-platform support

## 👨‍💻 Author

**@em_rival** - PMJ IT Team

## 📄 License

MIT License
