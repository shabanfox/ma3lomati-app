import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide", initial_sidebar_state="collapsed")

# 2. CSS صارم جداً لتوحيد الأحجام (Force Equal Dimensions)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر */
    .hero-banner { 
        background: #000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }

    /* الحل النهائي لتوحيد الكروت: استهداف الحاوية مباشرة */
    div.stButton > button {
        width: 100% !important;
        aspect-ratio: 1 / 0.8 !important; /* يجعل الكارت مستطيل ذهبي ثابت */
        height: 200px !important;       /* ارتفاع إجباري لا يتغير */
        background-color: #ffffff !important;
        border: 6px solid #000000 !important;
        border-radius: 25px !important;
        box-shadow: 10px 10px 0px #000000 !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        color: #000 !important;
        white-space: normal !important;
        word-wrap: break-word !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.2s !important;
    }

    div.stButton > button:hover {
        transform: translate(-5px, -5px) !important;
        box-shadow: 15px 15px 0px #f59e0b !important;
        border-color: #f59e0b !important;
    }

    /* تنسيق الحاسبات في صفحة الأدوات */
    .tool-card-result {
        background: #fff; border: 5px solid #000; padding: 25px;
        border-radius: 25px; box-shadow: 10px 10px 0px #000;
        text-align: center; margin-top: 20px;
    }
    .result-number { font-size: 2.8rem; font-weight: 900; color: #f59e0b; }
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

# --- منطق الصفحات ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🏢\nدليل المطورين"): st.session_state.view = 'comp'; st.rerun()
    if c2.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    col_view, _ = st.columns([0.7, 0.3])
    with col_view:
        if st.button("🔙 عودة للرئيسية", key="back_btn"): st.session_state.view = 'main'; st.rerun()
        search = st.text_input("🔍 ابحث عن المطور...")
        unique_devs = df[dev_col].dropna().unique()
        if search: unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items_per_page = 9
        start = st.session_state.page * items_per_page
        current = unique_devs[start : start + items_per_page]
        
        # توزيع الكروت في شبكة 3x3
        for i in range(0, len(current), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current):
                    name = current[i + j]
                    with cols[j]:
                        if st.button(name, key=f"dev_{name}"):
                            st.session_state.selected_dev = name
                            st.session_state.view = 'details'; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    t1, t2 = st.tabs(["💰 حاسبة القسط", "📈 حاسبة ROI"])
    with t1:
        c1, c2, c3 = st.columns(3)
        price = c1.number_input("سعر الوحدة", value=1000000)
        down = c2.number_input("المقدم %", value=10)
        yrs = c3.number_input("السنوات", value=8)
        res_down = price * (down/100)
        res_m = (price - res_down) / (yrs * 12) if yrs > 0 else 0
        st.markdown(f'<div class="tool-card-result"><h3>المقدم: <span class="result-number">{res_down:,.0f}</span></h3><h3>القسط: <span class="result-number">{res_m:,.0f}</span></h3></div>', unsafe_allow_html=True)

    with t2:
        c1, c2, c3 = st.columns(3)
        buy = c1.number_input("سعر الشراء", value=1000000)
        sell = c2.number_input("سعر البيع", value=1500000)
        rent = c3.number_input("الإيجار السنوي", value=60000)
        profit = (sell - buy) + rent
        roi = (profit / buy) * 100 if buy > 0 else 0
        st.markdown(f'<div class="tool-card-result"><h3>صافي الربح: <span class="result-number">{profit:,.0f}</span></h3><h3>ROI: <span class="result-number">%{roi:.1f}</span></h3></div>', unsafe_allow_html=True)

elif st.session_state.view == 'details':
    st.markdown(f'<div class="hero-banner"><h2>{st.session_state.selected_dev}</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.view = 'comp'; st.rerun()
    projs = df[df[dev_col] == st.session_state.selected_dev][proj_col].unique()
    for p in projs:
        st.markdown(f'<div style="background:#fff; border:3px solid #000; padding:15px; border-radius:15px; margin-bottom:10px; box-shadow:5px 5px 0px #000; font-weight:900;">🔹 {p}</div>', unsafe_allow_html=True)
