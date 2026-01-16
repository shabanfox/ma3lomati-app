import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="BrokerEdge Pro", layout="wide", initial_sidebar_state="collapsed")

# إدارة حالة الصفحات (Pagination)
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# 2. التنسيق (CSS) - وضع زر الخروج في الأعلى على اليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; }
    
    /* هيدر يحتوي على اللوجو وزر الخروج */
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        background: #1E293B; padding: 10px 30px; border-bottom: 3px solid #F59E0B;
    }
    .logout-btn {
        background: #EF4444; color: white !important; padding: 5px 15px;
        border-radius: 8px; text-decoration: none; font-weight: bold;
    }
    
    /* تصميم الشبكة (Grid) */
    .grid-card {
        background: white; border-radius: 12px; border: 1px solid #E2E8F0;
        padding: 15px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        min-height: 180px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. دالة جلب البيانات (تحويل الرابط لـ CSV لضمان التحميل)
def get_data(url):
    try:
        # تحويل الرابط تلقائياً من pubhtml إلى csv
        csv_url = url.split('/pubhtml')[0] + '/pub?output=csv'
        return pd.read_csv(csv_url).fillna("-")
    except:
        return pd.DataFrame()

# روابطك (المشاريع والمطورين)
url_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pubhtml"
url_developers = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pubhtml"

# 4. شريط الأدوات العلوي (زر الخروج فوق عاليسار)
st.markdown(f'''
    <div class="header-container">
        <div style="color:#F59E0B; font-size:22px; font-weight:900;">BROKER EDGE</div>
        <a href="/" target="_self" class="logout-btn">تسجيل الخروج</a>
    </div>
''', unsafe_allow_html=True)

# 5. القائمة الرئيسية
choice = option_menu(None, ["المشاريع", "المطورين", "الأدوات"], 
    icons=["building", "people", "gear"], orientation="horizontal")

# 6. وظيفة العرض الشبكي (6 عناصر مع تنقل)
def show_grid(df, key):
    limit = 6
    start = st.session_state[key] * limit
    page_data = df.iloc[start : start + limit]
    
    cols = st.columns(2) # عمودين (شكل شبكي)
    for i, (idx, row) in enumerate(page_data.iterrows()):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="grid-card">
                    <h3 style="color:#1E3A8A; margin:0;">{row.iloc[0]}</h3>
                    <p style="color:#64748B;">📍 {row.iloc[2] if len(row)>2 else "غير محدد"}</p>
                    <p>🏢 المطور: <b>{row.iloc[1] if len(row)>1 else "-"}</b></p>
                </div>
            """, unsafe_allow_html=True)

    # أزرار التنقل (التالي والسابق)
    st.write("---")
    col1, col2 = st.columns(2)
    with col1:
        if st.session_state[key] > 0:
            if st.button("السابق", key=f"prev_{key}"):
                st.session_state[key] -= 1
                st.rerun()
    with col2:
        if start + limit < len(df):
            if st.button("التالي", key=f"next_{key}"):
                st.session_state[key] += 1
                st.rerun()

# التنفيذ
if choice == "المشاريع":
    data = get_data(url_projects)
    if not data.empty: show_grid(data, 'p_page')
    else: st.warning("تأكد من عمل 'Publish to web' للشيت واختيار CSV")

elif choice == "المطورين":
    data = get_data(url_developers)
    if not data.empty: show_grid(data, 'd_page')
    else: st.warning("فشل تحميل بيانات المطورين")

elif choice == "الأدوات":
    st.subheader("🛠️ أدوات الحساب")
    price = st.number_input("سعر الوحدة", value=1000000)
    years = st.slider("عدد السنين", 1, 10, 5)
    st.success(f"القسط الشهري التقريبي: {round(price/(years*12), 2)}")
