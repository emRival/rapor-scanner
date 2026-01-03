"""
Tab Tabel Rekap
Menampilkan tabel rekap nilai dalam format multi-index
"""
import streamlit as st
import pandas as pd
from datetime import datetime

from utils.formatting import format_nilai, shorten_mapel, format_total, format_rata2, format_rank
from utils.excel import create_excel_report
from ui.styles import get_legend_text, get_footer_html


def render_tab_tabel(df, all_results, session_state):
    """Render tab tabel rekap"""
    unique_students = df.groupby(['Nama Siswa', 'Semester']).first().reset_index()[['Nama Siswa', 'Semester']]
    
    # Delete students section
    _render_delete_section(unique_students, session_state)
    
    if len(df) == 0:
        st.warning("Tidak ada data untuk ditampilkan.")
        return
    
    # Build pivot tables
    df_pivot_p = df.pivot_table(index=['Nama Siswa', 'Semester'], columns='Mata Pelajaran', values='P', aggfunc='first')
    df_pivot_k = df.pivot_table(index=['Nama Siswa', 'Semester'], columns='Mata Pelajaran', values='K', aggfunc='first')
    df_pivot_a = df.pivot_table(index=['Nama Siswa', 'Semester'], columns='Mata Pelajaran', values='A', aggfunc='first')
    
    mapel_list = sorted(df['Mata Pelajaran'].unique())
    
    df_pivot_p = df_pivot_p.reset_index()
    df_pivot_k = df_pivot_k.reset_index()
    df_pivot_a = df_pivot_a.reset_index()
    
    # Build display data
    multi_data, rows_with_zero = _build_display_data(df_pivot_p, df_pivot_k, df_pivot_a, mapel_list)
    
    # Calculate totals, averages, rankings
    valid_mapel = _get_valid_mapel_per_semester(df, mapel_list)
    totals, averages = _calculate_totals_averages(df_pivot_p, df_pivot_a, mapel_list, valid_mapel)
    rankings = _calculate_rankings(df_pivot_p, averages)
    
    # Add summary columns
    siswa_per_sem = _count_siswa_per_semester(df_pivot_p)
    _add_summary_columns(multi_data, df_pivot_p, totals, averages, rankings, siswa_per_sem)
    
    # Create display DataFrame
    mapel_short = {m: shorten_mapel(m) for m in mapel_list}
    df_display = _create_display_dataframe(multi_data, mapel_list, mapel_short)
    
    # Style and display
    styled_df = df_display.style.map(_highlight_dash)
    st.dataframe(styled_df, use_container_width=True, height=600)
    
    # Excel export
    display_data = _prepare_excel_data(df_pivot_p, df_pivot_k, df_pivot_a, mapel_list, 
                                        totals, averages, rankings, siswa_per_sem)
    output = create_excel_report(display_data, mapel_list, mapel_short)
    
    # Download section
    _render_download_section(output, all_results)
    
    # Footer
    st.markdown(get_footer_html(), unsafe_allow_html=True)


def _render_delete_section(unique_students, session_state):
    """Render section for deleting students"""
    with st.expander(f"🗑️ Hapus Siswa ({len(unique_students)} data)", expanded=False):
        students_to_delete = []
        cols = st.columns(5)
        for idx, row in unique_students.iterrows():
            nama, sem = row['Nama Siswa'], row['Semester']
            with cols[idx % 5]:
                if st.checkbox(nama[:20], key=f"cb_del_{nama}_{sem}", help=f"{nama} (Sem {sem})"):
                    students_to_delete.append((nama, sem))
        
        if students_to_delete:
            c1, c2 = st.columns([3, 1])
            with c1:
                st.warning(f"⚠️ {len(students_to_delete)} siswa dipilih")
            with c2:
                if st.button("🗑️ Hapus", type="primary"):
                    for nama, sem in students_to_delete:
                        session_state.all_results = [
                            r for r in session_state.all_results 
                            if not (r['Nama Siswa'] == nama and r['Semester'] == sem)
                        ]
                    st.rerun()


def _build_display_data(df_p, df_k, df_a, mapel_list):
    """Build multi_data list from pivot tables"""
    multi_data = []
    rows_with_zero = []
    
    for idx, row_p in df_p.iterrows():
        row_k = df_k.iloc[idx]
        row_a = df_a.iloc[idx]
        
        row_values = [row_p['Nama Siswa'], row_p['Semester']]
        has_zero = False
        
        for mapel in mapel_list:
            if mapel in df_p.columns:
                val_p = format_nilai(row_p.get(mapel, '-'))
                val_k = format_nilai(row_k.get(mapel, '-'))
                val_a = format_nilai(row_a.get(mapel, '-'))
                
                if val_p == '-' or val_k == '-' or val_a == '-':
                    has_zero = True
                
                row_values.extend([val_p, val_k, val_a])
        
        multi_data.append(row_values)
        rows_with_zero.append(has_zero)
    
    return multi_data, rows_with_zero


def _get_valid_mapel_per_semester(df, mapel_list):
    """Get valid mapel for each semester"""
    valid_mapel = {}
    for sem in df['Semester'].unique():
        sem_df = df[df['Semester'] == sem]
        valid = []
        for mapel in mapel_list:
            mapel_vals = sem_df[sem_df['Mata Pelajaran'] == mapel]['A'].dropna()
            has_valid = any(v != '-' and pd.notna(v) for v in mapel_vals)
            if has_valid:
                valid.append(mapel)
        valid_mapel[sem] = valid
    return valid_mapel


def _calculate_totals_averages(df_p, df_a, mapel_list, valid_mapel):
    """Calculate totals and averages"""
    totals = []
    averages = []
    
    for idx, row_p in df_p.iterrows():
        row_a = df_a.iloc[idx]
        semester = row_p['Semester']
        sem_valid = valid_mapel.get(semester, mapel_list)
        
        total = 0
        count = 0
        for mapel in sem_valid:
            if mapel in row_a.index:
                val = row_a.get(mapel)
                if pd.notna(val) and val != '-':
                    try:
                        total += float(val)
                        count += 1
                    except:
                        pass
        
        totals.append(round(total, 1) if total > 0 else 0)
        averages.append(round(total / count, 1) if count > 0 else 0)
    
    return totals, averages


def _calculate_rankings(df_p, averages):
    """Calculate rankings per semester"""
    rankings = [0] * len(averages)
    semester_indices = {}
    
    for idx, row_p in df_p.iterrows():
        sem = row_p['Semester']
        if sem not in semester_indices:
            semester_indices[sem] = []
        semester_indices[sem].append(idx)
    
    for sem, indices in semester_indices.items():
        sem_avgs = [(i, averages[i]) for i in indices]
        sem_avgs.sort(key=lambda x: x[1], reverse=True)
        for rank, (orig_idx, _) in enumerate(sem_avgs, 1):
            rankings[orig_idx] = rank
    
    return rankings


def _count_siswa_per_semester(df_p):
    """Count students per semester"""
    counts = {}
    for idx, row_p in df_p.iterrows():
        sem = row_p['Semester']
        counts[sem] = counts.get(sem, 0) + 1
    return counts


def _add_summary_columns(multi_data, df_p, totals, averages, rankings, siswa_per_sem):
    """Add Total, Rata2, Rank to multi_data"""
    for i, row in enumerate(multi_data):
        semester = row[1]
        total_siswa = siswa_per_sem.get(semester, 1)
        
        row.append(format_total(totals[i]))
        row.append(format_rata2(averages[i]))
        row.append(format_rank(rankings[i], total_siswa, semester))


def _create_display_dataframe(multi_data, mapel_list, mapel_short):
    """Create display DataFrame with MultiIndex columns"""
    level_0 = ['Nama Siswa', 'Sem'] + [mapel_short[m] for m in mapel_list for _ in ['P', 'K', 'A']] + ['Total', 'Rata2', 'Rank']
    level_1 = ['', ''] + ['P', 'K', 'A'] * len(mapel_list) + ['', '', '']
    multi_columns = pd.MultiIndex.from_arrays([level_0, level_1])
    
    df_display = pd.DataFrame(multi_data, columns=multi_columns)
    df_display.fillna('-', inplace=True)
    df_display.index = range(1, len(df_display) + 1)
    df_display.index.name = 'No'
    
    return df_display


def _highlight_dash(val):
    """Highlight dash cells with red"""
    if val == '-':
        return 'background-color: #ffcccc; color: #8B0000; font-weight: bold'
    return ''


def _prepare_excel_data(df_p, df_k, df_a, mapel_list, totals, averages, rankings, siswa_per_sem):
    """Prepare data for Excel export"""
    display_data = []
    
    for idx, row_p in df_p.iterrows():
        row_k = df_k.iloc[idx]
        row_a = df_a.iloc[idx]
        semester = row_p['Semester']
        total_siswa = siswa_per_sem.get(semester, 1)
        
        row_dict = {
            'Nama Siswa': row_p['Nama Siswa'],
            'Semester': semester,
            'has_zero': False
        }
        
        for mapel in mapel_list:
            if mapel in df_p.columns:
                val_p = format_nilai(row_p.get(mapel, '-'))
                val_k = format_nilai(row_k.get(mapel, '-'))
                val_a = format_nilai(row_a.get(mapel, '-'))
                
                row_dict[f'{mapel}_P'] = val_p
                row_dict[f'{mapel}_K'] = val_k
                row_dict[f'{mapel}_A'] = val_a
                
                if val_p == '-' or val_k == '-' or val_a == '-':
                    row_dict['has_zero'] = True
        
        # Add formatted summary columns
        if totals[idx] > 0:
            row_dict['Total'] = int(totals[idx]) if totals[idx] == int(totals[idx]) else round(totals[idx], 1)
        else:
            row_dict['Total'] = '-'
        
        row_dict['Rata2'] = round(averages[idx], 1) if averages[idx] > 0 else '-'
        row_dict['Rank'] = f"{rankings[idx]}/{total_siswa} (S{semester})" if rankings[idx] > 0 else '-'
        
        display_data.append(row_dict)
    
    return display_data


def _render_download_section(output, all_results):
    """Render download button and legend"""
    st.divider()
    
    semesters = list(set([r['Semester'] for r in all_results]))
    sem_str = f"Sem{'_'.join(str(s) for s in sorted(semesters))}"
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    filename = f"Rekap_Nilai_{sem_str}_{date_str}.xlsx"
    
    col_dl, col_legend = st.columns([1, 2])
    with col_dl:
        st.download_button(
            label="📥 Download Excel",
            data=output.getvalue(),
            file_name=filename,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
            type="primary"
        )
        st.caption(f"📄 {filename}")
    with col_legend:
        st.markdown(get_legend_text())
