import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة - يجب أن يكون أول سطر
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# رابط البيانات (تأكد من أنه رابط Raw CSV)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# إدارة الدخول
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# 2. التنسيق الفخم (CSS) مع شريط التمرير العريض
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    [data-testid="stSidebar"] { display: none; }
    
    /* شريط التمرير العريض جداً */
    ::-webkit-scrollbar { width: 25px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; border: 5px solid #161b22; }

    .login-box {
        background: #161b22; border: 2px solid #d4af37; border-radius: 25px;
        padding: 40px; text-align: center; margin: 50px auto; max-width: 500px;
    }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 25px; margin-bottom: 20px; transition: 0.3s;
    }
    .project-card:hover { border-color: #d4af37; }
    .gold { color: #d4af37 !important; font-weight: 900; }
    .price-badge { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: bold; float: left; }
    .info-box { background: rgba(212,175,55,0.05); border-right: 4px solid #d4af37; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
    """, unsafe_allow_html=True)

# دالة تحميل البيانات
@st.cache_data(ttl=10)
def load_data():
    try:
        res = requests.get(CSV_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except Exception as e:
        return pd.DataFrame()

# 3. منطق الصفحات
if not st.session_state['auth']:
    st.markdown('<div class="login-box"><h1 class="gold">منصة معلوماتي</h1><p>بوابة بروكرز مصر العقارية</p>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔐 دخول", "✉️ تسجيل"])
    with t1:
        st.text_input("الإيميل")
        st.text_input("الباسورد", type="password")
        if st.button("دخول للمنصة", use_container_width=True):
            st.session_state['auth'] = True
            st.rerun()
    with t2:
        st.text_input("الاسم")
        st.button("إنشاء حساب", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # زر الخروج فوق
    c_out1, c_out2 = st.columns([0.9, 0.1])
    with c_out2:
        if st.button("خروج"):
            st.session_state['auth'] = False
            st.rerun()

    st.markdown("<h2 class='gold' style='text-align:center;'>🏠 قاعدة بيانات المشاريع</h2>", unsafe_allow_html=True)
    
    # البحث في المنتصف
    _, s_col, _ = st.columns([1, 2, 1])
    with s_col:
        search = st.text_input("", placeholder="🔍 ابحث هنا...")

    df = load_data()
    if not df.empty:
        if search:
            df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
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
