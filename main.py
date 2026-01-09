import streamlit as st
import pandas as pd
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS (أسود ملكي وتباين فائق)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #ffffff; /* خلفية بيضاء صريحة */
    }
    
    /* الهيدر: فاتح على غامق (أبيض على أسود) */
    .compact-hero { 
        background: #000000; padding: 20px; border-radius: 0 0 20px 20px; 
        color: #ffffff; text-align: center; margin-bottom:20px; border-bottom: 5px solid #f59e0b;
    }
    .compact-hero h1, .compact-hero h2, .compact-hero h3 { color: #ffffff !important; font-weight: 900; }

    /* الكروت: غامق على فاتح (أسود على أبيض) */
    .nano-card {
        background: #ffffff; border: 3px solid #000000; 
        border-radius: 15px; padding: 15px; margin-bottom: 10px;
        box-shadow: 8px 8px 0px 0px #000000; /* ظل حاد للوضوح */
    }
    .c-dev { color: #000000 !important; font-size: 1.4rem; font-weight: 900; }
    .c-price { color: #000000 !important; font-size: 1.5rem; font-weight: 900; background: #fef08a; display: inline-block; padding: 2px 10px; border-radius: 5px; }

    /* صناديق الحسابات: تباين فائق */
    .calc-box { 
        background: #f8fafc; padding: 20px; border-radius: 15px; 
        border: 4px solid #000000; margin-top: 10px; 
    }
    .res-val { font-size: 2.5rem; font-weight: 900; color: #000000; display: block; }
    .res-lbl { font-size: 1.2rem; font-weight: 900; color: #000000; border-bottom: 2px solid #000; display: inline-block; margin-bottom: 10px; }

    /* خانات الإدخال: نصوص سوداء واضحة */
    .stNumberInput label { font-weight: 900 !important; color: #000000 !important; font-size: 1.3rem !important; }
    input { color: #000000 !important; font-weight: 900 !important; font-size: 1.4rem !important; border: 3px solid #000 !important; }
    
    /* الأزرار: أبيض على أسود */
    div.stButton > button { 
        background: #000000 !important; color: #ffffff !important; 
        font-weight: 900 !important; border-radius: 10px !important; 
        font-size: 1.2rem !important; height: 50px !important; border: 2px solid #ffffff !important;
    }
    /* Tabs: تعديل ألوان التبويبات للوضوح */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background-color: #e2e8f0; border-radius: 10px 10px 0 0; padding: 10px 20px; font-weight: 900; color: #000;
    }
    .stTabs [aria-selected="true"] { background-color: #000 !important; color: #fff !important; }
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

# 4. إدارة التنقل
if 'view' not in st.session_state: st.session_state.view = 'main'

if df is not None:
    # --- الصفحة الرئيسية ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#000; margin:50px 0; font-weight:900; font-size:3.5rem;'>🏠 منصة معلوماتى</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="nano-card" style="text-align:center;"><div style="font-size:4rem;">🏢</div><div class="c-dev">دليل الشركات</div></div>', unsafe_allow_html=True)
            if st.button("دخول قسم الشركات", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
        with c2:
            st.markdown('<div class="nano-card" style="text-align:center;"><div style="font-size:4rem;">🛠️</div><div class="c-dev">أدوات البروكر</div></div>', unsafe_allow_html=True)
            if st.button("دخول حاسبة الأدوات", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

    # --- صفحة الشركات ---
    elif st.session_state.view == 'comp':
        st.markdown('<div class="compact-hero"><h1>🔍 دليل الشركات والمشاريع</h1></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        f1, f2, f3 = st.columns([2,1,1])
        with f1: q = st.text_input("بحث بالاسم", placeholder="اكتب اسم المطور...")
        with f2: loc = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:,3].dropna().unique().tolist()))
        with f3: pr = st.number_input("أقصى سعر (كتابة)", value=0)

        # عرض الكروت الـ 9
        rows = df.head(9)
        for i in range(0, len(rows), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(rows):
                    r = rows.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="nano-card">
                            <div class="c-dev">{r[0]}</div>
                            <div style="color:#000; font-weight:900; font-size:1.1rem; margin-bottom:5px;">🏢 {r[2]}</div>
                            <div class="c-price">{r[4]}</div>
                            <div style="font-size:1.1rem; color:#000; font-weight:900; margin-top:5px;">📍 {r[3]}</div>
                        </div>
                        """, unsafe_allow_html=True)

    # --- صفحة الأدوات (إدخال يدوي + تباين عالي) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="compact-hero"><h1>🛠️ حاسبات البروكر والمستثمر</h1></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        tab1, tab2 = st.tabs(["💰 حاسبة الأقساط", "📈 حاسبة أرباح الاستثمار ROI"])

        with tab1:
            st.markdown("### 📝 أدخل بيانات الوحدة (كتابة):")
            i1, i2, i3 = st.columns(3)
            with i1: up = st.number_input("سعر الوحدة الإجمالي", value=2000000, step=100000)
            with i2: dp = st.number_input("نسبة المقدم %", value=10, step=5)
            with i3: yr = st.number_input("عدد سنوات التقسيط", value=8, step=1)
            
            calc_dp = up * (dp/100)
            calc_mo = (up - calc_dp)/(yr*12) if yr > 0 else 0

            st.markdown(f"""
                <div class="calc-box">
                    <div style="display:flex; justify-content:space-around; text-align:center;">
                        <div><span class="res-lbl">💳 المقدم المطلوب</span><span class="res-val">{calc_dp:,.0f} ج.م</span></div>
                        <div style="width:4px; height:80px; background:#000;"></div>
                        <div><span class="res-lbl">📅 القسط الشهري</span><span class="res-val">{calc_mo:,.0f} ج.م</span></div>
                        <div style="width:4px; height:80px; background:#000;"></div>
                        <div><span class="res-lbl">🗓️ الربع سنوي</span><span class="res-val">{calc_mo*3:,.0f} ج.م</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("### 📊 حساب الجدوى الاستثمارية (كتابة):")
            r1, r2, r3 = st.columns(3)
            with r1: b = st.number_input("سعر الشراء الحالي", value=2000000, key="buy_input")
            with r2: s = st.number_input("السعر المتوقع عند البيع", value=3500000, key="sell_input")
            with r3: rt = st.number_input("الإيجار الشهري المتوقع", value=15000, key="rent_input")
            
            profit = s - b
            roi_pct = (profit/b)*100 if b > 0 else 0
            
            st.markdown(f"""
                <div class="calc-box" style="border-color:#000;">
                    <div style="display:flex; justify-content:space-around; text-align:center;">
                        <div><span class="res-lbl">💰 صافي أرباح البيع</span><span class="res-val">{profit:,.0f} ج.م</span></div>
                        <div style="width:4px; height:80px; background:#000;"></div>
                        <div><span class="res-lbl">📈 عائد الاستثمار</span><span class="res-val">%{roi_pct:.1f}</span></div>
                        <div style="width:4px; height:80px; background:#000;"></div>
                        <div><span class="res-lbl">🏠 العائد الإيجاري سنوي</span><span class="res-val">%{(rt*12/b)*100:.1f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
