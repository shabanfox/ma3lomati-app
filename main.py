import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات النظام
st.set_page_config(page_title="معلوماتى PRO | 2026", layout="wide", initial_sidebar_state="expanded")

# 2. هندسة التصميم (Premium Dark & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية التطبيق والخطوط */
    [data-testid="stAppViewContainer"], [data-testid="stHeader"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    [data-testid="stSidebar"] { background-color: #0a0a0a; border-left: 1px solid #222; }
    
    /* تصميم الكارت المتطور */
    .project-card {
        background: linear-gradient(145deg, #111, #050505);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 25px; margin-bottom: 20px; color: white;
    }
    
    .price-badge { background: #f59e0b; color: black; padding: 4px 12px; border-radius: 6px; font-weight: 900; float: left; }
    .card-header { font-size: 1.4rem; font-weight: 900; color: #f59e0b; margin-bottom: 5px; }
    
    /* شبكة البيانات الصغير داخل الكارت */
    .info-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin: 15px 0; }
    .info-box { background: #1a1a1a; padding: 8px; border-radius: 8px; border: 1px solid #333; text-align: center; }
    .info-label { color: #888; font-size: 11px; display: block; }
    .info-val { color: #eee; font-weight: 700; font-size: 13px; }
    
    /* ستايل الفلاتر */
    .stSelectbox label, .stTextInput label { color: #f59e0b !important; font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. محرك البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

df = load_data()

# 4. القائمة العلوية
selected = option_menu(
    menu_title=None, 
    options=["🏗️ دليل المشاريع", "🏢 سجل المطورين", "🛠️ أدوات البروكر"], 
    icons=["building", "person-vcard", "calculator"], 
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "border-bottom": "2px solid #f59e0b", "padding": "0!important"},
        "nav-link": {"font-size": "16px", "color":"white", "text-align": "center"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- نظام الفلاتر الجانبي (يعمل في كل الصفحات) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/602/602182.png", width=80)
    st.markdown("### 🔍 تصفية النتائج")
    
    # فلتر البحث النصي الشامل
    search_query = st.text_input("بحث بالاسم، المطور، أو الميزة")
    
    # فلاتر التصنيف
    f_area = st.multiselect("📍 المنطقة", options=sorted(df['Area'].dropna().unique()))
    f_type = st.multiselect("🏠 نوع الوحدة", options=sorted(df['Unit Type'].dropna().unique() if 'Unit Type' in df.columns else df['Type'].dropna().unique()))
    f_dev = st.multiselect("🏢 المطور العقاري", options=sorted(df['Developer'].dropna().unique()))
    f_delivery = st.multiselect("📅 سنة التسليم", options=sorted(df['Delivery'].dropna().unique()))

# تطبيق الفلترة على الداتا
dff = df.copy()
if search_query:
    dff = dff[dff.apply(lambda r: search_query.lower() in str(r).lower(), axis=1)]
if f_area: dff = dff[dff['Area'].isin(f_area)]
if f_type: 
    target_col = 'Unit Type' if 'Unit Type' in df.columns else 'Type'
    dff = dff[dff[target_col].isin(f_type)]
if f_dev: dff = dff[dff['Developer'].isin(f_dev)]
if f_delivery: dff = dff[dff['Delivery'].isin(f_delivery)]

# --- العرض بناءً على الاختيار ---
if selected == "🏗️ دليل المشاريع":
    st.markdown(f"<h3 style='color:white;'>تم العثور على ({len(dff)}) مشروع مطابق</h3>", unsafe_allow_html=True)
    
    for _, row in dff.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">يبدأ من: {row.get('Min_Val', row.get('Start Price (sqm)', '-'))}</div>
                <div class="card-header">{row.get('Projects', row.get('Project Name', 'مشروع عقاري'))}</div>
                <div style="color:#888; font-size:14px;">بواسطة: <b style="color:#f59e0b;">{row.get('Developer', '-')}</b> | المالك: {row.get('DeveloperOwner', row.get('Owner', '-'))}</div>
                
                <div class="info-grid">
                    <div class="info-box"><span class="info-label">📍 المنطقة</span><span class="info-val">{row.get('Area', '-')}</span></div>
                    <div class="info-box"><span class="info-label">📐 المساحة (فدان)</span><span class="info-val">{row.get('Size (Acres)', '-')}</span></div>
                    <div class="info-box"><span class="info-label">📅 التسليم</span><span class="info-val">{row.get('Delivery', '-')}</span></div>
                    <div class="info-box"><span class="info-label">📈 نسبة الإشغال</span><span class="info-val">{row.get('Occupancy %', '-')}</span></div>
                </div>

                <div class="info-grid" style="margin-top:0;">
                    <div class="info-box"><span class="info-label">💵 المقدم</span><span class="info-val">{row.get('Down_Payment', '-')}</span></div>
                    <div class="info-box"><span class="info-label">⏳ التقسيط</span><span class="info-val">{row.get('Installments', '-')}</span></div>
                    <div class="info-box"><span class="info-label">👷 الاستشاري</span><span class="info-val">{row.get('Consultant', '-')}</span></div>
                    <div class="info-box"><span class="info-label">🏠 النوع</span><span class="info-val">{row.get('Unit Type', row.get('Type', '-'))}</span></div>
                </div>

                <div style="border-top:1px solid #222; padding-top:15px; margin-top:10px;">
                    <p style="color:#f59e0b; font-size:13px; margin-bottom:5px;"><b>★ الميزة التنافسية:</b></p>
                    <p style="color:#ccc; font-size:14px; line-height:1.4;">{row.get('Competitive Advantage', row.get('Description', '-'))}</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("🔍 قراءة التفاصيل الفنية الكاملة"):
            st.write(row.get('Detailed_Info', 'لا توجد تفاصيل إضافية مسجلة لهذا المشروع.'))

elif selected == "🏢 سجل المطورين":
    dev_info = dff[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
    for _, d_row in dev_info.iterrows():
        st.markdown(f"""
            <div class="project-card" style="border-right-color: #fff;">
                <h2 style="color:#f59e0b; margin:0;">🏢 {d_row['Developer']}</h2>
                <p style="color:#888;"><b>إدارة:</b> {d_row['Owner']}</p>
                <div style="background:#111; padding:15px; border-radius:10px; border:1px solid #222; color:#bbb;">
                    {d_row['Detailed_Info']}
                </div>
            </div>
        """, unsafe_allow_html=True)

elif selected == "🛠️ أدوات البروكر":
    st.info("الأدوات قيد التحديث لربطها ببيانات الأسعار والمساحات تلقائياً.")
