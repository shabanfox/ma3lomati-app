import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الفنية
st.set_page_config(page_title="Ma3lomati PRO | منصة معلوماتي", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (CSS Advanced)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #f8f9fa; color: #1a1a1a;
    }

    /* صفحة الدخول الهندسية */
    .login-container {
        background: #000; border-radius: 0 0 100px 100px;
        padding: 60px 20px; text-align: center; border-bottom: 6px solid #f59e0b;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1); margin-bottom: 40px;
    }
    .login-container h1 { color: #f59e0b; font-weight: 900; font-size: 2.8rem; margin: 0; }

    /* كروت المشاريع الاحترافية */
    .project-card {
        background: white; border-radius: 20px; padding: 25px;
        border: 1px solid #eef0f2; box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        margin-bottom: 25px; position: relative; transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 12px 30px rgba(0,0,0,0.1); border-right: 8px solid #f59e0b; }
    
    .badge-price {
        background: #000; color: #f59e0b; padding: 6px 15px;
        border-radius: 50px; font-weight: 700; font-size: 1.1rem;
        position: absolute; left: 20px; top: 20px;
    }

    .dev-name { color: #888; font-size: 0.9rem; font-weight: 600; margin-bottom: 5px; }
    .proj-name { color: #000; font-size: 1.6rem; font-weight: 900; margin-bottom: 15px; }

    /* شبكة البيانات داخل الكارت */
    .data-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }
    .data-item { background: #fdfdfd; padding: 10px; border-radius: 12px; border: 1px solid #f1f1f1; text-align: center; }
    .data-label { color: #999; font-size: 0.75rem; display: block; }
    .data-value { color: #000; font-weight: 700; font-size: 0.95rem; }

    /* الأزرار الاستراتيجية */
    div.stButton > button {
        border-radius: 12px !important; font-weight: 700 !important;
        transition: 0.3s !important; height: 50px;
    }
    .st-emotion-cache-19rxjzoef { background-color: #f59e0b !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة البيانات
@st.cache_data(ttl=600)
def load_and_fix_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

# 4. منطق الجلسة (Auth & Navigation)
if 'authenticated' not in st.session_state: st.session_state.authenticated = False
if 'page' not in st.session_state: st.session_state.page = 'home'

# --- شاشة الدخول ---
if not st.session_state.authenticated:
    st.markdown('<div class="login-container"><h1>معلوماتى العقارية PRO</h1><p style="color:#ccc;">النظام الذكي لإدارة بيانات السوق</p></div>', unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1, 1.2, 1])
    with col_l2:
        password = st.text_input("ادخل كود الوصول", type="password")
        if st.button("فتح النظام", use_container_width=True):
            if password == "Ma3lomati_2026":
                st.session_state.authenticated = True
                st.rerun()
            else: st.error("عذراً، كود الوصول غير صحيح")
    st.stop()

# --- محرك المنصة ---
df = load_and_fix_data()

# الهيدر العلوي للمنصة
st.markdown(f"""
    <div style="background:#000; padding:20px; border-radius:0 0 30px 30px; margin-bottom:30px; display:flex; justify-content:space-between; align-items:center;">
        <h2 style="color:#f59e0b; margin:0;">🏠 لوحة التحكم</h2>
        <p style="color:white; margin:0;">مرحباً بك في إصدار 2026</p>
    </div>
""", unsafe_allow_html=True)

# الملاحة (Tabs)
tab_home, tab_devs, tab_tools = st.tabs(["🏗️ قاعدة المشاريع", "🏢 دليل المطورين", "📊 الحاسبة والأدوات"])

# --- القسم الأول: المشاريع ---
with tab_home:
    # الفلاتر الذكية
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: search = st.text_input("🔍 بحث شامل...", placeholder="اسم المشروع، مطور، كلمة مفتاحية...")
    with c2: 
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("📍 تصفية بالمنطقة", areas)
    with c3:
        types = ["الكل"] + sorted(df['Type'].dropna().unique().tolist())
        sel_type = st.selectbox("🏠 نوع العقار", types)

    # معالجة الفلترة
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_area != "الكل": dff = dff[dff['Area'] == sel_area]
    if sel_type != "الكل": dff = dff[dff['Type'] == sel_type]

    st.markdown(f"**تم العثور على {len(dff)} مشروع متاح**")

    # عرض الكروت
    for _, row in dff.iterrows():
        st.markdown(f"""
        <div class="project-card">
            <div class="badge-price">{row.get('Min_Val (Start Price)', '-')}</div>
            <div class="dev-name">{row.get('Developer', 'مطور غير مسجل')}</div>
            <div class="proj-name">{row.get('Projects', 'اسم المشروع غير متوفر')}</div>
            
            <div class="data-grid">
                <div class="data-item"><span class="data-label">المنطقة</span><span class="data-value">{row.get('Area', '-')}</span></div>
                <div class="data-item"><span class="data-label">المقدم</span><span class="data-value">{row.get('Down_Payment', '-')}</span></div>
                <div class="data-item"><span class="data-label">التقسيط</span><span class="data-value">{row.get('Installments', '-')}</span></div>
            </div>
            
            <div style="background:#fcfcfc; padding:15px; border-radius:12px; border:1px dashed #ddd;">
                <span style="color:#f59e0b; font-weight:900;">★ الميزة التنافسية:</span><br>
                <span style="font-size:0.9rem; color:#444;">{row.get('Description', 'لا يوجد وصف متاح لهذا المشروع حالياً')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("📄 عرض التفاصيل التقنية وسابقة الأعمال"):
            col_ex1, col_ex2 = st.columns(2)
            with col_ex1:
                st.write(f"**المالك:** {row.get('Owner', '-')}")
                st.write(f"**الاستشاري:** {row.get('Consultant', '-')}")
            with col_ex2:
                st.write(f"**التسليم:** {row.get('Delivery', '-')}")
                st.write(f"**نوع الوحدات:** {row.get('Type', '-')}")
            st.info(row.get('Detailed_Info', 'لا توجد ملاحظات إضافية'))

# --- القسم الثاني: المطورين ---
with tab_devs:
    st.markdown("### 🏢 قاعدة بيانات المطورين العقاريين")
    dev_q = st.text_input("🔍 ابحث عن اسم المطور فقط...")
    
    unique_devs = df.drop_duplicates(subset=['Developer'])
    if dev_q: unique_devs = unique_devs[unique_devs['Developer'].str.contains(dev_q, na=False, case=False)]
    
    for _, dev_row in unique_devs.iterrows():
        with st.expander(f"🏢 {dev_row['Developer']} - سابقة الأعمال"):
            st.markdown(f"#### المالك: {dev_row.get('Owner', 'غير مسجل')}")
            st.write(dev_row.get('Detailed_Info', 'لا توجد معلومات إضافية'))

# --- القسم الثالث: الأدوات ---
with tab_tools:
    st.markdown("### 🛠️ الأدوات الذكية للبروكر")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.subheader("💰 حاسبة الأقساط")
        price = st.number_input("إجمالي سعر الوحدة", min_value=0, step=100000)
        down = st.number_input("المقدم", min_value=0, step=50000)
        years = st.slider("مدة التقسيط (سنوات)", 1, 15, 7)
        if price > 0:
            res = (price - down) / (years * 12)
            st.metric("القسط الشهري", f"{res:,.0f} ج.م")
    with col_t2:
        st.subheader("📈 حاسبة العائد (ROI)")
        inv = st.number_input("إجمالي الاستثمار", min_value=0)
        rent = st.number_input("الإيجار الشهري المتوقع", min_value=0)
        if inv > 0:
            roi = (rent * 12 / inv) * 100
            st.metric("نسبة العائد السنوي", f"{roi:.2f}%")
