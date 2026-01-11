import streamlit as st
import pandas as pd

# 1. إعدادات النظام وتصفير المسافات
st.set_page_config(page_title="Ma3lomati PRO Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (Premium Dark & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #050505; color: white;
    }

    /* تصميم أزرار التنقل العلوية (بديلة للمكتبة المفقودة) */
    .nav-container {
        display: flex; justify-content: center; gap: 20px; 
        padding: 20px; background: #000; border-bottom: 2px solid #f59e0b;
        position: sticky; top: 0; z-index: 999;
    }

    /* كروت المشاريع */
    .project-card {
        background: #111; border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 25px; margin-bottom: 25px;
        transition: 0.4s ease-in-out;
    }
    .project-card:hover { border-color: #f59e0b; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(245, 158, 11, 0.15); }

    /* صناديق المعلومات السريعة */
    .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 20px 0; }
    .stat-item { background: #1a1a1a; padding: 12px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 12px; display: block; margin-bottom: 5px; }
    .stat-value { color: #f59e0b; font-weight: 700; font-size: 14px; }

    /* تفاصيل السعر */
    .price-tag { background: #f59e0b; color: #000; padding: 5px 15px; border-radius: 8px; font-weight: 900; font-size: 1.2rem; }

    /* تخصيص أزرار Streamlit لتناسب التصميم */
    div.stButton > button {
        background-color: #111 !important; color: #f59e0b !important;
        border: 2px solid #f59e0b !important; border-radius: 10px !important;
        font-weight: 900 !important; width: 100% !important; height: 50px !important;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# 3. محرك البيانات (قراءة مباشرة من الرابط الخاص بك)
@st.cache_data(ttl=300)
def load_data():
    # تحويل رابط الـ HTML إلى CSV لقراءة البيانات برمجياً
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال بالبيانات: {e}")
        return pd.DataFrame()

df = load_data()

# 4. إدارة نظام التنقل (Custom Navigation)
if 'page' not in st.session_state: st.session_state.page = "المطورين والمشاريع"

st.markdown('<div class="nav-container">', unsafe_allow_html=True)
col_n1, col_n2 = st.columns(2)
with col_n1:
    if st.button("🏢 دليل المطورين والمشاريع"): st.session_state.page = "المطورين والمشاريع"
with col_n2:
    if st.button("🛠️ أدوات البروكر الذكية"): st.session_state.page = "أدوات البروكر"
st.markdown('</div>', unsafe_allow_html=True)

# --- شاشة المطورين والمشاريع ---
if st.session_state.page == "المطورين والمشاريع":
    st.markdown("<h1 style='text-align:center; color:#f59e0b; margin:20px 0;'>📊 بورصة العقارات المصرية</h1>", unsafe_allow_html=True)
    
    # فلاتر البحث المتقدمة
    with st.container():
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1:
            search = st.text_input("🔍 ابحث عن (مشروع، مطور، أو ميزة تنافسية...)", placeholder="مثال: التجمع، شركة اعمار...")
        with c2:
            areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
            selected_area = st.selectbox("📍 تصفية بالمنطقة", areas)
        with c3:
            types = ["الكل"] + sorted(df['Type'].dropna().unique().tolist())
            selected_type = st.selectbox("🏠 نوع الوحدة", types)

    # معالجة البيانات بناءً على الفلاتر
    dff = df.copy()
    if search:
        dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if selected_area != "الكل":
        dff = dff[dff['Area'] == selected_area]
    if selected_type != "الكل":
        dff = dff[dff['Type'] == selected_type]

    st.markdown(f"<p style='text-align:left; color:#888;'>تم العثور على {len(dff)} نتيجة</p>", unsafe_allow_html=True)

    # عرض المشاريع بنظام الـ Premium Cards
    for i in range(0, len(dff), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(dff):
                row = dff.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="project-card">
                            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                <div>
                                    <h2 style="color:#f59e0b; margin:0;">{row.get('Project Name', 'N/A')}</h2>
                                    <p style="color:#ccc; margin:5px 0;">بواسطة: <b>{row.get('Developer', '-')}</b></p>
                                </div>
                                <div class="price-tag">{row.get('Min_Val', row.get('Start Price (sqm)', '0'))} ج.م</div>
                            </div>
                            
                            <div class="stat-grid">
                                <div class="stat-item"><span class="stat-label">📍 المنطقة</span><span class="stat-value">{row.get('Area', '-')}</span></div>
                                <div class="stat-item"><span class="stat-label">💵 المقدم</span><span class="stat-value">{row.get('Down_Payment', '-')}</span></div>
                                <div class="stat-item"><span class="stat-label">⏳ التقسيط</span><span class="stat-value">{row.get('Installments', '-')}</span></div>
                            </div>

                            <div style="background:#1a1a1a; padding:15px; border-radius:10px; font-size:14px;">
                                <p style="margin:0;"><span style="color:#f59e0b; font-weight:bold;">🌟 الميزة:</span> {row.get('Competitive Advantage', '-')}</p>
                                <p style="margin:10px 0 0 0;"><span style="color:#f59e0b; font-weight:bold;">👷 الاستشاري:</span> {row.get('Consultant', '-')}</p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    # زر التفاصيل باستخدام Streamlit Modal (Expander)
                    with st.expander(f"📖 التفاصيل الكاملة لـ {row.get('Project Name')}"):
                        st.write(f"**المالك:** {row.get('DeveloperOwner', '-')}")
                        st.write(f"**تاريخ التسليم:** {row.get('Delivery', '-')}")
                        st.write(f"**الوصف التفصيلي:**")
                        st.info(row.get('Detailed_Info', row.get('Description', 'لا يوجد وصف إضافي')))

# --- شاشة أدوات البروكر ---
elif st.session_state.page == "أدوات البروكر":
    st.markdown("<h1 style='text-align:center; color:#f59e0b; margin:20px 0;'>🛠️ عُدة المستشار العقاري</h1>", unsafe_allow_html=True)
    
    t1, t2 = st.columns(2)
    with t1:
        st.markdown('<div class="project-card"><h3>💰 حاسبة القسط الذكية</h3>', unsafe_allow_html=True)
        total_price = st.number_input("إجمالي سعر الوحدة (ج.م)", min_value=0, step=100000)
        dp_pct = st.slider("نسبة المقدم (%)", 0, 50, 10)
        years = st.number_input("عدد سنوات التقسيط", 1, 15, 7)
        
        if total_price > 0:
            dp_val = total_price * (dp_pct / 100)
            monthly = (total_price - dp_val) / (years * 12)
            st.markdown(f"""
                <div style='text-align:center; background:#000; padding:20px; border-radius:15px; border:1px solid #f59e0b;'>
                    <p style='color:#888;'>المقدم المطلوب: {dp_val:,.0f} ج.م</p>
                    <h2 style='color:#f59e0b;'>القسط الشهري: {monthly:,.0f} ج.م</h2>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t2:
        st.markdown('<div class="project-card"><h3>📱 مشاركة بيانات مشروع</h3>', unsafe_allow_html=True)
        p_choice = st.selectbox("اختر المشروع", df['Project Name'].unique())
        if st.button("تجهيز نص العرض للواتساب"):
            p_data = df[df['Project Name'] == p_choice].iloc[0]
            wa_text = f"🏢 مشروع: {p_choice}\n📍 المنطقة: {p_data['Area']}\n💰 سعر المتر يبدأ من: {p_data['Min_Val']}\n💳 نظام السداد: {p_data['Down_Payment']} مقدم وتقسيط على {p_data['Installments']}"
            st.text_area("انسخ النص من هنا:", wa_text, height=150)
        st.markdown('</div>', unsafe_allow_html=True)
