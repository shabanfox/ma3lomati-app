import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والتصميم الفاخر
st.set_page_config(page_title="Ma3lomati PRO", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
        background-color: #050505; color: white;
    }
    .project-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
    }
    .price-tag {
        background: #f59e0b; color: black; padding: 5px 15px;
        border-radius: 8px; font-weight: 900; font-size: 1.2rem;
    }
    .stat-grid {
        display: flex; justify-content: space-between; gap: 10px; margin: 15px 0;
    }
    .stat-box {
        background: #1a1a1a; padding: 10px; border-radius: 8px;
        text-align: center; flex: 1; border: 1px solid #333;
    }
    .stat-label { color: #888; font-size: 12px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; font-size: 14px; }
    .feature-box {
        background: #151515; padding: 12px; border-radius: 8px;
        border-right: 3px solid #f59e0b; font-size: 14px; margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات (الأعمدة مطابقة تماماً للرابط)
@st.cache_data
def load_data():
    # الرابط المباشر للـ CSV المستخرج من جدولك
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    return df

try:
    df = load_data()
except Exception as e:
    st.error("فشل في تحميل البيانات من الرابط.")
    st.stop()

# 3. محرك البحث والفلاتر
st.title("📊 منصة معلوماتي العقارية PRO")

col_s, col_a = st.columns([3, 1])
with col_s:
    search_query = st.text_input("🔍 ابحث عن مشروع، مطور، أو منطقة...", placeholder="مثال: زد، التجمع، أوراسكوم...")
with col_a:
    # استخدام عمود Area من بياناتك 
    areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
    selected_area = st.selectbox("📍 تصفية بالمنطقة", areas)

# منطق الفلترة
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df.apply(lambda r: search_query.lower() in str(r).lower(), axis=1)]
if selected_area != "الكل":
    filtered_df = filtered_df[filtered_df['Area'] == selected_area]

# 4. عرض الكروت (مطابقة للأعمدة: Developer, Area, Projects, Min_Val, etc.) 
for i in range(0, len(filtered_df), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(filtered_df):
            row = filtered_df.iloc[i + j]
            with cols[j]:
                # بناء الكارت باستخدام أسماء الأعمدة الفعلية من الشيت 
                card_html = f"""
                <div class="project-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h2 style="color:#f59e0b; margin:0;">{row['Developer']}</h2>
                        <span class="price-tag">{row['Min_Val (Start Price)']}</span>
                    </div>
                    <p style="color:#ccc; margin:5px 0;"><b>المشاريع:</b> {row['Projects']}</p>
                    
                    <div class="stat-grid">
                        <div class="stat-box">
                            <span class="stat-label">📍 المنطقة</span>
                            <span class="stat-value">{row['Area']}</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-label">💵 المقدم</span>
                            <span class="stat-value">{row['Down_Payment']}</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-label">⏳ التقسيط</span>
                            <span class="stat-value">{row['Installments']}</span>
                        </div>
                    </div>
                    
                    <div class="feature-box">
                        <p style="margin:0;"><b>🌟 الوصف:</b> {row['Description']}</p>
                        <p style="margin:8px 0 0 0;"><b>🏠 النوع:</b> {row['Type']} | <b>📅 التسليم:</b> {row['Delivery']}</p>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                with st.expander("👁️ عرض التفاصيل الإضافية"):
                    st.write(f"**المالك:** {row['Owner']}")
                    st.write(f"**متوسط سعر المتر:** {row['Price (Meter Avg)']}")
                    st.info(row['Detailed_Info'])
