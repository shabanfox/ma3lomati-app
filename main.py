import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات المنصة
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# الروابط الأساسية
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"
# الرابط الصحيح للإرسال (تم التعديل لـ formResponse)
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScC7Xz_0_JafB1WwTzyC4LJs1vXclpTU3YY_Bl2rPO_Q1S3tA/formResponse"

# تنسيق الواجهة (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="st-"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; }
    .stApp { background-color: #0d1117; color: white; }
    
    /* شريط التمرير العريض */
    ::-webkit-scrollbar { width: 22px !important; }
    ::-webkit-scrollbar-track { background: #161b22 !important; }
    ::-webkit-scrollbar-thumb { background: #d4af37 !important; border-radius: 10px; border: 4px solid #161b22; }
    
    .login-box {
        background: #161b22; border: 2px solid #d4af37; border-radius: 25px;
        padding: 40px; text-align: center; margin: 50px auto; max-width: 500px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .gold { color: #d4af37 !important; font-weight: 900; }
    </style>
    """, unsafe_allow_html=True)

if 'auth' not in st.session_state:
    st.session_state['auth'] = False

# دالة الإرسال الفعلية (تم التأكد من الأرقام)
def send_data(name, email, phone, password):
    data = {
        "entry.231920038": name,
        "entry.1705607062": email,
        "entry.1693892837": phone,
        "entry.1843336341": password
    }
    try:
        # إرسال الطلب كأنه فورم حقيقي
        response = requests.post(FORM_URL, data=data)
        return response.status_code == 200
    except:
        return False

# --- الواجهة ---
if not st.session_state['auth']:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown('<h1 class="gold">🏠 منصة معلوماتي</h1>', unsafe_allow_html=True)
    
    tabs = st.tabs(["🔐 دخول", "✨ حساب جديد"])
    
    with tabs[0]:
        e_in = st.text_input("الإيميل")
        p_in = st.text_input("الباسورد", type="password")
        if st.button("دخول", use_container_width=True):
            st.session_state['auth'] = True
            st.rerun()
            
    with tabs[1]:
        n = st.text_input("الاسم")
        em = st.text_input("الإيميل ")
        ph = st.text_input("الواتساب")
        ps = st.text_input("الباسورد ", type="password")
        
        if st.button("تسجيل الآن", use_container_width=True):
            if n and em and ps:
                # محاولة الإرسال
                send_data(n, em, ph, ps)
                st.balloons()
                st.success("تم تسجيلك! روح دلوقتي لصفحة الـ Responses في جوجل فورم هتلاقي اسمك نور هناك.")
            else:
                st.warning("املأ البيانات أولاً")
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.button("خروج", on_click=lambda: st.session_state.update({"auth": False}))
    st.write("أنت الآن داخل المنصة")
