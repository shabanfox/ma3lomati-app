import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Luxury CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0.5rem !important; }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif;
    }

    /* أزرار اللغة والخروج الصغيرة */
    .side-btn-container {
        position: fixed;
        top: 20px;
        right: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
        z-index: 999;
    }
    
    /* تنسيق الكروت */
    .card-style {
        background: #1c2128;
        border: 1px solid #30363d;
        border-right: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s;
    }
    .card-style:hover { border-color: #f59e0b; background: #252a34; }

    /* تنسيق صفحة التفاصيل المقسمة */
    .detail-container {
        background: #161b22;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #30363d;
    }
    .info-section {
        margin-bottom: 20px;
        padding: 15px;
        background: rgba(245, 158, 11, 0.05);
        border-radius: 8px;
        border-right: 3px solid #f59e0b;
    }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 18px; margin-bottom: 5px; }
    .val-white { color: #ffffff; font-size: 17px; line-height: 1.7; }

    /* تصغير الأزرار العامة */
    div.stButton > button { border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 3. Data Loading ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 4. Session State ---
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'idx' not in st.session_state: st.session_state.idx = 0
if 'lang' not in st.session_state: st.session_state.lang = "AR"

# --- 5. UI Layout (Header & Side Buttons) ---
c1, c2 = st.columns([0.8, 0.2])
with c1:
    st.markdown("<h1 style='color:#f59e0b; margin-bottom:0;'>MA3LOMATI</h1>", unsafe_allow_html=True)
with c2:
    # أزرار صغيرة في اليمين تحت بعضها
    if st.button("🌐 EN/AR", key="btn_lang", use_container_width=True):
        st.session_state.lang = "EN" if st.session_state.lang == "AR" else "AR"
        st.rerun()
    if st.button("🚪 خروج", key="btn_exit", use_container_width=True):
        st.write("تم تسجيل الخروج")

menu = option_menu(None, ["الأدوات", "المطورين", "المشاريع", "اللونشات"], 
    icons=['tools', 'building', 'house', 'rocket'], 
    default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 6. Content Logic ---
if menu == "المطورين":
    active_df, col_main = df_d, 'Developer'
    mapping = {"👤 المالك / الإدارة": "Owner / Chairman", "🏢 عن الشركة": "Company Details", "🏗️ أهم المشاريع": "Key Projects"}
elif menu == "المشاريع":
    active_df, col_main = df_p, 'Project Name'
    mapping = {"📍 الموقع": "Area", "📝 وصف المشروع": "Details", "💰 الأسعار": "Price"}
elif menu == "اللونشات":
    active_df, col_main = df_l, 'Project'
    mapping = {"📍 المنطقة": "Area", "📅 الموعد": "Launch Date", "🚀 التفاصيل": "Details"}
else:
    active_df = pd.DataFrame()

if menu != "الأدوات":
    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.idx]
        if st.button("⬅ عودة للقائمة"):
            st.session_state.view = "grid"; st.rerun()
        
        st.markdown(f'<div class="detail-container">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:#f59e0b;">{item[col_main]}</h1><hr style="border-color:#333;">', unsafe_allow_html=True)
        
        for label, col in mapping.items():
            val = item.get(col, "---")
            st.markdown(f"""
                <div class="info-section">
                    <div class="label-gold">{label}</div>
                    <div class="val-white">{val}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 بحث...")
        filtered = active_df[active_df[col_main].astype(str).str.contains(search, case=False)] if search else active_df
        
        grid = st.columns(2)
        for i, (orig_idx, row) in enumerate(filtered.iterrows()):
            with grid[i % 2]:
                st.markdown(f"""
                <div class="card-style">
                    <div style="color:#f59e0b; font-size:20px; font-weight:900;">{row[col_main]}</div>
                    <div style="color:#888; font-size:14px;">📍 {str(row.get('Area', row.get('Owner / Chairman', '---')))[:40]}...</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"التفاصيل: {row[col_main]}", key=f"go_{orig_idx}"):
                    st.session_state.idx = orig_idx
                    st.session_state.view = "details"
                    st.rerun()
else:
    st.info("قسم الأدوات قيد التحديث")
