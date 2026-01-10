import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS المتطور (التثبيت + الألوان)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* شريط التنقل المثبت */
    .sticky-nav {
        position: fixed; top: 0; right: 0; left: 0; background: #ffffff;
        z-index: 999; padding: 10px 20px; border-bottom: 2px solid #f59e0b;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }

    .hero-oval-header {
        background: #000000; border: 5px solid #f59e0b; border-top: none; 
        padding: 30px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 20px auto;
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2rem; margin: 0; }

    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000;
    }
    .card-title { font-size: 1.5rem; font-weight: 900; color: #f59e0b; border-bottom: 3px solid #000; margin-bottom: 15px; }
    .card-label { font-weight: 900; color: #000; font-size: 1.1rem; display: block; margin-top: 10px; }
    .card-val { font-weight: 700; color: #444; }

    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 12px !important;
        box-shadow: 3px 3px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1rem !important; min-height: 45px !important; width: 100%;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; transform: translateY(-2px); }

    /* مساحة تعويضية بسبب الشريط المثبت */
    .content-spacer { margin-top: 100px; }
    
    .logout-box { position: fixed; top: 15px; left: 15px; z-index: 1000; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = 'comp'
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'current_page' not in st.session_state: st.session_state.current_page = 0

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
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        pwd = st.text_input("قفل الدخول 🔒", type="password")
        if st.button("دخول المنصة"):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("كلمة المرور غير صحيحة")
    st.stop()

# --- محتوى المنصة ---
df = load_data()

# زر الخروج
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"): st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# شريط التنقل المثبت في الأعلى
st.markdown('<div class="sticky-nav">', unsafe_allow_html=True)
nav1, nav2 = st.columns(2)
with nav1:
    if st.button("🏢 دليل المطورين", use_container_width=True):
        st.session_state.view = 'comp'; st.session_state.selected_dev = None; st.session_state.current_page = 0; st.rerun()
with nav2:
    if st.button("🛠️ أدوات البروكر", use_container_width=True):
        st.session_state.view = 'tools'; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# إضافة مسافة حتى لا يختفي المحتوى تحت الشريط المثبت
st.markdown('<div class="content-spacer"></div>', unsafe_allow_html=True)

# --- عرض المطورين ---
if st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        if st.button("🔙 عودة للقائمة"): st.session_state.selected_dev = None; st.rerun()
        
        c_r, c_l = st.columns([1.2, 1])
        with c_r:
            st.markdown(f'<div class="custom-card"><div class="card-title">{dev_name}</div><span class="card-label">👤 المالك:</span><span class="card-val">{row.get("Owner", "-")}</span><span class="card-label">📖 نبذة:</span><p class="card-val">{row.get("Description", "-")}</p></div>', unsafe_allow_html=True)
        with c_l:
            st.markdown(f'<div class="custom-card"><div class="card-title">📍 التفاصيل</div><span class="card-label">المناطق:</span><span class="card-val">{row.get("Area", "-")}</span><span class="card-label">الأسعار:</span><span class="card-val">{row.get("Price", "-")}</span><span class="card-label">التقسيط:</span><span class="card-val">{row.get("Installments", "-")}</span></div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="hero-oval-header"><h1>🏢 دليل المطورين</h1></div>', unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث عن المطور...")
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        # منطق الـ 9 كروت
        items_per_page = 9
        total_pages = max((len(dev_list) - 1) // items_per_page + 1, 1)
        start = st.session_state.current_page * items_per_page
        current_devs = dev_list[start : start + items_per_page]

        for i in range(0, len(current_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    name = current_devs[i + j]
                    if cols[j].button(name, key=f"dev_{name}"):
                        st.session_state.selected_dev = name; st.rerun()
        
        # أزرار التنقل (السابق والتالي)
        st.write("---")
        p1, p2, p3 = st.columns([1, 2, 1])
        with p1:
            if st.session_state.current_page > 0:
                if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
        with p2:
            st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
        with p3:
            if (start + items_per_page) < len(dev_list):
                if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

# --- عرض الأدوات ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-oval-header"><h1>🛠️ أدوات البروكر الذكية</h1></div>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="custom-card"><div class="card-title">💰 حاسبة الأقساط</div>', unsafe_allow_html=True)
        tp = st.number_input("إجمالي السعر", min_value=0, step=100000)
        dp = st.slider("المقدم (%)", 0, 50, 10)
        yr = st.number_input("السنوات", 1, 30, 7)
        if tp > 0:
            val = (tp - (tp * dp / 100)) / (yr * 12)
            st.markdown(f'<div style="background:#000; color:#f59e0b; padding:15px; border-radius:10px; text-align:center;"><h3>القسط: {val:,.0f} ج.م</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with t2:
        st.markdown('<div class="custom-card"><div class="card-title">📈 حاسبة العائد ROI</div>', unsafe_allow_html=True)
        inv = st.number_input("الاستثمار", min_value=0, step=100000)
        rt = st.number_input("الإيجار الشهري", min_value=0, step=1000)
        if inv > 0 and rt > 0:
            roi = (rt * 12 / inv) * 100
            st.markdown(f'<div style="background:#f59e0b; color:#000; padding:15px; border-radius:10px; text-align:center;"><h3>العائد: {roi:.2f}%</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
