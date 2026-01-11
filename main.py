import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
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
        border-radius: 8px; font-weight: 900; font-size: 1.1rem;
    }
    .stat-grid { display: flex; justify-content: space-between; gap: 10px; margin: 15px 0; }
    .stat-box { background: #1a1a1a; padding: 10px; border-radius: 8px; text-align: center; flex: 1; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 11px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; font-size: 13px; }
    .feature-box { background: #151515; padding: 12px; border-radius: 8px; border-right: 3px solid #f59e0b; font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات مع تنظيف الأعمدة
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    # تنظيف أسماء الأعمدة من المسافات الزائدة
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("فشل في تحميل البيانات.")
    st.stop()

# 3. واجهة البحث
st.title("📊 منصة معلوماتي العقارية PRO")

# التأكد من وجود عمود Area للفلترة
if 'Area' in df.columns:
    col_s, col_a = st.columns([3, 1])
    with col_s:
        search_query = st.text_input("🔍 ابحث عن (مشروع، مطور، ميزة...)", placeholder="اكتب هنا للبحث...")
    with col_a:
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        selected_area = st.selectbox("📍 المنطقة", areas)
else:
    search_query = st.text_input("🔍 ابحث هنا...")
    selected_area = "الكل"

# منطق الفلترة الشامل
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df.apply(lambda r: search_query.lower() in str(r).lower(), axis=1)]
if selected_area != "الكل":
    filtered_df = filtered_df[filtered_df['Area'] == selected_area]

st.write(f"تم العثور على {len(filtered_df)} نتيجة")

# 4. العرض الآمن (Safe Rendering)
# نستخدم .get() لتجنب خطأ الـ KeyError للأبد
for i in range(0, len(filtered_df), 2):
    cols = st.columns(2)
    for j in range(2):
        if i + j < len(filtered_df):
            row = filtered_df.iloc[i + j]
            with cols[j]:
                card_html = f"""
                <div class="project-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <h3 style="color:#f59e0b; margin:0;">{row.get('Developer', 'مطور غير مسجل')}</h3>
                        <span class="price-tag">{row.get('Min_Val (Start Price)', row.get('Min_Val', '-'))}</span>
                    </div>
                    <p style="color:#ccc; margin:5px 0;"><b>المشاريع:</b> {row.get('Projects', '-')}</p>
                    
                    <div class="stat-grid">
                        <div class="stat-box">
                            <span class="stat-label">📍 المنطقة</span>
                            <span class="stat-value">{row.get('Area', '-')}</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-label">💵 المقدم</span>
                            <span class="stat-value">{row.get('Down_Payment', '-')}</span>
                        </div>
                        <div class="stat-box">
                            <span class="stat-label">⏳ التقسيط</span>
                            <span class="stat-value">{row.get('Installments', '-')}</span>
                        </div>
                    </div>
                    
                    <div class="feature-box">
                        <p style="margin:0;"><b>🌟 الميزة:</b> {row.get('Description', row.get('Competitive Advantage', '-'))}</p>
                        <p style="margin:8px 0 0 0;"><b>🏠 النوع:</b> {row.get('Type', '-')} | <b>📅 التسليم:</b> {row.get('Delivery', '-')}</p>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
                with st.expander("👁️ تفاصيل إضافية"):
                    st.write(f"**المالك:** {row.get('Owner', '-')}")
                    st.write(f"**سعر المتر:** {row.get('Price (Meter Avg)', '-')}")
                    st.info(row.get('Detailed_Info', 'لا توجد تفاصيل إضافية حالياً'))
