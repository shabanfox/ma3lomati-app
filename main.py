import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS (التركيز على المطور Developer وتوزيع الشبكة)
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

    /* تصميم كارت المطور Developer */
    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        height: 110px !important;
        background-color: white !important; 
        border: 3px solid #000 !important;
        border-radius: 15px !important; 
        font-size: 1.2rem !important;
        font-weight: 900 !important; 
        color: #000 !important;
        box-shadow: 4px 4px 0px #000 !important; 
        margin-bottom: 15px !important;
        transition: 0.2s;
        display: flex; align-items: center; justify-content: center;
    }
    div.stButton > button[key^="dev_"]:hover {
        border-color: #f59e0b !important; 
        color: #f59e0b !important;
        transform: translateY(-3px);
        box-shadow: 7px 7px 0px #f59e0b !important;
    }

    .dev-profile-header { 
        background: #fdf6e9; padding: 25px; border-radius: 20px; 
        border: 2px solid #f59e0b; margin-bottom: 20px; text-align: center;
    }
    .project-card { 
        background: #f8f9fa; padding: 15px; border-radius: 10px; 
        margin-bottom: 10px; font-weight: 700; border-right: 5px solid #000;
        box-shadow: 2px 2px 5px rgba(0,0,0,0.05);
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

# إدارة التنقل (Navigation)
if 'page' not in st.session_state: st.session_state.page = "main"
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'page_num' not in st.session_state: st.session_state.page_num = 0

if not df.empty:
    # تحديد الأعمدة (مشروع، مطور)
    proj_col = df.columns[0]
    dev_col = df.columns[1] # هذا هو عمود Developer

    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)

    # --- الصفحة الرئيسية (عرض المطورين Developer) ---
    if st.session_state.page == "main":
        tab_list, tab_tools = st.tabs(["🏢 دليل المطورين", "🛠️ الأدوات"])

        with tab_list:
            search = st.text_input("🔍 ابحث عن Developer...", placeholder="اكتب اسم المطور هنا للبحث السريع")
            
            unique_devs = df[dev_col].dropna().unique()
            if search:
                unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

            # عرض 12 مطور في الصفحة (3 أعمدة × 4 صفوف)
            items = 12
            total_pages = (len(unique_devs) // items) + (1 if len(unique_devs) % items > 0 else 0)
            start_idx = st.session_state.page_num * items
            current_devs = unique_devs[start_idx : start_idx + items]

            # شبكة العرض (Grid)
            for i in range(0, len(current_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_devs):
                        dev_name = current_devs[i + j]
                        with cols[j]:
                            # استخدام زر بشكل كارت لفتح صفحة المطور
                            if st.button(dev_name, key=f"dev_{dev_name}"):
                                st.session_state.selected_dev = dev_name
                                st.session_state.page = "details"
                                st.rerun()

            # التحكم في الصفحات
            st.write("<br>", unsafe_allow_html=True)
            c1, mid, c2 = st.columns([1, 2, 1])
            with c1:
                if st.button("⬅️ السابق") and st.session_state.page_num > 0:
                    st.session_state.page_num -= 1; st.rerun()
            with mid:
                st.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.page_num + 1} من {total_pages}</p>", unsafe_allow_html=True)
            with c2:
                if st.button("التالي ➡️") and (start_idx + items) < len(unique_devs):
                    st.session_state.page_num += 1; st.rerun()

        with tab_tools:
            # أدوات البروكر الحسابية
            st.write("### 🧮 حاسبة سريعة")
            price = st.number_input("سعر الوحدة", value=1000000)
            years = st.slider("سنوات التقسيط", 1, 15, 8)
            st.success(f"القسط الشهري التقريبي: {(price/(years*12)):,.0f} ج.م")

    # --- صفحة المطور (Developer Details) ---
    elif st.session_state.page == "details":
        if st.button("🔙 العودة للقائمة"):
            st.session_state.page = "main"
            st.rerun()

        selected_dev = st.session_state.selected_dev
        st.markdown(f"""
            <div class="dev-profile-header">
                <h1 style='color:#000;'>🏢 {selected_dev}</h1>
                <p style='color:#555;'>هذه الصفحة مخصصة لعرض مشاريع المطور <b>{selected_dev}</b> وكافة تفاصيله.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.subheader("🏗️ قائمة المشاريع:")
        projects = df[df[dev_col] == selected_dev][proj_col].unique()
        
        # عرض المشاريع في عمودين
        p_cols = st.columns(2)
        for idx, p_name in enumerate(projects):
            with p_cols[idx % 2]:
                st.markdown(f'<div class="project-card">🔹 {p_name}</div>', unsafe_allow_html=True)

else:
    st.error("⚠️ لم يتم العثور على بيانات في ملف الـ CSV.")
