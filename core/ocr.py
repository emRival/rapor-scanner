"""
OCR Extractor using EasyOCR
Ekstrak teks dari PDF scan/gambar (FITUR EKSPERIMENTAL)
"""
from config import (
    OCR_DPI, OCR_CONFIDENCE_THRESHOLD, OCR_LANGUAGES, 
    OCR_GPU, OCR_PREPROCESSING
)

# Lazy imports untuk performance
OCR_AVAILABLE = False
OCR_READER = None

try:
    import easyocr
    from pdf2image import convert_from_bytes
    from PIL import Image, ImageEnhance, ImageFilter
    OCR_AVAILABLE = True
except ImportError:
    pass


def is_ocr_available():
    """Check if OCR dependencies are available"""
    return OCR_AVAILABLE


def get_ocr_reader(use_gpu=None):
    """Get or initialize OCR reader (lazy loading)"""
    global OCR_READER
    gpu = use_gpu if use_gpu is not None else OCR_GPU
    
    if OCR_READER is None and OCR_AVAILABLE:
        OCR_READER = easyocr.Reader(OCR_LANGUAGES, gpu=gpu, verbose=False)
    return OCR_READER


def preprocess_image(image, settings=None):
    """
    Preprocess image untuk meningkatkan akurasi OCR.
    
    Args:
        image: PIL Image
        settings: dict dengan opsi preprocessing (override config)
        
    Returns:
        PIL Image yang sudah diproses
    """
    opts = settings or OCR_PREPROCESSING
    
    # 1. Convert to grayscale
    if opts.get('grayscale', True):
        image = image.convert('L')
    
    # 2. Enhance contrast
    contrast = opts.get('contrast', 1.0)
    if contrast != 1.0:
        image = ImageEnhance.Contrast(image).enhance(contrast)
    
    # 3. Enhance sharpness
    sharpness = opts.get('sharpness', 1.0)
    if sharpness != 1.0:
        image = ImageEnhance.Sharpness(image).enhance(sharpness)
    
    # 4. Denoise (optional, slower)
    if opts.get('denoise', False):
        image = image.filter(ImageFilter.MedianFilter(size=3))
    
    # 5. Binarization (optional)
    if opts.get('binarize', False):
        threshold = opts.get('binarize_threshold', 128)
        image = image.point(lambda x: 0 if x < threshold else 255, '1')
        image = image.convert('L')  # Convert back to grayscale for OCR
    
    return image


def extract_text_ocr(pdf_bytes, dpi=None, confidence=None, preprocess_settings=None, use_gpu=None):
    """
    Ekstrak teks dari PDF scan menggunakan EasyOCR (FITUR EKSPERIMENTAL).
    
    Args:
        pdf_bytes: Bytes content dari file PDF
        dpi: DPI untuk konversi (default dari config)
        confidence: Confidence threshold (default dari config)
        preprocess_settings: Dict dengan opsi preprocessing (override config)
        use_gpu: Boolean untuk GPU usage (override config)
        
    Returns:
        tuple: (text, error_message)
    """
    if not OCR_AVAILABLE:
        return None, "OCR tidak tersedia (easyocr/pdf2image belum diinstall)"
    
    try:
        import numpy as np
        
        # Use provided values or defaults from config
        ocr_dpi = dpi or OCR_DPI
        ocr_confidence = confidence or OCR_CONFIDENCE_THRESHOLD
        
        reader = get_ocr_reader(use_gpu)
        if reader is None:
            return None, "Gagal inisialisasi OCR reader"
        
        # Convert PDF ke gambar
        images = convert_from_bytes(pdf_bytes, dpi=ocr_dpi)
        
        if not images:
            return None, "Tidak dapat mengkonversi PDF ke gambar"
        
        all_text = []
        for i, image in enumerate(images):
            # Preprocess image
            processed_img = preprocess_image(image, preprocess_settings)
            
            # Convert to numpy array untuk EasyOCR
            img_array = np.array(processed_img)
            
            # Jalankan OCR
            results = reader.readtext(img_array)
            
            # Filter hasil dengan confidence > threshold
            good_results = [(bbox, text, conf) for (bbox, text, conf) in results 
                           if conf > ocr_confidence]
            
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
