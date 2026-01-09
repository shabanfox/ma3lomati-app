import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (الأزرار العملاقة والتباين الفائق)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر الرئيسي */
    .main-title { 
        background: #000000; color: #ffffff; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 40px; border: 5px solid #000;
    }
    .main-title h1 { color: #ffffff !important; font-weight: 900; margin: 0; font-size: 3rem; }

    /* تصميم الأزرار العملاقة */
    div.stButton > button {
        width: 100% !important;
        height: 220px !important; /* ارتفاع عملاق */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 8px solid #000000 !important; /* برواز سميك جداً */
        border-radius: 30px !important;
        font-size: 2.5rem !important; /* خط ضخم */
        font-weight: 900 !important;
        box-shadow: 0px 20px 0px 0px #000000 !important; /* ظل حاد وعميق */
        transition: all 0.1s ease;
        margin-bottom: 40px;
    }
    
    div.stButton > button:hover {
        background-color: #f0f0f0 !important;
        transform: translateY(5px);
        box-shadow: 0px 15px 0px 0px #000000 !important;
    }

    div.stButton > button:active {
        transform: translateY(18px) !important;
        box-shadow: 0px 2px 0px 0px #000000 !important;
    }

    /* تحسين الكروت داخل الصفحات */
    .white-card {
        background: #ffffff; border: 4px solid #000000; border-radius: 15px;
        padding: 20px; margin-bottom: 15px; color: #000000;
        box-shadow: 8px 8px 0px 0px #000000;
    }
    .t-black { color: #000000 !important; font-weight: 900; }
    
    /* صناديق النتائج */
    .res-container { 
        background: #000000; color: #ffffff; padding: 30px; 
        border-radius: 25px; text-align: center; border: 5px solid #000;
    }
    .v-white { font-size: 3rem; font-weight: 900; color: #ffffff !important; }
    
    /* المدخلات */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.5rem !important; }
    input { border: 5px solid #000000 !important; font-weight: 900 !important; font-size: 1.8rem !important; border-radius: 15px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
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

# --- العرض ---
if df is not None:
    # أ. الشاشة الرئيسية (أزرار عملاقة في الوسط)
    if st.session_state.view == 'main':
        st.markdown('<div class="main-title"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
        
        # استخدام أعمدة لتوسيط الأزرار في الموبايل والكمبيوتر
        col_side_1, col_main, col_side_2 = st.columns([0.1, 0.8, 0.1])
        
        with col_main:
            if st.button("🏢 دليل المشاريع", key="main_btn_1"):
                st.session_state.view = 'comp'; st.rerun()
            
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            
            if st.button("🛠️ حاسبات البروكر", key="main_btn_2"):
                st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة الشركات
    elif st.session_state.view == 'comp':
        st.markdown('<div class="main-title"><h2>🔍 دليل المشاريع</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back_btn_comp"):
            st.session_state.view = 'main'; st.rerun()
        
        q = st.text_input("بحث...", placeholder="اسم المطور")
        for _, r in df.head(10).iterrows():
            st.markdown(f"""
            <div class="white-card">
                <div class="t-black" style="font-size:1.8rem;">{r[0]}</div>
                <div style="color:#1d4ed8; font-weight:900; font-size:1.3rem;">🏢 {r[2]}</div>
                <div class="t-black" style="font-size:1.8rem; background:#FFEB3B; display:inline-block; padding:5px 15px; margin-top:10px;">{r[4]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات
    elif st.session_state.view == 'tools':
        st.markdown('<div class="main-title"><h2>🛠️ الحاسبات</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back_btn_tools"):
            st.session_state.view = 'main'; st.rerun()

        u_p = st.number_input("سعر الوحدة", value=2000000)
        d_p = st.number_input("المقدم %", value=10)
        yrs = st.number_input("السنين", value=8)
        
        dv = u_p * (d_p/100)
        mv = (u_p - dv) / (yrs * 12) if yrs > 0 else 0
        
        st.markdown(f"""
            <div class="res-container">
                <div style="margin-bottom:20px;">
                    <span style="color:#aaa; font-size:1.5rem;">كاش المقدم المطلوب</span><br>
                    <span class="v-white">{dv:,.0f} ج.م</span>
                </div>
                <div>
                    <span style="color:#aaa; font-size:1.5rem;">القسط الشهري</span><br>
                    <span class="v-white" style="color:#22c55e !important;">{mv:,.0f} ج.م</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
