import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (توحيد المقاسات بالبكسل لضمان عدم التغير)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #121212; 
    }

    /* توحيد حاوية الأزرار لمنع الفوارق */
    div.stButton {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 0px;
    }

    /* الزر بمقاس ثابت لا يتغير بطول الكلمة */
    div.stButton > button {
        width: 100% !important; /* يأخذ كامل عرض العمود الموحد */
        min-width: 200px !important; 
        max-width: 300px !important;
        height: 200px !important; /* ارتفاع ثابت إجباري */
        
        border: none !important;
        border-radius: 20px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.3s ease-in-out;
        box-shadow: 0px 8px 20px rgba(0,0,0,0.5) !important;
        overflow: hidden !important; /* منع النص الطويل من تخريب المقاس */
    }

    /* الألوان التبادلية (أبيض وأصفر) */
    div.stButton > button[key*="even_"] { background-color: #ffffff !important; color: #000000 !important; }
    div.stButton > button[key*="odd_"] { background-color: #f59e0b !important; color: #000000 !important; }

    div.stButton > button:hover {
        transform: translateY(-10px) !important;
        filter: brightness(1.1);
        box-shadow: 0px 12px 25px rgba(245, 158, 11, 0.4) !important;
    }

    /* تنسيق النص داخل الكارت الموحد */
    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 1.4rem !important;
        line-height: 1.2 !important;
        text-align: center !important;
        white-space: normal !important; /* السماح بنزول السطر بدلاً من تمديد الزر */
        word-break: break-word !important;
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

# --- المنطق الرئيسي ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢\nدليل المطورين", key="main_dev"): st.session_state.view = 'companies'; st.rerun()
    with c2:
        if st.button("🛠️\nأدوات البروكر", key="main_tool"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المطورين</div>', unsafe_allow_html=True)
    
    b1, b2 = st.columns([1, 5])
    if b1.button("🔙 عودة", key="back"): st.session_state.view = 'home'; st.rerun()
    search = b2.text_input("", placeholder="🔍 ابحث عن المطور...")

    unique_devs = df[dev_col].dropna().unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # الشبكة: 4 أعمدة بمقاسات ثابتة
    items_per_page = 12
    start = st.session_state.page * items_per_page
    current_devs = unique_devs[start : start + items_per_page]

    st.markdown("<br>", unsafe_allow_html=True)
    
    # السر هنا: تقسيم الأعمدة وتكرار الصفوف
    for i in range(0, len(current_devs), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(current_devs):
                dev_name = current_devs[i + j]
                tag = "even" if (i + j) % 2 == 0 else "odd"
                with cols[j]:
                    # الأزرار ستأخذ نفس الحجم بفضل الـ CSS الإجباري
                    if st.button(str(dev_name), key=f"{tag}_{start+i+j}"):
                        st.sidebar.markdown(f"### 🏢 {dev_name}")
                        projs = df[df[dev_col] == dev_name].iloc[:, 0].unique()
                        for p in projs: st.sidebar.write(f"✅ {p}")

    # أزرار الصفحات
    st.markdown("<br>", unsafe_allow_html=True)
    n1, n2, n3 = st.columns([1, 2, 1])
    if n1.button("⬅️ السابق", key="prev") and st.session_state.page > 0:
        st.session_state.page -= 1; st.rerun()
    if n3.button("التالي ➡️", key="next") and (start + items_per_page) < len(unique_devs):
        st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="back_t"): st.session_state.view = 'home'; st.rerun()
