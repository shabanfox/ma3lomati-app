import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. رابط البيانات (CSV) ---
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة حالة الجلسة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_launch' not in st.session_state: st.session_state.selected_launch = None

# --- 4. وظيفة جلب البيانات ---
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
    
    /* تصميم كروت اللونشات */
    div.stButton > button[key^="lnch_"] {
        background: #161616 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-top: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        height: 160px !important;
        width: 100% !important;
        font-weight: bold !important;
        font-size: 18px !important;
        white-space: pre-line !important;
    }
    
    /* حاوية التفاصيل */
    .detail-card { background: #111; padding: 30px; border-radius: 20px; border-right: 8px solid #f59e0b; margin-top: 10px; }
    .label { color: #f59e0b; font-weight: bold; font-size: 15px; margin-bottom: 2px; }
    .value { color: #fff; font-size: 19px; margin-bottom: 20px; line-height: 1.5; }
    .usp-box { background: #1a1a1a; padding: 20px; border-radius: 12px; border: 1px dashed #f59e0b; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 6. تسجيل الدخول ---
if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI</h1>", unsafe_allow_html=True)
        pwd = st.text_input("Password", type="password")
        if st.button("LOGIN", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
            else: st.error("Wrong Password")
    st.stop()

# --- 7. المنيو الرئيسي ---
c_out, _ = st.columns([0.15, 0.85])
with c_out:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 8. محتوى اللونشات ---
if menu == "اللونشات":
    df_l = load_launches()
    
    if st.session_state.selected_launch is not None:
        item = st.session_state.selected_launch
        if st.button("⬅️ عودة لجميع اللونشات"):
            st.session_state.selected_launch = None
            st.rerun()
        
        # عرض التفاصيل بالترتيب الذي طلبته
        st.markdown(f"<div class='detail-card'>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color:#f59e0b; margin-bottom:0;'>{item.get('Project', 'Project Name')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#aaa; margin-top:0;'>🏢 {item.get('Developer', 'Developer Name')}</h3><hr style='border-color:#222;'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"<p class='label'>📍 Location (الموقع)</p><p class='value'>{item.get('Location', '---')}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='label'>📏 Units & Sizes (المساحات)</p><p class='value'>{item.get('Units & Sizes', '---')}</p>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"<p class='label'>💰 Price & Payment (السعر والسداد)</p><p class='value'>{item.get('Price & Payment', '---')}</p>", unsafe_allow_html=True)
        
        # عرض الـ USP بشكل مميز
        st.markdown(f"<p class='label'>🌟 Unique Selling Points (مميزات المشروع)</p>", unsafe_allow_html=True)
        st.markdown(f"<div class='usp-box'><p style='color:#eee; font-size:17px; line-height:1.7;'>{item.get('Unique Selling Points (USP)', 'سيتم التحديث قريباً...')}</p></div>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

    else:
        st.markdown("<h2 style='text-align:center; color:white;'>🚀 أحدث لونشات 2026</h2>", unsafe_allow_html=True)
        if not df_l.empty:
            cols = st.columns(3)
            for index, row in df_l.iterrows():
                with cols[index % 3]:
                    # الكارت يظهر المطور والمشروع والموقع
                    lbl = f"🏢 {row.get('Developer', 'Motaweer')}\n{row.get('Project', 'Project')}\n📍 {row.get('Location', 'Location')}"
                    if st.button(lbl, key=f"lnch_{index}"):
                        st.session_state.selected_launch = row
                        st.rerun()
        else:
            st.warning("برجاء التأكد من تعبئة البيانات في الشيت ونشره بصيغة CSV.")

# باقي الأقسام تظل كرسائل تحديث حالياً كما طلبنا سابقاً
elif menu == "المشاريع" or menu == "المطورين":
    st.markdown("<br><div style='text-align:center; padding:100px; color:#555;'><h1>🔄 جاري التحديث</h1><p>يتم رفع قاعدة بيانات 2026</p></div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
