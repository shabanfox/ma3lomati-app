import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة (يجب أن تكون أول أمر)
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. تهيئة الذاكرة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'user_db' not in st.session_state: st.session_state.user_db = {"admin": "2026"} # قاعدة بيانات مؤقتة
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'active_menu' not in st.session_state: st.session_state.active_menu = "المساعد الذكي"

# 3. شاشة التسجيل والدخول (قبل أي محتوى آخر)
if not st.session_state.auth:
    st.markdown("<h1 style='color:#f59e0b; text-align:center; padding-top:30px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 إنشاء حساب بروكر"])
    
    with tab_login:
        _, c2, _ = st.columns([1,1,1])
        with c2:
            u = st.text_input("اسم المستخدم", key="u_login")
            p = st.text_input("كلمة السر", type="password", key="p_login")
            if st.button("دخول للنظام", use_container_width=True):
                if u in st.session_state.user_db and st.session_state.user_db[u] == p:
                    st.session_state.auth = True
                    st.session_state.current_user = u
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        _, c2, _ = st.columns([1,1,1])
        with c2:
            nu = st.text_input("اسم مستخدم جديد")
            np = st.text_input("كلمة سر جديدة", type="password")
            if st.button("إنشاء حساب", use_container_width=True):
                if nu and np:
                    st.session_state.user_db[nu] = np
                    st.success("تم التسجيل! ادخل الآن من خانة تسجيل دخول")
                else:
                    st.error("برجاء ملء البيانات")
    st.stop() # يوقف الكود هنا لحد ما يسجل دخول

# --- لو وصل هنا يبقى مسجل دخول (باقي كود التطبيق) ---

# 4. جلب البيانات والأخبار (نفس كودك الأصلي)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.rename(columns={'Area': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 5. التصميم الهيدر والمنيو (نفس كودك مع تعديل بسيط)
st.markdown(f"<p style='text-align:left; color:#aaa;'>مرحباً بك: {st.session_state.current_user} | 2026</p>", unsafe_allow_html=True)

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# حل مشكلة تعليق الصفحات عند التنقل
if menu != st.session_state.active_menu:
    st.session_state.selected_item = None
    st.session_state.active_menu = menu
    st.rerun()

# 6. عرض المحتوى
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.selected_item = None
        st.rerun()
    st.write(st.session_state.selected_item) # عرض تفاصيل المشروع

else:
    if menu == "المساعد الذكي":
        st.title("🤖 المساعد الذكي")
        # كود المساعد...
    elif menu == "المشاريع":
        st.title("🏗️ دليل المشاريع")
        for i, r in df_p.head(10).iterrows():
            if st.button(f"{r['ProjectName']}", key=f"card_p_{i}"):
                st.session_state.selected_item = r
                st.rerun()
    elif menu == "المطورين":
        st.title("🏢 كبار المطورين")
        # كود المطورين...
    elif menu == "أدوات البروكر":
        st.title("🛠️ أدواتك الحسابية")
        if st.button("🚪 تسجيل الخروج"):
            st.session_state.auth = False
            st.rerun()
