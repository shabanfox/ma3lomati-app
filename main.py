import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التصميم (CSS) - تأكد أنه داخل st.markdown
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #050505; color: white;
    }
    .project-card {
        background: #111; border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
    }
    .stat-grid {
        display: flex; justify-content: space-between; gap: 10px; margin: 15px 0;
    }
    .stat-item {
        background: #1a1a1a; padding: 10px; border-radius: 8px; text-align: center; flex: 1; border: 1px solid #333;
    }
    .stat-label { color: #888; font-size: 11px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; font-size: 13px; }
    .price-tag { background: #f59e0b; color: #000; padding: 5px 12px; border-radius: 6px; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    return df

df = load_data()

# 4. الملاحة
if 'page' not in st.session_state: st.session_state.page = "database"

col_n1, col_n2 = st.columns(2)
with col_n1:
    if st.button("🏢 دليل المشاريع"): st.session_state.page = "database"
with col_n2:
    if st.button("🛠️ أدوات البروكر"): st.session_state.page = "tools"

# --- شاشة قاعدة البيانات ---
if st.session_state.page == "database":
    st.title("📊 محرك البحث العقاري")
    
    # الفلاتر
    f1, f2 = st.columns([3, 1])
    with f1: search = st.text_input("🔍 ابحث هنا...")
    with f2: area = st.selectbox("📍 المنطقة", ["الكل"] + list(df['Area'].unique()))

    # تصفية
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if area != "الكل": dff = dff[dff['Area'] == area]

    # العرض (هنا حل مشكلة ظهور الأكواد)
    for i in range(0, len(dff), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(dff):
                row = dff.iloc[i + j]
                with cols[j]:
                    # استخدام f-string داخل st.markdown واحد لكل كارت
                    card_html = f"""
                    <div class="project-card">
                        <div style="display: flex; justify-content: space-between;">
                            <h3 style="margin:0; color:#f59e0b;">{row['Project Name']}</h3>
                            <span class="price-tag">{row.get('Min_Val', 'N/A')}</span>
                        </div>
                        <p style="color:#888;">بواسطة: {row.get('Developer', '-')}</p>
                        
                        <div class="stat-grid">
                            <div class="stat-item"><span class="stat-label">📍 المنطقة</span><span class="stat-value">{row.get('Area', '-')}</span></div>
                            <div class="stat-item"><span class="stat-label">💵 المقدم</span><span class="stat-value">{row.get('Down_Payment', '-')}</span></div>
                            <div class="stat-item"><span class="stat-label">⏳ التقسيط</span><span class="stat-value">{row.get('Installments', '-')}</span></div>
                        </div>
                        
                        <div style="background:#151515; padding:10px; border-radius:10px; border-right:3px solid #f59e0b;">
                            <p style="margin:0; font-size:13px;"><b>🌟 الميزة:</b> {row.get('Competitive Advantage', '-')}</p>
                            <p style="margin:5px 0 0 0; font-size:13px;"><b>👷 الاستشاري:</b> {row.get('Consultant', '-')}</p>
                        </div>
                    </div>
                    """
                    st.markdown(card_html, unsafe_allow_html=True)
                    with st.expander("👁️ التفاصيل"):
                        st.write(row.get('Detailed_Info', 'لا يوجد وصف'))

elif st.session_state.page == "tools":
    st.header("🛠️ أدوات البروكر")
    st.info("سيتم إضافة الحاسبة هنا")
