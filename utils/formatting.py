"""
Formatting Utilities
Fungsi-fungsi untuk memformat nilai dan teks
"""
import pandas as pd


def format_nilai(val):
    """
    Format nilai untuk display.
    
    Args:
        val: Nilai (bisa int, float, string, atau NaN)
        
    Returns:
        str atau int: Nilai yang sudah diformat
    """
    if pd.isna(val) or val == '-':
        return '-'
    try:
        num = float(val)
        if num == int(num):
            return int(num)
        # Untuk angka desimal, bulatkan ke 1 desimal
        return round(num, 1)
    except (ValueError, TypeError):
        return str(val) if val else '-'


def shorten_mapel(name, max_len=15):
    """
    Singkatkan nama mata pelajaran.
    
    Args:
        name: Nama mapel lengkap
        max_len: Panjang maksimal
        
    Returns:
        str: Nama mapel yang disingkat
    """
    # Daftar singkatan umum
    replacements = {
        "Pendidikan": "Pend.",
        "Kewarganegaraan": "Kwn",
        "Indonesia": "Indo",
        "Keterampilan": "Ket.",
        "Pengetahuan": "Peng.",
        "Agama": "Ag.",
        "Budi Pekerti": "BP",
        "Pancasila": "Pcs",
        "Jasmani": "Jas.",
        "Olahraga": "OR",
        "Kesehatan": "Kes.",
        "Prakarya": "Pkr",
        "Kewirausahaan": "Kwu",
        "Informatika": "Inf.",
        "Bahasa": "B.",
        "Matematika": "MTK",
        "Sejarah": "Sej.",
        "Geografi": "Geo.",
        "Ekonomi": "Eko.",
        "Sosiologi": "Sos.",
        " dan ": " & ",
    }
    
    result = name
    for full, short in replacements.items():
        result = result.replace(full, short)
    
    if len(result) > max_len:
        result = result[:max_len-2] + ".."
    
    return result


def format_total(value):
    """Format total nilai untuk display"""
    if value > 0:
        if value == int(value):
            return str(int(value))
        return f"{value:.1f}"
    return '-'


def format_rata2(value):
    """Format rata-rata untuk display"""
    if value > 0:
        return f"{value:.1f}"
    return '-'


def format_rank(rank, total_siswa, semester):
    """Format ranking dengan info semester"""
    if rank > 0:
        return f"{rank}/{total_siswa} (S{semester})"
    return '-'
