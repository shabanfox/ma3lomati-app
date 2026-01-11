import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="معلوماتي العقارية PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (CSS) - اللون الأسود الفخم والذهبي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #050505; color: white;
    }
    
    /* تصميم أزرار التنقل العلوي */
    .nav-container {
        display: flex; justify-content: space-around; background: #111;
        padding: 15px; border-radius: 15px; border: 1px solid #222; margin-bottom: 25px;
    }
    
    /* كروت المشاريع والمطورين */
    .main-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
        transition: 0.3s;
    }
    .main-card:hover { border-color: #f59e0b; transform: translateY(-3px); }

    .price-tag {
        background: #f59e0b; color: #000; padding: 5px 15px;
        border-radius: 8px; font-weight: 900; font-size: 1.2rem;
    }

    .info-grid {
        display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
        gap: 10px; margin: 15px 0;
    }

    .info-item {
        background: #1a1a1a; padding: 10px; border-radius: 8px;
        text-align: center; border: 1px solid #333;
    }

    .info-label { color: #888; font-size: 11px; display: block; }
    .info-value { color: #f59e0b; font-weight: 700; font-size: 13px; }

    .desc-box {
        background: rgba(245, 158, 11, 0.05); padding: 12px;
        border-radius: 8px; border: 1px dashed #f59e0b; font-size: 13px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محرك البيانات المباشر
@st.cache_data(ttl=600)
def get_clean_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip() # تنظيف الأعمدة من أي مسافات مخفية
    return df

try:
    df = get_clean_data()
except:
    st.error("⚠️ خطأ في الاتصال بقاعدة البيانات. تأكد من تحديث الرابط.")
    st.stop()

# 4. إدارة الصفحات (Navigation)
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "🏗️ المشاريع"

# أزرار التنقل الرئيسية
t1, t2, t3 = st.columns(3)
with t1:
    if st.button("🏗️ المشاريع", use_container_width=True): st.session_state.active_tab = "🏗️ المشاريع"
with t2:
    if st.button("🏢 المطورين", use_container_width=True): st.session_state.active_tab = "🏢 المطورين"
with t3:
    if st.button("🛠️ الأدوات", use_container_width=True): st.session_state.active_tab = "🛠️ الأدوات"

st.divider()

# --- صفحة المشاريع ---
if st.session_state.active_tab == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع التفصيلي</h2>", unsafe_allow_html=True)
    
    c1, c2 = st.columns([3, 1])
    with c1: search = st.text_input("🔍 ابحث (اسم، ميزة، استشاري...)", placeholder="اكتب للبحث في 345 نتيجة...")
    with c2: 
        area_list = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("📍 المنطقة", area_list)

    # الفلترة
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_area != "الكل": dff = dff[dff['Area'] == sel_area]

    # العرض
    for _, row in dff.iterrows():
        st.markdown(f"""
        <div class="main-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <h2 style="color:#f59e0b; margin:0;">{row.get('Projects', 'مشروع غير مسمى')}</h2>
                <span class="price-tag">{row.get('Min_Val (Start Price)', '-')}</span>
            </div>
            <p style="color:#888;">المطور: {row.get('Developer', '-')}</p>
            
            <div class="info-grid">
                <div class="info-item"><span class="info-label">📍 المنطقة</span><span class="info-value">{row.get('Area', '-')}</span></div>
                <div class="info-item"><span class="info-label">💵 المقدم</span><span class="info-value">{row.get('Down_Payment', '-')}</span></div>
                <div class="info-item"><span class="info-label">⏳ التقسيط</span><span class="info-value">{row.get('Installments', '-')}</span></div>
                <div class="info-item"><span class="info-label">📅 التسليم</span><span class="info-value">{row.get('Delivery', '-')}</span></div>
            </div>
            
            <div class="desc-box">
                <b>🌟 الميزة التنافسية:</b> {row.get('Description', 'لا يوجد وصف متاح')}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- صفحة المطورين ---
elif st.session_state.active_tab == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b;'>🏢 سجل المطورين وسابقة الأعمال</h2>", unsafe_allow_html=True)
    
    dev_search = st.text_input("🔍 ابحث عن مطور معين...")
    
    dff_dev = df.copy()
    if dev_search: dff_dev = dff_dev[dff_dev['Developer'].str.contains(dev_search, na=False, case=False)]
    
    # عرض المطورين بشكل فريد (Unique Developers)
    unique_devs = dff_dev.drop_duplicates(subset=['Developer'])
    
    for _, row in unique_devs.iterrows():
        st.markdown(f"""
        <div class="main-card">
            <h2 style="color:#f59e0b; margin:0;">{row.get('Developer', '-')}</h2>
            <p style="color:#f59e0b;">👤 المالك: {row.get('Owner', '-')}</p>
            <div style="margin-top:10px; line-height:1.6;">
                <b>📜 سابقة الأعمال والتفاصيل:</b><br>
                {row.get('Detailed_Info', 'لا توجد معلومات إضافية مسجلة')}
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- صفحة الأدوات ---
elif st.session_state.active_tab == "🛠️ الأدوات":
    st.markdown("<h2 style='color:#f59e0b;'>🛠️ أدوات العمل اليومية</h2>", unsafe_allow_html=True)
    
    t_col1, t_col2 = st.columns(2)
    
    with t_col1:
        st.subheader("💰 حاسبة القسط السريع")
        u_price = st.number_input("سعر الوحدة", min_value=0, value=1000000, step=100000)
        u_down = st.number_input("المقدم المدفوع", min_value=0, value=100000, step=10000)
        u_years = st.slider("عدد سنوات التقسيط", 1, 15, 7)
        
        remaining = u_price - u_down
        monthly = remaining / (u_years * 12)
        st.metric("القسط الشهري", f"{monthly:,.0f} ج.م")

    with t_col2:
        st.subheader("📝 مولد عروض واتساب")
        p_name = st.selectbox("اختر المشروع", df['Projects'].dropna().unique())
        p_data = df[df['Projects'] == p_name].iloc[0]
        
        wa_msg = f"🏢 *عرض خاص من معلوماتي العقارية*\n\n" \
                 f"📌 المشروع: {p_name}\n" \
                 f"📍 المنطقة: {p_data['Area']}\n" \
                 f"💰 السعر يبدأ من: {p_data['Min_Val (Start Price)']}\n" \
                 f"💳 المقدم: {p_data['Down_Payment']}\n" \
                 f"⏳ التقسيط: {p_data['Installments']}\n" \
                 f"🌟 المميزات: {p_data['Description']}\n\n" \
                 f"للمعاينة والاستفسار تواصل معنا."
        
        st.text_area("النص الجاهز للنسخ:", wa_msg, height=200)
