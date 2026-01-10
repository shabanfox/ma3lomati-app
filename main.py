import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أسود وأبيض + كروت صفراء)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الخلفية سوداء غامقة والخط أبيض */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #000000 !important; color: #ffffff !important;
    }

    /* إلغاء الفواصل في شبكة المطورين */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    div.block-container { padding: 0rem !important; }

    /* تصميم كروت المطورين (كلها صفراء) */
    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 180px !important;
        background-color: #f59e0b !important; /* لون أصفر موحد */
        color: #000000 !important; /* خط أسود داخل الكارت */
        border: 0.5px solid #000000 !important; /* فواصل سوداء رقيقة */
        border-radius: 0px !important;
        margin: 0px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.3s;
    }

    div.stButton > button[key^="dev_"]:hover {
        background-color: #ffffff !important; /* ينور أبيض عند الوقوف عليه */
        transform: scale(0.98);
    }

    /* تصميم أزرار التحكم (السابق والتالي والعودة) */
    .control-center {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 20px;
        padding: 40px 0px;
    }

    .control-btn button {
        height: 40px !important;
        width: 120px !important;
        background-color: transparent !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
        font-size: 0.9rem !important;
    }

    .main-header {
        background: #000000; color: #ffffff; padding: 30px; text-align: center;
        border-bottom: 1px solid #333; font-weight: 900; font-size: 2.5rem;
    }
    
    /* تعديل لون نص البحث */
    input { color: white !important; background-color: #111 !important; border: 1px solid #333 !important; }
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

# --- منطق العرض ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">منصة معلوماتى</div>', unsafe_allow_html=True)
    st.write("<div style='height:150px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين", key="h_dev"): st.session_state.view = 'companies'; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر", key="h_tool"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">دليل المطورين</div>', unsafe_allow_html=True)

    # زر العودة متباعد
    st.write("")
    c_back, c_search = st.columns([1, 4])
    with c_back:
        st.markdown('<div class="control-btn">', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_search:
        search = st.text_input("", placeholder="🔍 ابحث عن اسم المطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # عرض الشبكة جهة اليمين
    col_grid, col_empty = st.columns([0.7, 0.3])

    with col_grid:
        items = 12
        start = st.session_state.page * items
        batch = unique_devs[start : start + items]

        for i in range(0, len(batch), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(batch):
                    dev_name = batch[i + j]
                    with cols[j]:
                        if st.button(str(dev_name), key=f"dev_{start+i+j}"):
                            st.sidebar.markdown(f"## {dev_name}")
                            projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                            for p in projs: st.sidebar.write(f"• {p}")

    # أزرار التنقل (في منتصف الصفحة تماماً)
    st.write("<div style='height:50px;'></div>", unsafe_allow_html=True)
    
    # استخدام حاوية مخصصة للتوسيط
    cont_p1, cont_p2, cont_p3 = st.columns([2, 1, 2])
    with cont_p2:
        st.markdown('<div style="display: flex; gap: 10px;">', unsafe_allow_html=True)
        col_n1, col_n2 = st.columns(2)
        with col_n1:
            st.markdown('<div class="control-btn">', unsafe_allow_html=True)
            if st.button("⬅️ السابق", key="prev") and st.session_state.page > 0:
                st.session_state.page -= 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with col_n2:
            st.markdown('<div class="control-btn">', unsafe_allow_html=True)
            if (start + items) < len(unique_devs):
                if st.button("التالي ➡️", key="next"):
                    st.session_state.page += 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    st.markdown('<div class="control-btn">', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="b_tool"): st.session_state.view = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
