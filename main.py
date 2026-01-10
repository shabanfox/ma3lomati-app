import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (أسود وذهبي مع لمسة عصرية)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header {visibility: hidden;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8f9fa;
    }

    .hero-banner { 
        background: #000; color: #f59e0b; padding: 20px; border-radius: 15px; 
        text-align: center; margin-bottom: 25px; border: 3px solid #f59e0b;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
    }

    /* تصميم كارت المطور كزر */
    div.stButton > button[key^="dev_"] {
        width: 100% !important; height: 120px !important;
        background-color: white !important; border: 2px solid #000 !important;
        border-radius: 15px !important; font-size: 1.3rem !important;
        font-weight: 900 !important; color: #000 !important;
        box-shadow: 5px 5px 0px #000 !important; transition: 0.3s;
    }
    div.stButton > button[key^="dev_"]:hover {
        border-color: #f59e0b !important; color: #f59e0b !important;
        transform: translate(-3px, -3px); box-shadow: 8px 8px 0px #f59e0b !important;
    }

    /* ستايل صفحة المطور */
    .dev-profile { background: white; padding: 30px; border-radius: 20px; border-right: 10px solid #f59e0b; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); }
    .project-card { background: #f1f1f1; padding: 15px; border-radius: 10px; margin-bottom: 10px; font-weight: 700; border-right: 5px solid #000; }
    
    /* زر العودة */
    div.stButton > button[key="back_btn"] {
        background-color: #000 !important; color: #f59e0b !important; border: 1px solid #f59e0b !important;
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

# إدارة التنقل (Navigation State)
if 'page' not in st.session_state: st.session_state.page = "main"
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page_num' not in st.session_state: st.session_state.page_num = 0

if not df.empty:
    proj_col = df.columns[0]
    dev_col = df.columns[1]

    # --- الهيدر ثابت ---
    st.markdown('<div class="hero-banner"><h1>🚀 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية (دليل المطورين) ---
    if st.session_state.page == "main":
        tab_list, tab_tools = st.tabs(["🔍 دليل الشركات والمشاريع", "🛠️ أدوات البروكر"])

        with tab_list:
            col_s, col_m = st.columns([1, 3])
            with col_s:
                st.write("### ⚙️ تصفية")
                search = st.text_input("🔍 ابحث عن مطور...")
            
            with col_m:
                unique_devs = df[dev_col].dropna().unique()
                if search:
                    unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

                # نظام الصفحات (10 مطورين)
                items = 10
                total_p = (len(unique_devs) // items) + (1 if len(unique_devs) % items > 0 else 0)
                start = st.session_state.page_num * items
                current_devs = unique_devs[start:start+items]

                st.info(f"عرض {len(current_devs)} مطور - صفحة {st.session_state.page_num + 1}")

                # عرض المطورين ككروت قابلة للضغط
                for d_name in current_devs:
                    if st.button(f"🏢 {d_name}", key=f"dev_{d_name}"):
                        st.session_state.selected_dev = d_name
                        st.session_state.page = "details"
                        st.rerun()

                # أزرار التنقل
                c1, c2 = st.columns(2)
                if c1.button("⬅️ السابق") and st.session_state.page_num > 0:
                    st.session_state.page_num -= 1; st.rerun()
                if c2.button("التالي ➡️") and (start + items) < len(unique_devs):
                    st.session_state.page_num += 1; st.rerun()

        with tab_tools:
            # (أدوات البروكر الحسابية تظل هنا)
            st.write("### 🛠️ الأدوات الحسابية")
            # حاسبة القسط السريع
            p = st.number_input("سعر الوحدة", 1000000)
            y = st.slider("السنوات", 1, 15, 8)
            st.metric("القسط التقريبي", f"{(p/ (y*12)):,.0f} ج.م")

    # --- صفحة نبذة عن المطور (Details Page) ---
    elif st.session_state.page == "details":
        if st.button("🔙 العودة للدليل", key="back_btn"):
            st.session_state.page = "main"
            st.rerun()

        dev = st.session_state.selected_dev
        st.markdown(f"""
            <div class="dev-profile">
                <h1>🏢 {dev}</h1>
                <p style='color: #666; font-size: 1.2rem;'>
                    تعتبر شركة <b>{dev}</b> من الشركات الرائدة في السوق العقاري المصري، 
                    وتتميز بمشاريعها ذات التصميم الفريد والجودة العالية في التنفيذ.
                </p>
                <hr>
                <h3>🏗️ مشاريع الشركة المتاحة:</h3>
            </div>
        """, unsafe_allow_html=True)

        # عرض مشاريع هذا المطور فقط
        dev_projs = df[df[dev_col] == dev][proj_col].unique()
        cols = st.columns(2)
        for idx, p_name in enumerate(dev_projs):
            with cols[idx % 2]:
                st.markdown(f'<div class="project-card">📍 {p_name}</div>', unsafe_allow_html=True)

else:
    st.error("⚠️ لم يتم العثور على بيانات.")
