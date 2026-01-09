import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - تحسين شكل التبويبات والأزرار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    .block-container { padding-top: 1rem !important; }

    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* تصميم كروت المشاريع داخل صفحة التفاصيل */
    .project-card {
        background: #ffffff; padding: 15px; border-radius: 10px;
        border: 1px solid #e2e8f0; margin-bottom: 10px;
        border-right: 5px solid #D4AF37;
    }

    /* تصميم رأس الصفحة */
    .header-box {
        background: white; padding: 20px; border-radius: 15px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 20px;
    }

    div.stButton > button {
        border-radius: 8px !important; font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# إدارة الحالة (Navigation)
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main' and df is not None:
    st.markdown('<div class="header-box"><h1 style="color:#003366; margin:0;">منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
    
    # عرض المطورين بشكل كروت (تبسيطاً للمثال الحالي)
    search_q = st.text_input("🔍 ابحث عن المطور...")
    f_df = df.copy()
    if search_q:
        f_df = f_df[f_df['Developer'].str.contains(search_q, na=False, case=False)]
    
    # عرض النتائج في شبكة
    cols = st.columns(2)
    for idx, (i, row) in enumerate(f_df.drop_duplicates(subset=['Developer']).head(10).iterrows()):
        with cols[idx % 2]:
            st.markdown(f"""
                <div style="background:white; padding:20px; border-radius:12px; border-right:5px solid #003366; margin-bottom:10px; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
                    <h3 style="margin:0; color:#003366;">{row['Developer']}</h3>
                    <p style="color:#64748b; font-size:0.9rem;">اضغط للتفاصيل والمشاريع</p>
                </div>
            """, unsafe_allow_html=True)
            if st.button("فتح ملف المطور", key=f"dev_{idx}", use_container_width=True):
                st.session_state.selected_dev = row['Developer']
                st.session_state.dev_data = row.to_dict()
                st.session_state.page = 'details'
                st.rerun()

# --- صفحة التفاصيل المحدثة (التي طلبتها) ---
elif st.session_state.page == 'details':
    dev_name = st.session_state.selected_dev
    dev_info = st.session_state.dev_data
    
    # زر العودة
    if st.button("⬅️ العودة للرئيسية"):
        st.session_state.page = 'main'
        st.rerun()

    # رأس صفحة المطور
    st.markdown(f"""
        <div style="background:#003366; color:white; padding:30px; border-radius:15px; text-align:center; margin-bottom:20px;">
            <h1 style="margin:0;">{dev_name}</h1>
            <p style="margin:0; opacity:0.8;">الملف التعريفي الكامل والمشاريع</p>
        </div>
    """, unsafe_allow_html=True)

    # إنشاء الأزرار (Tabs) المطلوبة
    tab_info, tab_projects = st.tabs(["ℹ️ معلومات المطور", "🏗️ مشاريع المطور"])

    with tab_info:
        st.markdown("### 📝 الزتونة الفنية")
        info_text = dev_info.get('Detailed_Info', 'لا توجد معلومات إضافية مسجلة حالياً لهذا المطور.')
        st.markdown(f"""
            <div style="background:white; padding:25px; border-radius:15px; border:1px solid #e2e8f0; line-height:1.8; font-size:1.1rem;">
                {info_text}
            </div>
        """, unsafe_allow_html=True)

    with tab_projects:
        st.markdown(f"### 🏙️ قائمة مشاريع {dev_name}")
        # فلترة البيانات لعرض كل السطور التي تخص هذا المطور
        projects_df = df[df['Developer'] == dev_name]
        
        if not projects_df.empty:
            for _, proj in projects_df.iterrows():
                st.markdown(f"""
                    <div class="project-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:900; color:#003366; font-size:1.1rem;">🏗️ مشروع في منطقة: {proj.get('Area', 'غير محدد')}</span>
                            <span style="background:#D4AF37; color:white; padding:2px 10px; border-radius:20px; font-size:0.8rem;">نشط</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("لم يتم العثور على مشاريع مسجلة لهذا المطور.")
