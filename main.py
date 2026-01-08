import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScC7Xz_0_JafB1WwTzyC4LJs1vXclpTU3YY_Bl2rPO_Q1S3tA/formResponse"

# 2. التنسيق (CSS) - شريط التمرير العريض وتصميم فخم
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    [data-testid="stSidebar"] { display: none; }
    
    /* شريط التمرير العريض الذهبي */
    ::-webkit-scrollbar { width: 22px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; border: 4px solid #161b22; }
    
    .login-box {
        background: #161b22; border: 2px solid #d4af37; border-radius: 25px;
        padding: 40px; text-align: center; margin: 50px auto; max-width: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .gold { color: #d4af37 !important; font-weight: 900; }
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 25px; margin-bottom: 20px;
    }
    .price-badge { background: #d4af37; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: bold; float: left; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# دالة إرسال البيانات لجوجل فورم (التسجيل الفعلي)
def send_to_google_form(name, email, phone, password):
    payload = {
        "entry.231920038": name,
        "entry.1705607062": email,
        "entry.1693892837": phone,
        "entry.1843336341": password
    }
    try:
        requests.post(FORM_URL, data=payload)
        return True
    except:
        return False

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except: return pd.DataFrame()

# --- الصفحات ---

if not st.session_state['auth']:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold">🏠 منصة معلوماتي</h1>', unsafe_allow_html=True)
    
    choice = st.tabs(["🔐 دخول", "✨ حساب جديد"])
    
    with choice[0]:
        email_in = st.text_input("البريد الإلكتروني")
        pass_in = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للمنصة", use_container_width=True):
            if email_in and pass_in:
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.error("أدخل بيانات الدخول")
                
    with choice[1]:
        n_name = st.text_input("الاسم بالكامل")
        n_email = st.text_input("الإيميل")
        n_phone = st.text_input("رقم الواتساب")
        n_pass = st.text_input("اختر كلمة مرور", type="password")
        
        if st.button("تأكيد التسجيل الفعلي", use_container_width=True):
            if n_name and n_email and n_pass:
                if send_to_google_form(n_name, n_email, n_phone, n_pass):
                    st.balloons()
                    st.success("تم حفظ بياناتك في جدول الإكسيل بنجاح! يمكنك الدخول الآن.")
                else:
                    st.error("حدث خطأ في الاتصال")
            else:
                st.warning("يرجى ملء جميع الخانات")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # الصفحة الرئيسية
    top1, top2 = st.columns([0.9, 0.1])
    with top2:
        if st.button("خروج"):
            st.session_state['auth'] = False
            st.rerun()
            
    st.markdown("<h2 class='gold' style='text-align:center;'>🏠 قاعدة بيانات المشاريع</h2>", unsafe_allow_html=True)
    
    # البحث
    _, s_col, _ = st.columns([1, 2, 1])
    with s_col:
        search = st.text_input("", placeholder="🔍 ابحث هنا عن أي شيء...")

    df = load_data()
    if not df.empty:
        if search:
            df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
        for _, row in df.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{row.get('السعر', 'اتصل')}</div>
                    <div class="gold" style="font-size:0.8em;">PROJECT REPORT</div>
                    <h2 style="margin:5px 0;">{row.get('المشروع', '-')}</h2>
                    <p>📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                    <div style="background:rgba(212,175,55,0.05); border-right:4px solid #d4af37; padding:15px; margin:15px 0; border-radius:5px;">
                        <b class="gold">📜 سابقة الأعمال:</b><br>{row.get('سابقة_الأعمال', '-')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
