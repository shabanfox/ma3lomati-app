import streamlit as st
import pandas as pd

# 1. إعدادات المنصة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. هندسة التصميم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #0f0f0f; color: white;
    }

    /* إلغاء الفراغات تماماً بين الكروت */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }
    div.block-container { padding: 0rem !important; }

    /* تصميم كارت المطور 1*1 */
    .dev-tile button {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 180px !important;
        border: none !important;
        border-radius: 0px !important;
        margin: 0px !important;
        font-weight: 900 !important;
        font-size: 1.2rem !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ألوان الشطرنج الذكية */
    .tile-white button { background-color: #ffffff !important; color: #000 !important; }
    .tile-yellow button { background-color: #f59e0b !important; color: #000 !important; }

    .dev-tile button:hover {
        transform: scale(0.95);
        filter: contrast(1.2);
        z-index: 5;
    }

    /* أزرار التحكم المصغرة والمبعدة */
    .nav-wrapper { padding: 30px; display: flex; gap: 10px; }
    
    .nav-btn button {
        height: 32px !important;
        width: 90px !important;
        background-color: transparent !important;
        color: #f59e0b !important;
        border: 1px solid #f59e0b !important;
        font-size: 0.75rem !important;
        border-radius: 4px !important;
        transition: 0.2s;
    }
    
    .nav-btn button:hover {
        background-color: #f59e0b !important;
        color: #000 !important;
    }

    .header-bar {
        background: linear-gradient(90deg, #000, #1a1a1a);
        padding: 20px; text-align: center;
        border-bottom: 4px solid #f59e0b;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب ومعالجة البيانات
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

# --- المحرك الرئيسي ---

if st.session_state.view == 'home':
    st.markdown('<div class="header-bar"><h1 style="color:#f59e0b; margin:0;">منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
    st.write("<div style='height:150px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 استعراض المطورين", key="main_1"): st.session_state.view = 'companies'; st.rerun()
    with c2:
        if st.button("🛠️ الأدوات العقارية", key="main_2"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="header-bar"><h2 style="color:#f59e0b; margin:0;">دليل المطورين</h2></div>', unsafe_allow_html=True)

    # صف العودة والبحث
    st.write("")
    h1, h2 = st.columns([1, 4])
    with h1:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with h2:
        search = st.text_input("", placeholder="🔍 ابحث عن المطور (مثلاً: Mountain View)...")

    # تصفية البيانات
    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة الملكية (70% يمين)
    col_grid, col_sidebar = st.columns([0.7, 0.3])

    with col_grid:
        items = 12
        start = st.session_state.page * items
        batch = unique_devs[start : start + items]

        for i in range(0, len(batch), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(batch):
                    dev_name = batch[i + j]
                    # منطق الشطرنج الإحترافي
                    row_idx = i // 4
                    color_tag = "tile-white" if (row_idx + j) % 2 == 0 else "tile-yellow"
                    
                    with cols[j]:
                        st.markdown(f'<div class="dev-tile {color_tag}">', unsafe_allow_html=True)
                        if st.button(str(dev_name), key=f"btn_{start+i+j}"):
                            st.session_state.selected_dev = dev_name
                        st.markdown('</div>', unsafe_allow_html=True)

    # السايدبار لعرض المشاريع
    if 'selected_dev' in st.session_state:
        with col_sidebar:
            st.markdown(f"<div style='padding:20px; border-right:2px solid #f59e0b;'>", unsafe_allow_html=True)
            st.subheader(f"🏗️ {st.session_state.selected_dev}")
            projs = df[df[dev_col] == st.session_state.selected_dev].iloc[:, 0].unique()
            for p in projs: st.write(f"• {p}")
            st.markdown("</div>", unsafe_allow_html=True)

    # أزرار التنقل السفلية (مبعدة)
    st.write("<div style='height:60px;'></div>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1, 8, 1])
    with n1:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if st.button("⬅️ السابق", key="prev") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
        if (start + items) < len(unique_devs):
            if st.button("التالي ➡️", key="next"):
                st.session_state.page += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="header-bar"><h2 style="color:#f59e0b; margin:0;">🛠️ الأدوات</h2></div>', unsafe_allow_html=True)
    st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="tool_back"): st.session_state.view = 'home'; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.info("سيتم إضافة الحاسبة العقارية هنا قريباً.")
