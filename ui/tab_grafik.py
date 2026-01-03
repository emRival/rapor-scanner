"""
Tab Grafik Perkembangan
Menampilkan analisis perkembangan nilai antar semester
"""
import streamlit as st
import pandas as pd
from utils.formatting import format_nilai


def render_tab_grafik(df):
    """Render tab grafik perkembangan"""
    semesters_available = sorted(df['Semester'].unique())
    
    if len(semesters_available) < 2:
        st.warning("⚠️ Grafik perkembangan membutuhkan data dari **minimal 2 semester** yang berbeda.")
        st.info("Upload file rapor dari semester lain untuk melihat grafik perbandingan.")
        return
    
    st.markdown("### 📈 Analisis Perkembangan Nilai Antar Semester")
    
    # Sub-tabs
    subtab_siswa, subtab_mapel, subtab_ringkasan = st.tabs([
        "👤 Per Siswa", 
        "📚 Per Mata Pelajaran",
        "📊 Ringkasan Kelas"
    ])
    
    all_students = sorted(df['Nama Siswa'].unique())
    all_mapel = sorted(df['Mata Pelajaran'].unique())
    
    with subtab_siswa:
        _render_per_siswa(df, all_students, all_mapel, semesters_available)
    
    with subtab_mapel:
        _render_per_mapel(df, all_students, all_mapel, semesters_available)
    
    with subtab_ringkasan:
        _render_ringkasan(df, all_mapel, semesters_available)


def _render_per_siswa(df, all_students, all_mapel, semesters):
    """Render sub-tab Per Siswa"""
    col_sel1, col_sel2 = st.columns([2, 1])
    
    with col_sel1:
        selected_student = st.selectbox("👤 Pilih Siswa", options=all_students, key="grafik_siswa")
    
    with col_sel2:
        nilai_type = st.selectbox("📊 Jenis Nilai", ["A (Nilai Akhir)", "P (Pengetahuan)", "K (Keterampilan)"], key="nilai_type_siswa")
        nilai_col = nilai_type[0]
    
    if not selected_student:
        return
    
    siswa_data = df[df['Nama Siswa'] == selected_student]
    
    # Pilih mapel untuk grafik
    selected_mapel = st.selectbox(
        "📚 Pilih Mata Pelajaran untuk Grafik",
        options=["-- Semua Mapel (Rata-rata) --"] + list(all_mapel),
        key="mapel_chart_siswa"
    )
    
    # Line Chart
    st.markdown("#### 📈 Grafik Perkembangan Per Semester")
    _render_line_chart(siswa_data, selected_mapel, nilai_col, semesters)
    
    # Tabel Perubahan
    st.markdown("#### 📋 Tabel Perubahan Antar Semester")
    _render_comparison_table(siswa_data, all_mapel, nilai_col, semesters)


def _render_line_chart(siswa_data, selected_mapel, nilai_col, semesters):
    """Render line chart untuk siswa"""
    chart_data = []
    
    if selected_mapel == "-- Semua Mapel (Rata-rata) --":
        for sem in semesters:
            sem_data = siswa_data[siswa_data['Semester'] == sem]
            if len(sem_data) > 0:
                avg = sem_data[nilai_col].mean()
                if pd.notna(avg):
                    chart_data.append({'Semester': f'Sem {sem}', 'Nilai': round(avg, 1)})
    else:
        mapel_data = siswa_data[siswa_data['Mata Pelajaran'] == selected_mapel]
        for sem in semesters:
            sem_data = mapel_data[mapel_data['Semester'] == sem]
            if len(sem_data) > 0:
                val = sem_data[nilai_col].values[0]
                if pd.notna(val) and val != '-':
                    chart_data.append({'Semester': f'Sem {sem}', 'Nilai': float(val)})
    
    if chart_data:
        df_line = pd.DataFrame(chart_data).set_index('Semester')
        st.line_chart(df_line, use_container_width=True, height=300)
    else:
        st.info("Tidak ada data untuk ditampilkan")


def _render_comparison_table(siswa_data, all_mapel, nilai_col, semesters):
    """Render tabel perbandingan nilai antar semester"""
    comparison_data = []
    sorted_sems = sorted(semesters)
    
    for mapel in all_mapel:
        mapel_data = siswa_data[siswa_data['Mata Pelajaran'] == mapel]
        row = {'Mata Pelajaran': mapel}
        
        # Ambil nilai per semester
        semester_values = {}
        for sem in semesters:
            sem_data = mapel_data[mapel_data['Semester'] == sem]
            if len(sem_data) > 0:
                val = sem_data[nilai_col].values[0]
                if pd.notna(val) and val != '-':
                    try:
                        semester_values[sem] = int(float(val)) if float(val) == int(float(val)) else round(float(val), 1)
                    except:
                        semester_values[sem] = None
                else:
                    semester_values[sem] = None
            else:
                semester_values[sem] = None
        
        # Kolom nilai per semester
        for sem in semesters:
            row[f'Sem {sem}'] = semester_values.get(sem, '-') if semester_values.get(sem) is not None else '-'
        
        # Hitung perubahan antar semester
        changes = []
        for i in range(len(sorted_sems) - 1):
            sem1, sem2 = sorted_sems[i], sorted_sems[i + 1]
            val1, val2 = semester_values.get(sem1), semester_values.get(sem2)
            if val1 is not None and val2 is not None:
                change = val2 - val1
                row[f'{sem1}→{sem2}'] = int(change) if change == int(change) else round(change, 1)
                changes.append(change)
            else:
                row[f'{sem1}→{sem2}'] = '-'
        
        # Total perubahan dan trend
        valid_vals = [v for v in semester_values.values() if v is not None]
        if len(valid_vals) >= 2:
            total_change = valid_vals[-1] - valid_vals[0]
            row['Total Δ'] = int(total_change) if total_change == int(total_change) else round(total_change, 1)
            
            if all(c > 0 for c in changes if isinstance(c, (int, float))):
                row['Trend'] = '📈 Naik'
            elif all(c < 0 for c in changes if isinstance(c, (int, float))):
                row['Trend'] = '📉 Turun'
            elif all(c == 0 for c in changes if isinstance(c, (int, float))):
                row['Trend'] = '➡️ Stabil'
            else:
                row['Trend'] = '📊 Fluktuatif'
        else:
            row['Total Δ'] = '-'
            row['Trend'] = '-'
        
        comparison_data.append(row)
    
    df_comp = pd.DataFrame(comparison_data)
    
    # Styling
    def color_change(val):
        if val == '-' or val is None or not isinstance(val, (int, float)):
            return ''
        if val > 0:
            return 'background-color: #90EE90; color: #006400; font-weight: bold'
        elif val < 0:
            return 'background-color: #FFB6C1; color: #8B0000; font-weight: bold'
        return 'background-color: #FFFACD'
    
    change_cols = [c for c in df_comp.columns if '→' in c or c == 'Total Δ']
    styled = df_comp.style.map(color_change, subset=change_cols)
    st.dataframe(styled, use_container_width=True, hide_index=True, height=400)


def _render_per_mapel(df, all_students, all_mapel, semesters):
    """Render sub-tab Per Mata Pelajaran"""
    col_m1, col_m2 = st.columns([2, 1])
    
    with col_m1:
        selected_mapel = st.selectbox("📚 Pilih Mata Pelajaran", options=all_mapel, key="mapel_view")
    
    with col_m2:
        nilai_type = st.selectbox("📊 Jenis Nilai", ["A (Nilai Akhir)", "P (Pengetahuan)", "K (Keterampilan)"], key="nilai_mapel")
        nilai_col = nilai_type[0]
    
    if not selected_mapel:
        return
    
    mapel_data = df[df['Mata Pelajaran'] == selected_mapel]
    
    # Statistik
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Rata-rata", f"{mapel_data[nilai_col].mean():.1f}")
    with col2:
        st.metric("⬆️ Tertinggi", f"{mapel_data[nilai_col].max():.0f}")
    with col3:
        st.metric("⬇️ Terendah", f"{mapel_data[nilai_col].min():.0f}")
    
    # Tabel detail
    st.markdown(f"#### 📋 Detail Nilai {selected_mapel}")
    detail_data = []
    
    for siswa in all_students:
        row = {'Nama Siswa': siswa}
        vals = []
        
        for sem in semesters:
            d = mapel_data[(mapel_data['Nama Siswa'] == siswa) & (mapel_data['Semester'] == sem)]
            if len(d) > 0:
                val = d[nilai_col].values[0]
                row[f'Sem {sem}'] = val
                vals.append(val)
            else:
                row[f'Sem {sem}'] = '-'
        
        if len(vals) >= 2:
            change = vals[-1] - vals[0]
            row['Δ'] = f"+{change:.0f}" if change >= 0 else f"{change:.0f}"
            row['Status'] = "📈" if change > 0 else ("📉" if change < 0 else "➡️")
        else:
            row['Δ'] = '-'
            row['Status'] = '-'
        
        detail_data.append(row)
    
    st.dataframe(pd.DataFrame(detail_data), use_container_width=True, hide_index=True, height=400)


def _render_ringkasan(df, all_mapel, semesters):
    """Render sub-tab Ringkasan Kelas"""
    st.markdown("#### 📊 Statistik Perkembangan Kelas")
    
    nilai_type = st.selectbox("📊 Jenis Nilai", ["A (Nilai Akhir)", "P (Pengetahuan)", "K (Keterampilan)"], key="nilai_ring")
    nilai_col = nilai_type[0]
    
    summary_data = []
    for mapel in all_mapel:
        mapel_d = df[df['Mata Pelajaran'] == mapel]
        row = {'Mata Pelajaran': mapel[:25]}
        
        avg_vals = []
        for sem in semesters:
            sem_d = mapel_d[mapel_d['Semester'] == sem]
            if len(sem_d) > 0:
                avg = sem_d[nilai_col].mean()
                row[f'Sem {sem}'] = round(avg, 1)
                avg_vals.append(avg)
            else:
                row[f'Sem {sem}'] = '-'
        
        if len(avg_vals) >= 2:
            change = avg_vals[-1] - avg_vals[0]
            row['Δ Rata2'] = f"+{change:.1f}" if change >= 0 else f"{change:.1f}"
            row['Trend'] = "📈" if change > 0 else ("📉" if change < 0 else "➡️")
        else:
            row['Δ Rata2'] = '-'
            row['Trend'] = '-'
        
        summary_data.append(row)
    
    df_summary = pd.DataFrame(summary_data)
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    naik = len([r for r in summary_data if r.get('Trend') == '📈'])
    turun = len([r for r in summary_data if r.get('Trend') == '📉'])
    tetap = len([r for r in summary_data if r.get('Trend') == '➡️'])
    
    with col1:
        st.metric("📈 Mapel Naik", naik, delta=f"{naik}/{len(all_mapel)}")
    with col2:
        st.metric("📉 Mapel Turun", turun, delta=f"-{turun}", delta_color="inverse")
    with col3:
        st.metric("➡️ Mapel Tetap", tetap)
    
    st.dataframe(df_summary, use_container_width=True, hide_index=True, height=500)
