import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (Layout الواسع)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

# الرابط الخاص بك
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrbBIxAKkX8ltCSfCTZ7S-E83MPBu4XClC4FLRzvGhZPoHoOgaFOfN2MUm1scyeZRAyT32yxSZy1R2/pub?output=xlsx"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

# 2. تحسين المظهر بـ CSS (خطوط وألوان براند)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; }
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 10px; }
    .main-title { color: #1E3A8A; font-size: 35px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = load_data()

    # --- Sidebar (لوحة التحكم الجانبية مثل المواقع الكبيرة) ---
    st.sidebar.header("⚙️ أدوات البحث")
    
    # فلتر المطور (مرتب أبجدياً)
    dev_list = ["الكل"] + sorted(df['المطور'].unique().tolist())
    selected_dev = st.sidebar.selectbox("🏗️ اختر المطور العقاري", dev_list)
    
    # فلتر المنطقة
    region_list = ["الكل"] + sorted(df['المنطقة'].unique().tolist())
    selected_region = st.sidebar.selectbox("📍 المنطقة", region_list)
    
    # فلتر نوع الوحدة
    unit_list = ["الكل"] + sorted(df['نوع الوحدة'].unique().tolist())
    selected_unit = st.sidebar.selectbox("🏠 نوع الوحدة", unit_list)

    # --- منطق الفلترة ---
    filtered_df = df.copy()
    if selected_dev != "الكل":
        filtered_df = filtered_df[filtered_df['المطور'] == selected_dev]
    if selected_region != "الكل":
        filtered_df = filtered_df[filtered_df['المنطقة'] == selected_region]
    if selected_unit != "الكل":
        filtered_df = filtered_df[filtered_df['نوع الوحدة'] == selected_unit]

    # --- الواجهة الرئيسية ---
    st.markdown("<div class='main-title'>🏙️ داتا مشاريع القاهرة الجديدة</div>", unsafe_allow_html=True)
    
    # خانة بحث ذكية سريعة فوق الجدول
    search_query = st.text_input("🔍 ابحث عن اسم مشروع محدد...", "")
    if search_query:
        filtered_df = filtered_df[filtered_df['اسم المشروع'].str.contains(search_query, case=False, na=False)]

    # إحصائيات سريعة (Dashboard)
    c1, c2, c3 = st.columns(3)
    c1.metric("عدد المشاريع", len(filtered_df))
    c2.metric("عدد المطورين", len(filtered_df['المطور'].unique()))
    c3.metric("المناطق", len(filtered_df['المنطقة'].unique()))

    # عرض الجدول الاحترافي (Interactive Table)
    # ده بيسمح للبروكر يعمل Sort و Filter من جوه الجدول نفسه زي الإكسيل
    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "السعر": st.column_config.TextColumn("💰 السعر"),
            "اسم المشروع": st.column_config.TextColumn("📌 المشروع"),
            "نظام السداد": st.column_config.TextColumn("💳 نظام السداد")
        }
    )

except Exception as e:
    st.error(f"خطأ في الوصول للبيانات. تأكد من أن ملف جوجل شيت يحتوي على الأعمدة الصحيحة.")
