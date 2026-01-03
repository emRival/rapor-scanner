"""
UI Styles
CSS styling untuk Streamlit app
"""
from config import APP_TITLE, APP_DESCRIPTION, APP_AUTHOR, APP_TEAM


def get_main_css():
    """Return main CSS styles for the app"""
    return """
<style>
    /* Header styling dengan gradient modern */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 15px;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    .main-header p {
        color: #e8e0f0;
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
    }
    
    /* Metric cards styling */
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #e4e8ec 100%);
        border-radius: 12px;
        padding: 1rem;
        text-align: center;
        border-left: 5px solid #667eea;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f0f2f6;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Button styling */
    .stDownloadButton button {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(17, 153, 142, 0.4) !important;
        transition: all 0.3s ease !important;
    }
    .stDownloadButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(17, 153, 142, 0.5) !important;
    }
    
    /* Fix header tabel */
    [data-testid="stDataFrame"] th {
        white-space: normal !important;
        word-wrap: break-word !important;
        text-align: center !important;
        vertical-align: middle !important;
        min-width: 60px !important;
        max-width: 150px !important;
        padding: 8px 4px !important;
        font-size: 12px !important;
        line-height: 1.2 !important;
        background-color: #f8f9fa !important;
    }
    [data-testid="stDataFrame"] td {
        text-align: center !important;
        padding: 4px !important;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #f8f9fa;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 10px;
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    
    /* Footer credit */
    .footer-credit {
        text-align: center;
        color: #888;
        font-size: 0.85rem;
        padding: 1rem 0;
        border-top: 1px solid #eee;
        margin-top: 2rem;
    }
</style>
"""


def get_header_html():
    """Return header HTML"""
    return f"""
<div class="main-header">
    <h1>{APP_TITLE}</h1>
    <p>{APP_DESCRIPTION}</p>
</div>
"""


def get_footer_html():
    """Return footer HTML with credits"""
    return f"""
<div class="footer-credit">
    <p>🛠️ Dibuat oleh <strong>{APP_AUTHOR}</strong> dari <strong>{APP_TEAM}</strong></p>
</div>
"""


def get_legend_text():
    """Return legend text for the table"""
    return """
**Keterangan Kolom:**
- **P** = Pengetahuan | **K** = Keterampilan | **A** = Nilai Akhir
- **Total** = Jumlah nilai A | **Rata2** = Rata-rata nilai A
- **Rank** = Peringkat siswa (dihitung **per semester masing-masing**)
- 🔴 Sel merah = Nilai tidak terbaca atau mapel tidak ada di semester tersebut
"""
