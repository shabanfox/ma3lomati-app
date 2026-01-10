import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (لتحقيق الشطرنج، التصغير، والتباعد)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #121212; 
    }

    /* --- شبكة المطورين المتلاصقة --- */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* الزر المربع 1*1 */
    .dev-card button {
        width: 100% !important; 
        height: 180px !important;
        aspect-ratio: 1 / 1 !important;
        border: none !important;
        border-radius: 0px !important;
        margin: 0px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ألوان الشطرنج */
    .bg-white button { background-color: #ffffff !important; color: #000 !important; }
    .bg-yellow button { background-color: #f59e0b !important; color: #000 !important; }

    /* --- أزرار التحكم (العودة، التالي، السابق) --- */
    /* تصغير الحجم وإبعادها عن الشبكة */
    .control-btn-style button {
        height: 35px !important;
        width: 120px !important;
        background-color: #262626 !important;
        color: #f59e0b !important;
        border: 1px solid #f59e0b !important;
        font-size: 0.8rem !important;
        font-weight: 400 !important;
        border-radius: 5px !important;
        margin: 40px 10px !important; /* تباعد كبير عن الشبكة */
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 20px; text-align: center;
        border-bottom: 5px solid #f59e0b; font-weight: 900; font-size: 2.2rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

df = load_data()
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0

# --- التطبيق ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى</div>', unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🏢 دليل المطورين", key="go_devs"): st.session_state.view = 'companies'; st.rerun()
    with c2: 
        if st.button("🛠️ أدوات البروكر", key="go_tools"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المطورين</div>', unsafe_allow_html=True)
    
    # 1. زر العودة (مصغر ومبعد)
    st.markdown('<div class="control-btn-style">', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية", key="back_home"): st.session_state.view = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder="🔍 ابحث عن المطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # 2. شبكة المطورين (شطرنج)
    col_grid, col_empty = st.columns([0.7, 0.3])
    with col_grid:
        items = 12
        start = st.session_state.page * items
        current_devs = unique_devs[start : start + items]

        for i in range(0, len(current_devs), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(current_devs):
                    dev_name = current_devs[i + j]
                    # حساب الشطرنج: صف + عمود
                    row_idx = i // 4
                    color_class = "bg-white" if (row_idx + j) % 2 == 0 else "bg-yellow"
                    
                    with cols[j]:
                        st.markdown(f'<div class="dev-card {color_class}">', unsafe_allow_html=True)
                        if st.button(str(dev_name), key=f"d_{start+i+j}"):
                            st.sidebar.markdown(f"### 🏗️ {dev_name}")
                            projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                            for p in projs: st.sidebar.write(f"• {p}")
                        st.markdown('</div>', unsafe_allow_html=True)

    # 3. أزرار التنقل (مصغرة ومبعدة جداً في الأسفل)
    st.markdown("<br><br><br>", unsafe_allow_html=True) # تباعد إضافي
    n1, n2, n3 = st.columns([1, 4, 1])
    with n1:
        st.markdown('<div class="control-btn-style">', unsafe_allow_html=True)
        if st.button("⬅️ السابق", key="prev_btn") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        st.markdown('<div class="control-btn-style">', unsafe_allow_html=True)
        if (start + items) < len(unique_devs):
            if st.button("التالي ➡️", key="next_btn"):
                st.session_state.page += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
