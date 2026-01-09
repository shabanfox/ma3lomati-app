import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - لضمان المظهر الاحترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .main-card {
        background: white; border-radius: 15px; padding: 20px;
        border-right: 8px solid #003366; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px; background-color: #f1f5f9; border-radius: 10px; padding: 10px 20px; font-weight: bold;
    }
    .stTabs [aria-selected="true"] { background-color: #003366 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. دالة جلب البيانات مع تنظيف العناوين
@st.cache_data
def load_data():
    # الرابط الخاص بالشيت (تأكد من نشره كـ CSV)
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        # مسح أي مسافات زائدة في أسماء الأعمدة لتجنب الأخطاء
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"حدث خطأ في جلب البيانات: {e}")
        return None

df = load_data()

# إدارة التنقل بين الصفحات
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الهيدر ---
st.markdown('<h1 style="text-align:center; color:#003366;">منصة معلوماتى العقارية</h1>', unsafe_allow_html=True)
st.write("---")

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    # الفلاتر الديناميكية
    c1, c2, c3 = st.columns(3)
    with c1:
        s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()))
    with c2:
        s_type = st.selectbox("🏠 نوع المشروع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()))
    with c3:
        s_dev = st.text_input("🔍 ابحث عن مطور محدد")

    # تطبيق الفلترة
    f_df = df.copy()
    if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]
    if s_type != "الكل": f_df = f_df[f_df['Type'] == s_type]
    if s_dev: f_df = f_df[f_df['Developer'].str.contains(s_dev, na=False, case=False)]

    # عرض المشاريع
    if f_df.empty:
        st.warning("لا توجد نتائج تطابق بحثك.")
    else:
        grid = st.columns(2)
        for idx, (i, row) in enumerate(f_df.iterrows()):
            with grid[idx % 2]:
                st.markdown(f"""
                    <div class="main-card">
                        <h3 style="margin:0; color:#003366;">{row['Project']}</h3>
                        <p style="color:#64748b; font-weight:bold;">{row['Developer']}</p>
                        <div style="display:flex; justify-content:space-between; margin-top:10px;">
                            <span style="color:#16a34a; font-weight:900;">💰 {row['Price']}</span>
                            <span style="color:#1e293b;">📍 {row['Area']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"تفاصيل {row['Project']}", key=f"btn_{i}", use_container_width=True):
                    st.session_state.selected_item = row.to_dict()
                    st.session_state.page = 'details'
                    st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.page = 'main'
        st.rerun()

    st.markdown(f"""
        <div style="background:white; padding:25px; border-radius:15px; border-right:12px solid #003366; margin:20px 0;">
            <h1 style="color:#003366; margin:0;">{item['Project']}</h1>
            <h4 style="color:#64748b;">المطور: {item['Developer']} | المالك: {item['Owner']}</h4>
        </div>
    """, unsafe_allow_html=True)

    # التبويبات (Tabs)
    tab1, tab2 = st.tabs(["📝 معلومات المطور والزتونة", "🏗️ مشاريع المطور الأخرى"])

    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🔍 تفاصيل العرض")
            st.info(f"**نوع المشروع:** {item['Type']}")
            st.info(f"**تاريخ الاستلام:** {item['Delivery']}")
            st.info(f"**نظام السداد:** مقدم {item['Down_Payment']} وقسط على {item['Installments']} سنوات")
        with col2:
            st.markdown("### 💡 الزتونة الفنية")
            st.success(item['Detailed_Info'])
            st.write(f"**وصف المشروع:** {item['Description']}")
            st.warning(f"**أقل قيمة استثمار:** {item['Min_Val']}")

    with tab2:
        st.subheader(f"كافة مشاريع شركة {item['Developer']}")
        # جلب المشاريع الأخرى لنفس المطور من الشيت
        other_projs = df[df['Developer'] == item['Developer']]
        for _, p in other_projs.iterrows():
            st.markdown(f"""
                <div style="background:#f1f5f9; padding:15px; border-radius:10px; margin-bottom:10px; border:1px solid #e2e8f0;">
                    <b>🏗️ {p['Project']}</b> - {p['Area']} <br>
                    السعر: {p['Price']} | نظام السداد: {p['Installments']} سنوات
                </div>
            """, unsafe_allow_html=True)
