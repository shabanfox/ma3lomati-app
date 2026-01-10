import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (تركيز كامل على اسم المطور + تأثير 3D)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 20px; text-align: center;
        border-bottom: 8px solid #f59e0b; font-weight: 900; font-size: 2.5rem;
    }

    /* إزالة المسافات تماماً لجعل الأزرار متلاصقة */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* أزرار أسماء المطورين 3D */
    div.stButton > button {
        width: 100% !important; 
        height: 140px !important; 
        background-color: #ffffff !important; 
        color: #000 !important;
        border: 2px solid #000 !important; 
        border-radius: 0px !important;
        margin: 0px !important;
        transition: 0.1s;
        
        /* تأثير الـ 3D الحاد */
        box-shadow: 6px 6px 0px #f59e0b, 12px 12px 0px #000;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button:hover {
        background-color: #000 !important;
        color: #f59e0b !important;
        transform: translate(-4px, -4px);
        box-shadow: 10px 10px 0px #f59e0b, 18px 18px 0px #333;
        z-index: 10;
        position: relative;
    }

    div.stButton > button p {
        font-weight: 900 !important; 
        font-size: 1.4rem !important; /* تكبير اسم المطور ليكون واضحاً */
        line-height: 1.2;
        text-align: center !important;
    }

    /* أزرار الهوم الرئيسية */
    .home-btn button {
        height: 250px !important; font-size: 2.5rem !important;
        border: 8px solid #000 !important; box-shadow: 15px 15px 0px #f59e0b !important;
    }

    /* قسم الفلاتر */
    .filter-box {
        background: #f9f9f9; padding: 15px; border: 3px solid #000; margin-bottom: 10px;
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
        return pd.DataFrame(columns=['المشروع','المطور','الموقع','السداد'])

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0
df = load_data()

# --- محتوى المنصة ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🏢\nدليل الشركات"): st.session_state.view = 'companies'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المطورين العقاريين</div>', unsafe_allow_html=True)
    
    # البحث والفلاتر
    with st.container():
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        f1, f2, f3 = st.columns([1, 3, 2])
        if f1.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
        search_q = f2.text_input("", placeholder="🔍 ابحث عن اسم المطور...")
        # استخراج المطورين الفريدين للفلترة
        devs_list = ["الكل"] + list(df['المطور'].unique() if 'المطور' in df.columns else [])
        selected_dev = f3.selectbox("🏢 تصفية حسب المطور", devs_list)
        st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق الفلاتر
    df_f = df
    if search_q:
        df_f = df_f[df_f['المطور'].str.contains(search_q, case=False, na=False)]
    if selected_dev != "الكل":
        df_f = df_f[df_f['المطور'] == selected_dev]

    # عرض الشبكة (60% يمين للأزرار المتلاصقة)
    col_grid, col_empty = st.columns([0.6, 0.4])

    with col_grid:
        items = 9
        # استخراج المطورين من البيانات المفلترة لعرضهم كأزرار
        unique_devs = df_f['المطور'].unique()
        start = st.session_state.page * items
        current_devs = unique_devs[start : start + items]

        for i in range(0, len(current_devs), 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    dev_name = current_devs[i + j]
                    with grid[j]:
                        if st.button(dev_name, key=f"dev_{start+i+j}"):
                            # عرض مشاريع هذا المطور في الجانب عند الضغط
                            dev_projects = df[df['المطور'] == dev_name]
                            st.sidebar.markdown(f"### 🏢 مطور: {dev_name}")
                            for idx, p_row in dev_projects.iterrows():
                                st.sidebar.write(f"🔹 **{p_row['المشروع']}** - {p_row['الموقع']}")
                            st.sidebar.divider()

        # أزرار التنقل
        st.write("")
        n1, n2, n3 = st.columns([1, 1, 1])
        if n1.button("⬅️ السابق") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        n2.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if n3.button("التالي ➡️") and (start + items) < len(unique_devs):
            st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'home'; st.rerun()
    st.success("الأدوات المالية جاهزة للعمل.")
