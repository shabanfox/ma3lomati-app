import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتصفير المسافات تماماً
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الشامل (الدخول + المنصة + لمسات متطورة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child {
        padding-top: 0rem !important;
        padding-left: 0rem !important;
        padding-right: 0rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #ffffff; margin: 0 !important; padding: 0 !important;
    }

    /* --- صفحة الدخول (البيضاوي المنسدل) --- */
    .login-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .hero-oval-header {
        background: #000000; border: 5px solid #f59e0b; border-top: none; 
        padding: 50px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.2); margin-bottom: 30px;
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.5rem; margin: 0; }
    .gold-lock { font-size: 60px; color: #f59e0b; margin-bottom: 20px; text-align: center; width: 100%; }

    .stTextInput input {
        background-color: #ffffff !important; color: #000000 !important;
        border: 3px solid #000000 !important; border-radius: 15px !important;
        text-align: center; font-size: 1.3rem !important; height: 60px !important;
        font-weight: 700; box-shadow: 5px 5px 0px #f59e0b !important;
    }

    /* --- تصميم محتوى المنصة --- */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        text-align: right;
    }
    .card-title { font-size: 1.8rem; font-weight: 900; color: #f59e0b; border-bottom: 3px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
    .card-label { font-weight: 900; color: #000; font-size: 1.2rem; display: block; margin-top: 10px; }
    .card-val { font-weight: 700; color: #444; font-size: 1.1rem; }

    /* ستايل الأزرار العام */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 50px !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }

    /* زر الخروج العائم */
    .logout-box { position: fixed; top: 10px; left: 10px; z-index: 999; }
    
    /* ستايل قائمة المشاريع */
    .project-item {
        background: #f8f9fa; border-right: 5px solid #f59e0b;
        padding: 10px 15px; margin-bottom: 10px; border-radius: 5px;
        font-weight: 700; color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = 'main'
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

# 4. شاشة تسجيل الدخول
def login_screen():
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown('<div class="gold-lock">🔒</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns([1, 1.5, 1])
    with col_b:
        pwd = st.text_input("الباسورد", type="password", placeholder="أدخل كلمة المرور", label_visibility="collapsed")
        if st.button("دخول", use_container_width=True):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True; st.rerun()
            else: st.error("⚠️ الباسورد غير صحيح")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.auth:
    login_screen(); st.stop()

# --- المنصة الرئيسية ---
df = load_data()

st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"):
    st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.session_state.current_page = 0; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # صفحة التفاصيل المتطورة
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        
        col_back, col_spacer = st.columns([1, 4])
        with col_back:
            if st.button("🔙 العودة"): st.session_state.selected_dev = None; st.rerun()
        
        col_r, col_l = st.columns([1.2, 1])
        with col_r:
            st.markdown(f'<div class="custom-card"><div class="card-title">👤 تفاصيل المالك والشركة</div><p class="card-label">المالك:</p><p class="card-val">{row.get("Owner", "-")}</p><p class="card-label">فلسفة الشركة:</p><p class="card-val">{row.get("Description", "-")}</p></div>', unsafe_allow_html=True)
            
            # قسم "مشاريع الشركة" التفاعلي
            with st.expander("🏗️ عرض قائمة المشاريع بالكامل", expanded=True):
                projects = str(row.get("Projects", "-")).split(",")
                for p in projects:
                    st.markdown(f'<div class="project-item">🔹 {p.strip()}</div>', unsafe_allow_html=True)

        with col_l:
            st.markdown(f'<div class="custom-card"><div class="card-title">📊 بيانات المشاريع</div><span class="card-label">📍 المناطق:</span> <span class="card-val">{row.get("Area", "-")}</span><span class="card-label">💰 الأسعار:</span> <span class="card-val">{row.get("Price", "-")}</span><span class="card-label">💵 المقدم:</span> <span class="card-val">{row.get("Down_Payment", "-")}</span><span class="card-label">📅 التقسيط:</span> <span class="card-val">{row.get("Installments", "-")}</span></div>', unsafe_allow_html=True)
            st.info("💡 نصيحة: تأكد من مراجعة أحدث العروض من قسم الأدوات.")

    else:
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        col_main, col_spacer = st.columns([0.7, 0.3]) # توزيع 70% يمين
        with col_main:
            if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
            search = st.text_input("🔍 ابحث عن مطور...")
            dev_list = df['Developer'].unique()
            if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
            
            # نظام الصفحات
            items_per_page = 9
            total_pages = (len(dev_list) - 1) // items_per_page + 1
            start_idx = st.session_state.current_page * items_per_page
            current_devs = dev_list[start_idx:start_idx + items_per_page]

            for i in range(0, len(current_devs), 3):
                grid_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_devs):
                        name = current_devs[i + j]
                        if grid_cols[j].button(name, key=f"dev_{name}", use_container_width=True):
                            st.session_state.selected_dev = name; st.rerun()
            
            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.current_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with n3:
                if (start_idx + items_per_page) < len(dev_list):
                    if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر المحترف</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="custom-card"><div class="card-title">💰 حاسبة الأقساط</div></div>', unsafe_allow_html=True)
        tp = st.number_input("إجمالي السعر", min_value=0, step=100000)
        dp_pct = st.number_input("المقدم (%)", 0, 100, 10)
        yrs = st.number_input("السنوات", 1, 30, 7)
        if tp > 0:
            dv = tp * (dp_pct / 100)
            mn = (tp - dv) / (yrs * 12)
            st.markdown(f'<div style="background:#000; color:#f59e0b; padding:10px; border-radius:10px; text-align:center;"><h5>المقدم: {dv:,.0f}</h5><h4>القسط: {mn:,.0f}</h4></div>', unsafe_allow_html=True)
    with t2:
        st.markdown('<div class="custom-card"><div class="card-title">📈 حاسبة العائد ROI</div></div>', unsafe_allow_html=True)
        inv = st.number_input("قيمة الاستثمار", min_value=0, step=100000)
        rt = st.number_input("الإيجار الشهري", min_value=0, step=1000)
        if inv > 0 and rt > 0:
            ann = rt * 12
            roi = (ann / inv) * 100
            st.markdown(f'<div style="background:#f59e0b; color:#000; padding:10px; border-radius:10px; text-align:center;"><h5>الدخل السنوي: {ann:,.0f}</h5><h4>العائد: {roi:.2f}%</h4></div>', unsafe_allow_html=True)
