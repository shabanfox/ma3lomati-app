import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والاتصال بالبيانات
st.set_page_config(page_title="منصة معلوماتى", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return None

# 2. تصميم CSS الاحترافي (ثبات الهوية البصرية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء إعدادات ستريمليت الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* التنسيق العام */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #FFFFFF; 
    }
    .block-container { padding-top: 1.5rem !important; }

    /* الهيدر الرئيسي (أسود وذهبي) */
    .hero-banner { 
        background: #000000; color: #FFD700; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 40px; border-bottom: 6px solid #FFD700;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .hero-banner h1 { color: #FFD700 !important; font-weight: 900; margin: 0; font-size: 2.4rem; }

    /* الأزرار الرئيسية (جنب بعض، عريضة، أنيقة) */
    div.stButton > button {
        width: 100% !important;
        height: 100px !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 5px solid #000000 !important;
        border-radius: 18px !important;
        font-size: 1.7rem !important;
        font-weight: 900 !important;
        box-shadow: 8px 8px 0px 0px #000000 !important;
        transition: 0.1s ease;
    }
    div.stButton > button:active {
        transform: translate(5px, 5px) !important;
        box-shadow: 0px 0px 0px 0px !important;
    }

    /* تصميم كروت المشاريع (النيومورفيزم الاحترافي) */
    .project-card {
        background: #FFFFFF; border: 4px solid #000000; padding: 22px; 
        border-radius: 22px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }
    .project-title { font-size: 1.9rem; font-weight: 900; color: #000000; margin-bottom: 8px; }
    .dev-name { color: #1e40af; font-weight: 900; font-size: 1.3rem; }
    .gold-tag { 
        font-weight: 900; font-size: 1.6rem; background: #FFD700; 
        display: inline-block; padding: 6px 18px; margin-top: 12px; border: 3px solid #000;
        border-radius: 10px;
    }

    /* صناديق نتائج الحاسبة */
    .res-box { 
        background: #000000; color: #FFFFFF; padding: 25px; 
        border-radius: 25px; text-align: center; border: 4px solid #FFD700;
    }
    .res-value { font-size: 2.6rem; font-weight: 900; color: #FFD700 !important; }
    
    /* المدخلات */
    label { font-weight: 900 !important; color: #000000 !important; font-size: 1.3rem !important; }
    input { border: 4px solid #000000 !important; font-weight: 900 !important; font-size: 1.5rem !important; border-radius: 12px !important; }
    </style>
""", unsafe_allow_html=True)

df = load_data()

# إدارة التنقل
if 'view' not in st.session_state: st.session_state.view = 'main'

if df is not None:
    # --- الشاشة الرئيسية ---
    if st.session_state.view == 'main':
        st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
        
        # وضع الأزرار جنباً إلى جنب (توسيط 90%)
        _, col_body, _ = st.columns([0.05, 0.9, 0.05])
        with col_body:
            c1, c2 = st.columns(2, gap="medium")
            with c1:
                if st.button("🏢\nدليل المشاريع", key="nav_proj"):
                    st.session_state.view = 'comp'; st.rerun()
            with c2:
                if st.button("🛠️\nأدوات البروكر", key="nav_tool"):
                    st.session_state.view = 'tools'; st.rerun()

    # --- صفحة المشاريع ---
    elif st.session_state.view == 'comp':
        st.markdown('<div class="hero-banner"><h2>🔍 دليل المشاريع العقارية</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        search_q = st.text_input("بحث سريع عن مشروع أو مطور...", placeholder="اكتب هنا...")
        
        # فلترة البيانات
        disp_df = df[df.apply(lambda r: search_q.lower() in r.astype(str).str.lower().values, axis=1)] if search_q else df.head(15)
        
        for _, row in disp_df.iterrows():
            st.markdown(f"""
            <div class="project-card">
                <div class="project-title">{row[0]}</div>
                <div class="dev-name">🏢 المطور: {row[2]}</div>
                <div class="gold-tag">{row[4]}</div>
                <div style="margin-top:10px; font-weight:700;">📍 الموقع: {row[3]}</div>
            </div>
            """, unsafe_allow_html=True)

    # --- صفحة الأدوات (الحاسبتين) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-banner"><h2>🛠️ الأدوات والحاسبات</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        # 1. حاسبة الأقساط
        st.markdown("<h3 style='border-right:8px solid #000; padding-right:12px; font-weight:900;'>💰 حاسبة القسط والمقدم</h3>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        with col_a: u_p = st.number_input("سعر الوحدة", value=2000000, key="calc_p")
        with col_b: u_d = st.number_input("المقدم %", value=10, key="calc_d")
        with col_c: u_y = st.number_input("سنين التقسيط", value=8, key="calc_y")
        
        calc_dv = u_p * (u_d/100)
        calc_mv = (u_p - calc_dv) / (u_y * 12) if u_y > 0 else 0
        
        st.markdown(f"""
            <div class="res-box">
                <span style="color:#bbb;">كاش المقدم:</span><br><span class="res-value">{calc_dv:,.0f} ج.م</span>
                <hr style="border-color:#333">
                <span style="color:#bbb;">القسط الشهري:</span><br><span class="res-value" style="color:#22c55e !important;">{calc_mv:,.0f} ج.م</span>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br><hr style='border:2px solid #000;'><br>", unsafe_allow_html=True)

        # 2. حاسبة الربح ROI
        st.markdown("<h3 style='border-right:8px solid #FFD700; padding-right:12px; font-weight:900;'>📈 حاسبة الاستثمار ROI</h3>", unsafe_allow_html=True)
        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1: b_v = st.number_input("سعر الشراء", value=2000000, key="roi_b")
        with col_r2: s_v = st.number_input("سعر البيع", value=3500000, key="roi_s")
        with col_r3: r_v = st.number_input("إيجار شهري", value=15000, key="roi_r")
        
        roi_prof = s_v - b_v
        roi_perc = (roi_prof/b_v)*100 if b_v > 0 else 0
        
        st.markdown(f"""
            <div class="res-box" style="border-color:#FFFFFF;">
                <span style="color:#bbb;">صافي الربح:</span><br><span class="res-value" style="color:#FFD700 !important;">{roi_prof:,.0f} ج.م</span>
                <hr style="border-color:#333">
                <span style="color:#bbb;">نسبة العائد الإجمالية:</span><br><span class="res-value">%{roi_perc:.1f}</span>
            </div>
        """, unsafe_allow_html=True)
else:
    st.error("يرجى التأكد من رابط البيانات والاتصال بالإنترنت")
