import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu
import time

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات (رابط اللونشات الجديد CSV) ---
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_launch' not in st.session_state: st.session_state.selected_launch = None

# --- 4. وظائف جلب البيانات (مع تسريع Cache) ---
@st.cache_data(ttl=60)
def load_launches():
    try:
        df = pd.read_csv(URL_LAUNCHES).fillna("---")
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# --- 5. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    /* ستايل كروت اللونشات (أزرار تفاعلية) */
    div.stButton > button[key^="lnch_"] {
        background: #161616 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-top: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        height: 180px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 18px !important;
        transition: 0.3s !important;
        white-space: pre-line !important; /* للسماح بنزول السطر */
    }
    div.stButton > button[key^="lnch_"]:hover {
        border-color: #f59e0b !important;
        transform: translateY(-5px) !important;
    }

    .smart-box { background: #111; border: 1px solid #333; padding: 40px; border-radius: 20px; border-right: 5px solid #f59e0b; text-align: center; color: white; }
    .tool-card { background: #1a1a1a; padding: 20px; border-radius: 15px; border-top: 4px solid #f59e0b; text-align: center; }
    input { text-align: right !important; direction: rtl !important; }
    </style>
""", unsafe_allow_html=True)

# --- 6. شاشة الدخول (Fast Login) ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><div style='text-align:center;'><h1 style='color:#f59e0b; font-size:55px;'>MA3LOMATI</h1><p style='color:#777;'>PRO VERSION 2026</p></div>", unsafe_allow_html=True)
        u_in = st.text_input("اسم المستخدم", key="u_login")
        p_in = st.text_input("كلمة المرور", type="password", key="p_login")
        if st.button("دخول آمن 🚀", use_container_width=True):
            if p_in == "2026" or u_in == "admin":
                st.session_state.auth = True
                st.session_state.current_user = u_in
                st.rerun()
            else: st.error("بيانات غير صحيحة")
    st.stop()

# --- 7. الهيدر وزر الخروج (يساراً) ---
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

# المنيو (اللونشات هي الصفحة الرئيسية)
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 8. منطق الأقسام ---

if menu == "اللونشات":
    # التحقق من حالة عرض التفاصيل
    if st.session_state.selected_launch is not None:
        item = st.session_state.selected_launch
        if st.button("⬅️ عودة لقائمة اللونشات"):
            st.session_state.selected_launch = None
            st.rerun()
        
        st.markdown(f"""
            <div class='smart-box' style='text-align:right;'>
                <h1 style='color:#f59e0b;'>{item.get('Project', 'مشروع جديد')}</h1>
                <h3>🏢 المطور: {item.get('Developer', '---')}</h3>
                <hr style='border-color:#333;'>
                <p style='font-size:20px;'>📍 الموقع: {item.get('Location', '---')}</p>
                <p style='font-size:20px;'>💰 مبلغ الجدية (EOI): <span style='color:#f59e0b;'>{item.get('EOI', '---')}</span></p>
                <p style='font-size:18px; color:#aaa; line-height:1.6;'>📝 تفاصيل إضافية: {item.get('Notes', 'لا توجد ملاحظات')}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: white;'>🚀 أحدث انطلاقات 2026</h2>", unsafe_allow_html=True)
        df_l = load_launches()
        if not df_l.empty:
            cols = st.columns(3)
            for index, row in df_l.iterrows():
                with cols[index % 3]:
                    # تصميم النص داخل الزر
                    label = f"🏢 {row.get('Developer', 'مطور')}\n{row.get('Project', 'مشروع')}\n📍 {row.get('Location', '---')}"
                    if st.button(label, key=f"lnch_{index}"):
                        st.session_state.selected_launch = row
                        st.rerun()
        else:
            st.info("جاري تحميل بيانات اللونشات من الشيت...")

elif menu == "المشاريع" or menu == "المطورين":
    st.markdown("<br><div class='smart-box'><h2>🔄 جاري التحديث...</h2><p>يتم الآن رفع قاعدة البيانات الجديدة لعام 2026</p></div>", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل متطلبات العميل هنا...</p></div>", unsafe_allow_html=True)
    st.text_area("وصف طلب العميل...")

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align: center; color: #f59e0b;'>🛠️ أدوات البروكر العقاري</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3); c4, c5, c6 = st.columns(3)
    tools = ["💳 القسط", "💰 العمولة", "📈 ROI", "📐 المساحة", "📝 الضريبة", "🏦 التمويل"]
    cols_list = [c1, c2, c3, c4, c5, c6]
    for i, col in enumerate(cols_list):
        with col:
            st.markdown(f"<div class='tool-card'><h4>{tools[i]}</h4></div>", unsafe_allow_html=True)
            st.number_input("القيمة", key=f"tool_{i}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
