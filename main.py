import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (تثبيت الألوان والخطوط والأزرار العريضة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* التنسيق العام للجسم */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }
    .block-container { padding-top: 2rem !important; }

    /* الهيدر الملكي */
    .hero-section { 
        background: #000000; color: #FFD700; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 50px; border: 5px solid #FFD700;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .hero-section h1 { color: #FFD700 !important; font-weight: 900; margin: 0; font-size: 3rem; }

    /* تنسيق الأزرار (جنب بعض في صف واحد عريض) */
    div.stButton > button {
        width: 100% !important;
        height: 150px !important; /* ارتفاع فخم وعريض */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 6px solid #000000 !important;
        border-radius: 25px !important;
        font-size: 2.2rem !important;
        font-weight: 900 !important;
        box-shadow: 12px 12px 0px 0px #000000 !important; /* ظل حاد وواضح */
        transition: all 0.1s ease-in-out;
        display: flex; align-items: center; justify-content: center;
    }
    
    /* تأثير الضغط على الزر */
    div.stButton > button:active {
        transform: translate(8px, 8px) !important;
        box-shadow: 0px 0px 0px 0px !important;
    }

    /* كروت النتائج (تباين أسود/ذهبي) */
    .result-container { 
        background: #000000; color: #ffffff; padding: 30px; 
        border-radius: 25px; text-align: center; border: 4px solid #FFD700;
        margin-top: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.2);
    }
    .result-value { font-size: 3rem; font-weight: 900; color: #FFD700 !important; display: block; }
    .result-label { font-size: 1.2rem; color: #cccccc; font-weight: 700; }

    /* كروت دليل المشاريع */
    .data-item {
        background: #ffffff; border: 4px solid #000000; padding: 25px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }

    /* تحسين شكل المدخلات الرقمية */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.5rem !important; }
    input { 
        border: 4px solid #000000 !important; font-weight: 900 !important; 
        font-size: 1.8rem !important; border-radius: 15px !important; text-align: center !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات من Google Sheets
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# إدارة التنقل بين الصفحات
if 'view' not in st.session_state: st.session_state.view = 'main'

# --- المحتوى الرئيسي ---
if df is not None:
    # أ. الشاشة الرئيسية (أزرار عريضة جنب بعض في المنتصف)
    if st.session_state.view == 'main':
        st.markdown('<div class="hero-section"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
        
        # توزيع الأزرار في صف واحد (توسيط بنسبة 90% من الشاشة)
        _, col_main, _ = st.columns([0.05, 0.9, 0.05])
        with col_main:
            c1, c2 = st.columns(2, gap="large")
            with c1:
                if st.button("🏢\nدليل المشاريع", key="btn_proj"):
                    st.session_state.view = 'comp'; st.rerun()
            with c2:
                if st.button("🛠️\nأدوات البروكر", key="btn_tool"):
                    st.session_state.view = 'tools'; st.rerun()

    # ب. صفحة المشاريع
    elif st.session_state.view == 'comp':
        st.markdown('<div class="hero-section"><h2>🔍 دليل المشاريع العقارية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        q = st.text_input("بحث سريع...", placeholder="اكتب اسم المشروع")
        for _, r in df.head(10).iterrows():
            st.markdown(f"""
            <div class="data-item">
                <div style="font-weight:900; font-size:2rem; color:#000;">{r[0]}</div>
                <div style="color:#2563eb; font-weight:900; font-size:1.4rem;">🏢 المطور: {r[2]}</div>
                <div style="font-weight:900; font-size:1.8rem; background:#FFD700; display:inline-block; padding:5px 20px; margin-top:10px; border:3px solid #000;">{r[4]}</div>
            </div>
            """, unsafe_allow_html=True)

    # ج. صفحة الأدوات (الحاسبتين معاً بوضوح تدرجي)
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-section"><h2>🛠️ أدوات الحاسبة الذكية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        # 💰 حاسبة الأقساط
        st.markdown("<h2 style='border-right:12px solid #000; padding-right:15px; font-weight:900;'>💰 حاسبة القسط والمقدم</h2>", unsafe_allow_html=True)
        a, b, c = st.columns(3)
        with a: price = st.number_input("سعر الوحدة", value=2000000, step=50000, key="c1")
        with b: down = st.number_input("المقدم %", value=10, key="c2")
        with c: years = st.number_input("السنين", value=8, key="c3")
        
        dv = price * (down/100)
        mv = (price - dv) / (years * 12) if years > 0 else 0
        
        st.markdown(f"""
            <div class="result-container">
                <span class="result-label">كاش المقدم المطلوب:</span>
                <span class="result-value">{dv:,.0f} ج.م</span>
                <hr style="border:1px solid #333; margin: 20px 0;">
                <span class="result-label">القسط الشهري:</span>
                <span class="result-value" style="color:#22c55e !important;">{mv:,.0f} ج.م</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:60px;'></div>", unsafe_allow_html=True)

        # 📈 حاسبة الربح ROI
        st.markdown("<h2 style='border-right:12px solid #FFD700; padding-right:15px; font-weight:900;'>📈 حاسبة الاستثمار (ROI)</h2>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        with r1: b_p = st.number_input("سعر الشراء", value=2000000, key="r1")
        with r2: s_p = st.number_input("سعر البيع المتوقع", value=3500000, key="r2")
        with r3: rent = st.number_input("الإيجار الشهري", value=15000, key="r3")
        
        prof = s_p - b_p
        roi = (prof/b_p)*100 if b_p > 0 else 0
        
        st.markdown(f"""
            <div class="result-container" style="border-color:#ffffff;">
                <span class="result-label">صافي أرباح إعادة البيع:</span>
                <span class="result-value" style="color:#FFD700 !important;">{prof:,.0f} ج.م</span>
                <hr style="border:1px solid #333; margin: 20px 0;">
                <span class="result-label">نسبة العائد الإجمالية ROI:</span>
                <span class="result-value">%{roi:.1f}</span>
            </div>
        """, unsafe_allow_html=True)

else:
    st.error("تأكد من اتصالك بالإنترنت وصحة رابط Google Sheets")
