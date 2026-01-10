import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (نظام الشبكة Grid مع التركيز على المطور)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff;
    }

    .hero-banner { 
        background: #000; color: #f59e0b; padding: 20px; border-radius: 15px; 
        text-align: center; margin-bottom: 25px; border: 3px solid #f59e0b;
    }

    /* كارت المطور Developer */
    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        height: 100px !important;
        background-color: white !important; 
        border: 2px solid #000 !important;
        border-radius: 12px !important; 
        font-size: 1.1rem !important;
        font-weight: 800 !important; 
        color: #000 !important;
        box-shadow: 4px 4px 0px #000 !important; 
        margin-bottom: 15px !important;
        transition: 0.2s;
    }
    div.stButton > button[key^="dev_"]:hover {
        border-color: #f59e0b !important; 
        color: #f59e0b !important;
        box-shadow: 6px 6px 0px #f59e0b !important;
    }

    .dev-profile-header { 
        background: #fdf6e9; padding: 25px; border-radius: 20px; 
        border: 2px solid #f59e0b; margin-bottom: 20px; text-align: center;
    }
    .project-card { 
        background: #f8f9fa; padding: 15px; border-radius: 10px; 
        margin-bottom: 10px; font-weight: 700; border-right: 5px solid #000;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
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

# إدارة التنقل والصفحات
if 'page' not in st.session_state: st.session_state.page = "main"
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page_num' not in st.session_state: st.session_state.page_num = 0

if not df.empty:
    # ربط الأعمدة: المطور هو البطل هنا
    proj_col = df.columns[0] # المشروع
    dev_col = df.columns[1]  # المطور (Developer)

    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى: دليل المطورين</h1></div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية: شبكة المطورين (Developers Grid) ---
    if st.session_state.page == "main":
        tab_list, tab_tools = st.tabs(["🏢 الشركات العقارية", "🛠️ الأدوات"])

        with tab_list:
            search = st.text_input("🔍 ابحث عن اسم المطور (Developer)...")
            
            # فلترة المطورين فقط
            unique_devs = df[dev_col].dropna().unique()
            if search:
                unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

            # نظام الصفحات (12 مطور - 3 أعمدة)
            items_per_page = 12
            total_pages = (len(unique_devs) // items_per_page) + (1 if len(unique_devs) % items_per_page > 0 else 0)
            start_idx = st.session_state.page_num * items_per_page
            current_devs = unique_devs[start_idx : start_idx + items_per_page]

            # عرض المطورين "جنب بعض"
            for i in range(0, len(current_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_devs):
                        dev_name = current_devs[i + j]
                        with cols[j]:
                            if st.button(dev_name, key=f"dev_{dev_name}"):
                                st.session_state.selected_dev = dev_name
                                st.session_state.page = "details"
                                st.rerun()

            # أزرار التنقل
            st.markdown("---")
            n1, n_info, n2 = st.columns([1, 2, 1])
            with n1:
                if st.button("⬅️ السابق") and st.session_state.page_num > 0:
                    st.session_state.page_num -= 1; st.rerun()
            with n_info:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page_num + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with n2:
                if st.button("التالي ➡️") and (start_idx + items_per_page) < len(unique_devs):
                    st.session_state.page_num += 1; st.rerun()

    # --- صفحة المطور (Developer Details) ---
    elif st.session_state.page == "details":
        if st.button("🔙 عودة للقائمة"):
            st.session_state.page = "main"
            st.rerun()

        dev = st.session_state.selected_dev
        st.markdown(f"""
            <div class="dev-profile-header">
                <h1>🏢 {dev}</h1>
                <p>عرض كافة مشاريع مطور <b>{dev}</b> العقارية</p>
            </div>
        """, unsafe_allow_html=True)
        
        projs = df[df[dev_col] == dev][proj_col].unique()
        p_cols = st.columns(2)
        for idx, p_name in enumerate(projs):
            with p_cols[idx % 2]:
                st.markdown(f'<div class="project-card">🔹 {p_name}</div>', unsafe_allow_html=True)

else:
    st.error("⚠️ لم يتم العثور على بيانات.")
