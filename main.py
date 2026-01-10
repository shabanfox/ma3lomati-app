import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS الموحد
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
    }
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; border-radius: 15px;
        text-align: center; margin-bottom: 20px; border: 2px solid #f59e0b;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f1f1; border-radius: 10px 10px 0 0; padding: 10px 20px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: white !important; }
    
    /* ستايل قائمة المشاريع داخل المطور */
    .project-box {
        background-color: #f9f9f9; padding: 10px; border-radius: 8_px;
        border-right: 4px solid #f59e0b; margin-bottom: 5px; font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات ومعالجة الأعمدة
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # تحديد الأعمدة: الأول للمشروع، والثاني للمطور (الشركة)
    proj_col = df.columns[0] 
    dev_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    loc_col = df.columns[2] if len(df.columns) > 2 else None

    st.markdown('<div class="main-header"><h1>🚀 منصة معلوماتى: دليل المطورين العقاريين</h1></div>', unsafe_allow_html=True)

    # --- التبويبات ---
    tab_search, tab_tools = st.tabs(["🏢 الشركات والمشاريع", "🛠️ أدوات البروكر"])

    with tab_search:
        col_side, col_main = st.columns([1, 3])

        with col_side:
            st.markdown("### ⚙️ تصفية المطورين")
            # البحث الآن يبحث في اسم المطور واسم المشروع معاً
            search_query = st.text_input("🔍 ابحث عن اسم المطور أو المشروع", placeholder="مثال: اعمار، سيتي إيدج...")
            
            if loc_col:
                all_locs = ["كل المناطق"] + sorted(df[loc_col].dropna().unique().tolist())
                selected_loc = st.selectbox("📍 المنطقة", all_locs)
            else:
                selected_loc = "كل المناطق"

        with col_main:
            # فلترة البيانات
            filtered_df = df.copy()
            
            if search_query:
                filtered_df = filtered_df[
                    filtered_df[dev_col].str.contains(search_query, na=False, case=False) |
                    filtered_df[proj_col].str.contains(search_query, na=False, case=False)
                ]
            
            if selected_loc != "كل المناطق" and loc_col:
                filtered_df = filtered_df[filtered_df[loc_col] == selected_loc]

            # الحصول على أسماء المطورين (الشركات) فقط
            unique_devs = filtered_df[dev_col].dropna().unique()
            st.success(f"✅ تم العثور على {len(unique_devs)} مطور عقاري")

            # عرض النتائج بنظام القوائم
            for dev in unique_devs:
                # العنوان هنا هو اسم المطور (Developer)
                with st.expander(f"🏢 المطور: {dev}"):
                    # عرض المشاريع التابعة لهذا المطور
                    dev_projects = filtered_df[filtered_df[dev_col] == dev][proj_col].unique()
                    for p in dev_projects:
                        st.markdown(f'<div class="project-box">📍 مشروع: {p}</div>', unsafe_allow_html=True)

    with tab_tools:
        st.markdown("### 🛠️ الأدوات الحسابية")
        t_col1, t_col2 = st.columns(2)
        
        with t_col1:
            st.info("💰 حاسبة القسط")
            price = st.number_input("سعر الوحدة", value=1000000)
            down = st.slider("المقدم (%)", 0, 50, 10)
            years = st.number_input("السنوات", 1, 15, 8)
            t_down = price * (down/100)
            monthly = (price - t_down) / (years * 12) if years > 0 else 0
            st.metric("المقدم المطلوب", f"{t_down:,.0f} ج.م")
            st.metric("القسط الشهري", f"{monthly:,.0f} ج.م")

        with t_col2:
            st.info("📈 حاسبة العائد ROI")
            buy = st.number_input("سعر الشراء", value=2000000)
            rent = st.number_input("الإيجار السنوي", value=160000)
            roi = (rent / buy) * 100 if buy > 0 else 0
            st.metric("نسبة العائد الاستثماري", f"{roi:.2f} %")

else:
    st.error("⚠️ لم يتم العثور على بيانات. تأكد من تحديث رابط الـ CSV.")
