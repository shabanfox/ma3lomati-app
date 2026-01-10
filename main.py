import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS المتطور (التباين العالي والخطوط الواضحة)
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
        background: #000000; border: 4px solid #f59e0b; border-top: none; 
        padding: 30px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 20px auto;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.2);
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.2rem; margin: 0; }

    /* الكروت الاحترافية */
    .custom-card {
        background: #ffffff; border: 3px solid #000000; padding: 25px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 10px 10px 0px #000;
    }
    
    /* نصوص واضحة جداً */
    .text-white-bold { color: #ffffff !important; font-weight: 900 !important; text-shadow: 1px 1px 2px #000; }
    .text-black-bold { color: #000000 !important; font-weight: 900 !important; font-size: 1.2rem; }

    /* تصميم أزرار التنقل (التبديل بين المطورين والأدوات) */
    .nav-btn-container { display: flex; gap: 10px; margin-bottom: 25px; }
    
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        height: 55px !important; font-size: 1.2rem !important;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: #000 !important; transform: translate(-2px, -2px); }

    /* ستايل المطور في الشبكة */
    .dev-slot {
        background: #f8f9fa; border: 2px solid #000; border-radius: 15px;
        padding: 15px; text-align: center; margin-bottom: 10px;
    }
    
    .logout-box { position: fixed; top: 10px; left: 10px; z-index: 999; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = 'comp' # البداية من المطورين
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
        pwd = st.text_input("قفل الدخول", type="password", placeholder="أدخل كلمة المرور")
        if st.button("فتح المنصة 🔓", use_container_width=True):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("❌ الباسورد غير صحيح")
    st.stop()

# --- المنصة بعد الدخول ---
df = load_data()
st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# زر الخروج العائم
st.markdown('<div class="logout-box">', unsafe_allow_html=True)
if st.button("🔒 خروج"): st.session_state.auth = False; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- شريط التنقل (بديل الرئيسية) ---
nav1, nav2 = st.columns(2)
with nav1:
    if st.button("🏢 دليل المطورين", use_container_width=True):
        st.session_state.view = 'comp'; st.session_state.selected_dev = None; st.rerun()
with nav2:
    if st.button("🛠️ أدوات البروكر", use_container_width=True):
        st.session_state.view = 'tools'; st.rerun()

st.write("---")

# --- عرض المحتوى ---
if st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # صفحة التفاصيل
        name = st.session_state.selected_dev
        row = df[df['Developer'] == name].iloc[0]
        if st.button("🔙 العودة للقائمة"): st.session_state.selected_dev = None; st.rerun()
        
        cr, cl = st.columns([1.3, 1])
        with cr:
            st.markdown(f'<div class="custom-card"><h2 class="text-black-bold">👤 {name}</h2><p class="text-black-bold">المالك: {row.get("Owner", "-")}</p><p>{row.get("Description", "-")}</p></div>', unsafe_allow_html=True)
            with st.expander("🏗️ مشاريع الشركة", expanded=True):
                for p in str(row.get("Projects", "-")).split(","):
                    st.markdown(f'<div style="background:#000; color:#fff; padding:10px; margin:5px; border-radius:10px; font-weight:700;">🔹 {p.strip()}</div>', unsafe_allow_html=True)
        with cl:
            st.markdown(f'<div class="custom-card" style="background:#000;"><h3 class="text-white-bold">📊 بيانات السوق</h3><p class="text-white-bold">📍 المناطق: {row.get("Area", "-")}</p><p class="text-white-bold">💰 الأسعار: {row.get("Price", "-")}</p><p class="text-white-bold">📅 التقسيط: {row.get("Installments", "-")}</p></div>', unsafe_allow_html=True)

    else:
        # شبكة المطورين 3*3
        search = st.text_input("🔍 ابحث فوراً عن مطور أو منطقة...", placeholder="اكتب هنا للبحث التفاعلي...")
        dev_list = df['Developer'].unique()
        if search: dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
        
        # توزيع الشبكة
        for i in range(0, len(dev_list), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(dev_list):
                    d_name = dev_list[i+j]
                    with cols[j]:
                        if st.button(d_name, key=f"btn_{d_name}", use_container_width=True):
                            st.session_state.selected_dev = d_name; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<h2 style="text-align:center;" class="text-black-bold">🛠️ حقيبة الأدوات الذكية</h2>', unsafe_allow_html=True)
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="custom-card"><h3 class="text-black-bold">💰 حاسبة القسط السريع</h3>', unsafe_allow_html=True)
        tp = st.number_input("إجمالي السعر", min_value=0, step=100000)
        dp = st.slider("المقدم (%)", 0, 50, 10)
        yr = st.number_input("السنوات", 1, 20, 7)
        if tp > 0:
            val_dp = tp * (dp/100)
            monthly = (tp - val_dp) / (yr * 12)
            st.markdown(f'<div style="background:#000; padding:15px; border-radius:15px; text-align:center;"><h5 class="text-white-bold">المقدم: {val_dp:,.0f}</h5><h3 style="color:#f59e0b; font-weight:900;">القسط: {monthly:,.0f}</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with t2:
        st.markdown('<div class="custom-card"><h3 class="text-black-bold">📈 حاسبة العائد ROI</h3>', unsafe_allow_html=True)
        inv = st.number_input("قيمة الاستثمار", min_value=0, step=100000)
        rent = st.number_input("الإيجار الشهري المتوقع", min_value=0, step=1000)
        if inv > 0 and rent > 0:
            roi = (rent * 12 / inv) * 100
            st.markdown(f'<div style="background:#f59e0b; padding:15px; border-radius:15px; text-align:center;"><h3 class="text-black-bold">العائد السنوي: {roi:.2f}%</h3></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
