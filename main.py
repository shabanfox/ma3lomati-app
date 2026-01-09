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

    /* هيدر صفحة الأدوات - تباين عالي جداً */
    .hero-tools {
        background: #f59e0b; 
        padding: 35px; 
        border-radius: 0 0 30px 30px;
        margin-bottom: 30px; 
        text-align: center;
        border-bottom: 5px solid #b45309;
    }
    .hero-tools h1 { color: #000000 !important; font-weight: 900; font-size: 2.5rem; margin: 0; }

    /* حاوية الحاسبة */
    .calc-box {
        background: #ffffff; 
        padding: 30px; 
        border-radius: 20px; 
        border: 4px solid #001a33; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }

    /* نصوص النتائج الواضحة جداً */
    .result-card {
        padding: 20px; 
        border-radius: 12px; 
        margin-bottom: 15px; 
        border: 2px solid #eee;
    }
    .label-big { color: #000000; font-size: 1.3rem; font-weight: 900; display: block; margin-bottom: 5px; }
    .value-huge { font-size: 2.2rem; font-weight: 900; display: block; line-height: 1; }

    /* تنسيق خانات الإدخال */
    .stNumberInput label { color: #000000 !important; font-size: 1.2rem !important; font-weight: 900 !important; }
    input { font-size: 1.3rem !important; font-weight: 700 !important; color: #000000 !important; }
    
    /* زر العودة */
    .back-btn button {
        background: #000 !important; color: #fff !important; font-weight: 900 !important;
    }
    </style>
""", unsafe_allow_html=True)

# دالة تحميل البيانات (نفس الدالة السابقة)
@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = get_data()

if 'view' not in st.session_state: st.session_state.view = 'main'

if df is not None:
    # --- الصفحة الرئيسية ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#000; margin:50px 0; font-weight:900; font-size:3rem;'>🏠 منصة معلوماتى</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏢 دخول قسم الشركات", use_container_width=True):
                st.session_state.view = 'companies'; st.rerun()
        with c2:
            if st.button("🛠️ دخول أدوات البروكر", use_container_width=True):
                st.session_state.view = 'tools'; st.rerun()

    # --- صفحة أدوات البروكر (التعديل المطلوب) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-tools"><h1>🛠️ حاسبة الأقساط والمقدم</h1></div>', unsafe_allow_html=True)
        
        if st.button("🔙 عودة للرئيسية"):
            st.session_state.view = 'main'; st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        
        col_input, col_display = st.columns([1, 1.2])

        with col_input:
            st.markdown("### 📝 بيانات الوحدة")
            # تم تغيير السلايدر إلى Number Input بخط كبير
            unit_price = st.number_input("إجمالي سعر الوحدة (جنيه)", value=2000000, step=100000)
            down_pct = st.number_input("نسبة المقدم المطلوب (%)", value=10, min_value=0, max_value=100, step=5)
            pay_years = st.number_input("عدد سنوات التقسيط", value=8, min_value=1, max_value=20, step=1)
            
            # الحسابات الفنية
            dp_value = unit_price * (down_pct / 100)
            remaining_balance = unit_price - dp_value
            mo_payment = remaining_balance / (pay_years * 12) if pay_years > 0 else 0

        with col_display:
            st.markdown("### 📊 تفصيل الدفعات للعميل")
            st.markdown(f"""
            <div class="calc-box">
                <div class="result-card" style="background: #fff7ed; border-color: #f59e0b;">
                    <span class="label-big">💰 قيمة المقدم (Cash):</span>
                    <span class="value-huge" style="color: #c2410c;">{dp_value:,.0f} ج.م</span>
                </div>
                
                <div class="result-card" style="background: #f0fdf4; border-color: #22c55e;">
                    <span class="label-big">📅 القسط الشهري:</span>
                    <span class="value-huge" style="color: #15803d;">{mo_payment:,.0f} ج.م</span>
                </div>
                
                <div class="result-card" style="background: #f0f9ff; border-color: #0ea5e9;">
                    <span class="label-big">🗓️ القسط الربع سنوي:</span>
                    <span class="value-huge" style="color: #0369a1;">{mo_payment*3:,.0f} ج.م</span>
                </div>
                
                <div style="text-align:center; padding-top:15px; border-top: 2px dashed #ccc; margin-top:10px;">
                    <p style="font-size:1.2rem; color:#000;">إجمالي المبلغ المتبقي: <b>{remaining_balance:,.0f} ج.م</b></p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("📸 جاهز للإرسال (تصوير الشاشة)"):
                st.success("الأرقام محدثة وجاهزة!")

    # --- صفحة الشركات (كما اعتمدناها) ---
    elif st.session_state.view == 'companies':
        # ... (كود صفحة الشركات السابق بنفس الـ 9 كروت) ...
        if st.button("🔙 عودة"): st.session_state.view = 'main'; st.rerun()
        st.write("قسم الشركات يعمل بنظام الـ 9 كروت المعتمد.")
