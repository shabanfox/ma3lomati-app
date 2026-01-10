import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (توحيد الأبعاد + نظام الألوان التبادلي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #121212; /* خلفية داكنة جداً للفخامة */
    }

    /* توحيد حاوية الأعمدة */
    [data-testid="column"] {
        padding: 5px !important;
    }

    /* تصميم الكروت المتساوية */
    div.stButton > button {
        width: 100% !important; 
        height: 200px !important; /* ارتفاع ثابت وموحد للكل */
        border: none !important;
        border-radius: 20px !important; /* حواف دائرية واضحة */
        transition: all 0.3s ease;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        box-shadow: 0px 10px 20px rgba(0,0,0,0.5) !important;
        padding: 20px !important;
    }

    /* تأثير الوقوف على الكارت */
    div.stButton > button:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0px 15px 30px rgba(245, 158, 11, 0.3) !important;
        filter: brightness(1.1);
    }

    /* البرمجة اللونية: أبيض وأصفر بالتناوب */
    /* نستخدم الكي (key) للتحكم في اللون */
    div.stButton > button[key*="colorW"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    
    div.stButton > button[key*="colorY"] {
        background-color: #f59e0b !important; /* لون أصفر/ذهبي */
        color: #000000 !important;
    }

    /* تنسيق النص داخل الكارت */
    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        line-height: 1.2 !important;
        word-wrap: break-word !important;
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 20px; text-align: center;
        border-bottom: 5px solid #f59e0b; font-weight: 900; font-size: 2.2rem;
        margin-bottom: 30px;
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
        return pd.DataFrame(columns=['Developer'])

df = load_data()
# تحديد اسم عمود المطور بذكاء
dev_col = 'Developer' if 'Developer' in df.columns else df.columns[1]

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0

# --- منطق العرض ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢\nدليل المطورين", key="main_dev"): 
            st.session_state.view = 'companies'
            st.rerun()
    with c2:
        if st.button("🛠️\nأدوات البروكر", key="main_tool"): 
            st.session_state.view = 'tools'
            st.rerun()

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المطورين العقاريين</div>', unsafe_allow_html=True)
    
    # صف البحث والعودة
    b1, b2 = st.columns([1, 5])
    if b1.button("🔙 عودة", key="back_home"): 
        st.session_state.view = 'home'
        st.rerun()
    search = b2.text_input("", placeholder="🔍 ابحث عن المطور...")

    unique_devs = df[dev_col].unique()
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]

    # رسم الشبكة (4 كروت في السطر لتطابق الصورة)
    items_per_page = 12
    start_idx = st.session_state.page * items_per_page
    subset = unique_devs[start_idx : start_idx + items_per_page]

    # حاوية الشبكة
    st.markdown("<br>", unsafe_allow_html=True)
    for i in range(0, len(subset), 4):
        cols = st.columns(4)
        for j in range(4):
            if i + j < len(subset):
                dev_name = subset[i + j]
                # تحديد اللون بالتبادل (أبيض أو أصفر)
                color_type = "colorW" if (i + j) % 2 == 0 else "colorY"
                with cols[j]:
                    # استخدام مفتاح (key) يحتوي على نوع اللون ليتم تلوينه بالـ CSS
                    if st.button(dev_name, key=f"dev_{color_type}_{start_idx+i+j}"):
                        st.sidebar.markdown(f"## 🏢 {dev_name}")
                        # عرض مشاريع المطور في السايدبار
                        projs = df[df[dev_col] == dev_name].iloc[:, 0].tolist()
                        for p in projs: st.sidebar.write(f"🔹 {p}")

    # التنقل بين الصفحات
    st.markdown("<br>", unsafe_allow_html=True)
    p1, p2, p3 = st.columns([1, 2, 1])
    if p1.button("⬅️ السابق") and st.session_state.page > 0:
        st.session_state.page -= 1; st.rerun()
    if p3.button("التالي ➡️") and (start_idx + items_per_page) < len(unique_devs):
        st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة", key="back_from_tools"): 
        st.session_state.view = 'home'
        st.rerun()
