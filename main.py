import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (يجب أن تكون أول أمر)
st.set_page_config(page_title="Ma3lomati PRO Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. تعريف التصميم الشامل (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء واجهة ستريمليت الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الحاوية الرئيسية */
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* شريط التنقل */
    .nav-bar {
        background-color: #000; padding: 10px; border-bottom: 2px solid #f59e0b;
        display: flex; justify-content: center; gap: 20px; margin-bottom: 25px;
    }

    /* كارت المشروع */
    .project-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
        color: white;
    }
    
    .price-tag {
        background: #f59e0b; color: black; padding: 4px 12px;
        border-radius: 6px; font-weight: 900; font-size: 1.1rem;
    }

    .stat-grid {
        display: flex; justify-content: space-between; gap: 10px; margin: 15px 0;
    }

    .stat-box {
        background: #1a1a1a; padding: 8px; border-radius: 8px;
        text-align: center; flex: 1; border: 1px solid #333;
    }

    .stat-label { color: #888; font-size: 11px; display: block; margin-bottom: 4px; }
    .stat-value { color: #f59e0b; font-weight: 700; font-size: 13px; }

    .feature-box {
        background: #151515; padding: 12px; border-radius: 8px;
        border-right: 3px solid #f59e0b; font-size: 13px;
    }
    
    /* تنسيق الأزرار لتتناسب مع التصميم */
    div.stButton > button {
        background-color: #f59e0b !important; color: black !important;
        font-weight: 900 !important; border-radius: 8px !important;
        border: none !important; width: 100%; height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات من Google Sheets
@st.cache_data(ttl=600)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(csv_url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"حدث خطأ في تحميل البيانات: {e}")
    st.stop()

# 4. الملاحة (Navigation)
if 'menu' not in st.session_state:
    st.session_state.menu = "database"

# أزرار التنقل العلوية
c1, c2 = st.columns(2)
with c1:
    if st.button("🏢 قاعدة بيانات المشاريع"): st.session_state.menu = "database"
with c2:
    if st.button("🛠️ أدوات الحاسبة"): st.session_state.menu = "tools"

st.write("---")

# --- شاشة قاعدة البيانات ---
if st.session_state.menu == "database":
    # منطقة الفلاتر
    col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
    with col_f1:
        search = st.text_input("🔍 ابحث عن أي شيء (مشروع، مطور، ميزة...)", placeholder="مثال: التجمع، زد، استلام فوري...")
    with col_f2:
        areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("📍 تصفية بالمنطقة", areas)
    with col_f3:
        types = ["الكل"] + sorted(df['Type'].dropna().unique().tolist())
        sel_type = st.selectbox("🏠 تصفية بالنوع", types)

    # معالجة الفلترة
    dff = df.copy()
    if search:
        dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_area != "الكل":
        dff = dff[dff['Area'].str.contains(sel_area, na=False)]
    if sel_type != "الكل":
        dff = dff[dff['Type'].str.contains(sel_type, na=False)]

    st.markdown(f"<p style='color:#888;'>تم العثور على {len(dff)} مشروع</p>", unsafe_allow_html=True)

    # عرض النتائج في صفوف (كل صف فيه مشروعين)
    for i in range(0, len(dff), 2):
        row_cols = st.columns(2)
        for j in range(2):
            if i + j < len(dff):
                data = dff.iloc[i + j]
                with row_cols[j]:
                    # هنا السر: بناء الكارت كـ HTML كامل داخل markdown واحد
                    card_content = f"""
                    <div class="project-card">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h2 style="color:#f59e0b; margin:0;">{data.get('Project Name', 'N/A')}</h2>
                            <span class="price-tag">{data.get('Min_Val', '0')}</span>
                        </div>
                        <p style="color:#ccc; margin:5px 0;">بواسطة: {data.get('Developer', '-')}</p>
                        
                        <div class="stat-grid">
                            <div class="stat-box">
                                <span class="stat-label">📍 المنطقة</span>
                                <span class="stat-value">{data.get('Area', '-')}</span>
                            </div>
                            <div class="stat-box">
                                <span class="stat-label">💵 المقدم</span>
                                <span class="stat-value">{data.get('Down_Payment', '-')}</span>
                            </div>
                            <div class="stat-box">
                                <span class="stat-label">⏳ التقسيط</span>
                                <span class="stat-value">{data.get('Installments', '-')}</span>
                            </div>
                        </div>
                        
                        <div class="feature-box">
                            <p style="margin:0;"><b>🌟 الميزة:</b> {data.get('Competitive Advantage', '-')}</p>
                            <p style="margin:8px 0 0 0;"><b>👷 الاستشاري:</b> {data.get('Consultant', '-')}</p>
                        </div>
                    </div>
                    """
                    st.markdown(card_content, unsafe_allow_html=True)
                    # زر التفاصيل (يعمل بآلية ستريمليت الأصلية خارج الـ HTML)
                    with st.expander("👁️ عرض التفاصيل والوصف"):
                        st.write(f"**حالة التسليم:** {data.get('Delivery', '-')}")
                        st.write(f"**المالك:** {data.get('DeveloperOwner', '-')}")
                        st.info(data.get('Detailed_Info', 'لا يوجد وصف إضافي'))

# --- شاشة الأدوات ---
elif st.session_state.menu == "tools":
    st.title("💰 حاسبة التمويل العقاري")
    # (هنا يمكنك إضافة كود الحاسبة لاحقاً)
    st.info("هذا القسم قيد التطوير ليناسب احتياجاتك")
