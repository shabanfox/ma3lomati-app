import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. CONFIG ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. CSS LUXURY (The Real Cards) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; height: 0px; }
    [data-testid="stAppViewContainer"] { background-color: #0e1117; direction: rtl; font-family: 'Cairo', sans-serif; }
    
    /* Card UI */
    .card-container {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        border-right: 6px solid #f59e0b;
        transition: 0.3s ease;
    }
    .card-container:hover { border-color: #f59e0b; transform: translateY(-5px); background: #22272e; }
    .card-title { color: #f59e0b; font-size: 22px; font-weight: 900; margin-bottom: 10px; }
    .card-loc { color: #8b949e; font-size: 14px; display: flex; align-items: center; gap: 5px; }

    /* Detail Page UI */
    .detail-header { background: #f59e0b; color: #000; padding: 15px 30px; border-radius: 10px; font-weight: 900; font-size: 24px; margin-bottom: 30px; }
    .info-box { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    .info-label { color: #f59e0b; font-weight: 700; font-size: 18px; margin-bottom: 10px; border-bottom: 1px solid #333; padding-bottom: 5px; }
    .info-value { color: #fff; font-size: 17px; line-height: 1.8; }
    
    /* Buttons */
    div.stButton > button { width: 100% !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA LOAD ---
@st.cache_data(ttl=60)
def load_all_sheets():
    # روابط الشيتات بتاعتك
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        d, p, l = pd.read_csv(U_D), pd.read_csv(U_P), pd.read_csv(U_L)
        return d.fillna("---"), p.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_d, df_p, df_l = load_all_sheets()

# --- 4. NAVIGATION ---
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'idx' not in st.session_state: st.session_state.idx = 0

menu = option_menu(None, ["المطورين", "المشاريع", "اللونشات"], 
    icons=['building', 'house', 'rocket'], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 5. LOGIC & MAPPING ---
if menu == "المطورين":
    active_df, name_col = df_d, 'Developer'
    mapping = {"👤 المالك / رئيس مجلس الإدارة": "Owner / Chairman", "🏢 تفاصيل الشركة": "Company Details", "🏗️ أهم المشاريع": "Key Projects"}
elif menu == "المشاريع":
    active_df, name_col = df_p, 'Project Name'
    mapping = {"📍 الموقع": "Area", "📝 وصف المشروع": "Details", "💰 الأسعار": "Price"}
else:
    active_df, name_col = df_l, 'Project'
    mapping = {"📍 المنطقة": "Area", "📅 موعد اللونش": "Launch Date", "🚀 التفاصيل": "Details"}

# --- 6. RENDER ---
if st.session_state.view == "details":
    # --- PAGE: DETAILS ---
    item = active_df.iloc[st.session_state.idx]
    if st.button("⬅ عودة للقائمة"):
        st.session_state.view = "grid"; st.rerun()
    
    st.markdown(f'<div class="detail-header">{item[name_col]}</div>', unsafe_allow_html=True)
    
    for label, col in mapping.items():
        val = item.get(col, "غير متوفر")
        st.markdown(f"""
            <div class="info-box">
                <div class="info-label">{label}</div>
                <div class="info-value">{val}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    # --- PAGE: GRID (CARDS) ---
    search = st.text_input("🔍 ابحث في القائمة...")
    filtered = active_df[active_df[name_col].astype(str).str.contains(search, case=False)] if search else active_df
    
    cols = st.columns(2)
    for i, (orig_idx, row) in enumerate(filtered.iterrows()):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="card-container">
                    <div class="card-title">{row[name_col]}</div>
                    <div class="card-loc">📍 {row.get('Area', row.get('Owner / Chairman', 'مصر'))}</div>
                </div>
            """, unsafe_allow_html=True)
            if st.button(f"فتح ملف {row[name_col]}", key=f"btn_{orig_idx}"):
                st.session_state.idx = orig_idx
                st.session_state.view = "details"
                st.rerun()
