import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. CSS احترافي للوظائف الجديدة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
    }
    .main-header {
        background: linear-gradient(90deg, #000000, #1a1a1a);
        color: #f59e0b; padding: 20px; border-radius: 15px;
        text-align: center; margin-bottom: 20px; border-bottom: 5px solid #f59e0b;
    }
    /* ستايل الفلاتر */
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-left: 1px solid #ddd; }
    
    /* أزرار مدمجة للنتائج */
    div.stButton > button {
        width: 100% !important; border-radius: 10px !important;
        border: 2px solid #000 !important; font-weight: 700 !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Developer', 'Project', 'Location'])

df = load_data()

# --- الهيدر الرئيسي ---
st.markdown('<div class="main-header"><h1>🚀 منصة معلوماتى العقارية الذكية</h1></div>', unsafe_allow_html=True)

# --- نظام التبويبات (Tabs) لدمج كل شيء ---
tab_devs, tab_tools, tab_search = st.tabs(["🏢 دليل المطورين والمشاريع", "🛠️ أدوات البروكر", "🔍 البحث المتقدم"])

# --- 1. تبويب المطورين ---
with tab_devs:
    col_filter, col_display = st.columns([1, 3])
    
    with col_filter:
        st.subheader("⚙️ فلاتر سريعة")
        search_dev = st.text_input("اسم المطور", placeholder="مثال: اعمار...")
        # إذا كان لديك عمود للمناطق في الداتا
        location_list = df['Location'].unique() if 'Location' in df.columns else ["كل المناطق"]
        selected_loc = st.selectbox("المنطقة", location_list)
        
    with col_display:
        filtered_df = df.copy()
        if search_dev:
            filtered_df = filtered_df[filtered_df['Developer'].str.contains(search_dev, na=False, case=False)]
        
        devs = filtered_df['Developer'].unique()
        st.write(f"✅ تم العثور على {len(devs)} مطور")
        
        for dev in devs[:12]: # عرض أول 12 كمثال
            with st.expander(f"🏢 {dev}"):
                projects = df[df['Developer'] == dev]['Project'].unique()
                for p in projects:
                    st.write(f"🔹 {p}")

# --- 2. تبويب الأدوات (في مكانها الصحيح) ---
with tab_tools:
    st.subheader("🧮 الحاسبات التمويلية")
    c1, c2 = st.columns(2)
    
    with c1:
        st.info("💰 حاسبة الأقساط")
        p = st.number_input("سعر الوحدة", value=1000000, step=100000)
        d = st.slider("المقدم (%)", 0, 50, 10)
        y = st.number_input("السنوات", 1, 20, 8)
        
        down_val = p * (d/100)
        monthly = (p - down_val) / (y * 12)
        st.success(f"المقدم: {down_val:,.0f} | القسط: {monthly:,.0f}")

    with c2:
        st.info("📈 حاسبة العائد ROI")
        buy = st.number_input("سعر الشراء", value=2000000)
        rent = st.number_input("الإيجار السنوي المتوقع", value=150000)
        roi = (rent / buy) * 100
        st.warning(f"نسبة العائد السنوي: {roi:.2f}%")

# --- 3. تبويب البحث المتقدم ---
with tab_search:
    st.subheader("🔎 ابحث عن أي مشروع مباشرة")
    search_query = st.text_input("اكتب اسم المشروع أو المطور هنا...", key="global_search")
    
    if search_query:
        results = df[df.apply(lambda row: search_query.lower() in row.astype(str).str.lower().values, axis=1)]
        st.dataframe(results, use_container_width=True)
