import streamlit as st
import pandas as pd
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (نفس الستايل والخطوط الواضحة اللي طلبتها)
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
    .hero-banner h1 { font-weight: 900; color: #f59e0b !important; font-size: 2.5rem; }
    
    .custom-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
    }
    .card-title { font-size: 1.8rem; font-weight: 900; color: #000; border-bottom: 3px solid #f59e0b; margin-bottom: 15px; }
    .info-row { margin-bottom: 10px; font-size: 1.2rem; }
    .label { font-weight: 900; color: #000; }
    .val { font-weight: 700; color: #f59e0b; }

    div.stButton > button {
        border: 3px solid #000 !important; border-radius: 15px !important;
        box-shadow: 5px 5px 0px #000 !important; font-weight: 900 !important;
        background-color: #fff !important; color: #000 !important;
        font-size: 1.2rem !important;
    }
    div.stButton > button:hover { transform: translate(-2px, -2px); box-shadow: 7px 7px 0px #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 3. البيانات (تم تنظيفها لتجنب الـ Syntax Error)
data_str = """Developer,Owner,Projects,Area,Price,Min_Val,Description,Type,Delivery,Installments,Down_Payment,Detailed_Info
Mountain View,عمرو سليمان,iCity,التجمع,8.5M,850K,مجتمعات السعادة,سكني,2027,8,10%,نظام 4D المبتكر وفصل حركة السيارات
Palm Hills,ياسين منصور,Badya,زايد,12M,1.2M,رائد السوق,فاخر,2026,7,10%,أول مدينة مستدامة بالذكاء الاصطناعي
SODIC,سوديك,Villette,التجمع,13M,650K,جودة عالمية,سكني,2025,7,5%,أقوى إدارة مرافق وصيانة في مصر
Emaar Misr,محمد العبار,Mivida,التجمع,18M,900K,فخامة إماراتية,عالمي,2026,8,5%,أعلى عائد استثماري في السوق
Ora Dev,نجيب ساويرس,Zed,زايد,16M,1.6M,رفاهية الأبراج,فاخر,2028,8,10%,تشطيبات فندقية كاملة بالتكييفات
Hassan Allam,حسن علام,Swan Lake,مستقبل,15.5M,775K,قمة الرقي,فاخر,2026,7,5%,المطور المفضل للطبقة الأرستقراطية
Madinet Masr,عبد الله سلام,Sarai,التجمع,7.2M,720K,تاريخ عريق,سكني,2025,8,10%,أكبر لاجون صناعي
Tatweer Misr,أحمد شلبي,Bloomfields,مستقبل,9.5M,475K,ابتكار تعليمي,متميز,2027,8,5%,منطقة جامعات دولية
TMG,هشام طلعت,مدينتي,السويس,11M,1.1M,مدن متكاملة,مدينة,2027,10,10%,نظام إدارة ذكية كاملة
Nile Dev,محمد طاهر,Nile Towers,العاصمة,5.2M,520K,ملوك الأبراج,تجاري,2028,10,10%,ثالث أعلى ناطحة سحاب
La Vista,علاء الهادي,LV City,العاصمة,15M,2.2M,فيلات فاخرة,فاخر,2026,6,15%,قوة ملاءة مالية جبارة
LMD,أحمد صبور,One Ninety,التجمع,10.5M,1.05M,تجربة فندقية,متميز,2027,8,10%,يضم فندق W Global
Misr Italia,عائلة العسال,IL Bosco,العاصمة,6.5M,650K,غابات عمودية,سكني,2026,9,10%,أول مطور يطبق مفهوم الأشجار"""

@st.cache_data
def load_data():
    return pd.read_csv(io.StringIO(data_str))

df = load_data()

# إدارة التنقل
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page' not in st.session_state: st.session_state.page = 0

# --- الصفحة الرئيسية ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<br><br>", unsafe_allow_html=True)
    _, mid, _ = st.columns([0.1, 0.8, 0.1])
    with mid:
        c1, c2 = st.columns(2, gap="large")
        if c1.button("🏢 دليل المطورين", use_container_width=True): 
            st.session_state.view = 'comp'; st.rerun()
        if c2.button("🛠️ أدوات البروكر", use_container_width=True): 
            st.session_state.view = 'tools'; st.rerun()

# --- صفحة دليل المطورين ---
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.view = 'main'; st.session_state.selected_dev = None; st.rerun()

    if st.session_state.selected_dev:
        # عرض تفاصيل المطور المختار
        item = df[df['Developer'] == st.session_state.selected_dev].iloc[0]
        st.markdown(f"""
            <div class="custom-card">
                <div class="card-title">🏢 {item['Developer']}</div>
                <div class="info-row"><span class="label">👤 المالك:</span> <span class="val">{item['Owner']}</span></div>
                <div class="info-row"><span class="label">🏗️ المشروع:</span> <span class="val">{item['Projects']}</span></div>
                <div class="info-row"><span class="label">📍 المنطقة:</span> <span class="val">{item['Area']}</span></div>
                <div class="info-row"><span class="label">💰 السعر:</span> <span class="val">{item['Price']}</span></div>
                <div class="info-row"><span class="label">💵 المقدم:</span> <span class="val">{item['Down_Payment']}</span></div>
                <div class="info-row"><span class="label">📅 سنوات التقسيط:</span> <span class="val">{item['Installments']}</span></div>
                <div class="info-row"><span class="label">🚚 الاستلام:</span> <span class="val">{item['Delivery']}</span></div>
                <hr>
                <div class="info-row"><span class="label">📝 نبذة:</span> {item['Description']}</div>
                <div class="info-row"><span class="label">💡 تفاصيل:</span> {item['Detailed_Info']}</div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("❌ إغلاق التفاصيل"):
            st.session_state.selected_dev = None; st.rerun()
    else:
        # عرض الشبكة
        search = st.text_input("🔍 ابحث عن المطور...")
        devs = df['Developer'].unique()
        if search: devs = [d for d in devs if search.lower() in d.lower()]
        
        per_page = 12
        start = st.session_state.page * per_page
        current = devs[start : start + per_page]
        
        for i in range(0, len(current), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(current):
                    name = current[i+j]
                    if cols[j].button(name, key=f"d_{name}", use_container_width=True):
                        st.session_state.selected_dev = name; st.rerun()

# --- صفحة الأدوات ---
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    # حاسبة بسيطة
    price = st.number_input("سعر الوحدة", value=1000000)
    down = st.number_input("المقدم %", value=10)
    st.markdown(f'<div class="custom-card"><h3>المقدم المطلوب: {price*(down/100):,.0f} ج.م</h3></div>', unsafe_allow_html=True)
