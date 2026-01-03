# Rapor Scanner Configuration

# Application Info
APP_TITLE = "📊 Rekap Nilai Rapor K13 (Kurikulum 2013)"
APP_DESCRIPTION = "Ekstrak nilai P (Pengetahuan), K (Keterampilan), A (Nilai Akhir) dari PDF Rapor Digital"
APP_AUTHOR = "@em_rival"
APP_TEAM = "PMJ IT Team"

# OCR Settings (dapat di-override dari UI)
OCR_DPI = 200                      # Default: 200, Range: 150-400
OCR_CONFIDENCE_THRESHOLD = 0.5     # Default: 0.5, Range: 0.1-0.9
OCR_LANGUAGES = ['id', 'en']       # Bahasa yang didukung
OCR_GPU = False                    # True jika ada GPU CUDA

# OCR Preprocessing Options
OCR_PREPROCESSING = {
    'grayscale': True,             # Convert ke grayscale
    'contrast': 1.5,               # Contrast enhancement (1.0 = normal)
    'sharpness': 1.2,              # Sharpness enhancement (1.0 = normal)
    'denoise': False,              # Noise reduction (lebih lambat)
    'binarize': False,             # Convert ke pure B&W
    'binarize_threshold': 128,     # Threshold untuk binarization (0-255)
}

# Export Settings
EXCEL_COLUMN_WIDTH_DEFAULT = 12
EXCEL_COLUMN_WIDTH_NAME = 25

# Value formatting
MAX_NAME_LENGTH = 100

# ===========================================
# REKOMENDASI RESOURCE CONTAINER
# ===========================================
# 
# MINIMUM (tanpa OCR / hanya PDF digital):
#   - RAM: 512MB
#   - CPU: 1 core
#   - Disk: 2GB
#
# RECOMMENDED (dengan OCR):
#   - RAM: 2GB (EasyOCR load model ~1GB)
#   - CPU: 2 cores
#   - Disk: 5GB
#
# OPTIMAL (OCR dengan GPU):
#   - RAM: 4GB
#   - CPU: 2-4 cores
#   - GPU: NVIDIA dengan CUDA
#   - Disk: 10GB
#
# ==========================================
