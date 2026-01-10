import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (نمط الشطرنج + تنسيق أزرار التحكم)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #121212; 
    }

    /* إلغاء المسافات في شبكة المطورين */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; padding: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    div.block-container { padding: 0rem !important; }

    /* تصميم أزرار المطورين (المربعات المتلاصقة) */
    .dev-btn button {
        width: 100% !important; 
        height: 180px !important; 
        aspect-ratio: 1 / 1 !important;
        border: 0.2px solid rgba(0,0,0,0.1) !important;
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        text-transform: uppercase;
        transition: 0.2s;
    }

    /* توزيع ألوان الشطرنج */
    .white-btn button { background-color: #ffffff !important; color: #000000 !important; }
    .yellow-btn button { background-color: #f59e0b !important; color: #000000 !important; }

    /* أزرار التحكم (العودة، السابق، التالي) - صغيرة ومتباعدة */
    .control-btn button {
        height: 40px !important;
        width: auto !important;
        background-color: #333 !important;
        color: white !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        margin: 20px 5px !important; /* تباعد عن الشبكة */
        border: 1px solid #f59e0b !important;
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 20px; text-align: center;
        border-bottom: 5px solid #f59e0b; font-weight: 900; font-size: 2.2rem;
    }
    
    /* مسافة للبحث */
    .search-area { padding: 20px; background: #1a1a1a; margin-bottom: 0px; }
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
    
    # منطقة التحكم العلوية (متباعدة)
    st.write("")
    col_back, col_search = st.columns([1, 5])
    with col_back:
        st.markdown('<div class="control-btn">', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back"): 
            st.session_state.view = 'home'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_search:
        search = st.text_input("", placeholder="🔍 ابحث عن مطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة جهة اليمين
    col_grid, col_empty = st.columns([0.7, 0.3])

    with col_grid:
        items = 12 
        start = st.session_state.page * items
        current_devs = unique_devs[start : start + items]

        # منطق الشطرنج (Checkerboard)
        for i in range(0, len(current_devs), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(current_devs):
                    dev_name = current_devs[i + j]
                    # تحديد اللون بناءً على الصف والعمود (i/4 هو رقم الصف، j هو رقم العمود)
                    row_idx = i // 4
                    if (row_idx + j) % 2 == 0:
                        color_class = "white-btn"
                    else:
                        color_class = "yellow-btn"
                    
                    with cols[j]:
                        st.markdown(f'<div class="dev-btn {color_class}">', unsafe_allow_html=True)
                        if st.button(str(dev_name), key=f"d_{start+i+j}"):
                            st.sidebar.markdown(f"### 🏗️ {dev_name}")
                            projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                            for p in projs: st.sidebar.write(f"• {p}")
                        st.markdown('</div>', unsafe_allow_html=True)

        # أزرار التنقل (متباعدة وصغيرة)
        st.markdown("<div style='height:40px;'></div>", unsafe_allow_html=True) # تباعد إضافي
        n1, n2, n3 = st.columns([1, 2, 1])
        with n1:
            st.markdown('<div class="control-btn">', unsafe_allow_html=True)
            if st.button("⬅️ السابق", key="p_p") and st.session_state.page > 0:
                st.session_state.page -= 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with n3:
            st.markdown('<div class="control-btn">', unsafe_allow_html=True)
            if st.button("التالي ➡️", key="n_p") and (start + items) < len(unique_devs):
                st.session_state.page += 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    st.markdown('<div class="control-btn">', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="bt"): st.session_state.view = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
