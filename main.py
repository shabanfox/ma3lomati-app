import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (البحث التفاعلي واللمسات الاحترافية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* صفحة الدخول البيضاوية */
    .hero-oval-header {
        background: #000; border: 5px solid #f59e0b; border-top: none; 
        padding: 50px 20px; border-radius: 0 0 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 30px auto;
    }
    
    /* ستايل البحث التفاعلي */
    .stTextInput input {
        border: 3px solid #f59e0b !important; border-radius: 20px !important;
        padding: 15px !important; font-size: 1.2rem !important;
        box-shadow: 6px 6px 0px #000 !important;
    }

    .hero-banner { 
        background: #000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }

    .custom-card {
        background: #fff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }

    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    
    .project-item {
        background: #f8f9fa; border-right: 5px solid #f59e0b;
        padding: 10px; margin-bottom: 8px; border-radius: 5px; font-weight: 700;
    }
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
        df.columns = [str(c).strip() for c in df.columns]; return df
    except: return pd.DataFrame()

# 4. شاشة تسجيل الدخول
def login_screen():
    st.markdown('<div class="hero-oval-header"><h1>منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown('<h1 style="text-align:center;">🔒</h1>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.5, 1])
    with c2:
        pwd = st.text_input("رمز الدخول", type="password", placeholder="أدخل الباسورد هنا")
        if st.button("دخول للمنصة", use_container_width=True):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("❌ الرمز غير صحيح")

if not st.session_state.auth:
    login_screen(); st.stop()

# --- المنصة الرئيسية ---
df = load_data()

if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # تفاصيل المطور
        name = st.session_state.selected_dev
        row = df[df['Developer'] == name].iloc[0]
        st.markdown(f'<div class="hero-banner"><h2>{name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة"): st.session_state.selected_dev = None; st.rerun()
        
        cr, cl = st.columns([1.2, 1])
        with cr:
            st.markdown(f'<div class="custom-card"><h3>👤 المالك</h3><p>{row.get("Owner", "-")}</p><h3>📖 الوصف</h3><p>{row.get("Description", "-")}</p></div>', unsafe_allow_html=True)
            with st.expander("🏗️ قائمة المشاريع التفصيلية", expanded=True):
                for p in str(row.get("Projects", "-")).split(","):
                    st.markdown(f'<div class="project-item">🔹 {p.strip()}</div>', unsafe_allow_html=True)
        with cl:
            st.markdown(f'<div class="custom-card"><h3>📊 البيانات</h3><b>📍 المناطق:</b> {row.get("Area", "-")}<br><b>💰 الأسعار:</b> {row.get("Price", "-")}<br><b>💵 المقدم:</b> {row.get("Down_Payment", "-")}<br><b>📅 التقسيط:</b> {row.get("Installments", "-")}</div>', unsafe_allow_html=True)

    else:
        # البحث التفاعلي والتوزيع 70%
        st.markdown('<div class="hero-banner"><h2>🏢 ابحث عن شريك نجاحك</h2></div>', unsafe_allow_html=True)
        col_main, col_filter = st.columns([0.7, 0.3])
        
        with col_filter:
            st.markdown('<div class="custom-card"><h4>🎯 فلاتر سريعة</h4></div>', unsafe_allow_html=True)
            quick_search = st.radio("اختر منطقة (تجريبي):", ["الكل", "التجمع", "زايد", "العاصمة"])
            if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()

        with col_main:
            # محرك البحث التفاعلي
            search_query = st.text_input("🔍 اكتب اسم المطور أو المشروع للبحث الفوري...", placeholder="مثلاً: اعمار، سوديك، ماونتن فيو...")
            
            dev_list = df['Developer'].unique()
            # تصفية تفاعلية للنتائج
            if search_query:
                filtered_devs = [d for d in dev_list if search_query.lower() in str(d).lower()]
            else:
                filtered_devs = dev_list

            st.write(f"تم العثور على ({len(filtered_devs)}) مطور")
            
            # عرض النتائج في شبكة ديناميكية
            for i in range(0, len(filtered_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(filtered_devs):
                        d_name = filtered_devs[i+j]
                        if cols[j].button(d_name, key=f"btn_{d_name}", use_container_width=True):
                            st.session_state.selected_dev = d_name; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ الأدوات الذكية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    t1, t2 = st.columns(2)
    # (حاسبات الأقساط والـ ROI كما هي في الكود السابق)
    with t1:
        st.markdown('<div class="custom-card"><h4>💰 الأقساط</h4></div>', unsafe_allow_html=True)
        # ... (كود الحاسبة)
    with t2:
        st.markdown('<div class="custom-card"><h4>📈 العائد</h4></div>', unsafe_allow_html=True)
        # ... (كود العائد)
