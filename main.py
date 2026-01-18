import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. الروابط (تأكد من تحديث روابط الـ CSV)
# ملاحظة: استبدل الروابط بالروابط المباشرة للـ CSV وليس HTML
u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=0&single=true&output=csv"
u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=2031754026&single=true&output=csv"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = True # مؤقتاً للتطوير
if 'current_user' not in st.session_state: st.session_state.current_user = "البروكر المحترف"
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 4. جلب البيانات بذكاء
@st.cache_data(ttl=60)
def load_full_data():
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        # تنظيف الأسماء
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_full_data()

# 5. التنسيق الجمالي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    .dev-card { background: #111; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 5px solid #f59e0b; margin-bottom: 10px; transition: 0.3s; }
    .dev-card:hover { border-right: 10px solid #f59e0b; transform: scale(1.01); }
    .usp-box { background: #1a1a1a; padding: 15px; border-radius: 10px; border-top: 2px solid #f59e0b; font-style: italic; }
    .stButton > button { width: 100% !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# 6. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 7. قسم المطورين المطور (شغلنا الأساسي) ---
if menu == "المطورين":
    if st.session_state.selected_dev is None:
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المطورين العقاريين في مصر</h2>", unsafe_allow_html=True)
        search_d = st.text_input("🔍 ابحث عن المطور لمعرفة تاريخه ونقاط القوة...", placeholder="مثلاً: Sodic, Emaar...")
        
        filtered_d = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        
        for i, row in filtered_d.iterrows():
            with st.container():
                st.markdown(f"""
                <div class='dev-card'>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <span style='color:#f59e0b; font-size:22px; font-weight:bold;'>{row['Developer']}</span>
                        <span style='background:#f59e0b; color:black; padding:2px 10px; border-radius:5px; font-weight:bold;'>{row.get('Category', 'A')}</span>
                    </div>
                    <p style='color:#ccc; margin-top:10px;'>👤 المالك: {row.get('Owner / CEO', '---')}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"فتح ملف {row['Developer']} الكامل 📖", key=f"btn_{i}"):
                    st.session_state.selected_dev = row.to_dict()
                    st.rerun()
    else:
        # صفحة المطور التفصيلية
        dev = st.session_state.selected_dev
        if st.button("⬅️ العودة للدليل"):
            st.session_state.selected_dev = None
            st.rerun()
            
        st.markdown(f"""
            <div style='background:#111; padding:25px; border-radius:20px; border-right:10px solid #f59e0b;'>
                <h1 style='color:#f59e0b;'>{dev['Developer']}</h1>
                <p style='font-size:18px;'>📅 <b>سنة التأسيس:</b> {dev.get('Establishment', '---')}</p>
                <p style='font-size:18px;'>👤 <b>رئيس مجلس الإدارة:</b> {dev.get('Owner / CEO', '---')}</p>
                <hr style='border-color:#333;'>
                <h3 style='color:#f59e0b;'>🌟 لماذا تختار هذا المطور؟ (USP)</h3>
                <div class='usp-box'>{dev.get('USP', 'مطور عقاري رائد في السوق المصري.')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        # ربط المشاريع تلقائياً
        st.markdown("<br><h3>📂 مشاريع المطور المتاحة حالياً:</h3>", unsafe_allow_html=True)
        my_projs = df_p[df_p['Developer'].str.contains(dev['Developer'], case=False, na=False)]
        
        if not my_projs.empty:
            for _, p in my_projs.iterrows():
                with st.expander(f"🏢 {p['ProjectName']} - {p.get('Location', '---')}"):
                    st.write(f"💰 **نظام السداد:** {p.get('Payment Plan', 'تواصل للتفاصيل')}")
                    st.write(f"📍 **الموقع:** {p.get('Location', '---')}")
                    st.markdown(f"[📲 إرسال تفاصيل المشروع لواتساب العميل](https://wa.me/?text={urllib.parse.quote('أرشح لك مشروع ' + p['ProjectName'] + ' من شركة ' + dev['Developer'])})")
        else:
            st.warning("لا توجد مشاريع مسجلة لهذا المطور حالياً في شيت المشاريع.")

# (بقية الأقسام المساعد والمشاريع تظل كما هي مع التأكد من ربط الداتا)
