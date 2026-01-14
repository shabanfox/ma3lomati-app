import streamlit as st
import pandas as pd
import math
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

# 3. وظيفة جلب البيانات (معالجة الشيتين)
@st.cache_data(ttl=60)
def load_all_data():
    # روابط الـ CSV (تأكد من عمل Publish as CSV من جوجل شيت)
    u_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_developers = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_projects).fillna("غير متوفر").astype(str)
        d = pd.read_csv(u_developers).fillna("غير متوفر").astype(str)
        p.columns = [c.strip() for c in p.columns]
        d.columns = [c.strip() for c in d.columns]
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header { visibility: hidden; }
    .luxury-header { background: rgba(15,15,15,0.9); border-bottom: 2px solid #f59e0b; padding: 15px 40px; display: flex; justify-content: space-between; align-items: center; border-radius: 0 0 25px 25px; margin-bottom: 10px; }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    .grid-card { background: #111; border: 1px solid #222; border-right: 5px solid #f59e0b; border-radius: 12px; padding: 15px; min-height: 220px; margin-bottom: 20px; }
    .ready-sidebar { background: #0f0f0f; border: 1px solid #222; border-radius: 15px; padding: 15px; height: 85vh; overflow-y: auto; border-top: 4px solid #10b981; }
    .ready-item { background: #161616; border-right: 4px solid #10b981; padding: 10px; border-radius: 8px; margin-bottom: 12px; }
    </style>
""", unsafe_allow_html=True)

# 5. نظام الحماية
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; padding-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# الهيدر
now = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#f59e0b;">⌚ {now}</div></div>', unsafe_allow_html=True)

# القائمة
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# التقسيم 70% و 30%
col_main, col_side = st.columns([0.7, 0.3])

with col_side:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    for _, row in ready_df.iterrows():
        st.markdown(f"<div class='ready-item'><b style='color:#f59e0b;'>{row.get('Project Name')}</b><br><small>{row.get('Area')}</small></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_main:
    if menu == "المشاريع":
        search = st.text_input("🔍 ابحث في المشاريع...")
        filtered = df_p.copy()
        if search: filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        for i in range(0, len(filtered), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(filtered):
                    r = filtered.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b;'>{r.get('Project Name')}</h3><p>📍 {r.get('Area')}</p><p>🏢 {r.get('Developer')}</p></div>", unsafe_allow_html=True)

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
        search_d = st.text_input("🔍 ابحث عن مطور...")
        
        filtered_d = df_d.copy()
        if search_d: filtered_d = filtered_d[filtered_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]

        for i in range(0, len(filtered_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(filtered_d):
                    r = filtered_d.iloc[i+j]
                    tier = r.get('Developer Category', 'N/A')
                    tier_color = "#f59e0b" if "A" in str(tier).upper() else "#aaa"
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card" style="border-right: 5px solid {tier_color};">
                                <div style="display:flex; justify-content:space-between;">
                                    <h3 style="color:#f59e0b; margin:0;">{r.get('Developer')}</h3>
                                    <span style="background:{tier_color}; color:black; padding:2px 8px; border-radius:5px; font-size:10px;">{tier}</span>
                                </div>
                                <p style="margin-top:10px;">👤 المالك: {r.get('Owner')}</p>
                                <p style="color:#10b981; font-weight:bold;">🏗️ المشاريع: {r.get('Number of Projects')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📖 سابقة الأعمال"):
                            st.write(r.get('Detailed_Info'))

    elif menu == "الأدوات":
        st.info("قسم الأدوات المتطور متاح هنا")
        # (يمكنك إضافة حاسبة الأقساط هنا)

if st.sidebar.button("🚪 خروج"):
    st.session_state.auth = False
    st.rerun()
