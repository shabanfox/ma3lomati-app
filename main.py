import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS احترافي (الواجهة الرئيسية + أزرار المطورين)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff;
    }

    /* الهيدر الرئيسي */
    .main-banner { 
        background: #000; color: #f59e0b; padding: 30px; border-radius: 20px; 
        text-align: center; margin-bottom: 40px; border: 4px solid #f59e0b;
    }

    /* الأزرار الكبيرة في صفحة البداية */
    div.stButton > button[key="main_devs"], div.stButton > button[key="main_tools"] {
        width: 100% !important;
        height: 200px !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        border-radius: 20px !important;
        border: 4px solid #000 !important;
        box-shadow: 10px 10px 0px #000 !important;
        transition: 0.3s;
    }
    div.stButton > button[key="main_devs"] { background-color: #f59e0b !important; color: #000 !important; }
    div.stButton > button[key="main_tools"] { background-color: #000 !important; color: #f59e0b !important; }
    div.stButton > button:hover { transform: translateY(-5px); box-shadow: 15px 15px 0px #f59e0b !important; }

    /* أزرار الشركات (Developer) داخل الشبكة */
    div.stButton > button[key^="dev_btn_"] {
        width: 100% !important;
        height: 80px !important;
        background-color: #ffffff !important;
        border: 2px solid #000 !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        color: #000 !important;
        box-shadow: 4px 4px 0px #000 !important;
        margin-bottom: 10px !important;
    }
    div.stButton > button[key^="dev_btn_"]:hover {
        border-color: #f59e0b !important;
        color: #f59e0b !important;
    }

    .proj-card { background: #f9f9f9; padding: 15px; border-radius: 10px; border-right: 5px solid #f59e0b; margin-bottom: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات من Google Sheets
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# إدارة حالة التطبيق (State Management)
if 'view' not in st.session_state: st.session_state.view = "home"
if 'selected_developer' not in st.session_state: st.session_state.selected_developer = None
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- صفحة البداية (الزرين الكبار) ---
if st.session_state.view == "home":
    st.markdown('<div class="main-banner"><h1>🚀 منصة معلوماتى العقارية</h1><h3>دليلك الذكي للمطورين وأدوات البروكر</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("🏢 الشركات\n(Developers)", key="main_devs"):
            st.session_state.view = "devs_grid"
            st.rerun()
    with col2:
        if st.button("🛠️ أدوات\nالبروكر", key="main_tools"):
            st.session_state.view = "tools_view"
            st.rerun()

# --- صفحة قائمة الشركات (تستخدم عمود Developer لعمل الأزرار) ---
elif st.session_state.view == "devs_grid":
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.view = "home"; st.rerun()
    
    st.markdown("## 🏢 دليل المطورين العقاريين")
    search = st.text_input("🔍 ابحث عن اسم المطور (Developer)...")
    
    # تحديد عمود المطور
    dev_col = df.columns[1] # عمود Developer
    all_developers = df[dev_col].dropna().unique()
    
    if search:
        all_developers = [d for d in all_developers if search.lower() in str(d).lower()]

    # نظام الشبكة والصفحات (عرض 15 مطور في كل صفحة)
    per_page = 15
    start = st.session_state.page_num * per_page
    end = start + per_page
    current_devs = all_developers[start:end]

    # إنشاء أزرار الشركات "جنب بعض"
    for i in range(0, len(current_devs), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(current_devs):
                dev_name = current_devs[i + j]
                with cols[j]:
                    # هنا الزر يقرأ مباشرة من عمود Developer
                    if st.button(dev_name, key=f"dev_btn_{dev_name}"):
                        st.session_state.selected_developer = dev_name
                        st.session_state.view = "dev_details"
                        st.rerun()
    
    # أزرار التنقل
    st.write("---")
    n1, n2, n3 = st.columns([1, 2, 1])
    if n1.button("⬅️ السابق") and st.session_state.page_num > 0:
        st.session_state.page_num -= 1; st.rerun()
    if n3.button("التالي ➡️") and end < len(all_developers):
        st.session_state.page_num += 1; st.rerun()

# --- صفحة تفاصيل المطور ومشاريع المطور ---
elif st.session_state.view == "dev_details":
    if st.button("🔙 العودة لقائمة الشركات"):
        st.session_state.view = "devs_grid"; st.rerun()
    
    selected = st.session_state.selected_developer
    st.markdown(f"""<div style='background:#000; color:#f59e0b; padding:20px; border-radius:15px; text-align:center;'>
                    <h1>🏢 {selected}</h1></div>""", unsafe_allow_html=True)
    
    st.write("### 🏗️ مشاريع المطور:")
    proj_col = df.columns[0]
    dev_col = df.columns[1]
    
    # فلترة المشاريع بناءً على المطور المختار
    dev_projects = df[df[dev_col] == selected][proj_col].unique()
    
    p_cols = st.columns(2)
    for idx, p in enumerate(dev_projects):
        with p_cols[idx % 2]:
            st.markdown(f'<div class="proj-card">🔹 {p}</div>', unsafe_allow_html=True)

# --- صفحة أدوات البروكر ---
elif st.session_state.view == "tools_view":
    if st.button("🔙 العودة للرئيسية"):
        st.session_state.view = "home"; st.rerun()
    
    st.title("🛠️ أدوات البروكر الذكية")
    t1, t2 = st.columns(2)
    with t1:
        st.subheader("💰 حاسبة الأقساط")
        val = st.number_input("قيمة العقار", 1000000)
        yrs = st.slider("عدد السنوات", 1, 15, 8)
        st.metric("القسط الشهري", f"{(val/(yrs*12)):,.0f} ج.م")
