import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتحسين عرض الموبايل
st.set_page_config(page_title="منصة معلوماتى", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي متوافق مع الهواتف والتباين العالي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #FFFFFF; 
    }

    /* الحاويات الرئيسية */
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }

    /* الهيدر: كتابة بيضاء على خلفية سوداء */
    .header-box { 
        background: #000000; padding: 15px; border-radius: 10px; 
        color: #FFFFFF; text-align: center; margin-bottom: 10px; 
    }
    .header-box h2 { color: #FFFFFF !important; font-weight: 900; margin: 0; font-size: 1.5rem; }

    /* الكروت: كتابة سوداء على خلفية بيضاء */
    .card-white {
        background: #FFFFFF; border: 3px solid #000000; border-radius: 12px;
        padding: 10px; margin-bottom: 8px; color: #000000;
    }
    .text-black { color: #000000 !important; font-weight: 900; }

    /* صناديق النتائج الملونة: كتابة بيضاء على خلفية غامقة */
    .res-box {
        padding: 10px; border-radius: 8px; text-align: center; margin-bottom: 5px;
    }
    .bg-orange { background: #E67E22; color: #FFFFFF; }
    .bg-green { background: #27AE60; color: #FFFFFF; }
    .bg-blue { background: #2980B9; color: #FFFFFF; }
    
    .val-text { font-size: 1.6rem; font-weight: 900; display: block; color: #FFFFFF !important; }
    .lbl-text { font-size: 0.9rem; font-weight: 700; color: #FFFFFF !important; }

    /* تحسين شكل خانات الإدخال للموبايل */
    .stNumberInput label { font-weight: 900 !important; color: #000000 !important; margin-bottom: 2px !important; }
    input { 
        border: 2px solid #000000 !important; border-radius: 5px !important; 
        font-weight: 900 !important; color: #000000 !important; padding: 5px !important;
    }

    /* التبويبات Tabs */
    .stTabs [data-baseweb="tab"] { 
        font-weight: 900 !important; color: #000 !important; background: #EEE; border-radius: 5px 5px 0 0; margin-left: 2px;
    }
    .stTabs [aria-selected="true"] { background: #000 !important; color: #FFF !important; }

    /* أزرار الموبايل العريضة */
    div.stButton > button { 
        width: 100%; background: #000 !important; color: #FFF !important; 
        font-weight: 900 !important; border-radius: 8px !important; border: 2px solid #000;
    }
    </style>
""", unsafe_allow_html=True)

# 3. دالة تحميل البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = load_data()

if 'view' not in st.session_state: st.session_state.view = 'main'

# --- التنقل ---
if df is not None:
    # 1. الصفحة الرئيسية
    if st.session_state.view == 'main':
        st.markdown('<div class="header-box"><h2>🏠 منصة معلوماتى العقارية</h2></div>', unsafe_allow_html=True)
        if st.button("🏢 دليل الشركات"): st.session_state.view = 'comp'; st.rerun()
        st.markdown("<div style='margin:5px;'></div>", unsafe_allow_html=True)
        if st.button("🛠️ أدوات وحاسبات البروكر"): st.session_state.view = 'tools'; st.rerun()

    # 2. صفحة الشركات
    elif st.session_state.view == 'comp':
        st.markdown('<div class="header-box"><h2>🔍 دليل الشركات</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        # بحث سريع
        q = st.text_input("بحث بالاسم (مطور/مشروع)", key="search_comp")
        
        # عرض الكروت (متوافق مع الموبايل)
        rows = df.head(10) # عرض أول 10 كروت للتجربة
        for _, r in rows.iterrows():
            st.markdown(f"""
            <div class="card-white">
                <div class="text-black" style="font-size:1.2rem;">{r[0]}</div>
                <div style="color:#2980B9; font-weight:800;">{r[2]}</div>
                <div class="text-black" style="background:#F1C40F; display:inline-block; padding:0 5px;">{r[4]}</div>
                <div style="font-size:0.9rem; font-weight:700;">📍 {r[3]}</div>
            </div>
            """, unsafe_allow_html=True)

    # 3. صفحة الأدوات (الحاسبة الرقمية)
    elif st.session_state.view == 'tools':
        st.markdown('<div class="header-box"><h2>🛠️ أدوات البروكر الذكية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        t1, t2 = st.tabs(["💰 حاسبة القسط", "📈 حاسبة الربح ROI"])

        with t1:
            up = st.number_input("سعر الوحدة الإجمالي", value=2000000, step=100000)
            dp = st.number_input("نسبة المقدم %", value=10)
            yr = st.number_input("عدد السنين", value=8)
            
            calc_dp = up * (dp/100)
            calc_mo = (up - calc_dp)/(yr*12) if yr > 0 else 0
            
            st.markdown(f"""
                <div class="res-box bg-orange">
                    <span class="lbl-text">كاش المقدم المطلوب</span>
                    <span class="val-text">{calc_dp:,.0f} ج.م</span>
                </div>
                <div class="res-box bg-green">
                    <span class="lbl-text">القسط الشهري</span>
                    <span class="val-text">{calc_mo:,.0f} ج.م</span>
                </div>
                <div class="res-box bg-blue">
                    <span class="lbl-text">القسط الربع سنوي</span>
                    <span class="val-text">{calc_mo*3:,.0f} ج.م</span>
                </div>
            """, unsafe_allow_html=True)

        with t2:
            buy = st.number_input("سعر الشراء", value=2000000, key="b_in")
            sell = st.number_input("سعر البيع المتوقع", value=3500000, key="s_in")
            rent = st.number_input("الإيجار الشهري", value=15000, key="r_in")
            
            prof = sell - buy
            st.markdown(f"""
                <div class="res-box bg-green">
                    <span class="lbl-text">صافي أرباح البيع</span>
                    <span class="val-text">{prof:,.0f} ج.م</span>
                </div>
                <div class="res-box bg-blue" style="background:#16A085;">
                    <span class="lbl-text">نسبة الربح الإجمالية</span>
                    <span class="val-text">%{(prof/buy)*100 if buy>0 else 0:.1f}</span>
                </div>
                <div class="res-box bg-orange" style="background:#2C3E50;">
                    <span class="lbl-text">العائد الإيجاري السنوي</span>
                    <span class="val-text">%{(rent*12/buy)*100 if buy>0 else 0:.1f}</span>
                </div>
            """, unsafe_allow_html=True)
