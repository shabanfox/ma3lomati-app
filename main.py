import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (التباين المطلق والوضوح الفائق)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الأساسيات */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #FFFFFF; 
    }
    .block-container { padding: 1rem !important; }

    /* الهيدر: أبيض على أسود */
    .black-header { 
        background: #000000; color: #FFFFFF; padding: 15px; border-radius: 10px; 
        text-align: center; margin-bottom: 15px; border: 2px solid #000;
    }
    .black-header h2 { color: #FFFFFF !important; font-weight: 900; margin: 0; }

    /* الكروت: أسود على أبيض */
    .white-card {
        background: #FFFFFF; border: 4px solid #000000; border-radius: 10px;
        padding: 12px; margin-bottom: 10px; color: #000000;
    }
    .t-black { color: #000000 !important; font-weight: 900; line-height: 1.2; }
    
    /* صناديق النتائج: تباين عالي جداً */
    .res-container {
        background: #000000; color: #FFFFFF; padding: 15px; border-radius: 12px;
        text-align: center; margin-top: 10px; border: 3px solid #000;
    }
    .res-item { margin-bottom: 10px; border-bottom: 1px dashed #555; padding-bottom: 5px; }
    .res-item:last-child { border-bottom: none; }
    .v-white { font-size: 2rem; font-weight: 900; color: #FFFFFF !important; display: block; }
    .l-white { font-size: 1rem; font-weight: 700; color: #CCCCCC !important; }

    /* المدخلات: أسود على أبيض وخط عريض */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.1rem !important; }
    input { 
        border: 3px solid #000000 !important; font-weight: 900 !important; 
        color: #000000 !important; font-size: 1.3rem !important;
    }

    /* الأزرار: أبيض على أسود */
    div.stButton > button { 
        width: 100%; background: #000000 !important; color: #FFFFFF !important; 
        font-weight: 900 !important; border-radius: 8px !important; font-size: 1.2rem !important;
        height: 50px; border: 2px solid #000;
    }
    
    /* التبويبات Tabs */
    .stTabs [data-baseweb="tab"] { font-weight: 900 !important; color: #000 !important; }
    .stTabs [aria-selected="true"] { border-bottom: 4px solid #000 !important; }
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

# --- التنقل والمحتوى ---
if df is not None:
    # أ. الشاشة الرئيسية
    if st.session_state.view == 'main':
        st.markdown('<div class="black-header"><h2>🏠 معلوماتى العقارية</h2></div>', unsafe_allow_html=True)
        if st.button("🏢 دليل الشركات"): st.session_state.view = 'comp'; st.rerun()
        st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
        if st.button("🛠️ أدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة الشركات
    elif st.session_state.view == 'comp':
        st.markdown('<div class="black-header"><h2>🔍 دليل الشركات</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة"): st.session_state.view = 'main'; st.rerun()
        
        q = st.text_input("ابحث عن مطور أو مشروع...", key="s_field")
        
        # عرض الكروت بنظام الموبايل (رأسي وواضح)
        f_df = df.head(15) # عرض كمية مناسبة
        for _, r in f_df.iterrows():
            st.markdown(f"""
            <div class="white-card">
                <div class="t-black" style="font-size:1.3rem;">{r[0]}</div>
                <div style="color:#1d4ed8; font-weight:900;">🏢 {r[2]}</div>
                <div class="t-black" style="font-size:1.4rem; background:#FFEB3B; display:inline-block; padding:2px 8px; margin:5px 0;">{r[4]}</div>
                <div class="t-black" style="font-size:1rem;">📍 {r[3]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات (الحاسبات)
    elif st.session_state.view == 'tools':
        st.markdown('<div class="black-header"><h2>🛠️ حاسبات ذكية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة"): st.session_state.view = 'main'; st.rerun()

        tab1, tab2 = st.tabs(["💰 القسط والمقدم", "📈 أرباح الاستثمار ROI"])

        with tab1:
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            u_p = st.number_input("سعر الوحدة (كتابة)", value=2000000, step=100000)
            d_p = st.number_input("المقدم % (كتابة)", value=10)
            yrs = st.number_input("السنين (كتابة)", value=8)
            
            dv = u_p * (d_p/100)
            mv = (u_p - dv) / (yrs * 12) if yrs > 0 else 0
            
            st.markdown(f"""
                <div class="res-container">
                    <div class="res-item">
                        <span class="l-white">كاش المقدم</span>
                        <span class="v-white">{dv:,.0f} ج.م</span>
                    </div>
                    <div class="res-item">
                        <span class="l-white">القسط الشهري</span>
                        <span class="v-white">{mv:,.0f} ج.م</span>
                    </div>
                    <div class="res-item">
                        <span class="l-white">الربع سنوي</span>
                        <span class="v-white">{mv*3:,.0f} ج.م</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with tab2:
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            b_i = st.number_input("سعر الشراء", value=2000000, key="b_i")
            s_i = st.number_input("سعر البيع المتوقع", value=3500000, key="s_i")
            r_i = st.number_input("الإيجار المتوقع/شهر", value=15000, key="r_i")
            
            prof = s_i - b_i
            roi = (prof/b_i)*100 if b_i > 0 else 0
            
            st.markdown(f"""
                <div class="res-container" style="background:#111;">
                    <div class="res-item">
                        <span class="l-white">صافي الربح</span>
                        <span class="v-white" style="color:#4CAF50 !important;">{prof:,.0f} ج.م</span>
                    </div>
                    <div class="res-item">
                        <span class="l-white">نسبة العائد (ROI)</span>
                        <span class="v-white" style="color:#FFC107 !important;">%{roi:.1f}</span>
                    </div>
                    <div class="res-item">
                        <span class="l-white">عائد الإيجار السنوي</span>
                        <span class="v-white">%{((r_i*12)/b_i)*100 if b_i>0 else 0:.1f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
