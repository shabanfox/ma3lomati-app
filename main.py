import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS مركز (لتحقيق الشطرنج والتباعد)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #121212; 
    }

    /* إلغاء الفواصل في شبكة المطورين */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* أزرار المطورين 1*1 */
    .stButton > button {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 180px !important;
        border: none !important;
        border-radius: 0px !important;
        margin: 0px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
    }

    /* تعريف ألوان الشطرنج */
    .white-cell button { background-color: #ffffff !important; color: #000 !important; }
    .yellow-cell button { background-color: #f59e0b !important; color: #000 !important; }

    /* تصميم أزرار التحكم (العودة - التالي - السابق) */
    .control-area {
        padding: 50px 20px; /* تباعد ضخم عن الشبكة */
        text-align: left; /* جعلها في اليسار */
    }
    
    .control-area button {
        height: 35px !important;
        width: 100px !important;
        font-size: 0.8rem !important;
        background-color: #333 !important;
        color: white !important;
        border: 1px solid #f59e0b !important;
        margin: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. تحميل البيانات
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

# --- الصفحات ---

if st.session_state.view == 'home':
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>🏠 منصة معلوماتى</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🏢 دخول دليل المطورين", key="h1"): st.session_state.view = 'companies'; st.rerun()
    with c2: 
        if st.button("🛠️ دخول الأدوات", key="h2"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    # زر العودة مصغر ومبعد
    st.markdown('<div class="control-area">', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    search = st.text_input("", placeholder="🔍 ابحث هنا...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة جهة اليمين 70%
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
                    # منطق الشطرنج الحقيقي
                    row_num = i // 4
                    col_num = j
                    color_class = "white-cell" if (row_num + col_num) % 2 == 0 else "yellow-cell"
                    
                    with cols[j]:
                        st.markdown(f'<div class="{color_class}">', unsafe_allow_html=True)
                        if st.button(str(dev_name), key=f"d_{start+i+j}"):
                            st.sidebar.info(f"مطور: {dev_name}")
                        st.markdown('</div>', unsafe_allow_html=True)

    # أزرار التنقل مصغرة ومبعدة في الأسفل جهة اليسار
    st.markdown('<div class="control-area">', unsafe_allow_html=True)
    n1, n2 = st.columns([1, 10]) # دفع الأزرار لليسار
    with n1:
        if st.button("⬅️ السابق", key="prev") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        if (start + items) < len(unique_devs):
            if st.button("التالي ➡️", key="next"):
                st.session_state.page += 1; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
