import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الشامل (النمط الأسود الفاخر)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    /* الخلفية السوداء الشاملة */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #000000 !important; color: #ffffff !important; margin: 0; padding: 0;
    }

    /* العنوان البيضاوي العلوي */
    .hero-oval-header {
        background: #111111; border: 3px solid #f59e0b; border-top: none; 
        padding: 30px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 30px auto;
        box-shadow: 0px 10px 30px rgba(245, 158, 11, 0.2);
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.5rem; margin: 0; }

    /* الكروت السوداء بحدود ذهبية */
    .custom-card {
        background: #111111; border: 2px solid #f59e0b; padding: 25px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 0px 4px 15px rgba(245, 158, 11, 0.1);
    }
    
    /* النصوص */
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1.3rem; display: block; margin-top: 15px; }
    .val-white { color: #ffffff; font-weight: 700; font-size: 1.2rem; }
    h2, h3, h4 { color: #f59e0b !important; font-weight: 900 !important; }

    /* الأزرار (أبيض بخط أسود لتباين قوي) */
    div.stButton > button {
        border: 2px solid #f59e0b !important; border-radius: 12px !important;
        font-weight: 900 !important; background-color: #ffffff !important; 
        color: #000000 !important; height: 50px !important; font-size: 1.1rem !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { 
        background-color: #f59e0b !important; color: #000000 !important; 
        box-shadow: 0px 0px 15px #f59e0b !important; transform: scale(1.02);
    }

    /* المدخلات (Input) */
    input { background-color: #111111 !important; color: #ffffff !important; border: 1px solid #f59e0b !important; }
    
    .logout-box { position: fixed; top: 10px; left: 10px; z-index: 999; }
    
    /* ستايل قائمة المشاريع */
    .project-box {
        background: #222; border-right: 4px solid #f59e0b; padding: 10px; 
        margin: 5px 0; border-radius: 5px; color: #fff; font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

# 4. شاشة الدخول
if not st.session_state.auth:
    st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<h3 style='text-align:center;'>تسجيل دخول آمن</h3>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرor", type="password", placeholder="Password")
        if st.button("دخول", use_container_width=True):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("❌ كلمة المرور خاطئة")
    st.stop()

# --- المنصة الرئيسية (النمط الأسود) ---
df = load_data()
st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# زر الخروج
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"): st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# التقسيم الرئيسي
col_tools, col_devs = st.columns([0.4, 0.6])

# --- الجانب الأيمن: أدوات البروكر ---
with col_tools:
    st.markdown('<div class="custom-card"><h3>🛠️ أدوات البروكر</h3></div>', unsafe_allow_html=True)
    
    # حاسبة القسط
    with st.container():
        st.markdown('<div class="custom-card"><h4>💰 حاسبة الأقساط</h4>', unsafe_allow_html=True)
        tp = st.number_input("إجمالي سعر الوحدة", min_value=0, step=100000)
        dp_pct = st.slider("نسبة المقدم (%)", 0, 50, 10)
        yrs = st.number_input("عدد السنوات", 1, 20, 7)
        if tp > 0:
            dv = tp * (dp_pct / 100)
            mn = (tp - dv) / (yrs * 12)
            st.markdown(f'<div style="background:#f59e0b; color:#000; padding:15px; border-radius:15px; text-align:center;"><h5>المقدم: {dv:,.0f} ج.م</h5><h3>القسط: {mn:,.0f} ج.م</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # حاسبة العائد
    with st.container():
        st.markdown('<div class="custom-card"><h4>📈 حاسبة ROI</h4>', unsafe_allow_html=True)
        inv = st.number_input("إجمالي الاستثمار", min_value=0, step=100000)
        rent = st.number_input("الإيجار الشهري المتوقع", min_value=0, step=1000)
        if inv > 0 and rent > 0:
            roi = (rent * 12 / inv) * 100
            st.markdown(f'<div style="border: 2px solid #f59e0b; color:#f59e0b; padding:15px; border-radius:15px; text-align:center;"><h3>نسبة العائد: {roi:.2f}%</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- الجانب الأيسر: دليل المطورين ---
with col_devs:
    if st.session_state.selected_dev:
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        
        st.markdown(f'<div class="custom-card" style="border-width:4px;"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للشبكة"): st.session_state.selected_dev = None; st.rerun()
        
        st.markdown(f'''
            <div class="custom-card">
                <span class="label-gold">👤 المالك:</span> <span class="val-white">{row.get("Owner", "-")}</span>
                <span class="label-gold">📖 الوصف:</span> <p class="val-white">{row.get("Description", "-")}</p>
                <span class="label-gold">📍 المناطق:</span> <span class="val-white">{row.get("Area", "-")}</span>
                <span class="label-gold">💰 الأسعار:</span> <span class="val-white">{row.get("Price", "-")}</span>
                <span class="label-gold">📅 نظام التقسيط:</span> <span class="val-white">{row.get("Installments", "-")}</span>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.expander("🏗️ عرض المشاريع"):
            for p in str(row.get("Projects", "-")).split(","):
                st.markdown(f'<div class="project-box">🔹 {p.strip()}</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="custom-card"><h3>🏢 دليل المطورين</h3></div>', unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن مطور أو منطقة...")
        
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        # شبكة 3*3
        for i in range(0, len(dev_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dev_list):
                    name = dev_list[i + j]
                    if cols[j].button(name, key=f"d_{name}", use_container_width=True):
                        st.session_state.selected_dev = name; st.rerun()
