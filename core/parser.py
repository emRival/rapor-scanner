"""
Rapor Data Parser
Parse teks rapor menjadi struktur data terstruktur
"""
import re
from config import MAX_NAME_LENGTH


def parse_rapor_data(text):
    """
    Parse data rapor dari teks.
    
    Args:
        text: Teks hasil ekstraksi dari PDF
        
    Returns:
        dict: Data rapor dengan keys: Nama, Semester, Nilai, Warnings
    """
    data = {
        "Nama": None,
        "Semester": None,
        "Nilai": [],
        "Warnings": []
    }
    
    if not text or len(text.strip()) < 50:
        data["Warnings"].append("Teks terlalu pendek atau kosong")
        return data

    # 1. Cari Nama (multiple patterns)
    name_patterns = [
        r"Nama Peserta Didik\s*[:;]?\s*(.*)",
        r"Nama\s*[:;]?\s*([A-Z][a-zA-Z\s]+)",
        r"Nama Siswa\s*[:;]?\s*(.*)"
    ]
    for pattern in name_patterns:
        name_match = re.search(pattern, text, re.IGNORECASE)
        if name_match:
            raw_name = name_match.group(1).strip()
            data["Nama"] = raw_name.lstrip(": ").strip()[:MAX_NAME_LENGTH]
            break
    
    if not data["Nama"]:
        data["Warnings"].append("Nama siswa tidak ditemukan")

    # 2. Cari Semester (multiple patterns)
    sem_patterns = [
        r"Semester\s*[:;]?\s*(\d+)",
        r"Semester\s*[:;]?\s*(Ganjil|Genap|I+|[VvIi]+)",
        r"Sem\.?\s*[:;]?\s*(\d+)"
    ]
    for pattern in sem_patterns:
        sem_match = re.search(pattern, text, re.IGNORECASE)
        if sem_match:
            sem_val = sem_match.group(1).strip()
            if sem_val.lower() == 'ganjil':
                sem_val = '1'
            elif sem_val.lower() == 'genap':
                sem_val = '2'
            data["Semester"] = sem_val
            break
    
    if not data["Semester"]:
        data["Warnings"].append("Semester tidak ditemukan")

    # 3. Cari Nilai
    lines = text.split('\n')
    nilai_pattern = r"(\d{2,3}(?:[,\.]\d{1,2})?)"
    patterns = [
        re.compile(rf"^\d+\.?\s+(.+?)\s+{nilai_pattern}\s+{nilai_pattern}\s+{nilai_pattern}\s+[A-Da-d][\-\+]?"),
        re.compile(rf"^\d+\.?\s+(.+?)\s+{nilai_pattern}\s+{nilai_pattern}\s+{nilai_pattern}\s*$"),
        re.compile(rf"^\d+[\.\s]+(.+?)\s+{nilai_pattern}\s+{nilai_pattern}\s+{nilai_pattern}"),
        re.compile(rf"^\d+[\.\s\|]*\s*(.+?)\s+{nilai_pattern}\s+{nilai_pattern}\s+{nilai_pattern}"),
        re.compile(rf"^([A-Za-z][A-Za-z\s]+(?:dan|Dan|[A-Za-z])+)\s+{nilai_pattern}\s+{nilai_pattern}\s+{nilai_pattern}\s+[A-Da-d]"),
        re.compile(rf"([A-Za-z][A-Za-z\s,\.]+?)\s{{2,}}{nilai_pattern}\s+{nilai_pattern}\s+{nilai_pattern}"),
    ]
    
    def parse_nilai(val):
        val = val.replace(',', '.')
        try:
            num = float(val)
            return int(num) if num == int(num) else num
        except:
            return 0
    
    found_values = set()
    skip_keywords = ["Mata Pelajaran", "Pengetahuan", "Keterampilan", "Nilai", "No"]
    
    for line in lines:
        line = line.strip()
        if not line or len(line) < 10:
            continue
            
        for pattern in patterns:
            match = pattern.search(line)
            if match:
                mapel = match.group(1).strip()
                
                if any(kw.lower() in mapel.lower() for kw in skip_keywords):
                    continue
                
                if mapel in found_values:
                    continue
                
                p = parse_nilai(match.group(2))
                k = parse_nilai(match.group(3))
                a = parse_nilai(match.group(4))
                
                if all(0 <= v <= 100 for v in [p, k, a] if isinstance(v, (int, float))):
                    data["Nilai"].append({
                        "Mata Pelajaran": mapel,
                        "P": p,
                        "K": k,
                        "A": a
                    })
                    found_values.add(mapel)
                break
    
    if len(data["Nilai"]) == 0:
        data["Warnings"].append("Tidak ada nilai yang dapat diekstrak")
    elif len(data["Nilai"]) < 5:
        data["Warnings"].append(f"Hanya {len(data['Nilai'])} mata pelajaran ditemukan")
    
    return data
