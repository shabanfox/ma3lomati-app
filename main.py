import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu 

# 1. إعدادات النظام
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التصميم الفخم (Black & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    .custom-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 25px; margin-bottom: 20px;
        transition: 0.3s all; color: white;
    }
    .custom-card:hover { border-color: #f59e0b; transform: translateY(-5px); }

    .price-tag {
        background: #f59e0b; color: black; padding: 5px 15px;
        border-radius: 8px; font-weight: 900; font-size: 16px;
    }

    .stat-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 15px 0; }
    .stat-box { background: #1a1a1a; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 12px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_master_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_master_data()

# 4. القائمة العلوية (تم تعديل الترتيب من اليسار إلى اليمين)
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-size": "18px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- 1. شاشة أدوات البروكر ---
if selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات العمل اليومية</h2>", unsafe_allow_html=True)
    
    col_calc, col_msg = st.columns(2)
    with col_calc:
        st.markdown("<div class='custom-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        p = st.number_input("إجمالي السعر", min_value=0, value=1000000)
        d = st.number_input("المقدم", min_value=0, value=100000)
        y = st.slider("السنوات", 1, 15, 7)
        if p > 0:
            st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>{(p-d)/(y*12):,.0f} ج.م/شهر</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_msg:
        st.markdown("<div class='custom-card'><h3>📱 رسالة واتساب</h3>", unsafe_allow_html=True)
        # التأكد من وجود عمود Projects لتجنب الأخطاء
        proj_list = df['Projects'].dropna().unique() if 'Projects' in df.columns else ["لا توجد مشاريع"]
        proj = st.selectbox("اختر المشروع", proj_list)
        if st.button("توليد نص العرض"):
            st.code(f"تحية طيبة.. أرشح لك مشروع {proj} بتفاصيل مميزة...")
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: search_p = st.text_input("🔍 ابحث عن مشروع أو ميزة...")
    with col2: area_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()) if 'Area' in df.columns else ["الكل"])
    with col3: type_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["الكل"])

    dff_p = df.copy()
    if search_p: dff_p = dff_p[dff_p.apply(lambda r: search_p.lower() in str(r).lower(), axis=1)]
    if 'Area' in dff_p.columns and area_p != "الكل": dff_p = dff_p[dff_p['Area'] == area_p]
    if 'Type' in dff_p.columns and type_p != "الكل": dff_p = dff_p[dff_p['Type'] == type_p]

    for _, row in dff_p.iterrows():
        st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between;">
                    <h3 style="color:#f59e0b; margin:0;">{row.get('Projects', 'اسم المشروع')}</h3>
                    <span class="price-tag">{row.get('Min_Val (Start Price)', '0')}</span>
                </div>
                <p style="color:#aaa; margin-bottom:0;">المطور: <b>{row.get('Developer', '-')}</b></p>
                <div class="stat-grid">
                    <div class="stat-box"><span class="stat-label">المنطقة</span><span class="stat-value">{row.get('Area', '-')}</span></div>
                    <div class="stat-box"><span class="stat-label">المقدم</span><span class="stat-value">{row.get('Down_Payment', '-')}</span></div>
                    <div class="stat-box"><span class="stat-label">التقسيط</span><span class="stat-value">{row.get('Installments', '-')}</span></div>
                </div>
                <div style="color:#ccc; font-size:14px; border-top:1px solid #222; padding-top:10px;">
                    <b>💡 الميزة:</b> {row.get('Description', '-')}
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 3. شاشة المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    search_d = st.text_input("🔍 ابحث عن اسم المطور أو المالك...")
    
    if not df.empty and 'Developer' in df.columns:
        # استخراج داتا المطورين فقط (بدون تكرار)
        subset_cols = [c for c in ['Developer', 'Owner', 'Detailed_Info'] if c in df.columns]
        dev_df = df[subset_cols].drop_duplicates(subset=['Developer'])
        
        if search_d:
            dev_df = dev_df[dev_df.apply(lambda r: search_d.lower() in str(r).lower(), axis=1)]

        for _, row in dev_df.iterrows():
            st.markdown(f"""
                <div class="custom-card" style="border-right-color: #fff;">
                    <h3 style="color:#f59e0b; margin:0;">🏢 {row.get('Developer', '-')}</h3>
                    <p style="color:#eee; margin-top:10px;">👤 <b>المالك:</b> {row.get('Owner', '-')}</p>
                    <div style="background:#1a1a1a; padding:15px; border-radius:10px; color:#bbb; font-size:14px; line-height:1.6;">
                        <b>📖 سابقة الأعمال والتفاصيل:</b><br>
                        {row.get('Detailed_Info', 'لا توجد تفاصيل إضافية مسجلة')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("لم يتم العثور على بيانات المطورين في الملف.")
