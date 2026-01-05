"""
Excel Export Utilities
Generate Excel report dengan openpyxl
"""
import io
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side, Font, PatternFill
from openpyxl.utils import get_column_letter
from config import EXCEL_COLUMN_WIDTH_DEFAULT, EXCEL_COLUMN_WIDTH_NAME


def create_excel_styles():
    """Create common Excel styles"""
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )
    center_align = Alignment(horizontal='center', vertical='center', wrap_text=True)
    bold_font = Font(bold=True)
    red_fill = PatternFill(start_color='FFCCCC', end_color='FFCCCC', fill_type='solid')
    
    return {
        'border': thin_border,
        'align': center_align,
        'bold': bold_font,
        'red_fill': red_fill
    }


def create_excel_report(display_data, mapel_list, mapel_short):
    """
    Create Excel report from display data.
    
    Args:
        display_data: List of dict dengan data per siswa
        mapel_list: List nama mapel
        mapel_short: Dict mapping nama mapel lengkap ke singkatan
        
    Returns:
        BytesIO: Excel file content
    """
    output = io.BytesIO()
    wb = Workbook()
    ws = wb.active
    ws.title = "Rekap Nilai"
    
    styles = create_excel_styles()
    
    # Header baris 1-2
    ws.cell(row=1, column=1, value="Nama Siswa")
    ws.cell(row=1, column=2, value="Semester")
    ws.merge_cells(start_row=1, start_column=1, end_row=2, end_column=1)
    ws.merge_cells(start_row=1, start_column=2, end_row=2, end_column=2)
    
    col_idx = 3
    for mapel in mapel_list:
        # Gunakan nama lengkap mata pelajaran, jangan disingkat
        ws.cell(row=1, column=col_idx, value=mapel)
        ws.merge_cells(start_row=1, start_column=col_idx, end_row=1, end_column=col_idx+2)
        ws.cell(row=2, column=col_idx, value="P")
        ws.cell(row=2, column=col_idx+1, value="K")
        ws.cell(row=2, column=col_idx+2, value="A")
        col_idx += 3
    
    # Header Total, Rata2, Rank
    ws.cell(row=1, column=col_idx, value="Total")
    ws.merge_cells(start_row=1, start_column=col_idx, end_row=2, end_column=col_idx)
    ws.cell(row=1, column=col_idx+1, value="Rata2")
    ws.merge_cells(start_row=1, start_column=col_idx+1, end_row=2, end_column=col_idx+1)
    ws.cell(row=1, column=col_idx+2, value="Rank")
    ws.merge_cells(start_row=1, start_column=col_idx+2, end_row=2, end_column=col_idx+2)
    col_idx += 3
    
    # Styling header
    for row in range(1, 3):
        for col in range(1, col_idx):
            cell = ws.cell(row=row, column=col)
            cell.border = styles['border']
            cell.alignment = styles['align']
            cell.font = styles['bold']
    
    # Data rows
    for row_idx, row_data in enumerate(display_data, start=3):
        has_zero = row_data.get('has_zero', False)
        
        ws.cell(row=row_idx, column=1, value=row_data['Nama Siswa'])
        ws.cell(row=row_idx, column=2, value=row_data['Semester'])
        
        col_idx = 3
        for mapel in mapel_list:
            val_p = row_data.get(f'{mapel}_P', '-')
            val_k = row_data.get(f'{mapel}_K', '-')
            val_a = row_data.get(f'{mapel}_A', '-')
            
            ws.cell(row=row_idx, column=col_idx, value=val_p)
            ws.cell(row=row_idx, column=col_idx+1, value=val_k)
            ws.cell(row=row_idx, column=col_idx+2, value=val_a)
            col_idx += 3
        
        # Total, Rata2, Rank
        ws.cell(row=row_idx, column=col_idx, value=row_data.get('Total', 0))
        ws.cell(row=row_idx, column=col_idx+1, value=row_data.get('Rata2', 0))
        ws.cell(row=row_idx, column=col_idx+2, value=row_data.get('Rank', 0))
        col_idx += 3
        
        # Styling data rows
        for col in range(1, col_idx):
            cell = ws.cell(row=row_idx, column=col)
            cell.border = styles['border']
            cell.alignment = styles['align']
            if cell.value == '-':
                cell.fill = styles['red_fill']
    
    # Auto-width kolom
    for col in range(1, col_idx):
        ws.column_dimensions[get_column_letter(col)].width = EXCEL_COLUMN_WIDTH_DEFAULT
    ws.column_dimensions['A'].width = EXCEL_COLUMN_WIDTH_NAME
    
    wb.save(output)
    return output
