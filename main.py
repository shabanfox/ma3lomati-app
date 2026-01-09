import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (تحسين العرض على الموبايل والكمبيوتر)
st.set_page_config(page_title="منصة معلوماتى", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (التباين المطلق، الأزرار الأفقية، والخطوط العريضة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية لستريمليت */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* إعدادات الجسم العام */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }
    .block-container { padding-top: 1.5rem !important; }

    /* الهيدر العلوي */
    .hero-header { 
        background: #000000; color: #ffffff; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 35px; border-bottom: 8px solid #2563eb;
    }
    .hero-header h1 { color: #ffffff !important; font-weight: 900; margin: 0; font-size: 2.5rem; }

    /* تنسيق الأزرار (جنب بعض في صف واحد) */
    .stButton > button {
        width: 100% !important;
        height: 140px !important; /* ارتفاع أنيق وعريض */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 6px solid #000000 !important;
        border-radius: 25px !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        box-shadow: 10px 10px 0px 0px #000000 !important;
        transition: all 0.1s;
        display: flex; align-items: center; justify-content: center;
    }

    /* تمييز الألوان للأزرار لكسر البهتان */
    div[data-testid="column"]:nth-child(1) .stButton > button {
        border-color: #2563eb !important; color: #2563eb !important;
        box-shadow: 10px 10px 0px 0px #2563eb !important;
    }
    div[data-testid="column"]:nth-child(2) .stButton > button {
        border-color: #e67e22 !important; color: #e67e22 !important;
        box-shadow: 10px 10px 0px 0px #e67e22 !important;
    }

    div.stButton > button:active {
        transform: translate(6px, 6px) !important;
        box-shadow: 0px 0px 0px 0px !important;
    }

    /* صناديق النتائج (تباين أسود/أبيض) */
    .res-card { 
        background: #000000; color: #ffffff; padding: 25px; 
        border-radius: 20px; text-align: center; border: 4px solid #000;
        margin-top: 15px;
    }
    .res-val { font-size: 2.8rem; font-weight: 900; color: #ffffff !important; }
    
    /* كروت المشاريع */
    .project-card {
        background: #fff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 12px; box-shadow: 7px 7px 0px #000;
    }

    /* المدخلات (خط عريض وواضح) */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.4rem !important; }
    input { 
        border: 4px solid #000000 !important; font-weight: 900 !important; 
        font-size: 1.6rem !important; border-radius: 12px !important; color: #000 !important;
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

# --- منطق العرض الرئيسي ---
if df is not None:
    # أ. الشاشة الرئيسية (أزرار جنب بعض)
    if st.session_state.view == 'main':
        st.markdown('<div class="hero-header"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
        
        st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True)
        
        # وضع الأزرار جنباً إلى جنب في منتصف الموقع
        _, col_main, _ = st.columns([0.05, 0.9, 0.05])
        with col_main:
            c1, c2 = st.columns(2, gap="large")
            with c1:
                if st.button("🏢\nدليل المشاريع", key="main_p"):
                    st.session_state.view = 'comp'; st.rerun()
            with c2:
                if st.button("🛠️\nأدوات البروكر", key="main_t"):
                    st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة الشركات والمشاريع
    elif st.session_state.view == 'comp':
        st.markdown('<div class="hero-header"><h2>🔍 دليل المشاريع العقارية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية", key="back_p"): st.session_state.view = 'main'; st.rerun()
        
        st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
        q = st.text_input("بحث سريع عن مشروع أو مطور...", key="search_field")
        
        # عرض البيانات بشكل كروت
        for _, r in df.head(15).iterrows():
            st.markdown(f"""
            <div class="project-card">
                <div style="font-weight:900; font-size:1.8rem; color:#000;">{r[0]}</div>
                <div style="color:#2563eb; font-weight:900; font-size:1.3rem;">🏢 المطور: {r[2]}</div>
                <div style="font-weight:900; font-size:1.7rem; background:#FFEB3B; display:inline-block; padding:5px 15px; margin-top:10px; border-radius:10px; border:2px solid #000;">{r[4]}</div>
                <div style="margin-top:10px; font-weight:700;">📍 الموقع: {r[3]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات (الحاسبتين معاً)
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-header"><h2>🛠️ الحاسبات الذكية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية", key="back_t"): st.session_state.view = 'main'; st.rerun()

        # 1. حاسبة الأقساط
        st.markdown("<h2 style='border-right:10px solid #2563eb; padding-right:15px; font-weight:900; margin-top:20px;'>💰 حاسبة القسط والمقدم</h2>", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a: u_price = st.number_input("سعر الوحدة", value=2000000, key="calc1")
        with b: u_down = st.number_input("المقدم %", value=10, key="calc2")
        with c: u_years = st.number_input("عدد السنين", value=8, key="calc3")
        
        dv = u_price * (u_down/100)
        mv = (u_price - dv) / (u_years * 12) if u_years > 0 else 0
        
        st.markdown(f"""
            <div class="res-card">
                <span style="color:#aaa; font-size:1.3rem;">كاش المقدم المطلوب:</span><br>
                <span class="res-val">{dv:,.0f} ج.م</span>
                <hr style="border:1px solid #333">
                <span style="color:#aaa; font-size:1.3rem;">القسط الشهري:</span><br>
                <span class="res-val" style="color:#22c55e !important;">{mv:,.0f} ج.م</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)

        # 2. حاسبة ROI
        st.markdown("<h2 style='border-right:10px solid #e67e22; padding-right:15px; font-weight:900;'>📈 حاسبة الربح ROI</h2>", unsafe_allow_html=True)
        x, y, z = st.columns(3)
        with x: b_price = st.number_input("سعر الشراء", value=2000000, key="roi1")
        with y: s_price = st.number_input("سعر البيع المتوقع", value=3500000, key="roi2")
        with z: rent_val = st.number_input("الإيجار المتوقع/شهر", value=15000, key="roi3")
        
        profit = s_price - b_price
        roi_perc = (profit/b_price)*100 if b_price > 0 else 0
        
        st.markdown(f"""
            <div class="res-card" style="border-color:#e67e22;">
                <span style="color:#aaa; font-size:1.3rem;">صافي أرباح البيع:</span><br>
                <span class="res-val" style="color:#e67e22 !important;">{profit:,.0f} ج.م</span>
                <hr style="border:1px solid #333">
                <span style="color:#aaa; font-size:1.3rem;">نسبة العائد الإجمالية:</span><br>
                <span class="res-val" style="color:#FFEB3B !important;">%{roi_perc:.1f}</span>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error("فشل تحميل البيانات، تأكد من رابط Google Sheets")
