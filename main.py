import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الموحد (خطوط عريضة وألوان واضحة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }
    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .hero-banner h1, .hero-banner h2 { font-weight: 900; color: #f59e0b !important; margin: 0; }
    
    /* ستايل الكروت الموحد */
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        text-align: right; transition: 0.3s;
    }
    .card-title { font-size: 1.8rem; font-weight: 900; color: #000; border-bottom: 3px solid #f59e0b; padding-bottom: 10px; margin-bottom: 15px; }
    .card-label { font-weight: 900; color: #000; font-size: 1.2rem; }
    .card-val { font-weight: 700; color: #f59e0b; font-size: 1.2rem; }

    /* أزرار المطورين */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 5px 5px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 80px !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 7px 7px 0px #f59e0b !important; border-color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات من Google Sheets (الرابط الذي أرسلته)
@st.cache_data(ttl=600)
def load_data():
    # الرابط بصيغة CSV لسهولة القراءة
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        # تنظيف أسماء الأعمدة من أي مسافات زائدة
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

# تهيئة الحالة (Session State)
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page' not in st.session_state: st.session_state.page = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

df = load_data()

# --- الصفحة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<div style='height:60px;'></div>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([0.1, 0.8, 0.1])
    with mid_col:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            if st.button("🏢\nدليل المطورين", use_container_width=True): 
                st.session_state.view = 'comp'
                st.rerun()
        with c2:
            if st.button("🛠️\nأدوات البروكر", use_container_width=True): 
                st.session_state.view = 'tools'
                st.rerun()

# --- صفحة دليل المطورين ---
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    
    if st.button("🔙 عودة للرئيسية"): 
        st.session_state.view = 'main'
        st.session_state.selected_dev = None
        st.session_state.page = 0
        st.rerun()
    
    # إذا تم اختيار مطور معين، اعرض تفاصيله
    if st.session_state.selected_dev:
        dev_row = df[df['Developer'] == st.session_state.selected_dev].iloc[0]
        
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">🏢 {dev_row['Developer']}</div>
                <p class="card-label">👤 المالك: <span class="card-val">{dev_row.get('Owner', 'غير متوفر')}</span></p>
                <p class="card-label">🏗️ المشروع الأبرز: <span class="card-val">{dev_row.get('Projects', 'غير متوفر')}</span></p>
                <p class="card-label">📍 المنطقة: <span class="card-val">{dev_row.get('Area', 'غير متوفر')}</span></p>
                <p class="card-label">💰 السعر: <span class="card-val">{dev_row.get('Price', 'غير متوفر')}</span></p>
                <p class="card-label">💵 المقدم: <span class="card-val">{dev_row.get('Down_Payment', 'غير متوفر')}</span></p>
                <p class="card-label">📅 التقسيط: <span class="card-val">{dev_row.get('Installments', 'غير متوفر')} سنوات</span></p>
                <hr>
                <p class="card-label">📝 نبذة:</p>
                <p style="font-size:1.1rem; font-weight:700;">{dev_row.get('Description', '')}</p>
                <p class="card-label">💡 تفاصيل إضافية:</p>
                <p style="font-size:1.1rem; color:#444; font-weight:700;">{dev_row.get('Detailed_Info', '')}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("❌ إغلاق التفاصيل والعودة"):
            st.session_state.selected_dev = None
            st.rerun()
            
    else:
        # عرض قائمة المطورين (شبكة أزرار)
        search = st.text_input("🔍 ابحث عن اسم المطور...", placeholder="اكتب اسم الشركة هنا...")
        
        unique_devs = df['Developer'].dropna().unique()
        if search:
            unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

        items_per_page = 12
        start_idx = st.session_state.page * items_per_page
        current_devs = unique_devs[start_idx : start_idx + items_per_page]

        # إنشاء الشبكة (Grid)
        for i in range(0, len(current_devs), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    dev_name = current_devs[i + j]
                    with grid_cols[j]:
                        if st.button(dev_name, key=f"btn_{dev_name}", use_container_width=True):
                            st.session_state.selected_dev = dev_name
                            st.rerun()

        # أزرار التنقل بين الصفحات
        st.write("---")
        nav_prev, nav_next = st.columns([1, 1])
        with nav_prev:
            if st.session_state.page > 0:
                if st.button("⬅️ السابق"): st.session_state.page -= 1; st.rerun()
        with nav_next:
            if (start_idx + items_per_page) < len(unique_devs):
                if st.button("التالي ➡️"): st.session_state.page += 1; st.rerun()

# --- صفحة الأدوات ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر الذكية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    # حاسبة القسط في بطاقة أنيقة
    st.write("### 💰 حاسبة الأقساط السريعة")
    c1, c2, c3 = st.columns(3)
    with c1: price = st.number_input("سعر الوحدة", value=1000000, step=100000)
    with c2: down_p = st.number_input("المقدم %", value=10)
    with c3: yrs = st.number_input("السنوات", value=8)
    
    dn_val = price * (down_p/100)
    mo_val = (price - dn_val) / (yrs * 12) if yrs > 0 else 0
    
    st.markdown(f"""
        <div class="custom-card" style="text-align:center;">
            <div class="card-label">كاش المقدم المطلوب</div>
            <div class="card-val" style="font-size:2.5rem;">{dn_val:,.0f} ج.م</div>
            <hr>
            <div class="card-label">القسط الشهري المتوقع</div>
            <div class="card-val" style="font-size:2.5rem; color:#22c55e;">{mo_val:,.0f} ج.م</div>
        </div>
    """, unsafe_allow_html=True)
