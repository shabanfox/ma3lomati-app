import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى - بروكر برو", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }
    
    /* تصميم الهيدر والبطاقات */
    .compact-hero { background: #001a33; padding: 15px; border-radius: 10px; color: white; text-align: center; margin-bottom:10px; }
    .hero-roi { background: #15803d; color: white; } /* أخضر مريح للمستثمر */
    
    .calc-box { background: white; padding: 15px; border-radius: 12px; border: 3px solid #001a33; margin-top: 10px; }
    .roi-box { border-color: #15803d; }
    
    .res-val { font-size: 1.8rem; font-weight: 900; color: #000; display: block; }
    .res-lbl { font-size: 0.9rem; font-weight: 700; color: #444; }

    /* أزرار التنقل */
    div.stButton > button { background: #001a33 !important; color: white !important; font-weight: 900 !important; border-radius: 8px !important; height: 40px !important;}
    input { font-size: 1.1rem !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# إدارة الصفحات
if 'view' not in st.session_state: st.session_state.view = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown("<h1 style='text-align:center; color:#001a33; margin:40px 0; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div style="background:white; padding:20px; border-radius:15px; border-top:8px solid #001a33; text-align:center;"><h2>🏢 الشركات</h2></div>', unsafe_allow_html=True)
        if st.button("فتح قسم الشركات", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
    with c2:
        st.markdown('<div style="background:white; padding:20px; border-radius:15px; border-top:8px solid #f59e0b; text-align:center;"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
        if st.button("فتح الأدوات والحاسبات", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

# --- صفحة أدوات البروكر (تحتوي على الحسابين) ---
elif st.session_state.view == 'tools':
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    tab1, tab2 = st.tabs(["🧮 حاسبة الأقساط", "📈 حاسبة أرباح الاستثمار (ROI)"])

    # --- التاب الأول: حاسبة الأقساط (التي اعتمدناها) ---
    with tab1:
        st.markdown('<div class="compact-hero" style="background:#f59e0b; color:black;"><h3>حاسبة القسط والمقدم</h3></div>', unsafe_allow_html=True)
        t1_in1, t1_in2, t1_in3 = st.columns(3)
        with t1_in1: u_p = st.number_input("سعر الوحدة", value=2000000)
        with t1_in2: d_p = st.number_input("المقدم %", value=10)
        with t1_in3: yrs = st.number_input("السنوات", value=8)
        
        dv = u_p * (d_p/100)
        mv = (u_p - dv) / (yrs * 12) if yrs > 0 else 0
        
        st.markdown(f"""
            <div class="calc-box">
                <div style="display:flex; justify-content:space-around; text-align:center;">
                    <div><span class="res-lbl">💳 المقدم</span><span class="res-val" style="color:#c2410c;">{dv:,.0f}</span></div>
                    <div style="width:2px; height:50px; background:#ddd;"></div>
                    <div><span class="res-lbl">📅 القسط شهري</span><span class="res-val" style="color:#15803d;">{mv:,.0f}</span></div>
                    <div style="width:2px; height:50px; background:#ddd;"></div>
                    <div><span class="res-lbl">🗓️ ربع سنوي</span><span class="res-val" style="color:#0369a1;">{mv*3:,.0f}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- التاب الثاني: حاسبة العائد ROI (الأداة الجديدة) ---
    with tab2:
        st.markdown('<div class="compact-hero hero-roi"><h3>📈 حاسبة العائد على الاستثمار</h3></div>', unsafe_allow_html=True)
        r_in1, r_in2, r_in3 = st.columns(3)
        with r_in1: buy_p = st.number_input("سعر الشراء الحالي", value=2000000)
        with r_in2: sell_p = st.number_input("السعر المتوقع عند البيع", value=3500000)
        with r_in3: rent_p = st.number_input("الإيجار الشهري المتوقع", value=15000)
        
        # حسابات ROI
        profit = sell_p - buy_p
        roi_pct = (profit / buy_p) * 100 if buy_p > 0 else 0
        annual_rent = rent_p * 12
        yield_pct = (annual_rent / buy_p) * 100 if buy_p > 0 else 0

        st.markdown(f"""
            <div class="calc-box roi-box">
                <div style="display:flex; justify-content:space-around; text-align:center;">
                    <div><span class="res-lbl">💰 صافي الربح (بيع)</span><span class="res-val" style="color:#15803d;">{profit:,.0f} ج.م</span></div>
                    <div style="width:2px; height:50px; background:#eee;"></div>
                    <div><span class="res-lbl">📈 نسبة الربح</span><span class="res-val" style="color:#166534;">%{roi_pct:.1f}</span></div>
                    <div style="width:2px; height:50px; background:#eee;"></div>
                    <div><span class="res-lbl">🏠 عائد إيجاري سنوي</span><span class="res-val" style="color:#1e40af;">%{yield_pct:.1f}</span></div>
                </div>
                <div style="text-align:center; margin-top:15px; padding-top:10px; border-top:1px dashed #ccc; color:#444; font-weight:700;">
                    هذا الاستثمار يحقق ربحاً قدره {profit:,.0f} جنيه في حال إعادة البيع.
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📋 نسخ تحليل الاستثمار للعميل"): st.success("تم التجهيز!")

# --- صفحة الشركات (احتياطاً للعمل) ---
elif st.session_state.view == 'comp':
    if st.button("🔙 عودة"): st.session_state.view = 'main'; st.rerun()
    st.info("قسم الشركات يعمل بنظام الـ 9 كروت المعتمد.")
