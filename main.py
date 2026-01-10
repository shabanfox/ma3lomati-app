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
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #000000 !important; color: #ffffff !important;
    }

    .hero-oval-header {
        background: #111111; border: 3px solid #f59e0b; border-top: none; 
        padding: 30px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 30px auto;
        box-shadow: 0px 10px 30px rgba(245, 158, 11, 0.2);
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.2rem; margin: 0; }

    .custom-card {
        background: #111111; border: 2px solid #f59e0b; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px;
    }
    
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1.2rem; display: block; margin-top: 10px; }
    .val-white { color: #ffffff; font-weight: 700; }

    /* الأزرار بيضاء بخط أسود عريض */
    div.stButton > button {
        border: 2px solid #f59e0b !important; border-radius: 12px !important;
        font-weight: 900 !important; background-color: #ffffff !important; 
        color: #000000 !important; height: 50px !important; width: 100%;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: #000 !important; }

    .logout-box { position: fixed; top: 10px; left: 10px; z-index: 999; }
    
    .page-info { text-align: center; color: #f59e0b; font-weight: 700; font-size: 1.1rem; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page' not in st.session_state: st.session_state.page = 0

@st.cache_data(ttl=300)
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

# 4. الحماية
if not st.session_state.auth:
    st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول"):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    st.stop()

# --- واجهة المنصة ---
df = load_data()
st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# زر الخروج
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"): st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# التقسيم (المطورين يمين 60% - الأدوات يسار 40%)
col_devs, col_tools = st.columns([0.6, 0.4])

# --- الجانب الأيمن: المطورين ---
with col_devs:
    if st.session_state.selected_dev:
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        st.markdown(f'<div class="custom-card"><h2>🏢 {dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للشبكة"): st.session_state.selected_dev = None; st.rerun()
        
        st.markdown(f'''
            <div class="custom-card">
                <span class="label-gold">👤 المالك:</span> <span class="val-white">{row.get("Owner", "-")}</span>
                <span class="label-gold">📍 المناطق:</span> <span class="val-white">{row.get("Area", "-")}</span>
                <span class="label-gold">💰 الأسعار:</span> <span class="val-white">{row.get("Price", "-")}</span>
                <span class="label-gold">📅 التقسيط:</span> <span class="val-white">{row.get("Installments", "-")}</span>
            </div>
        ''', unsafe_allow_html=True)
    else:
        st.markdown('<div class="custom-card"><h3>🏢 دليل المطورين</h3></div>', unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن مطور...")
        
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        # نظام الصفحات (9 كروت)
        limit = 9
        total_pages = (len(dev_list) - 1) // limit + 1
        start = st.session_state.page * limit
        current_devs = dev_list[start : start + limit]

        # شبكة 3x3
        for i in range(0, len(current_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    name = current_devs[i + j]
                    if cols[j].button(name, key=f"d_{name}"):
                        st.session_state.selected_dev = name; st.rerun()
        
        # أزرار التنقل
        st.write("---")
        p1, p2, p3 = st.columns([1, 2, 1])
        with p1:
            if st.session_state.page > 0:
                if st.button("⬅️ السابق"): st.session_state.page -= 1; st.rerun()
        with p2:
            st.markdown(f'<div class="page-info">صفحة {st.session_state.page + 1} من {total_pages}</div>', unsafe_allow_html=True)
        with p3:
            if (st.session_state.page + 1) < total_pages:
                if st.button("التالي ➡️"): st.session_state.page += 1; st.rerun()

# --- الجانب الأيسر: الأدوات ---
with col_tools:
    st.markdown('<div class="custom-card"><h3>🛠️ أدوات البروكر</h3></div>', unsafe_allow_html=True)
    
    # حاسبة القسط
    with st.container():
        st.markdown('<div class="custom-card"><h4>💰 حاسبة الأقساط</h4>', unsafe_allow_html=True)
        tp = st.number_input("السعر الإجمالي", min_value=0, step=100000)
        dp = st.slider("المقدم (%)", 0, 50, 10)
        yr = st.number_input("السنوات", 1, 20, 7)
        if tp > 0:
            res = (tp - (tp * dp / 100)) / (yr * 12)
            st.markdown(f'<div style="background:#f59e0b; color:#000; padding:15px; border-radius:15px; text-align:center;"><h3>القسط: {res:,.0f} ج.م</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # حاسبة ROI
    with st.container():
        st.markdown('<div class="custom-card"><h4>📈 حاسبة ROI</h4>', unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", min_value=0, step=100000)
        rent = st.number_input("الإيجار", min_value=0, step=1000)
        if inv > 0 and rent > 0:
            roi = (rent * 12 / inv) * 100
            st.markdown(f'<div style="border:2px solid #f59e0b; color:#f59e0b; padding:15px; border-radius:15px; text-align:center;"><h3>العائد: {roi:.2f}%</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
