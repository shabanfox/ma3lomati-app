import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أسود، أبيض، وكروت صفراء)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء زوائد ستريمليت */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* 1. الخلفية أسود غامق والكتابة أبيض */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] { 
        background-color: #000000 !important; 
        color: #ffffff !important;
        font-family: 'Cairo', sans-serif;
        direction: RTL;
    }

    /* 2. الكروت أصفر بالكامل 1*1 ومتلاصقة */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    
    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 180px !important;
        background-color: #fcc419 !important; /* أصفر صريح */
        color: #000000 !important; /* كتابة سوداء داخل الأصفر */
        border: 0.5px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        margin: 0px !important;
    }

    /* 3. أزرار التحكم (السابق والتالي) مصغرة */
    .control-btn button {
        height: 35px !important;
        width: 100px !important;
        background-color: transparent !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        font-size: 0.8rem !important;
        border-radius: 5px !important;
    }

    /* هيدر المنصة */
    .main-header {
        text-align: center; 
        padding: 40px; 
        border-bottom: 1px solid #333;
        font-size: 2.5rem;
        font-weight: 900;
        color: #ffffff;
    }
    
    /* تباعد البحث */
    .stTextInput input {
        background-color: #111 !important;
        color: white !important;
        border: 1px solid #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. تحميل البيانات
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
    st.markdown('<div class="main-header">منصة معلوماتى</div>', unsafe_allow_html=True)
    st.write("<div style='height:100px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🏢 دليل المطورين", key="home_dev"): st.session_state.view = 'companies'; st.rerun()
    with c2: 
        if st.button("🛠️ أدوات البروكر", key="home_tool"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">دليل المطورين</div>', unsafe_allow_html=True)

    # زر العودة بعيد عن الشبكة
    st.write("")
    col_back, col_search = st.columns([1, 4])
    with col_back:
        st.markdown('<div class="control-btn">', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back_btn"): st.session_state.view = 'home'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_search:
        search = st.text_input("", placeholder="🔍 ابحث عن مطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة جهة اليمين 70%
    grid_side, empty_side = st.columns([0.7, 0.3])
    with grid_side:
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
                            st.sidebar.title(dev_name)
                            projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                            for p in projs: st.sidebar.write(f"• {p}")

    # --- أزرار التالي والسابق في نص الصفحة وجنب بعض ---
    st.write("<div style='height:80px;'></div>", unsafe_allow_html=True) # تباعد عن الشبكة
    
    # 3 أعمدة (الأوسط هو اللي فيه الأزرار عشان يبقوا في النص بالظبط)
    _, center_col, _ = st.columns([2, 1, 2])
    with center_col:
        # عمودين صغيرين جوه السنتر كول عشان يبقوا لزق في بعض
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            st.markdown('<div class="control-btn">', unsafe_allow_html=True)
            if st.button("⬅️ السابق", key="prev_pg") and st.session_state.page > 0:
                st.session_state.page -= 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with btn_col2:
            st.markdown('<div class="control-btn">', unsafe_allow_html=True)
            if (start + items) < len(unique_devs):
                if st.button("التالي ➡️", key="next_pg"):
                    st.session_state.page += 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">أدوات البروكر</div>', unsafe_allow_html=True)
    st.markdown('<div class="control-btn">', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="tool_b"): st.session_state.view = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
