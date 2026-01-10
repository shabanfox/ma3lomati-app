import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS احترافي (أسود وذهبي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #fdfdfd;
    }
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; border-radius: 15px;
        text-align: center; margin-bottom: 25px; border-bottom: 5px solid #f59e0b;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    .stExpander { border: 2px solid #eee !important; border-radius: 10px !important; margin-bottom: 10px !important; background: white !important; }
    .project-item { background: #f9f9f9; padding: 10px; border-radius: 8px; border-right: 5px solid #f59e0b; margin: 5px 0; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات ومعالجتها
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
    # تحديد الأعمدة بناءً على هيكلة ملفك (الأول مشروع، الثاني مطور/شركة)
    proj_col = df.columns[0] 
    dev_col = df.columns[1] if len(df.columns) > 1 else df.columns[0]
    loc_col = df.columns[2] if len(df.columns) > 2 else None

    st.markdown('<div class="main-header"><h1>🏢 منصة معلوماتى: دليل الشركات العقارية</h1></div>', unsafe_allow_html=True)

    # --- التبويبات ---
    tab_search, tab_tools = st.tabs(["🔍 الشركات والمشاريع", "🛠️ أدوات البروكر"])

    with tab_search:
        col_side, col_main = st.columns([1, 3])

        with col_side:
            st.markdown("### ⚙️ فلاتر ذكية")
            search_query = st.text_input("🔍 ابحث عن اسم الشركة أو المشروع", placeholder="اكتب هنا...")
            
            if loc_col:
                all_locs = ["كل المناطق"] + sorted(df[loc_col].dropna().unique().tolist())
                selected_loc = st.selectbox("📍 تصفية حسب المنطقة", all_locs)
            else:
                selected_loc = "كل المناطق"

        with col_main:
            # معالجة الفلترة
            filtered_df = df.copy()
            
            if search_query:
                mask = (filtered_df[dev_col].str.contains(search_query, na=False, case=False)) | \
                       (filtered_df[proj_col].str.contains(search_query, na=False, case=False))
                filtered_df = filtered_df[mask]
            
            if selected_loc != "كل المناطق" and loc_col:
                filtered_df = filtered_df[filtered_df[loc_col] == selected_loc]

            # قائمة الشركات الفريدة
            unique_companies = filtered_df[dev_col].dropna().unique()
            st.info(f"📍 تم العثور على {len(unique_companies)} شركة عقارية")

            # عرض النتائج
            for company in unique_companies:
                with st.expander(f"🏢 شركة: {company}"):
                    company_projects = filtered_df[filtered_df[dev_col] == company][proj_col].unique()
                    for p in company_projects:
                        st.markdown(f'<div class="project-item">🔹 مشروع: {p}</div>', unsafe_allow_html=True)

    with tab_tools:
        # (تبويب الأدوات كما هو منظم سابقاً)
        st.markdown("### 🛠️ الأدوات الذكية")
        t1, t2 = st.columns(2)
        with t1:
            st.info("💰 حاسبة التمويل")
            pr = st.number_input("سعر الوحدة", value=1000000)
            dn = st.slider("المقدم (%)", 0, 50, 10)
            yr = st.number_input("السنوات", 1, 15, 8)
            res_dn = pr * (dn/100)
            res_mo = (pr - res_dn) / (yr * 12) if yr > 0 else 0
            st.metric("المقدم", f"{res_dn:,.0f} ج.م")
            st.metric("القسط الشهري", f"{res_mo:,.0f} ج.م")
        
        with t2:
            st.info("📈 حاسبة العائد")
            inv = st.number_input("مبلغ الاستثمار", value=2000000)
            rnt = st.number_input("الإيجار السنوي", value=180000)
            roi = (rnt / inv) * 100 if inv > 0 else 0
            st.metric("نسبة ROI", f"{roi:.2f} %")

else:
    st.error("⚠️ فشل في تحميل البيانات. يرجى التأكد من رابط ملف الـ CSV.")
