import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# الرابط المباشر للبيانات (CSV)
CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# إدارة حالة تسجيل الدخول
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# 2. تصميم الواجهة (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .stApp { background-color: #0d1117; font-family: 'Cairo', sans-serif; color: white; }
    .gold { color: #d4af37 !important; font-weight: 900; }
    .card {
        background: linear-gradient(145deg, #1c2128, #0d1117);
        border: 1px solid #30363d; border-radius: 20px;
        padding: 25px; margin-bottom: 25px; direction: rtl; text-align: right;
    }
    .price-tag { background: #d4af37; color: black; padding: 6px 18px; border-radius: 10px; font-weight: bold; float: left; }
    /* تنسيق صندوق تسجيل الدخول */
    .login-box {
        max-width: 400px; margin: auto; padding: 40px;
        background: #161b22; border-radius: 20px; border: 1px solid #d4af37;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# دالة تحميل البيانات
@st.cache_data(ttl=5)
def load_data():
    try:
        response = requests.get(CSV_URL)
        response.encoding = 'utf-8'
        df = pd.read_csv(StringIO(response.text))
        df.columns = [str(c).strip() for c in df.columns]
        df = df.astype(str).replace(['nan', 'NaN', 'None'], 'غير مدرج')
        return df
    except:
        return pd.DataFrame()

# --- المنطق البرمجي للصفحات ---

if not st.session_state['logged_in']:
    # صفحة تسجيل الدخول المنفصلة
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<h1 class='gold' style='text-align:center;'>🏠 معلوماتي العقارية</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center;'>بوابة بروكرز مصر - سجل دخولك للمتابعة</p>", unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["تسجيل دخول", "حساب جديد مجاني"])
        
        with tab1:
            user = st.text_input("اسم المستخدم أو البريد")
            pw = st.text_input("كلمة المرور", type="password")
            if st.button("دخول للمنصة", use_container_width=True):
                # هنا نضع شرط الدخول (للتجربة حالياً أي دخول سينجح)
                st.session_state['logged_in'] = True
                st.rerun()
        
        with tab2:
            st.text_input("الاسم")
            st.text_input("رقم الواتساب")
            st.button("إنشاء حسابي الآن", use_container_width=True)

else:
    # الصفحة الرئيسية (تعرض بعد تسجيل الدخول فقط)
    with st.sidebar:
        st.markdown(f"<h3 class='gold'>أهلاً بك يا بروكر</h3>", unsafe_allow_html=True)
        if st.button("تسجيل الخروج"):
            st.session_state['logged_in'] = False
            st.rerun()
        st.divider()

    st.markdown("<h2 style='text-align:center;' class='gold'>🏠 منصة معلوماتي العقارية</h2>", unsafe_allow_html=True)
    
    # البحث في المنتصف تماماً
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        search = st.text_input("", placeholder="🔍 ابحث عن المطور، المشروع، أو المالك...")

    df = load_data()
    if not df.empty:
        # الفلترة والعرض (كما في الكود السابق)
        f_df = df.copy()
        if search:
            f_df = f_df[f_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
        st.markdown(f"<p style='text-align:center;'>نتائج البحث: {len(f_df)}</p>", unsafe_allow_html=True)
        
        for _, row in f_df.iterrows():
            st.markdown(f"""
                <div class="card">
                    <div class="price-tag">{row.get('السعر', 'اتصل')}</div>
                    <div class="gold">ملف العقار</div>
                    <h2>{row.get('المشروع', '-')}</h2>
                    <p>🏢 {row.get('المطور', '-')} | 📍 {row.get('المنطقة', '-')}</p>
                    <div style="background: rgba(255,255,255,0.03); border-right: 4px solid #d4af37; padding: 15px; margin: 15px 0;">
                        <b>📜 سابقة الأعمال:</b> {row.get('سابقة_الأعمال', '-')}
                    </div>
                    <div style="display: flex; gap: 30px; font-size: 0.9em; border-top: 1px solid #333; padding-top: 10px;">
                        <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                        <div><span class="gold">💳 السداد:</span> {row.get('السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
