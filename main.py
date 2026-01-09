import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* كروت البوابة الرئيسية */
    .main-gate-card {
        background: white; border-radius: 20px; padding: 30px; text-align: center;
        border: 2px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: 0.3s; height: 250px; display: flex; flex-direction: column;
        align-items: center; justify-content: center;
    }
    .main-gate-card:hover { transform: translateY(-10px); border-color: #001a33; }
    .card-companies { border-top: 12px solid #001a33; }
    .card-tools { border-top: 12px solid #f59e0b; }
    .gate-title { font-size: 2.2rem; font-weight: 900; color: #000000; } /* خط غامق جداً */

    /* الهيدر الموحد لصفحة الشركات وأدوات البروكر */
    .hero-section {
        background: #001a33; padding: 30px; border-radius: 0 0 30px 30px;
        margin-bottom: 25px; color: #ffffff; text-align: center;
    }
    .hero-tools { background: #f59e0b; color: #000000; } /* أسود على ذهبي */

    /* كروت الشركات (الـ 9 كروت) */
    .premium-nano-card {
        background: #ffffff; border: 1px solid #cbd5e1; border-right: 8px solid #001a33;
        border-radius: 12px; padding: 15px; margin-bottom: 10px; min-height: 130px;
    }
    .c-dev { color: #000000 !important; font-size: 1.25rem; font-weight: 900; }
    .c-proj { color: #1e40af !important; font-size: 1.1rem; font-weight: 700; }
    .c-price { color: #065f46 !important; font-size: 1.4rem; font-weight: 900; }
    .c-meta { color: #1e293b; font-size: 0.95rem; font-weight: 700; background: #f1f5f9; padding: 4px; border-radius: 5px; }

    /* حاسبة البروكر - التباين العالي */
    .calc-box {
        background: #ffffff; padding: 25px; border-radius: 15px; 
        border: 3px solid #f59e0b; box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    .result-item {
        padding: 15px; border-radius: 10px; margin-bottom: 12px; border: 1px solid #ddd;
    }
    .label-text { color: #000000; font-size: 1.1rem; font-weight: 700; }
    .value-text { font-size: 1.8rem; font-weight: 900; display: block; }

    /* أزرار واضحة */
    div.stButton > button {
        background: #001a33 !important; color: #ffffff !important;
        font-size: 1rem !important; font-weight: 900 !important;
        height: 40px !important; border-radius: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# دالة البيانات
@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = get_data()

# إدارة التنقل
if 'view' not in st.session_state: st.session_state.view = 'main'

if df is not None:
    # --- 1. البوابة الرئيسية ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#000; margin:50px 0; font-weight:900; font-size:3rem;'>🏠 منصة معلوماتى</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="main-gate-card card-companies"><div class="gate-icon">🏢</div><div class="gate-title">الشركات</div></div>', unsafe_allow_html=True)
            if st.button("دخول قسم الشركات", use_container_width=True):
                st.session_state.view = 'companies'; st.rerun()
        with c2:
            st.markdown('<div class="main-gate-card card-tools"><div class="gate-icon">🛠️</div><div class="gate-title">أدوات البروكر</div></div>', unsafe_allow_html=True)
            if st.button("دخول أدوات البروكر", use_container_width=True):
                st.session_state.view = 'tools'; st.rerun()

    # --- 2. قسم الشركات (الـ 9 كروت) ---
    elif st.session_state.view == 'companies':
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        st.markdown('<h1 style="color:#ffffff; margin:0;">🔍 دليل المطورين والمشاريع</h1>', unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2,1,1])
        with f1: sq = st.text_input("بحث...", placeholder="اكتب اسم الشركة أو المشروع", label_visibility="collapsed")
        with f2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()))
        with f3: sp = st.number_input("أقصى سعر", value=0)
        st.markdown('</div>', unsafe_allow_html=True)

        # عرض الكروت بنظام 3*3
        f_df = df.copy()
        # (منطق الفلترة...)
        batch = f_df.head(9) # للتجربة عرض أول 9
        for i in range(0, len(batch), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(batch):
                    row = batch.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="premium-nano-card">
                            <div class="c-dev">{row[0]}</div>
                            <div class="c-proj">🏢 {row[2]}</div>
                            <div class="c-price">{row[4]}</div>
                            <div class="c-meta">📍 {row[3]}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("التفاصيل", key=f"d_{i+j}"): pass

    # --- 3. قسم أدوات البروكر (تباين عالي) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-section hero-tools">', unsafe_allow_html=True)
        if st.button("🔙 العودة"): st.session_state.view = 'main'; st.rerun()
        st.markdown('<h1 style="color:#000000; margin:0;">🛠️ حاسبة الأقساط الاحترافية</h1>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        col_in, col_out = st.columns([1, 1.2])
        with col_in:
            st.markdown("### 📝 مدخلات الحسبة")
            u_p = st.number_input("إجمالي سعر الوحدة", value=2500000)
            d_pct = st.slider("نسبة المقدم (%)", 0, 50, 10)
            years = st.slider("عدد سنوات التقسيط", 1, 15, 8)
            
            dp = u_p * (d_pct/100)
            mo = (u_p - dp) / (years * 12) if years > 0 else 0

        with col_out:
            st.markdown("### 📊 العرض المالي للعميل")
            st.markdown(f"""
            <div class="calc-box">
                <div class="result-item" style="background:#fff7ed;">
                    <span class="label-text">💳 قيمة المقدم المطلوب:</span>
                    <span class="value-text" style="color:#c2410c;">{dp:,.0f} ج.م</span>
                </div>
                <div class="result-item" style="background:#f0fdf4;">
                    <span class="label-text">📅 القسط الشهري:</span>
                    <span class="value-text" style="color:#15803d;">{mo:,.0f} ج.م</span>
                </div>
                <div class="result-item" style="background:#f0f9ff;">
                    <span class="label-text">🗓️ القسط الربع سنوي:</span>
                    <span class="value-text" style="color:#0369a1;">{mo*3:,.0f} ج.م</span>
                </div>
                <div style="text-align:center; margin-top:10px; color:#000; font-weight:900;">
                    إجمالي سعر الوحدة: {u_p:,.0f} ج.م
                </div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("✅ تأكيد الحسبة"): st.balloons()
