import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS الموحد (أسود وذهبي)
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
    /* تصميم صندوق المشاريع داخل المطور */
    .project-card {
        background-color: #f9f9f9; padding: 10px; border-radius: 8px;
        border-right: 4px solid #f59e0b; margin-bottom: 5px; font-weight: 700;
    }
    .stExpander { border: 1px solid #ddd !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات ومعالجة أسماء الأعمدة
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        # تنظيف الفراغات من أسماء الأعمدة
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # تحديد الأعمدة بناءً على الترتيب في ملفك (الأول مشروع والثاني مطور)
    proj_col = df.columns[0] # Project
    dev_col = df.columns[1]  # Developer
    loc_col = df.columns[2] if len(df.columns) > 2 else None

    st.markdown('<div class="main-header"><h1>🚀 منصة معلوماتى: دليل المطورين والمشاريع</h1></div>', unsafe_allow_html=True)

    # --- التبويبات ---
    tab_search, tab_tools = st.tabs(["🔍 دليل المطورين", "🛠️ أدوات البروكر"])

    with tab_search:
        col_side, col_main = st.columns([1, 3])

        with col_side:
            st.markdown("### ⚙️ فلاتر البحث")
            search_query = st.text_input("🔍 ابحث باسم المطور أو المشروع", placeholder="مثال: اعمار، بالم هيلز...")
            
            if loc_col:
                all_locs = ["كل المناطق"] + sorted(df[loc_col].dropna().unique().tolist())
                selected_loc = st.selectbox("📍 المنطقة", all_locs)
            else:
                selected_loc = "كل المناطق"

        with col_main:
            # منطق الفلترة
            filtered_df = df.copy()
            
            if search_query:
                filtered_df = filtered_df[
                    filtered_df[dev_col].str.contains(search_query, na=False, case=False) |
                    filtered_df[proj_col].str.contains(search_query, na=False, case=False)
                ]
            
            if selected_loc != "كل المناطق" and loc_col:
                filtered_df = filtered_df[filtered_df[loc_col] == selected_loc]

            # جلب أسماء المطورين الفريدة (Developer)
            unique_devs = filtered_df[dev_col].dropna().unique()
            st.success(f"✅ تم العثور على {len(unique_devs)} مطور عقاري")

            # عرض النتائج
            for dev in unique_devs:
                # هنا قمنا بتغيير العرض ليكون اسم المطور (Developer) هو العنوان
                with st.expander(f"🏢 المطور: {dev}"):
                    # عرض المشاريع الخاصة بهذا المطور فقط
                    dev_projects = filtered_df[filtered_df[dev_col] == dev][proj_col].unique()
                    for p in dev_projects:
                        st.markdown(f'<div class="project-card">📍 مشروع: {p}</div>', unsafe_allow_html=True)

    with tab_tools:
        # تبويب الأدوات كما هو
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
            st.metric("نسبة العائد", f"{roi:.2f} %")

else:
    st.error("⚠️ فشل في تحميل البيانات، تأكد من أن الملف منشور للويب بصيغة CSV.")
