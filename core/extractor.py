"""
PDF Digital Text Extractor
Ekstrak teks dari PDF yang dihasilkan secara digital (bukan scan)
"""
import pdfplumber


def extract_text_digital(pdf_file):
    """
    Ekstrak teks dari PDF digital.
    
    Args:
        pdf_file: File object atau path ke file PDF
        
    Returns:
        tuple: (text, error_message)
            - text: Teks yang diekstrak, atau None jika gagal
            - error_message: Pesan error jika gagal, atau None jika sukses
    """
    try:
        with pdfplumber.open(pdf_file) as pdf:
            if len(pdf.pages) == 0:
                return None, "PDF tidak memiliki halaman"
            
            # Gabungkan teks dari semua halaman (untuk rapor multi-page)
            all_text = []
            for page in pdf.pages:
                text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if text:
                    all_text.append(text)
            
            if not all_text:
                return None, "Tidak dapat mengekstrak teks (mungkin PDF scan/gambar)"
            
            return '\n'.join(all_text), None
    except Exception as e:
        return None, f"Error membaca PDF: {str(e)}"
