import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- 2. Enhanced CSS (التنسيق الموحد للكروت وصفحة التفاصيل) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; height: 0px; }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0a0c10;
        direction: rtl;
        font-family: 'Cairo', sans-serif;
    }

    /* تصميم الكروت في القائمة الرئيسية */
    .custom-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-right: 5px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        transition: 0.3s ease;
    }
    .custom-card:hover {
        border-color: #f59e0b;
        transform: translateY(-3px);
        background: #1c2128;
    }
    .card-h { color: #f59e0b; font-size: 20px; font-weight: 900; margin-bottom: 5px; }
    .card-p { color: #8b949e; font-size: 14px; }

    /* تصميم صفحة التفاصيل المقسمة */
    .detail-wrapper {
        background: #0d1117;
        padding: 35px;
        border-radius: 20px;
        border: 1px solid #30363d;
        margin-top: 10px;
    }
    .info-section {
        margin-bottom: 25px;
        padding: 15px;
        background: rgba(245, 158, 11, 0.03);
        border-radius: 10px;
        border-right: 3px solid #f59e0b;
    }
    .section-title {
        color: #f59e0b;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-text {
        color: #ffffff;
        font-size: 1.1rem;
        line-height: 1.8;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. Data Loading ---
@st.cache_data(ttl=60)
def load_data():
    # روابط الشيتات
    URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    
    try:
        p = pd.read_csv(URL_P).fillna("غير متوفر")
        d = pd.read_csv(URL_D).fillna("غير متوفر")
        l = pd.read_csv(URL_L).fillna("غير متوفر")
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 4. Session State ---
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_idx' not in st.session_state: st.session_state.current_idx = 0

# --- 5. Header & Navigation ---
st.markdown("<h1 style='text-align:center; color:#f59e0b; font-weight:900;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المطورين", "المشاريع", "اللونشات"], 
    icons=['tools', 'building', 'house', 'rocket'], 
    default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# تصحيح البيانات بناءً على الاختيار
if menu == "المطورين":
    active_df = df_d
    title_col = 'Developer'
    # تقسيمات المطور
    sections = {"👤 المالك / الإدارة": "Owner / Chairman", "🏢 عن الشركة": "Company Details", "🏗️ سابقة الأعمال": "Key Projects"}
elif menu == "المشاريع":
    active_df = df_p
    title_col = 'Project Name'
    # تقسيمات المشروع (تأكد من مطابقة أسماء الأعمدة في الشيت)
    sections = {"📍 الموقع": "Area", "📝 وصف المشروع": "Details", "💰 الأسعار وأنظمة السداد": "Price"}
else:
    active_df = df_l
    title_col = 'Project'
    sections = {"🚀 تفاصيل اللونش": "Details", "📍 المنطقة": "Area", "📅 الموعد": "Launch Date"}

# --- 6. View Logic ---

if menu == "الأدوات":
    st.info("قسم الأدوات قيد التحديث..")
else:
    if st.session_state.view == "details":
        # --- صفحة التفاصيل الموحدة والمقسمة ---
        item = active_df.iloc[st.session_state.current_idx]
        if st.button("⬅ عودة للقائمة"):
            st.session_state.view = "grid"
            st.rerun()
            
        st.markdown(f'<div class="detail-wrapper">', unsafe_allow_html=True)
        st.markdown(f'<h1 style="color:#f59e0b; margin-bottom:20px; border-bottom:2px solid #333; padding-bottom:10px;">{item[title_col]}</h1>', unsafe_allow_html=True)
        
        # عرض التقسيمات ديناميكياً
        for label, col in sections.items():
            val = item.get(col, "غير متوفر")
            st.markdown(f"""
            <div class="info-section">
                <div class="section-title">{label}</div>
                <div class="section-text">{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # --- صفحة الكروت (GRID) ---
        search = st.text_input("🔍 ابحث هنا...")
        filtered = active_df[active_df[title_col].astype(str).str.contains(search, case=False)] if search else active_df
        
        cols = st.columns(2)
        for i, (idx, row) in enumerate(filtered.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="custom-card">
                    <div class="card-h">{row[title_col]}</div>
                    <div class="card-p">📍 {str(row.get('Area', row.get('Owner / Chairman', 'مصر')))[:50]}...</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"عرض التفاصيل الكاملة لـ {row[title_col]}", key=f"btn_{idx}"):
                    st.session_state.current_idx = idx
                    st.session_state.view = "details"
                    st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
