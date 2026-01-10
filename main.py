import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS المطور (أزرار نانو زرقاء وتثبيت الكروت)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-banner { 
        background: #000; color: #f59e0b; padding: 20px; border-radius: 20px; 
        text-align: center; margin-bottom: 25px; border: 4px solid #f59e0b;
        box-shadow: 8px 8px 0px #000;
    }

    /* --- زر العودة نانو أزرق --- */
    div.stButton > button[key^="back_"] {
        background-color: #007bff !important; /* لون أزرق */
        color: white !important;
        font-size: 0.8rem !important; /* حجم نانو */
        padding: 2px 10px !important;
        height: auto !important;
        width: auto !important;
        min-height: 30px !important;
        border-radius: 8px !important;
        border: none !important;
        box-shadow: 2px 2px 0px #000 !important;
        margin-bottom: 15px !important;
    }
    div.stButton > button[key^="back_"]:hover {
        background-color: #0056b3 !important;
        transform: scale(0.95);
    }

    /* --- كروت المطورين: مقاس كبير وثابت 100% --- */
    div.stButton > button:not([key^="back_"]) {
        width: 100% !important;
        height: 200px !important; /* ارتفاع ثابت عملاق */
        min-height: 200px !important;
        background-color: #ffffff !important;
        border: 6px solid #000000 !important;
        border-radius: 25px !important;
        box-shadow: 10px 10px 0px #000000 !important;
        font-size: 1.7rem !important;
        font-weight: 900 !important;
        color: #000 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    .tool-result {
        background: #fff; border: 5px solid #000; padding: 20px;
        border-radius: 25px; box-shadow: 8px 8px 0px #000;
        text-align: center; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Developer', 'Project'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page' not in st.session_state: st.session_state.page = 0

df = st.session_state.data
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]
proj_col = df.columns[0]

# --- الشاشة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🏢\nدليل المطورين"): st.session_state.view = 'comp'; st.rerun()
    if c2.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

# --- صفحة المطورين ---
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    col_content, _ = st.columns([0.7, 0.3])
    with col_content:
        if st.button("🔙 عودة نانو", key="back_comp"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث...")
        unique_devs = df[dev_col].dropna().unique()
        if search: unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items = 9
        start = st.session_state.page * items
        curr = unique_devs[start : start + items]
        
        for i in range(0, len(curr), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr):
                    name = curr[i + j]
                    if cols[j].button(name, key=f"dev_{name}"):
                        st.session_state.selected_dev = name
                        st.session_state.view = 'details'; st.rerun()

# --- صفحة الأدوات ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ الأدوات الذكية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة نانو", key="back_tool"): st.session_state.view = 'main'; st.rerun()
    
    t1, t2 = st.tabs(["💰 القسط", "📈 ROI"])
    with t1:
        p = st.number_input("السعر", value=1000000)
        d = st.number_input("المقدم %", value=10)
        y = st.number_input("السنوات", value=8)
        res_d = p * (d/100)
        res_m = (p - res_d) / (y * 12) if y > 0 else 0
        st.markdown(f'<div class="tool-result"><h4>المقدم: {res_d:,.0f}</h4><h4 style="color:green">القسط: {res_m:,.0f}</h4></div>', unsafe_allow_html=True)
    
    with t2:
        b = st.number_input("شراء", value=1000000)
        s = st.number_input("بيع", value=1500000)
        profit = (s - b)
        st.markdown(f'<div class="tool-result"><h4>الربح: {profit:,.0f}</h4></div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.view == 'details':
    st.markdown(f'<div class="hero-banner"><h2>{st.session_state.selected_dev}</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة نانو", key="back_det"): st.session_state.view = 'comp'; st.rerun()
    projs = df[df[dev_col] == st.session_state.selected_dev][proj_col].unique()
    for p in projs:
        st.markdown(f'<div style="border:3px solid #000; padding:10px; border-radius:15px; margin-bottom:10px; box-shadow:4px 4px 0px #000;">🔹 {p}</div>', unsafe_allow_html=True)
