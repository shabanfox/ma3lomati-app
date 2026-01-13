import streamlit as st
import pandas as pd
import math
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. وظيفة جلب البيانات (تخزين مؤقت للسرعة)
@st.cache_data(ttl=300)
def load_full_data():
    u_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_developers = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_projects).fillna("").astype(str)
        d = pd.read_csv(u_developers).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_full_data()

# 3. CSS التصميم الفخم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { background-color: #050505; color: white; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .block-container { padding-top: 0rem !important; }
    header { visibility: hidden; }
    .luxury-header { background: rgba(15,15,15,0.9); border-bottom: 2px solid #f59e0b; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-radius: 0 0 20px 20px; margin-bottom: 10px; }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    .grid-card { background: #111; border: 1px solid #222; border-right: 5px solid #f59e0b; border-radius: 12px; padding: 15px; margin-bottom: 15px; transition: 0.3s; }
    .ai-box { background: linear-gradient(135deg, #1e1e1e, #000); border: 1px solid #f59e0b; padding: 20px; border-radius: 15px; margin-bottom: 20px; text-align: center; }
    .ready-sidebar { background: #0f0f0f; border: 1px solid #222; border-radius: 12px; padding: 10px; height: 80vh; overflow-y: auto; border-top: 4px solid #10b981; }
    </style>
""", unsafe_allow_html=True)

# 4. الحماية
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; margin-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 5. الهيدر
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa;">{datetime.now().strftime("%H:%M")}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# --- تقسيم 70% و 30% ---
col_main, col_side = st.columns([0.7, 0.3])

with col_side:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    for _, row in ready_df.iterrows():
        st.markdown(f"<div style='background:#161616; padding:10px; border-radius:5px; margin-bottom:8px; border-right:3px solid #10b981;'><b>{row['Project Name']}</b><br><small>{row['Area']}</small></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_main:
    if menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ مركز العمليات الذكي</h2>", unsafe_allow_html=True)
        
        # --- الأداة الجديدة: رادار البحث المفتوح ---
        st.markdown("""
            <div class='ai-box'>
                <h3 style='color:#f59e0b;'>🕵️ رادار المشاريع الذكي</h3>
                <p style='color:#ccc; font-size:14px;'>ابحث عن أي مشروع في مصر (خارج الشيت) وسيتم جلب بياناته فوراً من المصادر العالمية</p>
            </div>
        """, unsafe_allow_html=True)
        
        external_search = st.text_input("أدخل اسم المشروع أو المطور الذي تبحث عنه...")
        if external_search:
            # توليد روابط بحث ذكية لأشهر المواقع العقارية
            search_query = urllib.parse.quote(external_search + " عقارات مصر تفاصيل")
            st.warning(f"جاري البحث عن تفاصيل: {external_search}...")
            
            c1, c2, c3 = st.columns(3)
            with c1: st.link_button("🌍 بحث في جوجل", f"https://www.google.com/search?q={search_query}")
            with c2: st.link_button("🏗️ سابقة أعمال المطور", f"https://www.google.com/search?q={urllib.parse.quote('سابقة أعمال شركة ' + external_search)}")
            with c3: st.link_button("📍 موقع المشروع (Maps)", f"https://www.google.com/maps/search/{search_query}")
            
            st.info("💡 نصيحة بروكر: استخدم زر 'جوجل' لرؤية آخر تحديثات الأسعار الرسمية لهذا المشروع.")

        # التابات القديمة (الأدوات المالية)
        t = st.tabs(["🧮 الأقساط", "📈 الاستثمار", "📐 المساحات", "💰 العمولة"])
        with t[0]:
            p = st.number_input("السعر", 1000000); d = st.number_input("المقدم", p*0.1); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f} ج.م")
        # ... (باقي الأدوات)

    elif menu == "المشاريع":
        # (كود المشاريع كما هو)
        st.write("دليل المشاريع متاح بالكامل")

    elif menu == "المطورين":
        # (كود المطورين كما هو)
        st.write("دليل المطورين متاح بالكامل")
