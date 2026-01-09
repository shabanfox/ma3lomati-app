import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS (تركيز كامل على وضوح الخطوط والألوان)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #e2e8f0; /* خلفية أغمق قليلاً لبروز الكروت */
    }
    
    /* الهيدرات - ألوان صريحة وخطوط بيضاء ناصعة */
    .compact-hero { background: #000000; padding: 15px; border-radius: 12px; color: #ffffff; text-align: center; margin-bottom:15px; border: 2px solid #ffffff; }
    .hero-tools { background: #f59e0b; color: #000000; border: 2px solid #000; }
    .hero-roi { background: #16a34a; color: #ffffff; border: 2px solid #000; }

    /* كروت الشركات - تباين عالي جداً */
    .nano-card {
        background: #ffffff; border: 2px solid #000000; border-right: 10px solid #000000;
        border-radius: 12px; padding: 15px; margin-bottom: 10px;
        box-shadow: 5px 5px 0px 0px rgba(0,0,0,0.1);
    }
    .c-dev { color: #000000 !important; font-size: 1.3rem; font-weight: 900; }
    .c-price { color: #059669 !important; font-size: 1.4rem; font-weight: 900; }

    /* صناديق الحسابات - واضحة وضوح الشمس */
    .calc-box { 
        background: #ffffff; padding: 20px; border-radius: 15px; 
        border: 4px solid #000000; margin-top: 10px; 
    }
    .res-val { font-size: 2.2rem; font-weight: 900; color: #000000; display: block; }
    .res-lbl { font-size: 1.1rem; font-weight: 900; color: #000000; margin-bottom: 5px; display: block; }

    /* مدخلات الأرقام - خطوط سوداء عريضة */
    .stNumberInput label { font-weight: 900 !important; color: #000000 !important; font-size: 1.2rem !important; }
    input { color: #000000 !important; font-weight: 900 !important; font-size: 1.2rem !important; border: 2px solid #000 !important; }
    
    /* أزرار التنقل */
    div.stButton > button { 
        background: #000000 !important; color: #ffffff !important; 
        font-weight: 900 !important; border-radius: 10px !important; 
        font-size: 1.1rem !important; border: 2px solid #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظائف البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# 4. إدارة الصفحات
if 'view' not in st.session_state: st.session_state.view = 'main'

if df is not None:
    # --- الصفحة الرئيسية ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#000; margin:40px 0; font-weight:900; font-size:3.5rem;'>🏠 منصة معلوماتى</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="nano-card" style="text-align:center; height:180px;"><br><div style="font-size:3rem;">🏢</div><div class="c-dev">قسم الشركات</div></div>', unsafe_allow_html=True)
            if st.button("دخول الشركات", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
        with c2:
            st.markdown('<div class="nano-card" style="text-align:center; height:180px; border-right-color:#f59e0b;"><br><div style="font-size:3rem;">🛠️</div><div class="c-dev">أدوات البروكر</div></div>', unsafe_allow_html=True)
            if st.button("دخول الأدوات", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

    # --- صفحة الشركات ---
    elif st.session_state.view == 'comp':
        st.markdown('<div class="compact-hero"><h1>🔍 دليل الشركات والمشاريع</h1></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        f1, f2, f3 = st.columns([2,1,1])
        with f1: q = st.text_input("بحث بالاسم", placeholder="اكتب هنا...")
        with f2: loc = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:,3].dropna().unique().tolist()))
        with f3: pr = st.number_input("أقصى سعر", value=0)

        rows = df.head(9)
        for i in range(0, len(rows), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(rows):
                    r = rows.iloc[i+j]
                    with cols[j]:
                        st.markdown(f'<div class="nano-card"><div class="c-dev">{r[0]}</div><div style="color:#1d4ed8; font-weight:900;">{r[2]}</div><div class="c-price">{r[4]}</div><div style="font-size:1rem; color:#000; font-weight:700;">📍 {r[3]}</div></div>', unsafe_allow_html=True)
                        if st.button("عرض التفاصيل", key=f"d_{i+j}"): pass

    # --- صفحة الأدوات ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="compact-hero hero-tools"><h1>🛠️ حاسبات البروكر الذكية</h1></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        tab1, tab2 = st.tabs(["📊 حاسبة الأقساط", "📈 حاسبة الأرباح ROI"])

        with tab1:
            i1, i2, i3 = st.columns(3)
            with i1: up = st.number_input("إجمالي السعر", value=2000000)
            with i2: dp = st.number_input("المقدم %", value=10)
            with i3: yr = st.number_input("السنين", value=8)
            
            calc_dp = up * (dp/100)
            calc_mo = (up - calc_dp)/(yr*12) if yr > 0 else 0

            st.markdown(f"""
                <div class="calc-box">
                    <div style="display:flex; justify-content:space-around; text-align:center;">
                        <div><span class="res-lbl">💳 المقدم كاش</span><span class="res-val" style="color:#c2410c;">{calc_dp:,.0f}</span></div>
                        <div style="width:3px; height:60px; background:#000;"></div>
                        <div><span class="res-lbl">📅 القسط الشهري</span><span class="res-val" style="color:#059669;">{calc_mo:,.0f}</span></div>
                        <div style="width:3px; height:60px; background:#000;"></div>
                        <div><span class="res-lbl">🗓️ الربع سنوي</span><span class="res-val" style="color:#1d4ed8;">{calc_mo*3:,.0f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown('<div class="compact-hero hero-roi"><h3>حاسبة العائد الاستثماري (ROI)</h3></div>', unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1: b = st.number_input("سعر الشراء", value=2000000, key="b_roi")
            with r2: s = st.number_input("سعر البيع المتوقع", value=3000000, key="s_roi")
            with r3: rt = st.number_input("الإيجار المتوقع", value=15000, key="rt_roi")
            
            p = s - b
            st.markdown(f"""
                <div class="calc-box" style="border-color:#16a34a;">
                    <div style="display:flex; justify-content:space-around; text-align:center;">
                        <div><span class="res-lbl">💰 صافي الربح</span><span class="res-val" style="color:#16a34a;">{p:,.0f}</span></div>
                        <div style="width:3px; height:60px; background:#000;"></div>
                        <div><span class="res-lbl">📈 نسبة الربح</span><span class="res-val" style="color:#16a34a;">%{(p/b)*100 if b>0 else 0:.1f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
