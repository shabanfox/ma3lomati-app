import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS القسري (تكبير وتوحيد الكروت)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-banner { 
        background: #000; color: #f59e0b; padding: 30px; border-radius: 25px; 
        text-align: center; margin-bottom: 40px; border: 5px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }

    /* الكروت الكبيرة والمتساوية - الحجم الأقصى */
    div.stButton > button[key^="dev_btn_"] {
        width: 100% !important;
        height: 220px !important; /* تكبير الارتفاع ليكون بحجم أكبر كارت */
        min-height: 220px !important;
        max-height: 220px !important;
        background-color: #ffffff !important;
        border: 6px solid #000000 !important;
        border-radius: 30px !important;
        box-shadow: 12px 12px 0px #000000 !important;
        font-size: 1.8rem !important; /* تكبير الخط أيضاً ليتناسب مع الكارت */
        font-weight: 900 !important;
        color: #000 !important;
        transition: 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        line-height: 1.4 !important;
    }

    div.stButton > button[key^="dev_btn_"]:hover {
        transform: translate(-5px, -5px);
        box-shadow: 15px 15px 0px #f59e0b !important;
        border-color: #f59e0b !important;
        background-color: #fafafa !important;
    }

    /* تنسيق صفحة الأدوات والحاسبات */
    .tool-box-card {
        background: #ffffff; border: 5px solid #000; padding: 30px;
        border-radius: 25px; box-shadow: 10px 10px 0px #000;
        text-align: center; margin-top: 20px;
    }
    .val-text { font-size: 2.5rem; font-weight: 900; color: #f59e0b; margin: 10px 0; }
    
    /* جعل الحقول واضحة */
    .stNumberInput label { font-weight: 900 !important; font-size: 1.2rem !important; }
    </style>
""", unsafe_allow_html=True)

# 3. دالة جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Developer', 'Project'])

# إدارة الحالة (Session State)
if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page' not in st.session_state: st.session_state.page = 0

df = st.session_state.data
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]
proj_col = df.columns[0]

# --- الشاشة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
    st.write("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([0.1, 0.8, 0.1])
    with mid:
        c1, c2 = st.columns(2, gap="large")
        if c1.button("🏢\nدليل المطورين", use_container_width=True, key="btn_to_comp"): 
            st.session_state.view = 'comp'; st.rerun()
        if c2.button("🛠️\nأدوات البروكر", use_container_width=True, key="btn_to_tool"): 
            st.session_state.view = 'tools'; st.rerun()

# --- صفحة المطورين (كروت عملاقة متساوية) ---
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    col_content, _ = st.columns([0.7, 0.3])
    
    with col_content:
        if st.button("🔙 العودة للرئيسية", key="back_home"): st.session_state.view = 'main'; st.rerun()
        
        search = st.text_input("🔍 ابحث عن المطور...")
        unique_devs = df[dev_col].dropna().unique()
        if search: 
            unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
        
        # شبكة 3x3 متساوية الأبعاد 100%
        items_per_page = 9
        start = st.session_state.page * items_per_page
        current = unique_devs[start : start + items_per_page]
        
        for i in range(0, len(current), 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(current):
                    dev_name = current[i + j]
                    with grid[j]:
                        if st.button(dev_name, key=f"dev_btn_{dev_name}"):
                            st.session_state.selected_dev = dev_name
                            st.session_state.view = 'dev_details'; st.rerun()

        # التحكم في الصفحات
        st.write("<br>", unsafe_allow_html=True)
        p1, p2 = st.columns(2)
        if p1.button("⬅️ السابق") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        if p2.button("التالي ➡️") and (start + items_per_page) < len(unique_devs):
            st.session_state.page += 1; st.rerun()

# --- صفحة الأدوات (الحاسبات في مكانها) ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر الذكية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    tab_loan, tab_roi = st.tabs(["💰 حاسبة القسط", "📈 حاسبة العائد ROI"])
    
    with tab_loan:
        st.write("<br>", unsafe_allow_html=True)
        l1, l2, l3 = st.columns(3)
        p_val = l1.number_input("سعر الوحدة", value=2000000, step=100000)
        d_per = l2.number_input("نسبة المقدم %", value=10)
        y_val = l3.number_input("عدد السنوات", value=8)
        
        calc_down = p_val * (d_per / 100)
        calc_month = (p_val - calc_down) / (y_val * 12) if y_val > 0 else 0
        
        st.markdown(f'''
            <div class="tool-box-card">
                <h3>المقدم المطلوب</h3>
                <div class="val-text">{calc_down:,.0f} ج.م</div>
                <hr style="border:1px solid #eee">
                <h3>القسط الشهري</h3>
                <div class="val-text" style="color:#22c55e;">{calc_month:,.0f} ج.م</div>
            </div>
        ''', unsafe_allow_html=True)

    with tab_roi:
        st.write("<br>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        buy_p = r1.number_input("سعر الشراء", value=1000000)
        sell_p = r2.number_input("سعر البيع المتوقع", value=1600000)
        rent_a = r3.number_input("الإيجار السنوي", value=120000)
        
        total_profit = (sell_p - buy_p) + rent_a
        roi_perc = (total_profit / buy_p) * 100 if buy_p > 0 else 0
        
        st.markdown(f'''
            <div class="tool-box-card">
                <h3>صافي الربح المتوقع</h3>
                <div class="val-text">{total_profit:,.0f} ج.م</div>
                <hr style="border:1px solid #eee">
                <h3>نسبة العائد ROI</h3>
                <div class="val-text" style="color:#22c55e;">%{roi_perc:.1f}</div>
            </div>
        ''', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.view == 'dev_details':
    st.markdown(f'<div class="hero-banner"><h2>{st.session_state.selected_dev}</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للقائمة"): st.session_state.view = 'comp'; st.rerun()
    st.write("### 🏗️ قائمة المشاريع:")
    projs = df[df[dev_col] == st.session_state.selected_dev][proj_col].unique()
    for p in projs:
        st.markdown(f'<div style="background:#fff; border:4px solid #000; padding:20px; border-radius:15px; margin-bottom:12px; box-shadow:6px 6px 0px #000; font-weight:900; font-size:1.3rem;">🔹 {p}</div>', unsafe_allow_html=True)
