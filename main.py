import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# الروابط الخاصة بك
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScC7Xz_0_JafB1WwTzyC4LJs1vXclpTU3YY_Bl2rPO_Q1S3tA/formResponse"

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الخط والاتجاه */
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    
    /* إخفاء القائمة الجانبية */
    [data-testid="stSidebar"] { display: none; }

    /* --- شريط التمرير العريض جداً والذهبي --- */
    ::-webkit-scrollbar { width: 25px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { 
        background: #d4af37 !important; 
        border-radius: 12px; 
        border: 5px solid #161b22; 
    }
    ::-webkit-scrollbar-thumb:hover { background: #f1c40f !important; }

    /* حاوية الدخول */
    .login-box {
        background: #161b22; border: 2px solid #d4af37; border-radius: 25px;
        padding: 40px; text-align: center; margin: 50px auto; max-width: 550px;
        box-shadow: 0 15px 40px rgba(0,0,0,0.6);
    }
    
    .gold { color: #d4af37 !important; font-weight: 900; }
    
    /* كروت المشاريع */
    .project-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 20px;
        padding: 30px; margin-bottom: 25px; transition: 0.3s ease;
    }
    .project-card:hover { border-color: #d4af37; transform: translateY(-5px); }
    
    .price-badge { 
        background: #d4af37; color: black; padding: 8px 20px; 
        border-radius: 10px; font-weight: 800; float: left; font-size: 1.1em;
    }

    .info-box {
        background: rgba(212, 175, 55, 0.05);
        border-right: 5px solid #d4af37;
        padding: 20px; margin: 20px 0; border-radius: 8px;
    }
    
    /* تنسيق خانة البحث */
    .stTextInput > div > div > input {
        background-color: #161b22 !important; color: white !important;
        border: 2px solid #30363d !important; border-radius: 15px !important;
        height: 55px; text-align: center; font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)

# إدارة حالة الجلسة
if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# دالة إرسال البيانات لجوجل فورم
def save_to_google(name, email, phone, password):
    # الأرقام المستخرجة من الفورم الخاص بك
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

# دالة تحميل بيانات المشاريع
@st.cache_data(ttl=10)
def load_projects():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.astype(str).replace(['nan', 'NaN'], 'غير مدرج')
    except:
        return pd.DataFrame()

# --- منطق عرض الصفحات ---

if not st.session_state['auth']:
    # صفحة تسجيل الدخول / إنشاء الحساب
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold">🏢 منصة معلوماتي</h1>', unsafe_allow_html=True)
    st.markdown('<p style="opacity:0.8;">بوابة بروكرز مصر العقارية</p>', unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 دخول", "✨ حساب جديد"])
    
    with tab_login:
        login_email = st.text_input("البريد الإلكتروني", key="l_email")
        login_pass = st.text_input("كلمة المرور", type="password", key="l_pass")
        if st.button("دخول للمنصة الآن", use_container_width=True):
            if login_email and login_pass:
                st.session_state['auth'] = True
                st.rerun()
            else:
                st.warning("الرجاء إدخال بيانات الدخول")
                
    with tab_signup:
        s_name = st.text_input("الاسم بالكامل")
        s_email = st.text_input("الإيميل")
        s_phone = st.text_input("رقم الواتساب")
        s_pass = st.text_input("اختر كلمة مرور", type="password")
        
        if st.button("إنشاء حسابي وتفعيل العضوية", use_container_width=True):
            if s_name and s_email and s_pass:
                # إرسال فعلي للبيانات
                save_to_google(s_name, s_email, s_phone, s_pass)
                st.balloons()
                st.success("تم تسجيل بياناتك بنجاح! يمكنك الآن تسجيل الدخول.")
            else:
                st.error("برجاء ملء الخانات الأساسية")
    st.markdown('</div>', unsafe_allow_html=True)

else:
    # الصفحة الرئيسية بعد الدخول
    c1, c2 = st.columns([0.9, 0.1])
    with c2:
        if st.button("خروج 🚪"):
            st.session_state['auth'] = False
            st.rerun()
            
    st.markdown("<h1 class='gold' style='text-align:center;'>📂 دليل المشاريع والمطورين</h1>", unsafe_allow_html=True)
    
    # محرك البحث في المنتصف
    _, s_box, _ = st.columns([1, 2, 1])
    with s_box:
        search_term = st.text_input("", placeholder="🔍 ابحث عن المطور، المنطقة، أو اسم المشروع...")

    df_data = load_projects()
    
    if not df_data.empty:
        # فلترة البيانات بناءً على البحث
        if search_term:
            df_data = df_data[df_data.apply(lambda r: search_term.lower() in str(r).lower(), axis=1)]
        
        st.markdown(f"<p style='text-align:center; opacity:0.7;'>تم إيجاد {len(df_data)} نتيجة</p>", unsafe_allow_html=True)

        for _, row in df_data.iterrows():
            st.markdown(f"""
                <div class="project-card">
                    <div class="price-badge">{row.get('السعر', 'اتصل')}</div>
                    <div class="gold" style="font-size: 0.8em; font-weight: bold;">PROJECT DATA SHEET</div>
                    <h2 style="margin: 10px 0;">{row.get('المشروع', '-')}</h2>
                    <p style="font-size: 1.1em; opacity: 0.9;">📍 {row.get('المنطقة', '-')} | 🏢 {row.get('المطور', '-')}</p>
                    
                    <div class="info-box">
                        <b class="gold">📜 سابقة الأعمال والخبرة:</b><br>
                        {row.get('سابقة_الأعمال', 'لا توجد بيانات متاحة')}
                    </div>
                    
                    <div style="display: flex; gap: 40px; border-top: 1px solid #30363d; padding-top: 15px; font-size: 0.9em;">
                        <div><span class="gold">👤 المالك:</span> {row.get('المالك', '-')}</div>
                        <div><span class="gold">💳 نظام السداد:</span> {row.get('السداد', '-')}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("جاري مزامنة البيانات من الإكسيل...")
