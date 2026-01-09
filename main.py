import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (الأزرار المتوازية والجماليات الفائقة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f6; 
    }

    /* الهيدر الرئيسي */
    .main-title { 
        background: #000000; color: #ffffff; padding: 20px; border-radius: 15px; 
        text-align: center; margin-bottom: 30px; border-bottom: 6px solid #f59e0b;
    }
    .main-title h1 { color: #ffffff !important; font-weight: 900; margin: 0; font-size: 2.2rem; }

    /* حاوية الأزرار لجعلها جنب بعض */
    .stButton > button {
        width: 100% !important;
        height: 250px !important; /* ارتفاع متناسق */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 5px solid #000000 !important;
        border-radius: 20px !important;
        font-size: 1.8rem !important;
        font-weight: 900 !important;
        box-shadow: 0px 15px 0px 0px #000000 !important;
        transition: all 0.1s ease;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    div.stButton > button:hover {
        background-color: #f8f9fa !important;
        transform: translateY(4px);
        box-shadow: 0px 10px 0px 0px #000000 !important;
    }

    div.stButton > button:active {
        transform: translateY(12px) !important;
        box-shadow: 0px 3px 0px 0px #000000 !important;
    }

    /* كروت المشاريع */
    .white-card {
        background: #ffffff; border: 3px solid #000000; border-radius: 12px;
        padding: 15px; margin-bottom: 10px; color: #000000;
        box-shadow: 5px 5px 0px 0px #000000;
    }
    .t-black { color: #000000 !important; font-weight: 900; }
    
    /* صناديق النتائج */
    .res-container { 
        background: #000000; color: #ffffff; padding: 25px; 
        border-radius: 20px; text-align: center; border: 4px solid #000;
    }
    .v-white { font-size: 2.5rem; font-weight: 900; color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = load_data()

if 'view' not in st.session_state: st.session_state.view = 'main'

# --- العرض ---
if df is not None:
    # أ. الشاشة الرئيسية (الأزرار جنب بعض)
    if st.session_state.view == 'main':
        st.markdown('<div class="main-title"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
        
        # توزيع الأزرار جنب بعض في صف واحد
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("<h3 style='text-align:center; font-weight:900;'>🏢 المشاريع</h3>", unsafe_allow_html=True)
            if st.button("📂\nدليل المشاريع", key="btn_p"):
                st.session_state.view = 'comp'; st.rerun()
        
        with col2:
            st.markdown("<h3 style='text-align:center; font-weight:900;'>🛠️ الأدوات</h3>", unsafe_allow_html=True)
            if st.button("🧮\nأدوات البروكر", key="btn_t"):
                st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة الشركات
    elif st.session_state.view == 'comp':
        st.markdown('<div class="main-title"><h2>🔍 دليل المشاريع</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        q = st.text_input("بحث بالاسم...", key="search")
        for _, r in df.head(10).iterrows():
            st.markdown(f"""
            <div class="white-card">
                <div class="t-black" style="font-size:1.5rem;">{r[0]}</div>
                <div style="color:#1d4ed8; font-weight:900;">🏢 {r[2]}</div>
                <div class="t-black" style="font-size:1.6rem; background:#FFEB3B; display:inline-block; padding:2px 10px;">{r[4]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات
    elif st.session_state.view == 'tools':
        st.markdown('<div class="main-title"><h2>🛠️ الحاسبات</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        u_p = st.number_input("سعر الوحدة", value=2000000)
        d_p = st.number_input("المقدم %", value=10)
        yrs = st.number_input("السنين", value=8)
        
        dv = u_p * (d_p/100)
        mv = (u_p - dv) / (yrs * 12) if yrs > 0 else 0
        
        st.markdown(f"""
            <div class="res-container">
                <div style="margin-bottom:15px;"><span style="color:#aaa;">كاش المقدم</span><br><span class="v-white">{dv:,.0f}</span></div>
                <div><span style="color:#aaa;">القسط الشهري</span><br><span class="v-white" style="color:#4CAF50 !important;">{mv:,.0f}</span></div>
            </div>
        """, unsafe_allow_html=True)
