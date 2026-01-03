"""
OCR Extractor using EasyOCR
Ekstrak teks dari PDF scan/gambar (FITUR EKSPERIMENTAL)
"""
from config import OCR_DPI, OCR_CONFIDENCE_THRESHOLD, OCR_LANGUAGES

# Lazy imports untuk performance
OCR_AVAILABLE = False
OCR_READER = None

try:
    import easyocr
    from pdf2image import convert_from_bytes
    from PIL import Image
    OCR_AVAILABLE = True
except ImportError:
    pass


def is_ocr_available():
    """Check if OCR dependencies are available"""
    return OCR_AVAILABLE


def get_ocr_reader():
    """Get or initialize OCR reader (lazy loading)"""
    global OCR_READER
    if OCR_READER is None and OCR_AVAILABLE:
        OCR_READER = easyocr.Reader(OCR_LANGUAGES, gpu=False, verbose=False)
    return OCR_READER


def extract_text_ocr(pdf_bytes):
    """
    Ekstrak teks dari PDF scan menggunakan EasyOCR (FITUR EKSPERIMENTAL).
    
    Args:
        pdf_bytes: Bytes content dari file PDF
        
    Returns:
        tuple: (text, error_message)
    """
    if not OCR_AVAILABLE:
        return None, "OCR tidak tersedia (easyocr/pdf2image belum diinstall)"
    
    try:
        import numpy as np
        
        reader = get_ocr_reader()
        if reader is None:
            return None, "Gagal inisialisasi OCR reader"
        
        # Convert PDF ke gambar
        images = convert_from_bytes(pdf_bytes, dpi=OCR_DPI)
        
        if not images:
            return None, "Tidak dapat mengkonversi PDF ke gambar"
        
        all_text = []
        for i, image in enumerate(images):
            # Convert PIL Image ke numpy array untuk EasyOCR
            img_array = np.array(image)
            
            # Jalankan OCR
            results = reader.readtext(img_array)
            
            # Filter hasil dengan confidence > threshold
            good_results = [(bbox, text, conf) for (bbox, text, conf) in results 
                           if conf > OCR_CONFIDENCE_THRESHOLD]
            
            # Kelompokkan berdasarkan posisi Y (baris)
            rows = {}
            for (bbox, text, conf) in good_results:
                y_center = (bbox[0][1] + bbox[2][1]) / 2
                y_row = round(y_center / 20) * 20
                
                if y_row not in rows:
                    rows[y_row] = []
                rows[y_row].append((bbox[0][0], text))
            
            # Susun teks per baris, urut berdasarkan posisi X
            page_lines = []
            for y in sorted(rows.keys()):
                row_items = sorted(rows[y], key=lambda x: x[0])
                line_text = ' '.join([item[1] for item in row_items])
                page_lines.append(line_text)
            
            if page_lines:
                all_text.append('\n'.join(page_lines))
        
        if not all_text:
            return None, "OCR tidak dapat mendeteksi teks dari gambar"
        
        return '\n'.join(all_text), None
    except Exception as e:
        return None, f"Error OCR: {str(e)}"
