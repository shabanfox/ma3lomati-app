import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (الأزرار العريضة والجماليات العالية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* الحاوية الرئيسية */
    .block-container { padding: 1.5rem !important; }

    /* الهيدر */
    .main-title { 
        background: linear-gradient(90deg, #000000 0%, #333333 100%);
        color: #FFFFFF; padding: 25px; border-radius: 20px; 
        text-align: center; width: 100%; margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .main-title h1 { color: #FFFFFF !important; font-weight: 900; margin: 0; font-size: 2.5rem; }

    /* تصميم الأزرار العريضة الفخمة */
    div.stButton > button {
        width: 100% !important;
        height: 160px !important;
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        border-radius: 25px !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        box-shadow: 0 15px 0px 0px #000000 !important; /* ظل حاد */
        transition: all 0.1s ease;
        margin-bottom: 25px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    div.stButton > button:hover {
        background: #f1f5f9 !important;
        transform: translateY(4px);
        box-shadow: 0 10px 0px 0px #000000 !important;
    }

    div.stButton > button:active {
        transform: translateY(12px) !important;
        box-shadow: 0 2px 0px 0px #000000 !important;
    }

    /* تحسين الكروت داخل الصفحات */
    .white-card {
        background: #FFFFFF; border: 3px solid #000000; border-radius: 15px;
        padding: 15px; margin-bottom: 12px; color: #000000;
        box-shadow: 5px 5px 0px 0px #000000;
    }
    .t-black { color: #000000 !important; font-weight: 900; }
    
    /* صناديق النتائج */
    .res-container { 
        background: #000000; color: #FFFFFF; padding: 25px; 
        border-radius: 20px; text-align: center; border: 4px solid #f59e0b;
    }
    .v-white { font-size: 2.8rem; font-weight: 900; color: #FFFFFF !important; }
    
    /* المدخلات */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.3rem !important; }
    input { border: 4px solid #000000 !important; font-weight: 900 !important; font-size: 1.5rem !important; border-radius: 12px !important; }
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

# --- المحتوى ---
if df is not None:
    # أ. الشاشة الرئيسية (أزرار عريضة وفخمة)
    if st.session_state.view == 'main':
        st.markdown('<div class="main-title"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
        
        # الأزرار تأخذ عرض الصفحة بالكامل (مع هامش بسيط للجمال)
        c1, c2, c3 = st.columns([0.1, 0.8, 0.1])
        with c2:
            if st.button("🏢 تصفح دليل المشاريع والشركات", key="main_comp"):
                st.session_state.view = 'comp'; st.rerun()
            
            st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
            
            if st.button("🛠️ فتح حاسبات وأدوات البروكر", key="main_tools"):
                st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة الشركات
    elif st.session_state.view == 'comp':
        st.markdown('<div class="main-title"><h2>🔍 دليل المشاريع</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية", key="back_comp"):
            st.session_state.view = 'main'; st.rerun()
        
        q = st.text_input("بحث سريع...", placeholder="اكتب اسم المطور أو المشروع")
        f_df = df.head(15)
        for _, r in f_df.iterrows():
            st.markdown(f"""
            <div class="white-card">
                <div class="t-black" style="font-size:1.6rem;">{r[0]}</div>
                <div style="color:#2563eb; font-weight:900; font-size:1.2rem;">🏢 {r[2]}</div>
                <div class="t-black" style="font-size:1.7rem; background:#fef08a; display:inline-block; padding:2px 15px; margin-top:5px; border-radius:5px;">{r[4]}</div>
                <div class="t-black" style="font-size:1.1rem; margin-top:5px; color:#444;">📍 {r[3]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات
    elif st.session_state.view == 'tools':
        st.markdown('<div class="main-title"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية", key="back_tools"):
            st.session_state.view = 'main'; st.rerun()

        t1, t2 = st.tabs(["💰 حاسبة القسط", "📈 حاسبة الربح ROI"])
        
        with t1:
            u_p = st.number_input("سعر الوحدة الإجمالي", value=2000000, step=100000)
            d_p = st.number_input("المقدم %", value=10)
            yrs = st.number_input("عدد السنين", value=8)
            
            dv = u_p * (d_p/100)
            mv = (u_p - dv) / (yrs * 12) if yrs > 0 else 0
            
            st.markdown(f"""
                <div class="res-container">
                    <div style="margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;">
                        <span style="color:#aaa; font-size:1.2rem;">كاش المقدم المطلوب</span><br>
                        <span class="v-white">{dv:,.0f} ج.م</span>
                    </div>
                    <div style="margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;">
                        <span style="color:#aaa; font-size:1.2rem;">القسط الشهري</span><br>
                        <span class="v-white" style="color:#22c55e !important;">{mv:,.0f} ج.م</span>
                    </div>
                    <div>
                        <span style="color:#aaa; font-size:1.2rem;">القسط الربع سنوي</span><br>
                        <span class="v-white" style="color:#3b82f6 !important;">{mv*3:,.0f} ج.م</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with t2:
            buy = st.number_input("سعر الشراء", value=2000000, key="buy_v")
            sell = st.number_input("سعر البيع المتوقع", value=3500000, key="sell_v")
            rent = st.number_input("الإيجار الشهري", value=15000, key="rent_v")
            
            prof = sell - buy
            st.markdown(f"""
                <div class="res-container" style="background:#000;">
                    <div style="margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;">
                        <span style="color:#aaa; font-size:1.2rem;">صافي أرباح إعادة البيع</span><br>
                        <span class="v-white" style="color:#22c55e !important;">{prof:,.0f} ج.م</span>
                    </div>
                    <div style="margin-bottom:20px; border-bottom:1px solid #333; padding-bottom:10px;">
                        <span style="color:#aaa; font-size:1.2rem;">نسبة العائد الإجمالية ROI</span><br>
                        <span class="v-white" style="color:#f59e0b !important;">%{ (prof/buy)*100 if buy>0 else 0:.1f}</span>
                    </div>
                    <div>
                        <span style="color:#aaa; font-size:1.2rem;">عائد الإيجار السنوي</span><br>
                        <span class="v-white">%{ ((rent*12)/buy)*100 if buy>0 else 0:.1f}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
