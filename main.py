import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- 3. التصميم الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .smart-box { background: #161616; border: 1px solid #333; padding: 40px; border-radius: 20px; border-right: 5px solid #f59e0b; text-align: center; color: white; margin-top: 20px; }
    .update-text { color: #f59e0b; font-size: 24px; font-weight: bold; }
    .tool-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; }
    
    /* زر الخروج */
    .stButton > button[key="exit_btn"] { background-color: transparent !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. شاشة الدخول ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><div style='text-align:center;'><h1 style='color:#f59e0b; font-size:55px;'>MA3LOMATI</h1><p style='color:#777;'>PRO VERSION 2026</p></div>", unsafe_allow_html=True)
        u_in = st.text_input("اسم المستخدم", key="u_fast")
        p_in = st.text_input("كلمة المرور", type="password", key="p_fast")
        if st.button("دخول آمن 🚀", use_container_width=True):
            if p_in == "2026" or u_in == "admin":
                st.session_state.auth = True
                st.session_state.current_user = u_in
                st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# --- 5. واجهة المستخدم الرئيسية ---

# الهيدر وزر الخروج
c_out, c_title = st.columns([0.15, 0.85])
with c_out:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="exit_btn"):
        st.session_state.auth = False; st.rerun()

st.markdown(f"""
    <div style="background: #111; padding: 20px; border-radius: 20px; text-align: center; border-bottom: 4px solid #f59e0b; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b;">مرحباً بك: {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# المنيو الجديد (إضافة اللونشات)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 6. محتوى الأقسام ---

if menu == "اللونشات":
    st.markdown("<div class='smart-box'><h1>🚀 اللونشات الجديدة (2026)</h1><p>تابع أحدث انطلاقات المشاريع العقارية أولاً بأول</p><hr><h3 style='color:#f59e0b;'>قريباً: سيتم إدراج قائمة اللونشات الحالية هنا</h3></div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل متطلبات العميل للحصول على تحليل ذكي</p></div>", unsafe_allow_html=True)
    st.text_area("وصف الطلب...")

elif menu == "المشاريع":
    st.markdown("<div class='smart-box'><h2 class='update-text'>🔄 جاري التحديث...</h2><p>يتم الآن مراجعة وتحديث قاعدة بيانات المشاريع لعام 2026</p></div>", unsafe_allow_html=True)

elif menu == "المطورين":
    st.markdown("<div class='smart-box'><h2 class='update-text'>🔄 جاري التحديث...</h2><p>يتم الآن تحديث قوائم المطورين العقاريين وتصنيفاتهم الجديدة</p></div>", unsafe_allow_html=True)

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align: center; color: #f59e0b;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
    tools = [c1, c2, c3, c4, c5, c6]
    labels = ["💳 القسط", "💰 العمولة", "📈 ROI", "📐 المساحة", "📝 الضريبة", "🏦 التمويل"]
    for i, col in enumerate(tools):
        with col:
            st.markdown(f"<div class='tool-card'><h4>{labels[i]}</h4></div>", unsafe_allow_html=True)
            st.number_input("القيمة", key=f"t_{i}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- 3. التصميم الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .smart-box { background: #161616; border: 1px solid #333; padding: 40px; border-radius: 20px; border-right: 5px solid #f59e0b; text-align: center; color: white; margin-top: 20px; }
    .update-text { color: #f59e0b; font-size: 24px; font-weight: bold; }
    .tool-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; }
    
    /* زر الخروج */
    .stButton > button[key="exit_btn"] { background-color: transparent !important; color: #ff4b4b !important; border: 1px solid #ff4b4b !important; }
    </style>
""", unsafe_allow_html=True)

# --- 4. شاشة الدخول ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><div style='text-align:center;'><h1 style='color:#f59e0b; font-size:55px;'>MA3LOMATI</h1><p style='color:#777;'>PRO VERSION 2026</p></div>", unsafe_allow_html=True)
        u_in = st.text_input("اسم المستخدم", key="u_fast")
        p_in = st.text_input("كلمة المرور", type="password", key="p_fast")
        if st.button("دخول آمن 🚀", use_container_width=True):
            if p_in == "2026" or u_in == "admin":
                st.session_state.auth = True
                st.session_state.current_user = u_in
                st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# --- 5. واجهة المستخدم الرئيسية ---

# الهيدر وزر الخروج
c_out, c_title = st.columns([0.15, 0.85])
with c_out:
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="exit_btn"):
        st.session_state.auth = False; st.rerun()

st.markdown(f"""
    <div style="background: #111; padding: 20px; border-radius: 20px; text-align: center; border-bottom: 4px solid #f59e0b; margin-bottom: 20px;">
        <h1 style="color: white; margin: 0;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b;">مرحباً بك: {st.session_state.current_user}</p>
    </div>
""", unsafe_allow_html=True)

# المنيو الجديد (إضافة اللونشات)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 6. محتوى الأقسام ---

if menu == "اللونشات":
    st.markdown("<div class='smart-box'><h1>🚀 اللونشات الجديدة (2026)</h1><p>تابع أحدث انطلاقات المشاريع العقارية أولاً بأول</p><hr><h3 style='color:#f59e0b;'>قريباً: سيتم إدراج قائمة اللونشات الحالية هنا</h3></div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل متطلبات العميل للحصول على تحليل ذكي</p></div>", unsafe_allow_html=True)
    st.text_area("وصف الطلب...")

elif menu == "المشاريع":
    st.markdown("<div class='smart-box'><h2 class='update-text'>🔄 جاري التحديث...</h2><p>يتم الآن مراجعة وتحديث قاعدة بيانات المشاريع لعام 2026</p></div>", unsafe_allow_html=True)

elif menu == "المطورين":
    st.markdown("<div class='smart-box'><h2 class='update-text'>🔄 جاري التحديث...</h2><p>يتم الآن تحديث قوائم المطورين العقاريين وتصنيفاتهم الجديدة</p></div>", unsafe_allow_html=True)

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align: center; color: #f59e0b;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
    tools = [c1, c2, c3, c4, c5, c6]
    labels = ["💳 القسط", "💰 العمولة", "📈 ROI", "📐 المساحة", "📝 الضريبة", "🏦 التمويل"]
    for i, col in enumerate(tools):
        with col:
            st.markdown(f"<div class='tool-card'><h4>{labels[i]}</h4></div>", unsafe_allow_html=True)
            st.number_input("القيمة", key=f"t_{i}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
