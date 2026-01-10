import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# تصميم CSS احترافي (عريض وواضح)
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
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        text-align: right;
    }
    .card-title { font-size: 1.8rem; font-weight: 900; color: #f59e0b; border-bottom: 3px solid #000; padding-bottom: 10px; margin-bottom: 15px; }
    .card-label { font-weight: 900; color: #000; font-size: 1.2rem; display: block; margin-top: 10px; }
    .card-val { font-weight: 700; color: #444; font-size: 1.1rem; }
    
    /* ستايل الأزرار */
    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.1rem !important; min-height: 70px !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 6px 6px 0px #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 2. وظيفة جلب البيانات من الرابط (محول إلى صيغة CSV للقراءة)
@st.cache_data(ttl=300) # يحدّث البيانات كل 5 دقائق
def load_data():
    # الرابط الذي أرسلته محول بصيغة تسمح لـ Pandas بقراءتها
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(sheet_url)
        # تنظيف أسماء الأعمدة من أي مسافات
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات من جوجل شيت: {e}")
        return pd.DataFrame()

# تهيئة الحالة
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'view' not in st.session_state: st.session_state.view = 'main'

df = load_data()

# التحقق من وجود الأعمدة المطلوبة
required_cols = ['Developer', 'Owner', 'Projects', 'Description', 'Detailed_Info']

# --- التنقل ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين الشامل", use_container_width=True): 
            st.session_state.view = 'comp'; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر الذكية", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    if st.session_state.selected_dev:
        # --- صفحة التفاصيل العميقة ---
        dev_name = st.session_state.selected_dev
        row = df[df['Developer'] == dev_name].iloc[0]
        
        st.markdown(f'<div class="hero-banner"><h2>{dev_name}</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للقائمة"): 
            st.session_state.selected_dev = None; st.rerun()
            
        col_r, col_l = st.columns([1.2, 1])
        
        with col_r:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">👤 تفاصيل المالك</div>
                    <p class="card-val">{row.get('Owner', 'غير متوفر')}</p>
                    <div class="card-title" style="margin-top:20px;">📖 فلسفة الشركة وقصتها</div>
                    <p class="card-val" style="line-height:1.6;">{row.get('Description', 'لا يوجد وصف')}</p>
                </div>
            """, unsafe_allow_html=True)
            
        with col_l:
            st.markdown(f"""
                <div class="custom-card">
                    <div class="card-title">🏗️ معلومات المشاريع</div>
                    <span class="card-label">📍 المناطق:</span> <span class="card-val">{row.get('Area', '-')}</span>
                    <span class="card-label">💰 الأسعار:</span> <span class="card-val">{row.get('Price', '-')}</span>
                    <span class="card-label">💵 المقدم:</span> <span class="card-val">{row.get('Down_Payment', '-')}</span>
                    <span class="card-label">📅 التقسيط:</span> <span class="card-val">{row.get('Installments', '-')}</span>
                </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">💡 سابقة الأعمال والتفاصيل الفنية</div>
                <p class="card-label" style="color:#f59e0b;">قائمة المشاريع:</p>
                <p class="card-val" style="font-weight:900;">{row.get('Projects', '-')}</p>
                <hr>
                <p class="card-val" style="line-height:1.7; background:#f0f0f0; padding:15px; border-radius:10px;">
                    {row.get('Detailed_Info', 'لا توجد تفاصيل إضافية')}
                </p>
            </div>
        """, unsafe_allow_html=True)

    else:
        # --- قائمة المطورين (شبكة أزرار) ---
        st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        search = st.text_input("🔍 ابحث عن مطور...")
        dev_list = df['Developer'].unique()
        if search:
            dev_list = [d for d in dev_list if search.lower() in str(d).lower()]
            
        cols = st.columns(3)
        for i, dev in enumerate(dev_list):
            with cols[i % 3]:
                if st.button(dev, key=f"btn_{dev}", use_container_width=True):
                    st.session_state.selected_dev = dev
                    st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 الرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.info("سيتم إضافة الحاسبات المتقدمة هنا قريباً")
