import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الموحد (المشاريع والأدوات)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .hero-banner h1, .hero-banner h2 { font-weight: 900; color: #f59e0b !important; margin: 0; }

    /* ستايل الكروت الموحد (للمطورين وللأدوات) */
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        text-align: center; transition: 0.3s;
    }
    .card-title { font-size: 1.5rem; font-weight: 900; color: #000; }
    .card-val { font-size: 2.2rem; font-weight: 900; color: #f59e0b; margin-top: 10px; }

    /* أزرار التنقل والتحكم */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 5px 5px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 7px 7px 0px #f59e0b !important; }

    /* تحسين المدخلات (Inputs) لتناسب التصميم */
    input { border: 3px solid #000 !important; border-radius: 10px !important; font-weight: 700 !important; }
    label { font-weight: 900 !important; font-size: 1.1rem !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Developer'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page' not in st.session_state: st.session_state.page = 0

df = st.session_state.data
target_col = 'Developer' if 'Developer' in df.columns else df.columns[1]

# --- الصفحة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<div style='height:80px;'></div>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([0.1, 0.8, 0.1])
    with mid_col:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            if st.button("🏢\nدليل المطورين", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
        with c2:
            if st.button("🛠️\nأدوات البروكر", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

# --- صفحة دليل المطورين ---
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    col_main, _ = st.columns([0.7, 0.3])
    
    with col_main:
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.session_state.page = 0; st.rerun()
        
        search = st.text_input("🔍 ابحث عن المطور (بحث سريع)...")
        unique_devs = df[target_col].dropna().unique()
        
        # بحث سريع ومتوافق
        if search:
            unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        items_per_page = 9
        start_idx = st.session_state.page * items_per_page
        current_devs = unique_devs[start_idx : start_idx + items_per_page]

        for i in range(0, len(current_devs), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    with grid_cols[j]:
                        st.markdown(f'<div class="custom-card" style="height:150px;"><div class="card-title">{current_devs[i+j]}</div></div>', unsafe_allow_html=True)

        # أزرار التنقل
        st.write("<br>", unsafe_allow_html=True)
        nav_prev, nav_next = st.columns([1, 1])
        with nav_prev:
            if st.session_state.page > 0:
                if st.button("⬅️ السابق"): st.session_state.page -= 1; st.rerun()
        with nav_next:
            if (start_idx + items_per_page) < len(unique_devs):
                if st.button("التالي ➡️"): st.session_state.page += 1; st.rerun()

# --- صفحة الأدوات (بتصميم المشاريع الموحد) ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر الذكية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📈 حاسبة العائد ROI"])
    
    with t1:
        st.write("<br>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: price = st.number_input("سعر الوحدة الإجمالي", value=1000000, step=100000)
        with c2: down_payment = st.number_input("المقدم %", value=10)
        with c3: years = st.number_input("سنوات التقسيط", value=8)
        
        calc_dn = price * (down_payment/100)
        calc_mo = (price - calc_dn) / (years * 12) if years > 0 else 0
        
        # عرض النتيجة بنفس ستايل كروت المشاريع
        st.markdown(f"""
            <div class="custom-card">
                <span style="font-weight:700;">المقدم المطلوب</span>
                <div class="card-val">{calc_dn:,.0f} ج.م</div>
                <hr style="width:100%; border:1px solid #eee;">
                <span style="font-weight:700;">القسط الشهري</span>
                <div class="card-val" style="color:#22c55e;">{calc_mo:,.0f} ج.م</div>
            </div>
        """, unsafe_allow_html=True)

    with t2:
        st.write("<br>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        with r1: buy_p = st.number_input("سعر الشراء", value=1000000)
        with r2: sell_p = st.number_input("سعر البيع المتوقع", value=1500000)
        with r3: annual_rent = st.number_input("الإيجار السنوي", value=100000)
        
        profit = (sell_p - buy_p) + annual_rent
        roi = (profit / buy_p) * 100 if buy_p > 0 else 0
        
        st.markdown(f"""
            <div class="custom-card">
                <span style="font-weight:700;">إجمالي الربح الاستثماري</span>
                <div class="card-val">{profit:,.0f} ج.م</div>
                <hr style="width:100%; border:1px solid #eee;">
                <span style="font-weight:700;">نسبة العائد (ROI)</span>
                <div class="card-val" style="color:#22c55e;">%{roi:.1f}</div>
            </div>
        """, unsafe_allow_html=True)
