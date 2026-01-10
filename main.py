import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS احترافي (Premium UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    @import url('https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.1/font/bootstrap-icons.css');

    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #050505; /* خلفية سوداء عميقة */
    }

    /* --- شبكة المطورين (المربعات المتلاصقة 1*1) --- */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* تصميم الزر المربع كأنه كارت فخم */
    div.stButton > button {
        width: 100% !important; 
        aspect-ratio: 1 / 1 !important;
        height: 180px !important;
        border: 0.1px solid rgba(255,255,255,0.05) !important;
        border-radius: 0px !important;
        margin: 0px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.4s ease;
        box-shadow: inset 0px 0px 20px rgba(0,0,0,0.2) !important;
    }

    /* نمط الشطرنج بألوان مطفية (Matte) */
    div.stButton > button[key*="even_"] { background-color: #ffffff !important; color: #1a1a1a !important; }
    div.stButton > button[key*="odd_"] { background-color: #eab308 !important; color: #1a1a1a !important; }

    div.stButton > button:hover {
        filter: brightness(1.2);
        transform: scale(0.98);
        z-index: 10;
        box-shadow: 0px 0px 30px rgba(234, 179, 8, 0.2) !important;
    }

    /* تنسيق النص (الاسم) */
    div.stButton > button p {
        font-weight: 800 !important;
        font-size: 1.1rem !important;
        margin-top: 10px !important;
        letter-spacing: 0.5px;
    }

    /* --- أزرار التحكم (صغيرة جداً ومبعدة) --- */
    .control-container {
        padding: 40px 20px;
        display: flex;
        justify-content: flex-start;
        gap: 20px;
    }
    
    .small-btn button {
        height: 30px !important;
        width: 80px !important;
        background-color: transparent !important;
        color: #eab308 !important;
        border: 1px solid #eab308 !important;
        font-size: 0.7rem !important;
        border-radius: 4px !important;
    }

    .main-header {
        padding: 30px; text-align: center;
        background: linear-gradient(180deg, #111, #050505);
        border-bottom: 2px solid #eab308;
        margin-bottom: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. تحميل البيانات
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

# --- العرض ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header"><h1 style="color:#eab308;">منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<div style='height:150px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 دليل المطورين", key="h_dev"): st.session_state.view = 'companies'; st.rerun()
    with c2:
        if st.button("🛠️ الأدوات", key="h_tool"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    # هيدر الصفحة
    st.markdown('<div class="main-header"><h2 style="color:#eab308; margin:0;">دليل المطورين العقاريين</h2></div>', unsafe_allow_html=True)

    # صف أزرار التحكم (العودة والبحث) متباعدين
    st.write("")
    c_back, c_search = st.columns([1, 6])
    with c_back:
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        if st.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c_search:
        search = st.text_input("", placeholder="🔍 ابحث عن المطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة المتلاصقة (70% يمين)
    col_grid, col_empty = st.columns([0.7, 0.3])

    with col_grid:
        items = 12
        start = st.session_state.page * items
        current_batch = unique_devs[start : start + items]

        for i in range(0, len(current_batch), 4):
            cols = st.columns(4)
            for j in range(4):
                if i + j < len(current_batch):
                    dev_name = current_batch[i + j]
                    # منطق الشطرنج الإحترافي
                    row = i // 4
                    tag = "even" if (row + j) % 2 == 0 else "odd"
                    
                    with cols[j]:
                        # إضافة أيقونة رمزية (لوجو) فوق الاسم
                        icon = "🏢" if tag == "even" else "🏗️"
                        btn_text = f"{icon}\n\n{dev_name}"
                        if st.button(btn_text, key=f"{tag}_{start+i+j}"):
                            st.sidebar.markdown(f"### {dev_name}")
                            projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                            for p in projs: st.sidebar.write(f"• {p}")

    # أزرار التنقل (صغيرة جداً في الأسفل)
    st.write("<div style='height:50px;'></div>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1, 8, 1])
    with n1:
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        if st.button("⬅️ السابق", key="p_v") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with n3:
        st.markdown('<div class="small-btn">', unsafe_allow_html=True)
        if (start + items) < len(unique_devs):
            if st.button("التالي ➡️", key="n_v"):
                st.session_state.page += 1; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
