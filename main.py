import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS احترافي ومضغوط (High Contrast & Compact)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }

    /* البوابة الرئيسية */
    .gate-card {
        background: white; border-radius: 15px; padding: 20px; text-align: center;
        border: 2px solid #e2e8f0; border-top: 8px solid #001a33;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); transition: 0.3s; height: 200px;
    }
    .gate-card:hover { transform: translateY(-5px); border-color: #001a33; }
    .gate-title { font-size: 1.8rem; font-weight: 900; color: #000; margin-top: 10px; }

    /* الهيدر النحيف (توفير مساحة) */
    .compact-hero {
        background: #001a33; padding: 15px; border-radius: 10px; margin-bottom: 15px; color: white; text-align: center;
    }
    .compact-hero-tools { background: #f59e0b; color: #000; }

    /* الكروت الصغيرة (9 كروت) */
    .nano-card {
        background: white; border: 1px solid #cbd5e1; border-right: 6px solid #001a33;
        border-radius: 8px; padding: 10px; margin-bottom: 5px; min-height: 110px;
    }
    .c-dev { color: #000 !important; font-size: 1.1rem; font-weight: 900; }
    .c-price { color: #15803d !important; font-size: 1.2rem; font-weight: 900; }

    /* الحاسبة المضغوطة */
    .calc-result-box {
        background: white; padding: 12px; border-radius: 12px; border: 3px solid #001a33;
        display: flex; justify-content: space-around; align-items: center; margin-top: 10px;
    }
    .res-val { font-size: 1.8rem; font-weight: 900; color: #000; display: block; }
    .res-lbl { font-size: 0.9rem; font-weight: 700; color: #444; }

    /* تحسين شكل المدخلات */
    .stNumberInput label { font-weight: 900 !important; color: #000 !important; font-size: 1rem !important; }
    
    /* أزرار التنقل */
    div.stButton > button {
        background: #001a33 !important; color: white !important; font-weight: 900 !important; border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. معالجة البيانات
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
        st.markdown("<h1 style='text-align:center; color:#001a33; margin:30px 0; font-weight:900;'>🏠 منصة معلوماتى</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="gate-card"><div style="font-size:3rem;">🏢</div><div class="gate-title">الشركات</div></div>', unsafe_allow_html=True)
            if st.button("فتح الشركات", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
        with c2:
            st.markdown('<div class="gate-card" style="border-top-color:#f59e0b;"><div style="font-size:3rem;">🛠️</div><div class="gate-title">أدوات البروكر</div></div>', unsafe_allow_html=True)
            if st.button("فتح الأدوات", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

    # --- صفحة الشركات ---
    elif st.session_state.view == 'comp':
        st.markdown('<div class="compact-hero"><h2>🔍 دليل الشركات والمشاريع</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        # فلاتر مضغوطة
        f1, f2, f3 = st.columns([2,1,1])
        with f1: q = st.text_input("بحث بالاسم", placeholder="اكتب هنا...", label_visibility="collapsed")
        with f2: loc = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:,3].unique().tolist()))
        with f3: pr = st.number_input("أقصى سعر", value=0)

        # عرض الكروت (أول 9 للتوضيح)
        st.markdown("<br>", unsafe_allow_html=True)
        rows = df.head(9)
        for i in range(0, len(rows), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(rows):
                    r = rows.iloc[i+j]
                    with cols[j]:
                        st.markdown(f'<div class="nano-card"><div class="c-dev">{r[0]}</div><div style="color:#1d4ed8; font-weight:700;">{r[2]}</div><div class="c-price">{r[4]}</div><div style="font-size:0.8rem; color:#666;">📍 {r[3]}</div></div>', unsafe_allow_html=True)
                        if st.button("التفاصيل", key=f"d_{i+j}"): pass

    # --- صفحة أدوات البروكر (المضغوطة كلياً) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="compact-hero compact-hero-tools"><h2>🛠️ حاسبة البروكر السريعة</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        # سطر واحد للمدخلات وسطر واحد للنتائج
        in1, in2, in3 = st.columns(3)
        with in1: up = st.number_input("سعر الوحدة", value=2000000, step=100000)
        with in2: dp_p = st.number_input("المقدم %", value=10, min_value=0)
        with in3: yrs = st.number_input("السنين", value=8, min_value=1)

        # الحسابات
        val_dp = up * (dp_p / 100)
        val_mo = (up - val_dp) / (yrs * 12) if yrs > 0 else 0

        # النتائج في سطر واحد فخم
        st.markdown(f"""
            <div class="calc-result-box">
                <div style="text-align:center;"><span class="res-lbl">💳 كاش المقدم</span><span class="res-val" style="color:#c2410c;">{val_dp:,.0f}</span></div>
                <div style="width:2px; height:50px; background:#ddd;"></div>
                <div style="text-align:center;"><span class="res-lbl">📅 قسط شهري</span><span class="res-val" style="color:#15803d;">{val_mo:,.0f}</span></div>
                <div style="width:2px; height:50px; background:#ddd;"></div>
                <div style="text-align:center;"><span class="res-lbl">🗓️ قسط ربع سنوي</span><span class="res-val" style="color:#0369a1;">{val_mo*3:,.0f}</span></div>
            </div>
            <div style="text-align:center; margin-top:10px; font-weight:900; color:#000;">إجمالي المبلغ المتبقي للتقسيط: {up-val_dp:,.0f} ج.م</div>
        """, unsafe_allow_html=True)
        
        if st.button("📸 حفظ الحسبة للعميل"): st.balloons()
