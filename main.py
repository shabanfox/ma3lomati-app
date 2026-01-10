import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (مربعات متساوية 1:1 + تراص مطلق)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #121212; 
    }

    /* إلغاء المسافات تماماً لجعلها شبكة واحدة */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; padding: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    div.block-container { padding: 0rem !important; }

    /* إجبار الزر على شكل مربع 1*1 */
    div.stButton > button {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important; /* طول يساوي العرض دائماً */
        border: 0.5px solid rgba(0,0,0,0.2) !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.2s;
        overflow: hidden !important; /* يمنع الكلام من تمطيط المربع */
    }

    /* الألوان التبادلية */
    div.stButton > button[key*="even_"] { background-color: #ffffff !important; color: #000 !important; }
    div.stButton > button[key*="odd_"] { background-color: #f59e0b !important; color: #000 !important; }

    div.stButton > button:hover {
        filter: brightness(1.2);
        z-index: 10;
        transform: scale(1.0);
    }

    /* تنسيق النص ليناسب المربع */
    div.stButton > button p {
        font-weight: 900 !important;
        font-size: clamp(0.8rem, 2vw, 1.3rem) !important; /* حجم خط مرن يتناسب مع المربع */
        line-height: 1.2 !important;
        text-align: center !important;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 3; /* يظهر 3 أسطر كحد أقصى ثم نقاط */
        -webkit-box-orient: vertical;
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 25px; text-align: center;
        border-bottom: 5px solid #f59e0b; font-weight: 900; font-size: 2.5rem;
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
        return pd.DataFrame(columns=['Developer', 'Project'])

df = load_data()
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0

# --- الصفحات ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢\nدليل المطورين", key="m1"): st.session_state.view = 'companies'; st.rerun()
    with c2:
        if st.button("🛠️\nأدوات البروكر", key="m2"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المطورين</div>', unsafe_allow_html=True)
    
    # البحث
    b1, b2 = st.columns([1, 6])
    if b1.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
    search = b2.text_input("", placeholder="🔍 ابحث عن مطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة 1*1 جهة اليمين (70% من الشاشة)
    col_grid, col_empty = st.columns([0.7, 0.3])

    with col_grid:
        items = 12 # عرض 12 مطور في الصفحة (3 صفوف * 4 أعمدة)
        start = st.session_state.page * items
        current_devs = unique_devs[start : start + items]

        # رسم الشبكة المربعة المتلاصقة
        for i in range(0, len(current_devs), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(current_devs):
                    dev_name = current_devs[i + j]
                    color_tag = "even" if (i + j) % 2 == 0 else "odd"
                    with cols[j]:
                        if st.button(str(dev_name), key=f"{color_tag}_{start+i+j}"):
                            st.sidebar.markdown(f"### 🏗️ {dev_name}")
                            projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                            for p in projs: st.sidebar.write(f"• {p}")

        # أزرار التنقل
        st.write("")
        n1, n2, n3 = st.columns([1, 2, 1])
        if n1.button("⬅️ السابق", key="prev_p") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        if n3.button("التالي ➡️", key="next_p") and (start + items) < len(unique_devs):
            st.session_state.page += 1; st.rerun()
