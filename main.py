import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (تطبيق صارم للألوان والترتيب)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء أي زوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الخلفية سوداء غامقة والكتابة بيضاء */
    html, body, [data-testid="stAppViewContainer"] { 
        background-color: #000000 !important; 
        direction: RTL; 
        font-family: 'Cairo', sans-serif;
    }
    
    /* إجبار لون الخط الأبيض في كل مكان */
    h1, h2, h3, p, span, div, label { color: #ffffff !important; }

    /* إلغاء المسافات بين الأعمدة لشبكة المطورين */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    div.block-container { padding: 0rem !important; }

    /* الكروت الصفراء 1*1 */
    div.stButton > button[key^="dev_"] {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 180px !important;
        background-color: #FFD700 !important; /* أصفر ذهبي */
        color: #000000 !important; /* كتابة سوداء داخل الأصفر */
        border: 1px solid #000000 !important;
        border-radius: 0px !important;
        font-weight: 900 !important;
        font-size: 1.3rem !important;
        margin: 0px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* أزرار التحكم (التالي والسابق) في المنتصف وجنب بعض */
    .control-center-box {
        display: flex;
        justify-content: center; /* توسيط أفقي */
        gap: 0px; /* جعلهم بجانب بعض تماماً */
        padding: 50px 0;
    }

    .nav-btn button {
        height: 40px !important;
        width: 120px !important;
        background-color: #222 !important;
        color: #ffffff !important;
        border: 1px solid #ffffff !important;
        font-size: 0.9rem !important;
        border-radius: 0px !important; /* حواف حادة لتناسب التصميم */
    }
    
    /* مربع البحث */
    input { background-color: #111 !important; color: white !important; border: 1px solid #333 !important; }
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
    st.markdown('<h1 style="text-align:center; padding:50px;">منصة معلوماتى</h1>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("🏢 دليل المطورين", key="h1"): st.session_state.view = 'companies'; st.rerun()
    with c2: 
        if st.button("🛠️ أدوات البروكر", key="h2"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<h2 style="text-align:center; padding:20px; background:#111;">دليل المطورين</h2>', unsafe_allow_html=True)
    
    # صف البحث والعودة
    col_back, col_search = st.columns([1, 4])
    with col_back:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col_search:
        search = st.text_input("", placeholder="🔍 ابحث عن مطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة جهة اليمين (70%)
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

    # --- أزرار التالي والسابق جنب بعض في نص الصفحة ---
    st.write("<div style='height:100px;'></div>", unsafe_allow_html=True) # تباعد
    
    # استخدام columns لتوسيط الأزرار
    _, center_box, _ = st.columns([2, 1, 2])
    with center_box:
        # أزرار بجانب بعض تماماً
        c_prev, c_next = st.columns(2)
        with c_prev:
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if st.button("⬅️ السابق", key="prev_p") and st.session_state.page > 0:
                st.session_state.page -= 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with c_next:
            st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
            if (start + items) < len(unique_devs):
                if st.button("التالي ➡️", key="next_p"):
                    st.session_state.page += 1; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<h2 style="text-align:center;">🛠️ أدوات البروكر</h2>', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="b"): st.session_state.view = 'home'; st.rerun()
