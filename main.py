import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0e1117;
        direction: rtl !important;
        text-align: right !important;
        font-family: 'Cairo', sans-serif;
    }

    /* أزرار اللغة والخروج الصغيرة تحت بعض في اليمين */
    .stButton > button[key="btn_lang"], .stButton > button[key="btn_exit"] {
        font-size: 12px !important;
        padding: 2px 10px !important;
        height: 30px !important;
        min-height: 30px !important;
        margin-bottom: 5px !important;
    }

    /* تصميم الكروت */
    .card-style {
        background: #1c2128;
        border: 1px solid #30363d;
        border-right: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 10px;
    }

    /* صفحة التفاصيل المقسمة */
    .detail-container {
        background: #161b22;
        padding: 25px;
        border-radius: 15px;
        border: 1px solid #30363d;
    }
    .info-section {
        margin-bottom: 15px;
        padding: 12px;
        background: rgba(245, 158, 11, 0.05);
        border-radius: 8px;
        border-right: 3px solid #f59e0b;
    }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 16px; }
    .val-white { color: #ffffff; font-size: 16px; line-height: 1.6; }
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
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 5. UI Layout (Header & Side Buttons) ---
col_head, col_side = st.columns([0.85, 0.15])
with col_head:
    st.markdown("<h1 style='color:#f59e0b;'>MA3LOMATI</h1>", unsafe_allow_html=True)
with col_side:
    # الأزرار تحت بعض في أقصى اليمين
    st.button("🌐 EN/AR", key="btn_lang", use_container_width=True)
    st.button("🚪 خروج", key="btn_exit", use_container_width=True)

menu = option_menu(None, ["الأدوات", "المطورين", "المشاريع", "اللونشات"], 
    icons=['tools', 'building', 'house', 'rocket'], 
    default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 6. Logic Mapping ---
if menu == "المطورين":
    active_df, col_main = df_d, 'Developer'
    mapping = {"👤 المالك / الإدارة": "Owner / Chairman", "🏢 عن الشركة": "Company Details", "🏗️ سابقة الأعمال": "Key Projects"}
elif menu == "المشاريع":
    active_df, col_main = df_p, 'Project Name'
    mapping = {"📍 الموقع": "Area", "📝 وصف المشروع": "Details", "💰 الأسعار": "Price"}
elif menu == "اللونشات":
    active_df, col_main = df_l, 'Project'
    mapping = {"📍 المنطقة": "Area", "📅 موعد الإطلاق": "Launch Date", "🚀 التفاصيل": "Details"}
else:
    active_df = pd.DataFrame()

# --- 7. View Logic ---
if active_df.empty:
    st.info("القسم قيد التحديث")
else:
    if st.session_state.view == "details":
        item = active_df.iloc[st.session_state.idx]
        if st.button("⬅ عودة للقائمة"):
            st.session_state.view = "grid"; st.rerun()
        
        st.markdown(f'<div class="detail-container">', unsafe_allow_html=True)
        st.markdown(f'<h2 style="color:#f59e0b;">{item[col_main]}</h2><hr>', unsafe_allow_html=True)
        for label, col in mapping.items():
            st.markdown(f'<div class="info-section"><div class="label-gold">{label}</div><div class="val-white">{item.get(col, "---")}</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # البحث
        search = st.text_input("🔍 بحث...")
        filtered = active_df[active_df[col_main].astype(str).str.contains(search, case=False)] if search else active_df
        
        # الترقيم (Pagination)
        limit = 6
        start = st.session_state.page_num * limit
        end = start + limit
        display_df = filtered.iloc[start:end]
        
        # عرض الكروت
        grid = st.columns(2)
        for i, (orig_idx, row) in enumerate(display_df.iterrows()):
            with grid[i % 2]:
                st.markdown(f'<div class="card-style"><div style="color:#f59e0b; font-weight:900;">{row[col_main]}</div><div style="color:#888; font-size:13px;">📍 {str(row.get("Area", "مصر"))[:40]}</div></div>', unsafe_allow_html=True)
                if st.button(f"فتح {row[col_main]}", key=f"go_{orig_idx}"):
                    st.session_state.idx = orig_idx; st.session_state.view = "details"; st.rerun()

        # أزرار التنقل (السابق والتالي)
        st.write("---")
        nav_prev, nav_page, nav_next = st.columns([1, 2, 1])
        with nav_prev:
            if st.session_state.page_num > 0:
                if st.button("⬅ السابق", use_container_width=True):
                    st.session_state.page_num -= 1; st.rerun()
        with nav_page:
            st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
        with nav_next:
            if end < len(filtered):
                if st.button("التالي ➡", use_container_width=True):
                    st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
