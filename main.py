import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (نفس شكل الصورة - مقاسات موحدة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #121212; 
    }

    /* تصميم الكروت المتساوية تماماً */
    div.stButton > button {
        width: 100% !important; 
        height: 200px !important; /* طول ثابت لكل الكروت */
        border: none !important;
        border-radius: 20px !important;
        transition: all 0.3s ease;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        box-shadow: 0px 8px 15px rgba(0,0,0,0.4) !important;
        padding: 15px !important;
    }

    /* الألوان التبادلية بناءً على رقم الزر */
    /* الكروت البيضاء */
    div.stButton > button[key*="even_"] { background-color: #ffffff !important; color: #000000 !important; }
    /* الكروت الصفراء */
    div.stButton > button[key*="odd_"] { background-color: #f59e0b !important; color: #000000 !important; }

    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        filter: brightness(1.1);
    }

    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 1.6rem !important;
        line-height: 1.1 !important;
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 20px; text-align: center;
        border-bottom: 5px solid #f59e0b; font-weight: 900; font-size: 2.2rem;
        margin-bottom: 20px;
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

# تحديد اسم العمود (Developer)
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0

# --- منطق الصفحات ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button("🏢\nدليل المطورين", key="btn_home_dev"):
            st.session_state.view = 'companies'; st.rerun()
    with c2:
        if st.button("🛠️\nأدوات البروكر", key="btn_home_tool"):
            st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المطورين</div>', unsafe_allow_html=True)
    
    # شريط البحث
    col_b, col_s = st.columns([1, 5])
    if col_b.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
    search = col_s.text_input("", placeholder="🔍 ابحث عن اسم المطور هنا...")

    # تصفية المطورين
    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # عرض الشبكة 4 كروت في السطر (متساوية الطول والعرض)
    items_per_page = 12
    start = st.session_state.page * items_per_page
    current_devs = unique_devs[start : start + items_per_page]

    st.write("") # فاصل بسيط
    for i in range(0, len(current_devs), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(current_devs):
                dev_name = current_devs[i + j]
                # نظام الألوان التبادلي: زوجي = أبيض (even)، فردي = أصفر (odd)
                tag = "even" if (i + j) % 2 == 0 else "odd"
                with cols[j]:
                    if st.button(dev_name, key=f"{tag}_{start+i+j}"):
                        st.sidebar.markdown(f"### 🏢 {dev_name}")
                        projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                        for p in projs: st.sidebar.write(f"✅ {p}")

    # أزرار الصفحات
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1, 2, 1])
    if n1.button("⬅️ السابق") and st.session_state.page > 0:
        st.session_state.page -= 1; st.rerun()
    if n3.button("التالي ➡️") and (start + items_per_page) < len(unique_devs):
        st.session_state.page += 1; st.rerun()
