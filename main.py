import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (التصميم اللي عجبك مع تعديل الحجم والمكان)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر */
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border: 4px solid #000; font-weight: 900; font-size: 2rem; margin-bottom: 30px;
    }

    /* أزرار النانو بالتصميم الأصلي (حواف حادة + ظل حاد) */
    div.stButton > button {
        width: 100% !important;
        height: 110px !important; /* حجم نانو مدمج */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        border-radius: 0px !important; /* حواف مربعة تماماً */
        box-shadow: 6px 6px 0px #000 !important; /* الظل اللي عجبك */
        padding: 5px !important;
        transition: 0.1s;
        display: block !important;
    }

    div.stButton > button:hover {
        background-color: #f59e0b !important;
        border-color: #000 !important;
        box-shadow: 3px 3px 0px #000 !important;
        transform: translate(2px, 2px);
    }

    /* تنسيق النص داخل زر الكارت */
    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 1rem !important;
        line-height: 1.2;
        color: #000;
        margin: 0 !important;
    }
    
    /* تقليل الفجوات بين الكروت */
    [data-testid="column"] {
        padding: 5px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_row' not in st.session_state: st.session_state.selected_row = None

df = load_data()

# --- المحتوى ---

if st.session_state.view == 'main':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى</div>', unsafe_allow_html=True)
    
    # التقسيم: اليمين للأزرار (60%) واليسار فارغ (40%)
    col_right, col_left = st.columns([0.6, 0.4])

    with col_right:
        # عرض 9 مشاريع فقط في شبكة 3x3 متقاربة جداً
        for i in range(0, 9, 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    with grid[j]:
                        # محتوى الزر (المشروع + المطور)
                        card_text = f"📌 {row[0]}\n{row[2]}"
                        if st.button(card_text, key=f"n_{i+j}"):
                            st.session_state.selected_row = row
                            st.session_state.view = 'details'
                            st.rerun()

elif st.session_state.view == 'details':
    r = st.session_state.selected_row
    st.markdown(f'<div class="main-header">📍 تفاصيل {r[0]}</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للشبكة"):
        st.session_state.view = 'main'
        st.rerun()

    st.markdown(f"""
    <div style="border:8px solid #000; padding:30px; background:#fff; box-shadow: 15px 15px 0px #f59e0b;">
        <h1 style="font-weight:900;">{r[0]}</h1>
        <h2 style="color:#f59e0b;">المطور: {r[2]}</h2>
        <hr style="border:2px solid #000">
        <h3>الموقع: {r[3]}</h3>
        <div style="background:#000; color:#fff; padding:15px; font-size:1.5rem; font-weight:900;">
            💰 السداد: {r[4]}
        </div>
    </div>
    """, unsafe_allow_html=True)
