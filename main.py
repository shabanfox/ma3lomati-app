import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (توزيع المطورين جنب بعضهم)
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
        box-shadow: 0px 10px 20px rgba(0,0,0,0.1);
    }

    /* تصميم كارت المطور كزر شبكي */
    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        height: 100px !important;
        background-color: white !important; 
        border: 3px solid #000 !important;
        border-radius: 15px !important; 
        font-size: 1.1rem !important;
        font-weight: 900 !important; 
        color: #000 !important;
        box-shadow: 4px 4px 0px #000 !important; 
        margin-bottom: 10px !important;
        transition: 0.2s;
    }
    div.stButton > button[key^="dev_"]:hover {
        border-color: #f59e0b !important; 
        color: #f59e0b !important;
        transform: translateY(-2px);
        box-shadow: 6px 6px 0px #f59e0b !important;
    }

    /* ستايل صفحة التفاصيل */
    .dev-profile { background: #fff; padding: 25px; border-radius: 20px; border: 2px solid #eee; margin-bottom: 20px; }
    .project-card { background: #f8f9fa; padding: 15px; border-radius: 10px; margin-bottom: 10px; font-weight: 700; border-right: 5px solid #f59e0b; }
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

# إدارة التنقل
if 'page' not in st.session_state: st.session_state.page = "main"
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page_num' not in st.session_state: st.session_state.page_num = 0

if not df.empty:
    proj_col = df.columns[0]
    dev_col = df.columns[1]

    st.markdown('<div class="hero-banner"><h1>🚀 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية (دليل المطورين جنب بعض) ---
    if st.session_state.page == "main":
        tab_list, tab_tools = st.tabs(["🔍 دليل الشركات والمشاريع", "🛠️ أدوات البروكر"])

        with tab_list:
            search = st.text_input("🔍 ابحث عن مطور أو شركة...", placeholder="اكتب هنا للبحث السريع")
            
            unique_devs = df[dev_col].dropna().unique()
            if search:
                unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

            # نظام الصفحات (عرض 12 مطور - 4 صفوف في كل صف 3)
            items = 12
            total_p = (len(unique_devs) // items) + (1 if len(unique_devs) % items > 0 else 0)
            start = st.session_state.page_num * items
            current_devs = unique_devs[start:start+items]

            # إنشاء الشبكة (Grid)
            for i in range(0, len(current_devs), 3):
                cols = st.columns(3) # هنا جعلناهم "جنب بعض" في 3 أعمدة
                for j in range(3):
                    if i + j < len(current_devs):
                        d_name = current_devs[i + j]
                        with cols[j]:
                            if st.button(d_name, key=f"dev_{d_name}"):
                                st.session_state.selected_dev = d_name
                                st.session_state.page = "details"
                                st.rerun()

            # أزرار التنقل بالأسفل
            st.write("<br>", unsafe_allow_html=True)
            c1, mid, c2 = st.columns([1, 2, 1])
            with c1:
                if st.button("⬅️ السابق") and st.session_state.page_num > 0:
                    st.session_state.page_num -= 1; st.rerun()
            with mid:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page_num + 1} من {total_p}</p>", unsafe_allow_html=True)
            with c2:
                if st.button("التالي ➡️") and (start + items) < len(unique_devs):
                    st.session_state.page_num += 1; st.rerun()

        with tab_tools:
            st.write("### 🛠️ الأدوات الحسابية")
            t1, t2 = st.columns(2)
            with t1:
                p = st.number_input("سعر الوحدة", 1000000)
                y = st.slider("السنوات", 1, 15, 8)
                st.metric("القسط الشهري", f"{(p/ (y*12)):,.0f} ج.م")
            with t2:
                buy = st.number_input("سعر الشراء", 2000000)
                rent = st.number_input("الإيجار السنوي", 150000)
                st.metric("ROI %", f"{(rent/buy)*100:.2f}%")

    # --- صفحة المطور المنفصلة ---
    elif st.session_state.page == "details":
        if st.button("🔙 العودة للدليل"):
            st.session_state.page = "main"
            st.rerun()

        dev = st.session_state.selected_dev
        st.markdown(f'<div class="dev-profile"><h2>🏢 شركة {dev}</h2><p>نبذة سريعة عن المطور ومكانته في السوق العقاري المصري.</p></div>', unsafe_allow_html=True)
        
        st.subheader("🏗️ مشاريع المطور:")
        dev_projs = df[df[dev_col] == dev][proj_col].unique()
        
        # عرض المشاريع أيضاً في عمودين
        p_cols = st.columns(2)
        for idx, p_name in enumerate(dev_projs):
            with p_cols[idx % 2]:
                st.markdown(f'<div class="project-card">📍 {p_name}</div>', unsafe_allow_html=True)
