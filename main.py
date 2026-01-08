import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Professional Real Estate Radar", layout="wide")

# الرابط الخاص بك
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrbBIxAKkX8ltCSfCTZ7S-E83MPBu4XClC4FLRzvGhZPoHoOgaFOfN2MUm1scyeZRAyT32yxSZy1R2/pub?output=xlsx"

@st.cache_data(ttl=60)
def load_data():
    df = pd.read_excel(SHEET_URL)
    df.columns = df.columns.str.strip()
    return df

# 2. تصميم الخلفية الاحترافية والطبقات (UI Deep Design)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    /* خلفية التطبيق كاملة - تدرج لوني عميق */
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a);
        background-attachment: fixed;
        font-family: 'Cairo', sans-serif;
    }

    /* تحويل الجوانب لشكل شفاف (Glassmorphism) */
    [data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* الكروت الزجاجية الاحترافية */
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 24px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 20px;
        transition: 0.4s all ease;
        color: white;
    }
    .glass-card:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: #38bdf8; /* لون سماوي احترافي */
        transform: translateY(-5px);
    }

    /* تنسيق النصوص */
    .dev-title { color: #38bdf8; font-size: 0.85rem; font-weight: bold; text-transform: uppercase; }
    .project-name { color: #f8fafc; font-size: 1.6rem; font-weight: 700; margin: 8px 0; }
    .price-box {
        background: linear-gradient(90deg, #0ea5e9, #2563eb);
        padding: 8px 16px;
        border-radius: 12px;
        font-weight: bold;
        color: white;
        display: inline-block;
    }
    
    /* تعديل شكل المدخلات لتناسب الخلفية الداكنة */
    .stTextInput input, .stSelectbox div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
    }
    
    h1, h2, h3, p, span, label { color: white !important; }
    </style>
    """, unsafe_allow_html=True)

try:
    df = load_data()

    # --- Sidebar ---
    with st.sidebar:
        st.markdown("<h2 style='text-align:center;'>🔍 الفلاتر الذكية</h2>", unsafe_allow_html=True)
        dev_choice = st.selectbox("المطور العقاري", ["الكل"] + sorted(df['المطور'].unique().tolist()))
        unit_choice = st.multiselect("نوع الوحدة", df['نوع الوحدة'].unique().tolist())
        st.write("---")
        price_in = st.text_input("بحث سريع برقم السعر")

    # --- Main Content ---
    st.markdown("<h1 style='text-align: right; font-size: 3rem;'>رادار المشاريع <span style='color:#38bdf8;'>.</span></h1>", unsafe_allow_html=True)
    
    search_q = st.text_input("🎯 ابحث عن المطور أو اسم المشروع هنا...", placeholder="مثلاً: شركة اعمار، تاج سيتي...")

    # Filtering logic
    f_df = df.copy()
    if dev_choice != "الكل": f_df = f_df[f_df['المطور'] == dev_choice]
    if unit_choice: f_df = f_df[f_df['نوع الوحدة'].isin(unit_choice)]
    if search_q: f_df = f_df[f_df.apply(lambda r: search_q.lower() in str(r).lower(), axis=1)]
    if price_in: f_df = f_df[f_df['السعر'].astype(str).str.contains(price_in)]

    st.markdown(f"**عدد المشاريع المتاحة الآن: {len(f_df)}**")

    # Displaying Grid
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="glass-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div style="text-align: right;">
                        <div class="dev-title">{row['المطور']}</div>
                        <div class="project-name">{row['اسم المشروع']}</div>
                        <div style="color: #94a3b8;">📍 {row['المنطقة']}</div>
                    </div>
                    <div class="price-box">{row['السعر']} ج.م</div>
                </div>
                <div style="display: flex; gap: 40px; margin-top: 25px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.1);">
                    <div>
                        <div style="color: #64748b; font-size: 0.8rem;">نوع الوحدة</div>
                        <div style="font-weight: bold;">{row['نوع الوحدة']}</div>
                    </div>
                    <div>
                        <div style="color: #64748b; font-size: 0.8rem;">نظام السداد</div>
                        <div style="font-weight: bold;">{row['نظام السداد']}</div>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"خطأ: يرجى التأكد من بيانات الشيت. {e}")
