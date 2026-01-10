import streamlit as st
import pandas as pd
import io

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (هوية بصرية أسود وذهبي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header {visibility: hidden;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff;
    }
    .main-banner { 
        background: #000; color: #f59e0b; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
    }
    /* الأزرار الكبيرة الرئيسية */
    div.stButton > button[key="btn_devs_home"], div.stButton > button[key="btn_tools_home"] {
        width: 100% !important; height: 220px !important; font-size: 2.2rem !important;
        font-weight: 900 !important; border-radius: 25px !important; border: 4px solid #000 !important;
        box-shadow: 10px 10px 0px #000 !important; transition: 0.3s;
    }
    div.stButton > button[key="btn_devs_home"] { background-color: #f59e0b !important; color: #000 !important; }
    div.stButton > button[key="btn_tools_home"] { background-color: #000 !important; color: #f59e0b !important; }
    
    /* كروت المطورين (Grid) */
    div.stButton > button[key^="grid_"] {
        width: 100% !important; height: 90px !important; background: white !important;
        border: 2px solid #000 !important; border-radius: 12px !important;
        font-weight: 800 !important; box-shadow: 4px 4px 0px #000 !important; margin-bottom: 10px;
    }
    div.stButton > button[key^="grid_"]:hover { border-color: #f59e0b !important; color: #f59e0b !important; }
    
    .stat-card { background: #fdf6e9; padding: 15px; border-radius: 10px; border: 1px solid #f59e0b; text-align: center; }
    .desc-box { background: #f8f9fa; padding: 20px; border-radius: 15px; border-right: 8px solid #000; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. تحميل البيانات (دقة عالية)
@st.cache_data
def get_data():
    csv_data = """Developer,Owner,Projects,Area,Price,Min_Val,Description,Type,Delivery,Installments,Down_Payment,Detailed_Info
Mountain View,عمرو سليمان,iCity,التجمع,8.5M,850K,مجتمعات السعادة,سكني,2027,8,10%,نظام 4D المبتكر وفصل حركة السيارات
Palm Hills,ياسين منصور,Badya,زايد,12M,1.2M,رائد السوق,فاخر,2026,7,10%,أول مدينة مستدامة بالذكاء الاصطناعي
SODIC,سوديك,Villette,التجمع,13M,650K,جودة عالمية,سكني,2025,7,5%,أقوى إدارة مرافق وصيانة في مصر
Emaar Misr,محمد العبار,Mivida,التجمع,18M,900K,فخامة إماراتية,عالمي,2026,8,5%,أعلى عائد استثماري في السوق
Ora Dev,نجيب ساويرس,Zed,زايد,16M,1.6M,رفاهية الأبراج,فاخر,2028,8,10%,تشطيبات فندقية كاملة بالتكييفات
Hassan Allam,حسن علام,Swan Lake,مستقبل,15.5M,775K,قمة الرقي,فاخر,2026,7,5%,المطور المفضل للطبقة الأرستقراطية
Madinet Masr,عبد الله سلام,Sarai,التجمع,7.2M,720K,تاريخ عريق,سكني,2025,8,10%,أكبر لاجون صناعي في القاهرة الجديدة
Tatweer Misr,أحمد شلبي,Bloomfields,مستقبل,9.5M,475K,ابتكار تعليمي,متميز,2027,8,5%,منطقة جامعات دولية داخل الكمبوند
TMG,هشام طلعت,مدينتي,السويس,11M,1.1M,مدن متكاملة,مدينة,2027,10,10%,نظام إدارة ذكية وتحصيل إلكتروني
Nile Dev,محمد طاهر,Nile Towers,العاصمة,5.2M,520K,ملوك الأبراج,تجاري,2028,10,10%,ثالث أعلى ناطحة سحاب في أفريقيا
La Vista,علاء الهادي,LV City,العاصمة,15M,2.2M,فيلات فاخرة,فاخر,2026,6,15%,قوة ملاءة مالية جبارة وبناء ذاتي
LMD,أحمد صبور,One Ninety,التجمع,10.5M,1.05M,تجربة فندقية,متميز,2027,8,10%,يضم فندق W Global ومنطقة تجارية
Misr Italia,عائلة العسال,IL Bosco,العاصمة,6.5M,650K,غابات عمودية,سكني,2026,9,10%,أول مطور يطبق مفهوم الأشجار على المباني
Orascom,سميح ساويرس,O West,أكتوبر,11.5M,575K,مطور الجونة,عالمي,2026,8,5%,روح الجونة في قلب مدينة أكتوبر
PRE,أديب سلامة,The Brooks,التجمع,9.2M,920K,تصاميم هندسية,متميز,2027,8,10%,شلالات مائية ومناظر طبيعية فريدة
Marakez,فواز الحكير,District 5,القطامية,10.8M,1.08M,مولات وسكن,متكامل,2026,8,10%,صاحب مول العرب ويربط التجمع بالسخنة
City Edge,حكومي,North Edge,العلمين,14M,700K,المطور الوطني,فندقي,2025,7,5%,ناطحات سحاب مباشرة على البحر
Hyde Park,ماجد شريف,Hyde Park,التجمع,9M,900K,القلب الأخضر,سكني,2026,8,10%,أكبر نادي رياضي بالقاهرة الجديدة
Inertia,أحمد العدوي,Jefaira,الساحل,7.9M,790K,جيل الشباب,سياحي,2027,8,10%,مدينة ساحلية تعمل طوال العام
Iwan,وليد مختار,The Axis,زايد,8.4M,840K,توازن نفسي,مودرن,2026,8,10%,فلسفة الـ Wellness ومساحات للتأمل
Akam,عصام منصور,Scene 7,العاصمة,5.5M,550K,سكن رياضي,سكني,2026,10,10%,11 أكاديمية رياضية دولية
Taj Misr,مصطفى خليل,De Joya,العاصمة,4.8M,240K,الأكثر مبيعاً,اقتصادي,2026,10,5%,أقل نسبة تحميل في مساحات الشقق
Equity,أحمد السويدي,Waterway,التجمع,13.5M,2.0M,الرفاهية,فاخر,2025,7,15%,البراند رقم 1 في مصر حالياً
New Giza,صلاح دياب,New Giza,أكتوبر,14M,2.1M,الفخامة,فاخر,2025,6,15%,أرقى مجتمع سكني متكامل في أكتوبر
Saudi Egy,شراكة دولية,Jayd,التجمع,9.8M,980K,ثقة دولية,متميز,2026,8,10%,شركة SED العريقة بسابقة أعمال ضخمة"""
    # ملاحظة: تم اختصار البيانات هنا للمثال، ولكن الكود سيقرأ كل ما ترسله.
    return pd.read_csv(io.StringIO(csv_data))

df = get_data()

# إدارة حالة التطبيق
if 'nav' not in st.session_state: st.session_state.nav = "home"
if 'dev_pick' not in st.session_state: st.session_state.dev_pick = None
if 'p_num' not in st.session_state: st.session_state.p_num = 0

# --- 1. صفحة البداية ---
if st.session_state.nav == "home":
    st.markdown('<div class="main-banner"><h1>🚀 منصة معلوماتى العقارية</h1><p>دليلك الشامل للمطورين وأدوات البروكر الذكية</p></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        if st.button("🏢 الشركات\n(Developers)", key="btn_devs_home"):
            st.session_state.nav = "list"; st.rerun()
    with col2:
        if st.button("🛠️ أدوات\nالبروكر", key="btn_tools_home"):
            st.session_state.nav = "tools"; st.rerun()

# --- 2. صفحة قائمة الشركات (Grid) ---
elif st.session_state.nav == "list":
    if st.button("🔙 العودة للرئيسية"): st.session_state.nav = "home"; st.rerun()
    
    st.title("🏢 دليل المطورين العقاريين")
    q = st.text_input("🔍 ابحث عن اسم المطور...", placeholder="مثال: Mountain View, SODIC...")
    
    devs = df['Developer'].unique()
    if q: devs = [d for d in devs if q.lower() in d.lower()]
    
    # شبكة الأزرار
    per_p = 12
    start = st.session_state.p_num * per_p
    subset = devs[start : start+per_p]
    
    for i in range(0, len(subset), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(subset):
                d_name = subset[i+j]
                with cols[j]:
                    if st.button(d_name, key=f"grid_{d_name}"):
                        st.session_state.dev_pick = d_name
                        st.session_state.nav = "details"; st.rerun()
    
    # التنقل
    st.write("---")
    c1, c2, c3 = st.columns([1,2,1])
    if c1.button("⬅️ السابق") and st.session_state.p_num > 0:
        st.session_state.p_num -= 1; st.rerun()
    if c3.button("التالي ➡️") and (start+per_p) < len(devs):
        st.session_state.p_num += 1; st.rerun()

# --- 3. صفحة تفاصيل المطور (Profile) ---
elif st.session_state.nav == "details":
    if st.button("🔙 العودة للقائمة"): st.session_state.nav = "list"; st.rerun()
    
    d = st.session_state.dev_pick
    row = df[df['Developer'] == d].iloc[0]
    
    st.markdown(f"""
        <div class="main-banner">
            <h1>🏢 {d}</h1>
            <p>المالك: <b>{row['Owner']}</b> | التصنيف: <b>{row['Type']}</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    col_a.markdown(f'<div class="stat-card"><h3>📍 المنطقة</h3><p>{row["Area"]}</p></div>', unsafe_allow_html=True)
    col_b.markdown(f'<div class="stat-card"><h3>💰 السعر يبدأ من</h3><p>{row["Price"]}</p></div>', unsafe_allow_html=True)
    col_c.markdown(f'<div class="stat-card"><h3>💳 المقدم</h3><p>{row["Down_Payment"]}</p></div>', unsafe_allow_html=True)
    
    st.markdown(f"""
        <div class="desc-box">
            <h3>📖 نبذة عن المطور ( {row['Description']} )</h3>
            <p>{row['Detailed_Info']}</p>
            <hr>
            <p>🚀 <b>المشروع الأبرز:</b> {row['Projects']}</p>
            <p>⏳ <b>تاريخ الاستلام:</b> {row['Delivery']}</p>
            <p>📅 <b>سنوات التقسيط:</b> {row['Installments']} سنوات</p>
        </div>
    """, unsafe_allow_html=True)

# --- 4. صفحة أدوات البروكر ---
elif st.session_state.nav == "tools":
    if st.button("🔙 العودة للرئيسية"): st.session_state.nav = "home"; st.rerun()
    st.title("🛠️ أدوات البروكر العقاري")
    # حاسبة القسط
    with st.expander("💰 حاسبة القسط السريع", expanded=True):
        p = st.number_input("سعر الوحدة الإجمالي", 1000000)
        d = st.slider("نسبة المقدم %", 0, 50, 10)
        y = st.number_input("سنوات التقسيط", 1, 15, 8)
        down_val = p * (d/100)
        monthly = (p - down_val) / (y * 12)
        st.metric("القسط الشهري", f"{monthly:,.0f} ج.م")
