import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (الأسود والذهبي الملكي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الخلفية سوداء غامقة */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #000000 !important; 
        direction: RTL; 
        font-family: 'Cairo', sans-serif;
    }

    /* إلغاء المسافات بين كروت المطورين */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    div.block-container { padding: 0rem !important; }

    /* الكروت بلون ذهبي ملكي متدرج */
    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 180px !important;
        /* تدرج ذهبي فخم */
        background: linear-gradient(135deg, #BF953F, #FCF6BA, #B38728, #FBF5B7, #AA771C) !important;
        color: #000000 !important; 
        border: 0.5px solid rgba(0,0,0,0.3) !important;
        border-radius: 0px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        margin: 0px !important;
        transition: 0.4s;
    }

    /* تأثير عند الوقوف على الكارت الذهبي */
    div.stButton > button[key^="dev_"]:hover {
        filter: brightness(1.2);
        transform: scale(0.97);
        box-shadow: 0px 0px 20px rgba(212, 175, 55, 0.4) !important;
    }

    /* أزرار التنقل (السابق والتالي) صغيرة وجنب بعض في النص */
    .stButton > button[key^="nav_"] {
        height: 35px !important;
        width: 110px !important;
        background-color: transparent !important;
        color: #D4AF37 !important; /* لون الخط ذهبي */
        border: 1px solid #D4AF37 !important;
        border-radius: 2px !important;
        font-size: 0.8rem !important;
    }

    h1, h2 { color: #D4AF37 !important; text-align: center; padding: 20px; font-weight: 900; }
    
    /* مربع البحث */
    input { background-color: #111 !important; color: white !important; border: 1px solid #D4AF37 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

df = load_data()
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0

# --- العرض ---

if st.session_state.view == 'home':
    st.markdown('<h1>منصة معلوماتى العقارية</h1>', unsafe_allow_html=True)
    st.write("<br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🏢 دخول دليل المطورين", key="nav_h1"): st.session_state.view = 'companies'; st.rerun()
    with c2: 
        if st.button("🛠️ دخول أدوات البروكر", key="nav_h2"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<h2>دليل المطورين</h2>', unsafe_allow_html=True)

    # صف العودة والبحث
    st.write("")
    c_back, c_search = st.columns([1, 5])
    with c_back:
        if st.button("🔙 عودة", key="nav_back"): st.session_state.view = 'home'; st.rerun()
    with c_search:
        search = st.text_input("", placeholder="🔍 ابحث عن المطور هنا...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة الذهبية جهة اليمين 70%
    col_grid, col_empty = st.columns([0.7, 0.3])
    with col_grid:
        items = 12
        start = st.session_state.page * items
        batch = unique_devs[start : start + items]

        for i in range(0, len(batch), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(batch):
                    dev_name = batch[i + j]
                    with cols[j]:
                        if st.button(str(dev_name), key=f"dev_{start+i+j}"):
                            st.sidebar.markdown(f"### {dev_name}")
                            projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                            for p in projs: st.sidebar.write(f"• {p}")

    # أزرار التنقل (السابق والتالي) ممركزة وجنب بعض
    st.write("<div style='height:80px;'></div>", unsafe_allow_html=True)
    
    # تقسيم الأعمدة لتوسيط الأزرار
    _, mid_col, _ = st.columns([2.2, 1, 2])
    with mid_col:
        btn_l, btn_r = st.columns(2)
        with btn_l:
            if st.button("⬅️ السابق", key="nav_prev") and st.session_state.page > 0:
                st.session_state.page -= 1; st.rerun()
        with btn_r:
            if (start + items) < len(unique_devs):
                if st.button("التالي ➡️", key="nav_next"):
                    st.session_state.page += 1; st.rerun()
