import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] {
        background: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b; padding: 50px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 0px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3.5rem; font-weight: 900; margin: 0; }
    .ticker-wrap {
        width: 100%; background: rgba(245, 158, 11, 0.1); border-bottom: 1px solid #333; overflow: hidden; white-space: nowrap; padding: 15px 0; margin-bottom: 25px;
    }
    .ticker { display: inline-block; animation: ticker 45s linear infinite; color: #f59e0b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-150%); } }
    
    /* تنسيق الأدوات */
    .tool-card {
        background: #111; padding: 20px; border-radius: 15px; border: 1px solid #333; border-top: 4px solid #f59e0b; margin-bottom: 20px;
    }
    .tool-result {
        background: rgba(245, 158, 11, 0.15); padding: 15px; border-radius: 10px; border: 1px dashed #f59e0b; color: #fff; font-size: 1.2rem; font-weight: bold; text-align: center; margin-top: 10px;
    }
    div.stButton > button[key*="card_"] { 
        background: white !important; color: #000 !important; border-right: 15px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 140px !important; font-weight: 900 !important; font-size: 1.2rem !important; white-space: pre-wrap !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- (تم اختصار دوال البيانات والدخول للحفاظ على مساحة الرد - هي نفس الموجودة في الكود السابق) ---
# [ضع دوال load_all_data و login_check هنا]

# --- 7. قسم أدوات الحساب المطور (كامل الأدوات) ---
# سيتم استدعاؤه عندما يكون menu == "أدوات الحساب"

def render_tools():
    col_main, col_side = st.columns([0.7, 0.3])
    
    with col_main:
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ مركز أدوات البروكر الذكي</h2>", unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4 = st.tabs(["💰 المالية الأساسية", "📈 الاستثمار", "🏠 التمويل العقاري", "🎁 العروض"])
        
        with tab1:
            st.markdown("### حاسبة الأقساط والعمولات")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="tool-card">', unsafe_allow_html=True)
                price = st.number_input("سعر الوحدة الكلي", value=5000000, step=100000)
                down_pct = st.number_input("المقدم %", value=10, step=5)
                years = st.number_input("سنوات التقسيط", value=8, step=1)
                rem = price - (price * down_pct / 100)
                monthly = rem / (years * 12) if years > 0 else 0
                st.markdown(f'<div class="tool-result">القسط الشهري: {monthly:,.0f} ج.م</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="tool-card">', unsafe_allow_html=True)
                deal_val = st.number_input("قيمة الصفقة (للمناقشة)", value=5000000, step=100000)
                comm_pct = st.number_input("نسبة العمولة %", value=2.5, step=0.5, format="%.1f")
                tax = st.checkbox("خصم ضرائب (14% مثلاً)")
                total_comm = deal_val * (comm_pct / 100)
                if tax: total_comm *= 0.86
                st.markdown(f'<div class="tool-result">صافي العمولـة: {total_comm:,.0f} ج.م</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.markdown("### تحليل العائد الاستثماري (ROI)")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown('<div class="tool-card">', unsafe_allow_html=True)
                st.write("📈 عائد الإيجار السنوي")
                inv_price = st.number_input("تكلفة الاستثمار (الشراء)", value=8000000)
                rent_val = st.number_input("الإيجار الشهري المتوقع", value=45000)
                roi = ((rent_val * 12) / inv_price) * 100 if inv_price > 0 else 0
                st.markdown(f'<div class="tool-result">العائد السنوي: {roi:.2f}%</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            with c2:
                st.markdown('<div class="tool-card">', unsafe_allow_html=True)
                st.write("🔮 القيمة المستقبلية (توقع التضخم)")
                current_v = st.number_input("السعر الحالي", value=5000000)
                inf_rate = st.slider("نسبة زيادة العقار السنوية %", 10, 50, 25)
                after_yrs = st.number_input("بعد كم سنة؟", value=3)
                future_v = current_v * (1 + inf_rate/100)**after_yrs
                st.markdown(f'<div class="tool-result">القيمة المتوقعة: {future_v:,.0f} ج.م</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

        with tab3:
            st.markdown('<div class="tool-card">', unsafe_allow_html=True)
            st.write("🏦 حاسبة التمويل العقاري (البنك)")
            bank_price = st.number_input("سعر الوحدة للتمويل", value=3000000)
            int_rate = st.number_input("فائدة البنك السنوية % (متناقصة)", value=20.0)
            bank_yrs = st.number_input("مدة التمويل (سنة)", value=15)
            # معادلة القسط الثابت
            r = (int_rate / 100) / 12
            n = bank_yrs * 12
            if r > 0:
                p_bank = (bank_price * r * (1 + r)**n) / ((1 + r)**n - 1)
            else: p_bank = bank_price / n if n > 0 else 0
            st.markdown(f'<div class="tool-result">القسط البنكي الشهري: {p_bank:,.0f} ج.م</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with tab4:
            st.markdown('<div class="tool-card">', unsafe_allow_html=True)
            st.write("💰 حاسبة الكاش باك (Cash Back)")
            unit_p = st.number_input("إجمالي سعر الوحدة", key="cb_p", value=10000000)
            cb_pct = st.slider("نسبة الخصم أو الكاش باك %", 0, 40, 5)
            st.markdown(f'<div class="tool-result">مبلغ الخصم: {unit_p * (cb_pct/100):,.0f} ج.م</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="tool-result" style="background:green;">السعر بعد الخصم: {unit_p * (1 - cb_pct/100):,.0f} ج.م</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown("<h3 style='color:#f59e0b;'>💡 نصائح بيعية</h3>", unsafe_allow_html=True)
        st.info("""
        - **للعميل المستثمر:** ركز دائماً على تبويب الـ **ROI** والقيمة المستقبلية.
        - **للعميل السكني:** ركز على تبويب **القسط** والتمويل العقاري.
        - **لإغلاق الصفقة:** استخدم حاسبة **الكاش باك** لتوضيح قيمة التوفير الفوري.
        """)
        st.warning("⚠️ ملاحظة: هذه الحسابات تقريبية لتسهيل عملية الشرح للعميل.")

# استدعاء القسم في جسم الكود الرئيسي:
# if menu == "أدوات الحساب":
#     render_tools()
