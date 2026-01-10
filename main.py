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
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f1f1; border-radius: 10px 10px 0 0; padding: 10px 20px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: white !important; }
    
    /* تصميم صندوق المشروع */
    .project-card {
        background-color: #ffffff; padding: 12px; border-radius: 10px;
        border-right: 5px solid #000; margin-bottom: 8px;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
        font-weight: 700; color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات ومعالجة الأعمدة
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        # تنظيف أسماء الأعمدة من أي مسافات مخفية
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # الربط الديناميكي: العمود الأول هو المشروع، والثاني هو المطور (الشركة)
    proj_col = df.columns[0] 
    dev_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    loc_col = df.columns[2] if len(df.columns) > 2 else None

    st.markdown('<div class="main-header"><h1>🚀 منصة معلوماتى: دليل الشركات العقارية</h1></div>', unsafe_allow_html=True)

    # --- التبويبات الرئيسية ---
    tab_search, tab_tools = st.tabs(["🏢 دليل الشركات والمشاريع", "🛠️ أدوات البروكر"])

    with tab_search:
        col_side, col_main = st.columns([1, 3])

        with col_side:
            st.markdown("### ⚙️ فلترة وتصفية")
            # بحث ذكي يبحث في اسم الشركة أو اسم المشروع
            search_query = st.text_input("🔍 ابحث عن اسم الشركة أو المشروع...", placeholder="مثال: بالم هيلز، مراسي...")
            
            if loc_col:
                all_locs = ["كل المناطق"] + sorted(df[loc_col].dropna().unique().tolist())
                selected_loc = st.selectbox("📍 تصفية بالمنطقة", all_locs)
            else:
                selected_loc = "كل المناطق"

        with col_main:
            # منطق الفلترة
            filtered_df = df.copy()
            
            if search_query:
                # فلترة بناءً على المطور أو المشروع
                filtered_df = filtered_df[
                    filtered_df[dev_col].str.contains(search_query, na=False, case=False) |
                    filtered_df[proj_col].str.contains(search_query, na=False, case=False)
                ]
            
            if selected_loc != "كل المناطق" and loc_col:
                filtered_df = filtered_df[filtered_df[loc_col] == selected_loc]

            # تجميع أسماء الشركات (المطورين) الفريدة
            unique_companies = filtered_df[dev_col].dropna().unique()
            st.info(f"✅ تم العثور على {len(unique_companies)} شركة عقارية")

            # عرض النتائج بنظام الـ Expander
            for company in unique_companies:
                with st.expander(f"🏢 شركة: {company}"):
                    # جلب المشاريع التابعة لهذه الشركة فقط
                    company_projects = filtered_df[filtered_df[dev_col] == company][proj_col].unique()
                    for project in company_projects:
                        st.markdown(f'<div class="project-card">🔹 مشروع: {project}</div>', unsafe_allow_html=True)

    with tab_tools:
        st.markdown("### 🛠️ الحاسبات الذكية")
        t_col1, t_col2 = st.columns(2)
        
        with t_col1:
            st.info("💰 حاسبة القسط الشهري")
            price = st.number_input("سعر الوحدة الإجمالي", value=1000000)
            down = st.slider("نسبة المقدم (%)", 0, 50, 10)
            years = st.number_input("مدة التقسيط (سنوات)", 1, 15, 8)
            t_down = price * (down/100)
            monthly = (price - t_down) / (years * 12) if years > 0 else 0
            st.metric("المقدم النقدي", f"{t_down:,.0f} ج.م")
            st.metric("القسط الشهري", f"{monthly:,.0f} ج.م")

        with t_col2:
            st.info("📈 حاسبة ROI")
            buy = st.number_input("سعر الشراء", value=2000000)
            rent = st.number_input("الإيجار السنوي المتوقع", value=180000)
            roi = (rent / buy) * 100 if buy > 0 else 0
            st.metric("نسبة العائد الاستثماري", f"{roi:.2f} %")

else:
    st.error("⚠️ لم يتم العثور على بيانات. تأكد من أن ملف Google Sheets متاح للعامة (Public).")
