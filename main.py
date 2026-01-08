import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# رابط البيانات
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# حالة الدخول
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# 2. التنسيق (CSS) المتطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    [data-testid="stSidebar"] { display: none; }
    
    /* تنسيق كادر الدخول */
    .login-box {
        background: #161b22; border: 2px solid #d4af37; border-radius: 25px;
        padding: 40px; text-align: center; margin-top: 50px;
    }
    
    /* تنسيق كروت المشاريع */
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 25px; margin-bottom: 20px;
    }
    .gold { color: #d4af37 !important; font-weight: 900; }
    .price-badge { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: bold; float: left; }
    .info-box { background: rgba(212,175,55,0.05); border-right: 4px solid #d4af37; padding: 15px; border-radius: 5px; margin: 15px 0; }
    
    /* حقل البحث */
    .stTextInput > div > div > input {
        background-color: #161b22 !important; color: white !important;
        border: 2px solid #30363d !important; border-radius: 12px !important;
        height: 50px; text-align: center;
    }

    /* زر الخروج العائم على اليسار */
    .stButton > button {
        transition: 0.3s;
    }
    
    /* تعريف مكان زر الخروج الخاص */
    div.stButton > button:first-child {
        position: fixed;
        left: 20px;
        top: 50%;
        transform: translateY(-50%);
        width: 120px;
        height: 60px;
        background-color: #d4af37 !important;
        color: black !important;
        font-weight: bold !important;
        border-radius: 15px !important;
        z-index: 999999;
        border: 2px solid #000 !important;
        box-shadow: -5px 5px 15px rgba(0,0,0,0.5);
    }
    
    div.stButton > button:first-child:hover {
        width: 140px;
        background-color: #ff4b4b !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(CSV_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except: return pd.DataFrame()

# 3. عرض الصفحات
if not st.session_state['auth']:
    # صفحة تسجيل الدخول
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown('<div class="login-box"><h1 class="gold">منصة معلوماتي</h1><p>بوابة بروكرز مصر</p></div>', unsafe_allow_html=True)
        tab1, tab2 = st.tabs(["🔐 دخول", "✉️ تسجيل"])
        with tab1:
            st.text_input("الإيميل")
            st.text_input("الباسورد", type="password")
            if st.button("دخول المنصة", use_container_width=True):
                st.session_state['auth'] = True
                st.rerun()
        with tab2:
            st.text_input("الاسم")
            st.button("إنشاء حساب", use_container_width=True)
else:
    # الصفحة الرئيسية (بعد الدخول)
    
    # زر الخروج العائم (بسبب الـ CSS سيبقى ثابتاً على اليسار)
    if st.button("خروج من المنصة"):
        st.session_state['auth'] = False
        st.rerun()
            
    st.markdown("<h2 class='gold' style='text-align:center;'>🏠 قاعدة بيانات المشاريع</h2>", unsafe_allow_html=True)
    
    # محرك البحث
    col_s1, col_s2, col_s3 = st.columns([1, 2, 1])
    with col_s2:
        search = st.text_input("", placeholder="🔍 ابحث هنا عن مطور، منطقة، أو مشروع...")

    df = load_data()
    if not df.empty:
        if search:
            df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
        st.markdown(f"<p style='text-align:center;'>تم إيجاد {len(df)} مشروع</p>", unsafe_allow_html=True)
        
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{row.get('السعر', 'اتصل')}</div>
                    <div class="gold" style="font-size:0.8em;">PROJECT REPORT</div>
                    <h2 style="margin:10px 0;">{row.get('المشروع', '-')}</h2>
                    <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                    <div class="info-box">
                        <b class="gold">📜 سابقة الأعمال:</b><br>{row.get('سابقة_الأعمال', '-')}
                    </div>
                    <div style="display:flex; gap:30px; border-top:1px solid #333; padding-top:10px; font-size:0.9em;">
                        <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                        <div><span class="gold">💳 السداد:</span> {row.get('السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
