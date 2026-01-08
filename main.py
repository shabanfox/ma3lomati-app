import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الفاخرة
st.set_page_config(
    page_title="Luxury Real Estate Radar",
    layout="wide",
    initial_sidebar_state="expanded"
)

# رابط البيانات الخاص بك
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrbBIxAKkX8ltCSfCTZ7S-E83MPBu4XClC4FLRzvGhZPoHoOgaFOfN2MUm1scyeZRAyT32yxSZy1R2/pub?output=xlsx"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

# 2. تصميم الواجهة بهوية بصرية قوية (Navy, Gold, and White)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* الخطوط والخلفية العامة */
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        background-color: #f8f9fa;
    }
    
    /* تخصيص الـ Sidebar */
    [data-testid="stSidebar"] {
        background-color: #001e3c;
        color: white;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* تصميم الكروت الحديثة */
    .stat-card {
        background: white;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border-top: 4px solid #c5a059; /* لون ذهبي هادئ */
        text-align: center;
    }
    
    .project-row {
        background: white;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        border-right: 5px solid #001e3c;
        transition: 0.3s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .project-row:hover {
        transform: scale(1.01);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .price-badge {
        background-color: #e3f2fd;
        color: #0d47a1;
        padding: 5px 12px;
        border-radius: 8px;
        font-weight: bold;
        font-size: 0.9em;
    }
    
    /* إخفاء القوائم غير الضرورية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

try:
    df = load_data()

    # --- Sidebar (الفلاتر الاحترافية) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/602/602275.png", width=80) # أيقونة تعبيرية
        st.title("البحث المتقدم")
        st.markdown("---")
        
        selected_dev = st.selectbox("🏗️ المطور العقاري", ["الكل"] + sorted(df['المطور'].unique().tolist()))
        selected_unit = st.multiselect("🏠 نوع الوحدة", df['نوع الوحدة'].unique().tolist())
        selected_region = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['المنطقة'].unique().tolist()))
        
        st.markdown("---")
        price_limit = st.text_input("🔍 بحث برقم السعر (مثلاً: 5,000,000)", "")

    # --- منطق الفلترة ---
    f_df = df.copy()
    if selected_dev != "الكل": f_df = f_df[f_df['المطور'] == selected_dev]
    if selected_unit: f_df = f_df[f_df['نوع الوحدة'].isin(selected_unit)]
    if selected_region != "الكل": f_df = f_df[f_df['المنطقة'] == selected_region]
    if price_limit: f_df = f_df[f_df['السعر'].astype(str).str.contains(price_limit)]

    # --- العرض الرئيسي (The Main Board) ---
    st.markdown("<h1 style='color: #001e3c;'>Dashboard | لوحة تحكم القاهرة الجديدة</h1>", unsafe_allow_html=True)
    
    # صف الإحصائيات (KPIs)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="stat-card"><small>إجمالي المشاريع</small><h2>{len(f_df)}</h2></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="stat-card"><small>المطورين</small><h2>{len(f_df["المطور"].unique())}</h2></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="stat-card"><small>المناطق</small><h2>{len(f_df["المنطقة"].unique())}</h2></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="stat-card"><small>متوسط الأسعار</small><h4>تحليل لحظي</h4></div>', unsafe_allow_html=True)

    st.write("### 📝 قائمة المشاريع التفصيلية")
    
    # البحث السريع باسم المشروع
    quick_search = st.text_input("🎯 ابحث عن مشروع محدد مباشرة بالاسم...", placeholder="مثلاً: زيد، ميفيدا، هايد بارك...")
    if quick_search:
        f_df = f_df[f_df['اسم المشروع'].str.contains(quick_search, case=False, na=False)]

    # عرض البيانات بنظام الـ Rows الأنيق
    for _, row in f_df.iterrows():
        with st.container():
            st.markdown(f"""
                <div class="project-row">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="text-align: right;">
                            <h3 style="margin:0; color:#001e3c;">{row['اسم المشروع']}</h3>
                            <p style="margin:0; color:#666;">شركة {row['المطور']} | {row['المنطقة']}</p>
                        </div>
                        <div style="text-align: left;">
                            <span class="price-badge">{row['السعر']} ج.م</span>
                        </div>
                    </div>
                    <div style="margin-top: 10px; display: flex; gap: 20px; font-size: 14px;">
                        <span><b>نوع الوحدة:</b> {row['نوع الوحدة']}</span>
                        <span><b>نظام السداد:</b> {row['نظام السداد']}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ يرجى التأكد من أسماء الأعمدة في ملف الإكسيل: {e}")
