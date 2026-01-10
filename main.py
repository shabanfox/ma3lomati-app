import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أسود صريح، كروت صفراء، توسيط أزرار التنقل)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* 1. إخفاء زوائد المنصة بالكامل */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* 2. الخلفية سوداء غامقة جداً */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #000000 !important; 
        direction: RTL; 
        font-family: 'Cairo', sans-serif;
    }

    /* 3. شبكة المطورين: صفراء 1*1 متلاصقة جهة اليمين */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    div.block-container { padding: 0rem !important; }

    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 160px !important;
        background-color: #FFCC00 !important; /* أصفر فاقع */
        color: #000000 !important; /* نص أسود */
        border: 0.5px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: 900 !important;
        margin: 0px !important;
    }

    /* 4. أزرار التحكم: تصغير وتوسيط وتلاصق */
    .stButton > button[key^="nav_"] {
        height: 35px !important;
        width: 100px !important;
        background-color: #111 !important;
        color: #fff !important;
        border: 1px solid #fff !important;
        border-radius: 4px !important;
        font-size: 0.8rem !important;
    }

    /* توسيط الأزرار في نص الصفحة */
    .center-nav {
        display: flex;
        justify-content: center;
        gap: 10px;
        padding: 50px 0px;
        width: 100%;
    }
    
    /* جعل الهيدر أبيض فوق الأسود */
    h1, h2 { color: white !important; text-align: center; padding: 20px; }
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
        if st.button("🏢 دليل المطورين", key="nav_h1"): st.session_state.view = 'companies'; st.rerun()
    with c2: 
        if st.button("🛠️ أدوات البروكر", key="nav_h2"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<h2>دليل المطورين</h2>', unsafe_allow_html=True)

    # صف العودة والبحث
    st.markdown('<div style="padding: 10px;">', unsafe_allow_html=True)
    c_back, c_search = st.columns([1, 5])
    with c_back:
        if st.button("🔙 عودة", key="nav_back"): st.session_state.view = 'home'; st.rerun()
    with c_search:
        search = st.text_input("", placeholder="🔍 ابحث هنا...")
    st.markdown('</div>', unsafe_allow_html=True)

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة جهة اليمين 70%
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

    # --- أزرار التالي والسابق في نص الصفحة وجنب بعض بالظبط ---
    st.markdown('<div style="height:60px;"></div>', unsafe_allow_html=True)
    
    # استخدام أعمدة لتوسيط الأزرار بشكل هندسي دقيق
    _, mid_col, _ = st.columns([2, 1, 2])
    with mid_col:
        btn_left, btn_right = st.columns(2)
        with btn_left:
            if st.button("⬅️ السابق", key="nav_prev") and st.session_state.page > 0:
                st.session_state.page -= 1; st.rerun()
        with btn_right:
            if (start + items) < len(unique_devs):
                if st.button("التالي ➡️", key="nav_next"):
                    st.session_state.page += 1; st.rerun()
