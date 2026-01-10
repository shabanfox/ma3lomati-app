

import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# تصميم CSS
st.markdown("""
    <style>
    #MainMenu, footer, header {visibility: hidden; display: none;}
    body { background-color: #000; color: #f59e0b; direction: RTL; }
    .stButton>button { border: 2px solid #f59e0b !important; background-color: #000 !important; color: #f59e0b !important; height: 60px !important; width: 100% !important; font-weight: bold; }
    .stButton>button:hover { background-color: #f59e0b !important; color: #000 !important; }
    </style>
""", unsafe_allow_html=True)

# نظام الدخول البسيط للتجربة
if "auth" not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    pwd = st.text_input("كلمة المرور", type="password")
    if st.button("دخول"):
        if pwd == "123": # جرب بـ 123 للتأكد فقط
            st.session_state.auth = True
            st.rerun()
    st.stop()

# الأزرار الثلاثة بجانب بعضها
st.title("🏠 منصة معلوماتى العقارية")
c1, c2, c3 = st.columns(3)
with c1:
    if st.button("🏠 الرئيسية"): st.info("أنت في الرئيسية")
with c2:
    if st.button("🛠️ أدوات البروكر"): st.success("تم الانتقال للأدوات")
with c3:
    if st.button("🏢 دليل المطورين"): st.warning("تم الانتقال للمطورين")
