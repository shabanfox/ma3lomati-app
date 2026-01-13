import streamlit as st
import pandas as pd
import math
import feedparser
from streamlit_option_menu import option_menu 
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. تحميل البيانات من الشيتين
@st.cache_data(ttl=60)
def load_all_data():
    u_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_developers = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        df_p = pd.read_csv(u_projects).fillna("").astype(str)
        df_d = pd.read_csv(u_developers).fillna("").astype(str)
        df_p.columns = df_p.columns.str.strip()
        df_d.columns = df_d.columns.str.strip()
        return df_p, df_d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #0a0a0a; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر الزجاجي */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; margin-bottom: 10px; border-radius: 0 0 20px 20px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; text-shadow: 0 0 10px rgba(245, 158, 11, 0.3); }}

    /* الكروت الجانبية (Ready to Move) */
    .ready-card {{
        background: linear-gradient(135deg, #1e1e1e, #111);
        border: 1px solid #333; border-right: 4px solid #10b981; /* أخضر للاستلام الفوري */
        border-radius: 10px; padding: 12px; margin-bottom: 10px;
    }}
    .ready-tag {{
        background: #10b981; color: white; font-size: 10px; padding: 2px 8px; border-radius: 5px; font-weight: bold;
    }}

    /* الكروت الأساسية */
    .grid-card {{ 
        background: #161616; border: 1px solid #222; border-right: 5px solid #f59e0b; 
        border-radius: 15px; padding: 15px; margin-bottom: 15px;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- الهيدر ---
now = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:12px;">PRO 2026</span></div><div style="color:#f59e0b;">⌚ {now}</div></div>', unsafe_allow_html=True)

# المنيو
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# --- تقسيم الشاشة 70% أساسي و 30% جانبي ---
main_col, side_col = st.columns([0.7, 0.3])

# --- الجزء الجانبي (30%) - Ready to Move ---
with side_col:
    st.markdown("<h4 style='color:#10b981; border-bottom: 1px solid #333; padding-bottom:5px;'>🔑 استلام فوري (Ready)</h4>", unsafe_allow_html=True)
    # تصفية المشاريع التي تحتوي على كلمة "فوري" أو "جاهز" في خانة المميزات أو الاسم
    ready_projects = df_p[df_p.apply(lambda row: row.astype(str).str.contains('فوري|جاهز|استلام فوري', case=False).any(), axis=1)].head(5)
    
    if not ready_projects.empty:
        for _, row in ready_projects.iterrows():
            st.markdown(f"""
                <div class="ready-card">
                    <span class="ready-tag">استلام فوري</span>
                    <div style="color:#fff; font-weight:bold; margin-top:5px;">{row['Project Name']}</div>
                    <div style="color:#aaa; font-size:12px;">📍 {row['Area']}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("تفاصيل السعر"):
                st.write(f"المطور: {row['Developer']}")
    else:
        st.write("لا يوجد مشاريع جاهزة حالياً")

# --- الجزء الرئيسي (70%) ---
with main_col:
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
        s_p = st.text_input("🔍 بحث سريـع...")
        dff_p = df_p.copy()
        if s_p: dff_p = dff_p[dff_p['Project Name'].str.contains(s_p, case=False)]
        
        limit = 6
        total_pages = math.ceil(len(dff_p) / limit)
        curr_page = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]

        for i in range(0, len(curr_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_page):
                    row = curr_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class='grid-card'>
                                <h3 style='color:#f59e0b; margin:0;'>{row.get('Project Name')}</h3>
                                <p style='margin:5px 0;'>📍 {row.get('Area')} | 📐 {row.get('Project Area')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔎 كامل التفاصيل"):
                            st.info(f"✨ المميزات: {row.get('Project Features')}")
        
        st.write("---")
        c1, c2 = st.columns(2)
        if c1.button("التالي"): st.session_state.p_idx += 1; st.rerun()
        if c2.button("السابق"): st.session_state.p_idx -= 1; st.rerun()

    elif menu == "المطورين":
        # (كود المطورين كما هو)
        st.write("قسم المطورين قيد العرض...")

    elif menu == "الأدوات":
        # (كود الأدوات الـ 6 كما هو)
        st.write("أدوات البروكر جاهزة...")
