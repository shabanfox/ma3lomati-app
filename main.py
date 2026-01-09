import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (أزرار نانو حادة + محاذاة يمين)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر الملكي */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 15px; border-radius: 0px; 
        text-align: center; margin-bottom: 20px; border-bottom: 6px solid #f59e0b;
    }

    /* أزرار نانو (Nano-Cards) حادة ومصغرة */
    div.stButton > button {
        width: 100% !important; 
        height: 90px !important; /* حجم نانو مدمج */
        background-color: #ffffff !important; 
        color: #000000 !important;
        border: 4px solid #000000 !important; 
        border-radius: 0px !important; /* حواف حادة */
        box-shadow: 6px 6px 0px 0px #000000 !important;
        transition: 0.1s;
        margin-bottom: 10px !important;
    }
    div.stButton > button:hover { 
        transform: translate(2px, 2px); 
        box-shadow: 2px 2px 0px #f59e0b !important; 
        background-color: #000 !important;
        color: #f59e0b !important;
    }
    div.stButton > button p { font-weight: 900 !important; font-size: 0.95rem !important; line-height: 1.2; }

    /* صناديق الحاسبات */
    .calc-box { 
        background: #000; color: #fff; padding: 20px; border-radius: 0px; 
        border: 4px solid #f59e0b; text-align: center; margin-bottom: 15px;
    }
    .val-text { font-size: 2.2rem; font-weight: 900; color: #f59e0b !important; }
    
    /* تقليل المسافات بين الأعمدة للشبكة المتقاربة */
    [data-testid="column"] { padding: 5px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_row' not in st.session_state: st.session_state.selected_row = None

# --- المحتوى الرئيسي ---
if st.session_state.data is not None:
    
    # أ. الصفحة الرئيسية (الشبكة المصغرة 2x3 يميناً)
    if st.session_state.view == 'main':
        st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
        
        col_right, col_left = st.columns([0.6, 0.4])
        
        with col_right:
            st.markdown("<h3 style='font-weight:900;'>🏢 دليل المشاريع (Nano 2x3)</h3>", unsafe_allow_html=True)
            # عرض 6 مشاريع فقط في شبكة 2 عمود و 3 صفوف
            for i in range(0, 6, 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(st.session_state.data):
                        row = st.session_state.data.iloc[i + j]
                        with cols[j]:
                            # الزر عند الضغط عليه يفتح صفحة التفاصيل
                            if st.button(f"📌 {row[0]}\n🏢 {row[2]}", key=f"btn_{i+j}"):
                                st.session_state.selected_row = row
                                st.session_state.view = 'details'
                                st.rerun()
            
            st.markdown("---")
            if st.button("🛠️ فتح حاسبات الأدوات", key="main_tools"):
                st.session_state.view = 'tools'
                st.rerun()

        with col_left:
            st.info("💡 اضغط على كارت المشروع من اليمين لعرض التفاصيل الكاملة هنا.")

    # ب. صفحة التفاصيل (تظهر عند الضغط على أي زر نانو)
    elif st.session_state.view == 'details':
        r = st.session_state.selected_row
        st.markdown(f'<div class="hero-banner"><h1>📍 {r[0]}</h1></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        st.markdown(f"""
            <div style="border:8px solid #000; padding:30px; background:#fff; box-shadow: 12px 12px 0px #f59e0b;">
                <h1 style="font-weight:900;">{r[0]}</h1>
                <h2 style="color:#f59e0b;">المطور: {r[2]}</h2>
                <hr style="border:2px solid #000">
                <h3>📍 الموقع: {r[3]}</h3>
                <div style="background:#000; color:#fff; padding:20px; font-size:1.8rem; font-weight:900; margin-top:20px;">
                    💰 {r[4]}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ج. صفحة الأدوات والحاسبات
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-banner"><h2>🛠️ الحاسبات المالية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        t1, t2 = st.tabs(["💰 القسط الشهري", "📈 عائد الاستثمار ROI"])
        
        with t1:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            i1, i2 = st.columns(2)
            pr = i1.number_input("سعر الوحدة الإجمالي", value=3000000)
            yr = i2.number_input("عدد سنوات التقسيط", value=8)
            calc_mo = pr / (yr * 12) if yr > 0 else 0
            st.markdown(f'<div class="calc-box"><span style="color:#ccc;">القسط الشهري</span><br><span class="val-text">{calc_mo:,.0f} ج.م</span></div>', unsafe_allow_html=True)

        with t2:
            st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
            r1, r2 = st.columns(2)
            buy = r1.number_input("سعر الشراء", value=2000000)
            sell = r2.number_input("سعر البيع المتوقع", value=3500000)
            roi = ((sell - buy) / buy) * 100 if buy > 0 else 0
            st.markdown(f'<div class="calc-box" style="border-color:#fff;"><span style="color:#ccc;">نسبة الربح ROI</span><br><span class="val-text">%{roi:.1f}</span></div>', unsafe_allow_html=True)
