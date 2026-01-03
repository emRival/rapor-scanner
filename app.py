"""
Rapor Scanner App - Main Entry Point
Aplikasi untuk ekstrak nilai dari PDF Rapor K13

Author: @em_rival (PMJ IT Team)
"""
import streamlit as st
import pandas as pd
import hashlib

# Import from local modules
from config import APP_TITLE
from core.extractor import extract_text_digital
from core.ocr import extract_text_ocr, is_ocr_available
from core.parser import parse_rapor_data
from ui.styles import get_main_css, get_header_html
from ui.tab_tabel import render_tab_tabel
from ui.tab_grafik import render_tab_grafik


# --- Page Config ---
st.set_page_config(page_title="Rekap Nilai Rapor K13", layout="wide", page_icon="📊")

# --- Apply Styles ---
st.markdown(get_main_css(), unsafe_allow_html=True)
st.markdown(get_header_html(), unsafe_allow_html=True)

# --- Upload Section ---
col_upload, col_info = st.columns([2, 1])
with col_upload:
    uploaded_files = st.file_uploader(
        "📁 Upload PDF Rapor", 
        type=["pdf"], 
        accept_multiple_files=True,
        help="Pilih satu atau lebih file PDF rapor"
    )
with col_info:
    st.info("💡 **Tips:** Upload banyak file sekaligus. Nilai desimal (89,5) juga didukung.")

# --- Session State ---
if 'all_results' not in st.session_state:
    st.session_state.all_results = []
if 'processed_files' not in st.session_state:
    st.session_state.processed_files = {}


def process_uploaded_files(files):
    """Process uploaded PDF files"""
    progress = st.progress(0)
    new_count = 0
    errors = []
    warnings = []
    
    for i, pdf_file in enumerate(files):
        # Create unique key
        content = pdf_file.read()
        pdf_file.seek(0)
        unique_key = f"{pdf_file.name}_{hashlib.md5(content).hexdigest()[:8]}"
        
        if unique_key in st.session_state.processed_files:
            progress.progress((i + 1) / len(files))
            continue
        
        # Extract text
        text, error = extract_text_digital(pdf_file)
        
        # Try OCR if digital fails
        is_ocr = False
        if error and is_ocr_available():
            with st.spinner(f"🔬 [EKSPERIMENTAL] OCR: {pdf_file.name}..."):
                text, ocr_error = extract_text_ocr(content)
            if text:
                error = None
                is_ocr = True
                st.toast(f"⚠️ {pdf_file.name}: OCR (hasil mungkin tidak sempurna)", icon="🔬")
            else:
                error = f"{error}. OCR gagal: {ocr_error}"
        
        if error:
            errors.append((pdf_file.name, error))
            progress.progress((i + 1) / len(files))
            continue
        
        # Parse data
        data = parse_rapor_data(text)
        name = data['Nama'] or pdf_file.name.replace(".pdf", "").replace("_", " ")
        semester = data['Semester'] or "-"
        
        if data.get('Warnings'):
            warnings.append((pdf_file.name, name, data['Warnings']))
        
        if data['Nilai']:
            for item in data['Nilai']:
                st.session_state.all_results.append({
                    "Nama Siswa": name,
                    "Semester": semester,
                    "Mata Pelajaran": item["Mata Pelajaran"],
                    "P": item["P"],
                    "K": item["K"],
                    "A": item["A"],
                    "Source File": pdf_file.name,
                    "Unique Key": unique_key
                })
            st.session_state.processed_files[unique_key] = f"{name} (Sem {semester})"
            new_count += 1
        else:
            errors.append((pdf_file.name, "Tidak ada nilai yang diekstrak"))
        
        progress.progress((i + 1) / len(files))
    
    progress.empty()
    return new_count, errors, warnings


# --- Process Files ---
if uploaded_files:
    new_count, errors, warnings = process_uploaded_files(uploaded_files)
    
    if new_count > 0:
        st.success(f"✅ {new_count} file berhasil diproses")
    
    if errors:
        with st.expander(f"❌ {len(errors)} File Gagal", expanded=False):
            for fname, err in errors:
                st.error(f"**{fname}:** {err}")
    
    if warnings:
        with st.expander(f"⚠️ {len(warnings)} Peringatan", expanded=False):
            for fname, sname, warns in warnings:
                st.warning(f"**{fname}** ({sname}): {', '.join(warns)}")

# --- Reset Button ---
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🗑️ Reset Semua", type="secondary"):
        st.session_state.all_results = []
        st.session_state.processed_files = {}
        st.rerun()

# --- Display Data ---
if st.session_state.all_results:
    df = pd.DataFrame(st.session_state.all_results)
    unique_students = df[['Nama Siswa', 'Semester']].drop_duplicates()
    
    # Metrics
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("📚 Total Data", len(unique_students))
    with c2:
        st.metric("📄 File", len(st.session_state.processed_files))
    with c3:
        st.metric("📖 Mapel", df['Mata Pelajaran'].nunique())
    with c4:
        sems = sorted(df['Semester'].unique())
        st.metric("📅 Semester", ", ".join(str(s) for s in sems))
    
    # Tabs
    tab_tabel, tab_grafik = st.tabs(["📋 Tabel Rekap", "📈 Grafik Perkembangan"])
    
    with tab_tabel:
        render_tab_tabel(df, st.session_state.all_results, st.session_state)
    
    with tab_grafik:
        render_tab_grafik(df)