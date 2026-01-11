import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وتصفير المسافات
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الشامل (الأبيض الفخم مع لمسات ذهبية وسوداء)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child {
        padding-top: 0rem !important;
    }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #ffffff;
    }

    /* --- تصميم صفحة الدخول --- */
    .login-wrapper { display: flex; flex-direction: column; align-items: center; width: 100%; }
    .hero-oval-header {
        background: #000000; border: 5px solid #f59e0b; border-top: none; 
        padding: 50px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px;
        box-shadow: 0px 15px 30px rgba(0,0,0,0.2); margin-bottom: 30px;
    }
    .hero-oval-header h1 { color: #f59e0b; font-weight: 900; font-size: 2.5rem; margin: 0; }

    /* --- تصميم محتوى المنصة --- */
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 20px; border-radius: 15px; 
        text-align: center; margin-bottom: 25px; border: 3px solid #f59e0b;
    }
    .custom-card {
        background: #ffffff; border: 3px solid #000; padding: 20px; 
        border-radius: 15px; margin-bottom: 15px; box-shadow: 6px 6px 0px #000;
        text-align: right;
    }
    .price-tag { background: #f59e0b; color: #000; padding: 5px 12px; border-radius: 8px; font-weight: 900; float: left; }
    .card-title { font-size: 1.5rem; font-weight: 900; color: #000; margin-bottom: 10px; }
    .stat-label { font-weight: 900; color: #f59e0b; font-size: 1rem; }
    .stat-val { font-weight: 700; color: #333; }

    /* ستايل الأزرار */
    div.stButton > button {
        border: 2px solid #000 !important; border-radius: 12px !important;
        font-weight: 900 !important; background-color: #fff !important; color: #000 !important;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: #000 !important; border-color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الجلسة والبيانات
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

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
    st.write("## 🔒 منطقة الأعضاء")
    col_a, col_b, col_c = st.columns([1, 1.5, 1])
    with col_b:
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للمنصة", use_container_width=True):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("⚠️ كلمة المرور خاطئة")
    st.markdown('</div>', unsafe_allow_html=True)

if not st.session_state.auth:
    login_screen()
    st.stop()

# --- بعد تسجيل الدخول ---
df = load_data()

# شريط الخروج العلوى
if st.sidebar.button("🔒 تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()

# التنقل الرئيسي
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 لوحة التحكم الرئيسية</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("🏗️ دليل المشاريع", use_container_width=True): st.session_state.view = 'projects'; st.rerun()
    with c2:
        if st.button("🏢 سجل المطورين", use_container_width=True): st.session_state.view = 'devs'; st.rerun()
    with c3:
        if st.button("🛠️ الأدوات الذكية", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

# --- صفحة المشاريع (التركيز على الداتا الكاملة) ---
elif st.session_state.view == 'projects':
    st.markdown('<div class="hero-banner"><h2>🏗️ محرك البحث عن المشاريع</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    col_f1, col_f2 = st.columns([3, 1])
    with col_f1: search = st.text_input("🔍 ابحث (اسم، ميزة، مطور...)", placeholder="مثال: زد، التجمع، استلام فوري...")
    with col_f2: 
        area_list = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("📍 المنطقة", area_list)

    # فلترة
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_area != "الكل": dff = dff[dff['Area'] == sel_area]

    st.write(f"تم العثور على {len(dff)} نتيجة")
    
    for _, row in dff.iterrows():
        st.markdown(f"""
        <div class="custom-card">
            <span class="price-tag">{row.get('Min_Val (Start Price)', '-')}</span>
            <div class="card-title">{row.get('Projects', 'اسم المشروع')}</div>
            <p><b>المطور:</b> {row.get('Developer', '-')}</p>
            <hr style="border:1px solid #eee">
            <div style="display: flex; justify-content: space-between;">
                <div><span class="stat-label">📍 المنطقة:</span> <span class="stat-val">{row.get('Area', '-')}</span></div>
                <div><span class="stat-label">💵 المقدم:</span> <span class="stat-val">{row.get('Down_Payment', '-')}</span></div>
                <div><span class="stat-label">⏳ التقسيط:</span> <span class="stat-val">{row.get('Installments', '-')}</span></div>
            </div>
            <div style="margin-top:15px; padding:10px; background:#f9f9f9; border-radius:8px;">
                <b>🌟 الميزة التنافسية:</b> {row.get('Description', row.get('Competitive Advantage', '-'))}
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("👁️ تفاصيل إضافية (الاستشاري، المالك، الوصف)"):
            st.write(f"**المالك:** {row.get('Owner', '-')}")
            st.write(f"**الاستشاري:** {row.get('Consultant', '-')}")
            st.info(row.get('Detailed_Info', 'لا توجد تفاصيل إضافية'))

# --- صفحة المطورين ---
elif st.session_state.view == 'devs':
    st.markdown('<div class="hero-banner"><h2>🏢 سجل المطورين وسابقة الأعمال</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    dev_search = st.text_input("🔍 ابحث عن مطور...")
    unique_devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset='Developer')
    if dev_search: unique_devs = unique_devs[unique_devs['Developer'].str.contains(dev_search, na=False, case=False)]

    for _, row in unique_devs.iterrows():
        with st.expander(f"🏢 {row['Developer']}"):
            st.markdown(f"**المالك:** {row['Owner']}")
            st.markdown(f"**عن الشركة:**")
            st.write(row['Detailed_Info'])

# --- صفحة الأدوات ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ الأدوات والآلات الحاسبة</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📈 حاسبة العائد ROI"])
    with t1:
        tp = st.number_input("إجمالي السعر", min_value=0, value=1000000)
        dp = st.number_input("المقدم المدفوع", min_value=0, value=100000)
        yrs = st.slider("سنوات التقسيط", 1, 15, 7)
        if tp > 0:
            monthly = (tp - dp) / (yrs * 12)
            st.success(f"القسط الشهري: {monthly:,.0f} ج.م")
    with t2:
        inv = st.number_input("قيمة الاستثمار", min_value=0)
        rent = st.number_input("الإيجار الشهري المتوقع", min_value=0)
        if inv > 0:
            roi = (rent * 12 / inv) * 100
            st.warning(f"العائد السنوي المتوقع: {roi:.2f} %")
