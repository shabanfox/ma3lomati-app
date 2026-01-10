import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS الملكي (أزرار 3D متلاصقة)
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

    /* إزالة الفواصل تماماً لجعل الأزرار متلاصقة */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* أزرار المطورين 3D الضخمة */
    div.stButton > button {
        width: 100% !important; 
        height: 140px !important; 
        background-color: #ffffff !important; 
        color: #000 !important;
        border: 2px solid #000 !important; 
        border-radius: 0px !important;
        margin: 0px !important;
        transition: 0.1s;
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
        font-size: 1.5rem !important;
    }

    /* أزرار الهوم الرئيسية */
    .home-btn button {
        height: 250px !important; font-size: 2.5rem !important;
        border: 10px solid #000 !important; box-shadow: 15px 15px 0px #f59e0b !important;
    }

    .filter-box {
        background: #f9f9f9; padding: 15px; border: 3px solid #000; margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات ومعالجتها بشكل ذكي
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['Project','Developer','Location','Payment'])

df = load_data()

# البحث عن العمود الصحيح (إما Developer أو المطور)
def get_col_name(possible_names, default_idx):
    for name in possible_names:
        if name in df.columns:
            return name
    return df.columns[default_idx] if len(df.columns) > default_idx else df.columns[0]

dev_col = get_col_name(['Developer', 'المطور', 'الشركة'], 1)
proj_col = get_col_name(['Project', 'المشروع', 'الاسم'], 0)
loc_col = get_col_name(['Location', 'الموقع', 'المنطقة'], 2)

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0

# --- محرك التطبيق ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🏢\nدليل المطورين"): st.session_state.view = 'companies'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المطورين العقاريين</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        f1, f2, f3 = st.columns([1, 3, 2])
        if f1.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
        search_q = f2.text_input("", placeholder=f"🔍 ابحث عن {dev_col}...")
        
        all_devs = sorted(df[dev_col].dropna().unique())
        selected_dev = f3.selectbox("🏢 تصفية القائمة", ["الكل"] + list(all_devs))
        st.markdown('</div>', unsafe_allow_html=True)

    # تطبيق الفلترة
    df_f = df
    if search_q:
        df_f = df_f[df_f[dev_col].astype(str).str.contains(search_q, case=False, na=False)]
    if selected_dev != "الكل":
        df_f = df_f[df_f[dev_col] == selected_dev]

    # عرض الشبكة 60% يمين
    col_grid, col_empty = st.columns([0.6, 0.4])

    with col_grid:
        unique_devs_filtered = df_f[dev_col].unique()
        items = 9
        start = st.session_state.page * items
        current_batch = unique_devs_filtered[start : start + items]

        for i in range(0, len(current_batch), 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(current_batch):
                    dev_name = current_batch[i + j]
                    with grid[j]:
                        if st.button(str(dev_name), key=f"dev_{start+i+j}"):
                            # عرض المشاريع في الجانب
                            projects = df[df[dev_col] == dev_name]
                            st.sidebar.markdown(f"### 🏗️ مشاريع {dev_name}")
                            for _, row in projects.iterrows():
                                st.sidebar.write(f"• **{row[proj_col]}** ({row[loc_col]})")
        
        # أزرار التنقل
        st.write("")
        n1, n2, n3 = st.columns([1, 1, 1])
        if n1.button("⬅️ السابق") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        n2.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if n3.button("التالي ➡️") and (start + items) < len(unique_devs_filtered):
            st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'home'; st.rerun()
    st.success("الأدوات المالية جاهزة.")
