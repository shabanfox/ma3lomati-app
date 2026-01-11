import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية - الإصدار الشامل", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS المطور (أبيض/أسود/ذهبي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #ffffff;
    }

    /* كارت المطور الذكي */
    .dev-card {
        background: #ffffff; border: 3px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        transition: 0.3s; cursor: pointer; text-align: center;
    }
    .dev-card:hover { transform: translateY(-5px); box-shadow: 10px 10px 0px #f59e0b; }

    /* تفاصيل المشروع الفاخرة */
    .detail-container { background: #000; color: #fff; padding: 30px; border-radius: 30px; border: 4px solid #f59e0b; }
    .gold-title { color: #f59e0b; font-weight: 900; font-size: 2rem; border-bottom: 2px solid #333; padding-bottom: 10px; }
    .info-box { background: #1a1a1a; padding: 15px; border-radius: 15px; border-right: 5px solid #f59e0b; margin: 10px 0; }
    .label-gold { color: #f59e0b; font-weight: 700; font-size: 1.1rem; }
    .val-white { color: #ffffff; font-size: 1.05rem; }

    /* هيدر الدخول */
    .hero-oval-header {
        background: #000000; border: 5px solid #f59e0b; border-top: none; 
        padding: 50px 20px; border-radius: 0px 0px 500px 500px; 
        text-align: center; width: 100%; max-width: 800px; margin: 0 auto 30px auto;
    }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة البيانات (تحميل كافة الأعمدة)
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

# 4. الحماية والدخول
if not st.session_state.auth:
    st.markdown('<div class="hero-oval-header"><h1 style="color:#f59e0b">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    c_a, c_b, c_c = st.columns([1, 1.5, 1])
    with c_b:
        pwd = st.text_input("🔒 الباسورد", type="password")
        if st.button("دخول", use_container_width=True):
            if pwd == "Ma3lomati_2026": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    st.stop()

df = load_data()

# --- التنقل بين الصفحات ---
if st.session_state.view == 'main':
    st.markdown('<div style="background:#000; color:#f59e0b; padding:40px; text-align:center; border-radius:0 0 50px 50px; border-bottom:5px solid #f59e0b;"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("##")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢 دليل المشاريع والمطورين (300+)", use_container_width=True): st.session_state.view = 'comp'; st.rerun()
    with col2:
        if st.button("🛠️ الحاسبة العقارية الذكية", use_container_width=True): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # --- صفحة تفاصيل المشروع والمطور (استخدام كل الأعمدة الجديدة) ---
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        
        st.markdown(f'<div class="detail-container">', unsafe_allow_html=True)
        st.markdown(f'<div class="gold-title">🏗️ {row.get("Project Name", dev_name)}</div>', unsafe_allow_html=True)
        
        if st.button("🔙 العودة للبحث"): st.session_state.selected_dev = None; st.rerun()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
                <div class="info-box"><span class="label-gold">🏢 المطور:</span> <span class="val-white">{row.get('Developer', '-')}</span></div>
                <div class="info-box"><span class="label-gold">👤 المالك:</span> <span class="val-white">{row.get('Owner', row.get('DeveloperOwner', '-'))}</span></div>
                <div class="info-box"><span class="label-gold">📍 المنطقة:</span> <span class="val-white">{row.get('Area', '-')}</span></div>
                <div class="info-box"><span class="label-gold">💰 سعر المتر:</span> <span class="val-white">{row.get('Start Price (sqm)', row.get('Price', '-'))} ج.م</span></div>
                <div class="info-box"><span class="label-gold">📏 المساحة:</span> <span class="val-white">{row.get('Size (Acres)', '-')} فدان</span></div>
            """, unsafe_allow_html=True)
            
        with c2:
            st.markdown(f"""
                <div class="info-box"><span class="label-gold">💵 المقدم:</span> <span class="val-white">{row.get('Down_Payment', '-')}</span></div>
                <div class="info-box"><span class="label-gold">⏳ التقسيط:</span> <span class="val-white">{row.get('Installments', '-')}</span></div>
                <div class="info-box"><span class="label-gold">📅 التسليم:</span> <span class="val-white">{row.get('Delivery', '-')}</span></div>
                <div class="info-box"><span class="label-gold">🏠 نوع الوحدة:</span> <span class="val-white">{row.get('Type', row.get('Unit Type', '-'))}</span></div>
                <div class="info-box"><span class="label-gold">👷 الاستشاري:</span> <span class="val-white">{row.get('Consultant', '-')}</span></div>
            """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class="info-box" style="border-right-color:#fff;">
                <span class="label-gold">🌟 الميزة التنافسية:</span><br>
                <span class="val-white">{row.get('Competitive Advantage', '-')}</span>
            </div>
            <div class="info-box">
                <span class="label-gold">📖 نبذة تفصيلية:</span><br>
                <span class="val-white" style="font-size:0.9rem;">{row.get('Detailed_Info', row.get('Description', 'لا يوجد وصف متاح'))}</span>
            </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    else:
        # --- قائمة المطورين والبحث ---
        st.markdown('<div style="background:#000; color:#f59e0b; padding:20px; text-align:center;"><h2>دليل المشاريع الشامل</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        search = st.text_input("🔍 ابحث باسم المشروع، المطور، أو المنطقة...")
        
        # تصفية البيانات
        filtered_df = df
        if search:
            filtered_df = df[df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
        
        # عرض النتائج في كروت
        devs = filtered_df['Developer'].unique()
        for i in range(0, len(devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(devs):
                    d_name = devs[i+j]
                    # عرض اسم المشروع كعنوان رئيسي في الكارت إذا توفر
                    p_name = filtered_df[filtered_df['Developer'] == d_name]['Project Name'].iloc[0]
                    if cols[j].button(f"🏢 {p_name}\n({d_name})", key=f"btn_{d_name}", use_container_width=True):
                        st.session_state.selected_dev = d_name; st.rerun()

elif st.session_state.view == 'tools':
    # (كود الحاسبة كما هو مع إضافة حاسبة سريعة بناءً على سعر المتر في الشيت)
    st.markdown("## 🛠️ الحاسبة العقارية")
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    # ... (كود الحاسبة)
