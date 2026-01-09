import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (التباين المطلق - تركيز على الصفحة الرئيسية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #FFFFFF; 
    }
    
    /* جعل المحتوى في المنتصف */
    .main-center {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
    }

    /* الهيدر الرئيسي */
    .main-title { 
        background: #000000; color: #FFFFFF; padding: 20px; border-radius: 15px; 
        text-align: center; width: 100%; margin-bottom: 30px; border: 4px solid #000;
    }
    .main-title h1 { color: #FFFFFF !important; font-weight: 900; margin: 0; font-size: 2.5rem; }

    /* الكروت الضخمة في المنتصف */
    .big-gate-card {
        background: #FFFFFF; border: 6px solid #000000; border-radius: 20px;
        padding: 30px; text-align: center; margin-bottom: 20px;
        box-shadow: 10px 10px 0px 0px #000000;
    }
    .gate-label { color: #000000 !important; font-size: 2rem; font-weight: 900; margin-top: 15px; }
    .gate-icon { font-size: 5rem; }

    /* أزرار ضخمة */
    div.stButton > button { 
        width: 100%; background: #000000 !important; color: #FFFFFF !important; 
        font-weight: 900 !important; border-radius: 12px !important; font-size: 1.5rem !important;
        height: 65px; border: 3px solid #FFFFFF; margin-top: 10px;
    }
    
    /* تحسين القوائم والحاسبات */
    .white-card {
        background: #FFFFFF; border: 4px solid #000000; border-radius: 10px;
        padding: 15px; margin-bottom: 10px; color: #000000;
    }
    .t-black { color: #000000 !important; font-weight: 900; }
    .res-container { background: #000000; color: #FFFFFF; padding: 20px; border-radius: 15px; text-align: center; }
    .v-white { font-size: 2.2rem; font-weight: 900; color: #FFFFFF !important; }
    
    /* المدخلات */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.2rem !important; }
    input { border: 3px solid #000000 !important; font-weight: 900 !important; font-size: 1.4rem !important; }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = load_data()

if 'view' not in st.session_state: st.session_state.view = 'main'

# --- منطق العرض ---
if df is not None:
    # أ. الشاشة الرئيسية (التركيز على الكرتين في المنتصف)
    if st.session_state.view == 'main':
        st.markdown('<div class="main-title"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
        
        # استخدام أعمدة فارغة لتوسيط الكروت
        empty_l, center_col, empty_r = st.columns([1, 4, 1])
        
        with center_col:
            # كرت الشركات
            st.markdown('<div class="big-gate-card"><div class="gate-icon">🏢</div><div class="gate-label">دليل المشاريع</div></div>', unsafe_allow_html=True)
            if st.button("دخول قسم الشركات والمشاريع"):
                st.session_state.view = 'comp'; st.rerun()
            
            st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
            
            # كرت الأدوات
            st.markdown('<div class="big-gate-card" style="border-color:#E67E22;"><div class="gate-icon">🛠️</div><div class="gate-label" style="color:#E67E22 !important;">أدوات وحاسبات</div></div>', unsafe_allow_html=True)
            if st.button("دخول أدوات وحاسبات البروكر"):
                st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة الشركات
    elif st.session_state.view == 'comp':
        st.markdown('<div class="main-title"><h2>🔍 دليل المشاريع</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        q = st.text_input("ابحث عن مطور أو مشروع...", key="comp_search")
        f_df = df.head(20)
        for _, r in f_df.iterrows():
            st.markdown(f"""
            <div class="white-card">
                <div class="t-black" style="font-size:1.4rem;">{r[0]}</div>
                <div style="color:#1d4ed8; font-weight:900;">🏢 {r[2]}</div>
                <div class="t-black" style="font-size:1.5rem; background:#FFEB3B; display:inline-block; padding:2px 10px;">{r[4]}</div>
                <div class="t-black" style="font-size:1.1rem;">📍 {r[3]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات
    elif st.session_state.view == 'tools':
        st.markdown('<div class="main-title"><h2>🛠️ الحاسبة الذكية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        t1, t2 = st.tabs(["💰 حاسبة القسط", "📈 حاسبة الربح ROI"])
        
        with t1:
            u_p = st.number_input("سعر الوحدة الإجمالي", value=2000000, step=100000)
            d_p = st.number_input("المقدم %", value=10)
            yrs = st.number_input("عدد السنين", value=8)
            
            dv = u_p * (d_p/100)
            mv = (u_p - dv) / (yrs * 12) if yrs > 0 else 0
            
            st.markdown(f"""
                <div class="res-container">
                    <div style="margin-bottom:15px;"><span style="color:#CCC;">كاش المقدم المطلوب</span><br><span class="v-white">{dv:,.0f} ج.م</span></div>
                    <div style="margin-bottom:15px;"><span style="color:#CCC;">القسط الشهري</span><br><span class="v-white" style="color:#4CAF50 !important;">{mv:,.0f} ج.م</span></div>
                    <div><span style="color:#CCC;">القسط الربع سنوي</span><br><span class="v-white">{mv*3:,.0f} ج.م</span></div>
                </div>
            """, unsafe_allow_html=True)

        with t2:
            buy = st.number_input("سعر الشراء", value=2000000, key="b_tool")
            sell = st.number_input("سعر البيع المتوقع", value=3500000, key="s_tool")
            rent = st.number_input("الإيجار الشهري", value=15000, key="r_tool")
            
            prof = sell - buy
            st.markdown(f"""
                <div class="res-container" style="background:#111;">
                    <div style="margin-bottom:15px;"><span style="color:#CCC;">صافي أرباح البيع</span><br><span class="v-white" style="color:#4CAF50 !important;">{prof:,.0f} ج.م</span></div>
                    <div style="margin-bottom:15px;"><span style="color:#CCC;">نسبة العائد ROI</span><br><span class="v-white" style="color:#FFC107 !important;">%{ (prof/buy)*100 if buy>0 else 0:.1f}</span></div>
                    <div><span style="color:#CCC;">عائد الإيجار السنوي</span><br><span class="v-white">%{ ((rent*12)/buy)*100 if buy>0 else 0:.1f}</span></div>
                </div>
            """, unsafe_allow_html=True)
