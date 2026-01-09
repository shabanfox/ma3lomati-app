import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (الأزرار العريضة الأنيقة والوضوح العالي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر */
    .header-top { 
        background: #000000; color: #ffffff; padding: 15px; border-radius: 12px; 
        text-align: center; margin-bottom: 25px; border: 4px solid #000;
    }
    .header-top h1 { color: #ffffff !important; font-weight: 900; margin: 0; font-size: 2rem; }

    /* الأزرار العريضة والأنيقة (Slim & Wide) */
    div.stButton > button {
        width: 100% !important;
        height: 80px !important; /* ارتفاع أنيق ونحيف */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        border-radius: 15px !important;
        font-size: 1.6rem !important;
        font-weight: 900 !important;
        box-shadow: 0px 8px 0px 0px #000000 !important;
        transition: all 0.1s ease;
        margin-bottom: 15px;
    }
    
    div.stButton > button:active {
        transform: translateY(6px) !important;
        box-shadow: 0px 2px 0px 0px #000000 !important;
    }

    /* كروت المشاريع */
    .card-res {
        background: #ffffff; border: 3px solid #000000; border-radius: 12px;
        padding: 15px; margin-bottom: 10px; color: #000000;
        box-shadow: 5px 5px 0px 0px #000000;
    }

    /* صناديق نتائج الحاسبات */
    .res-box { 
        background: #000000; color: #ffffff; padding: 20px; 
        border-radius: 15px; text-align: center; border: 3px solid #000;
        margin-top: 10px;
    }
    .val-white { font-size: 2.2rem; font-weight: 900; color: #ffffff !important; display: block; }
    .lbl-white { font-size: 1rem; font-weight: 700; color: #cccccc !important; }

    /* المدخلات */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.2rem !important; }
    input { border: 3px solid #000000 !important; font-weight: 900 !important; font-size: 1.4rem !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = load_data()

if 'view' not in st.session_state: st.session_state.view = 'main'

# --- العرض الرئيسي ---
if df is not None:
    # أ. الشاشة الرئيسية (أزرار عريضة وأنيقة)
    if st.session_state.view == 'main':
        st.markdown('<div class="header-top"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
        
        _, col_center, _ = st.columns([0.1, 0.8, 0.1])
        with col_center:
            if st.button("🏢 دليل المشاريع العقارية", key="btn_projects"):
                st.session_state.view = 'comp'; st.rerun()
            
            if st.button("🛠️ أدوات وحاسبات البروكر", key="btn_tools"):
                st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة الشركات
    elif st.session_state.view == 'comp':
        st.markdown('<div class="header-top"><h2>🔍 دليل المشاريع</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        q = st.text_input("بحث...", placeholder="اكتب اسم المشروع أو المطور")
        for _, r in df.head(10).iterrows():
            st.markdown(f"""
            <div class="card-res">
                <div style="font-weight:900; font-size:1.5rem;">{r[0]}</div>
                <div style="color:#1d4ed8; font-weight:900;">🏢 {r[2]}</div>
                <div style="font-weight:900; font-size:1.6rem; background:#FFEB3B; display:inline-block; padding:2px 10px;">{r[4]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات (الأداتين مع بعض)
    elif st.session_state.view == 'tools':
        st.markdown('<div class="header-top"><h2>🛠️ أدوات الحاسبة الذكية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        # الأداة الأولى: الأقساط
        st.markdown("<h3 style='text-align:right; font-weight:900; border-right:5px solid #000; padding-right:10px;'>💰 أولاً: حاسبة الأقساط</h3>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: price = st.number_input("سعر الوحدة", value=2000000, key="p1")
        with c2: down = st.number_input("المقدم %", value=10, key="p2")
        with c3: years = st.number_input("السنين", value=8, key="p3")
        
        dv = price * (down/100)
        mv = (price - dv) / (years * 12) if years > 0 else 0
        
        st.markdown(f"""
            <div class="res-box">
                <span class="lbl-white">كاش المقدم: <b style="color:white; font-size:1.5rem;">{dv:,.0f}</b> | القسط الشهري: <b style="color:#22c55e; font-size:1.8rem;">{mv:,.0f}</b></span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border:2px solid #000;'>", unsafe_allow_html=True)

        # الأداة الثانية: ROI
        st.markdown("<h3 style='text-align:right; font-weight:900; border-right:5px solid #22c55e; padding-right:10px;'>📈 ثانياً: حاسبة الربح (ROI)</h3>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        with r1: b_p = st.number_input("سعر الشراء", value=2000000, key="r1")
        with r2: s_p = st.number_input("سعر البيع المتوقع", value=3500000, key="r2")
        with r3: rent = st.number_input("الإيجار شهرياً", value=15000, key="r3")
        
        prof = s_p - b_p
        roi = (prof/b_p)*100 if b_p > 0 else 0
        
        st.markdown(f"""
            <div class="res-box" style="border-color:#22c55e;">
                <span class="lbl-white">صافي الربح: <b style="color:#22c55e; font-size:1.8rem;">{prof:,.0f}</b> | نسبة العائد: <b style="color:#FFEB3B; font-size:1.8rem;">%{roi:.1f}</b></span>
            </div>
        """, unsafe_allow_html=True)
