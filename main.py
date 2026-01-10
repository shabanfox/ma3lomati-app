import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتصفير المسافات
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS المتطور (تباين عالي + خطوط واضحة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* العنوان البيضاوي العلوي */
    .hero-oval-header {
        background: #000000; border: 5px solid #f59e0b; border-top: none; 
        padding: 30px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 30px auto;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.2);
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.2rem; margin: 0; }

    /* كروت الأدوات والبيانات */
    .custom-card {
        background: #ffffff; border: 4px solid #000000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }
    .card-black { background: #000000 !important; color: #ffffff !important; border: 4px solid #f59e0b !important; }

    /* نصوص واضحة جداً */
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1.2rem; display: block; margin-top: 10px; }
    .val-white { color: #ffffff; font-weight: 700; font-size: 1.1rem; }
    .text-black-bold { color: #000000; font-weight: 900; font-size: 1.3rem; }

    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 12px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        height: 50px !important; font-size: 1.1rem !important;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; transform: translate(-2px, -2px); }

    .logout-box { position: fixed; top: 10px; left: 10px; z-index: 999; }
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
        pwd = st.text_input("قفل الدخول 🔒", type="password", placeholder="أدخل كلمة المرور")
        if st.button("دخول", use_container_width=True):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("❌ الباسورد غير صحيح")
    st.stop()

# --- المنصة الرئيسية ---
df = load_data()
st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# زر الخروج
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"): st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# تقسيم الصفحة الرئيسية لجزئين (أدوات على اليمين - مطورين على اليسار)
col_tools, col_devs = st.columns([0.4, 0.6])

# --- الجزء الأول: أدوات البروكر (Right Side) ---
with col_tools:
    st.markdown('<div class="custom-card"><h2 class="text-black-bold">🛠️ أدوات البروكر الذكية</h2></div>', unsafe_allow_html=True)
    
    # حاسبة الأقساط
    with st.container():
        st.markdown('<div class="custom-card"><h4>💰 حاسبة الأقساط</h4>', unsafe_allow_html=True)
        tp = st.number_input("إجمالي السعر", min_value=0, step=100000, key="calc_tp")
        dp_pct = st.slider("المقدم (%)", 0, 50, 10)
        yrs = st.number_input("السنوات", 1, 20, 7)
        if tp > 0:
            dv = tp * (dp_pct / 100)
            mn = (tp - dv) / (yrs * 12)
            st.markdown(f'<div style="background:#000; color:#f59e0b; padding:15px; border-radius:15px; text-align:center;"><h5>المقدم: {dv:,.0f}</h5><h3>القسط: {mn:,.0f}</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # حاسبة ROI
    with st.container():
        st.markdown('<div class="custom-card"><h4>📈 حاسبة العائد ROI</h4>', unsafe_allow_html=True)
        inv = st.number_input("قيمة الاستثمار", min_value=0, step=100000)
        rt = st.number_input("الإيجار الشهري", min_value=0, step=1000)
        if inv > 0 and rt > 0:
            roi = (rt * 12 / inv) * 100
            st.markdown(f'<div style="background:#f59e0b; color:#000; padding:15px; border-radius:15px; text-align:center;"><h3>العائد السنوي: {roi:.2f}%</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# --- الجزء الثاني: دليل المطورين (Left Side) ---
with col_devs:
    if st.session_state.selected_dev:
        # عرض تفاصيل المطور المختار
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        
        st.markdown(f'<div class="custom-card card-black"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة لشبكة المطورين"): st.session_state.selected_dev = None; st.rerun()
        
        # تفاصيل الشركة
        st.markdown(f'''
            <div class="custom-card card-black">
                <span class="label-gold">👤 المالك:</span> <span class="val-white">{row.get("Owner", "-")}</span>
                <span class="label-gold">📖 الوصف:</span> <p class="val-white">{row.get("Description", "-")}</p>
                <hr style="border-color:#f59e0b">
                <span class="label-gold">📍 المناطق:</span> <span class="val-white">{row.get("Area", "-")}</span>
                <span class="label-gold">💰 الأسعار:</span> <span class="val-white">{row.get("Price", "-")}</span>
                <span class="label-gold">📅 التقسيط:</span> <span class="val-white">{row.get("Installments", "-")}</span>
            </div>
        ''', unsafe_allow_html=True)
        
        with st.expander("🏗️ عرض قائمة المشاريع", expanded=True):
            for p in str(row.get("Projects", "-")).split(","):
                st.markdown(f'<div style="background:#eee; color:#000; padding:8px; margin:4px; border-radius:8px; font-weight:700; border-right:5px solid #f59e0b">🔹 {p.strip()}</div>', unsafe_allow_html=True)
    
    else:
        # شبكة المطورين 3*3
        st.markdown('<div class="custom-card"><h2 class="text-black-bold">🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن مطور...")
        
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        # عرض المطورين في شبكة 3*3
        for i in range(0, len(dev_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dev_list):
                    name = dev_list[i + j]
                    if cols[j].button(name, key=f"d_{name}", use_container_width=True):
                        st.session_state.selected_dev = name; st.rerun()
