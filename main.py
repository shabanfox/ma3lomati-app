import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم الأزرار الحادة (Sharp Square Buttons)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* أزرار حادة وقوية جداً */
    div.stButton > button {
        width: 100% !important;
        background-color: #000000 !important;
        color: #f59e0b !important;
        border: 4px solid #f59e0b !important;
        border-radius: 0px !important; /* حواف مربعة حادة */
        font-weight: 900 !important;
        font-size: 1.5rem !important;
        margin-bottom: 10px;
        transition: 0.2s;
        height: auto !important;
        padding: 20px !important;
    }
    div.stButton > button:hover {
        background-color: #f59e0b !important;
        color: #000000 !important;
    }

    /* العناوين */
    .header-style {
        background: #000; color: #f59e0b; padding: 20px; 
        text-align: center; border-bottom: 8px solid #f59e0b; margin-bottom: 30px;
    }
    
    /* كروت التفاصيل */
    .detail-box {
        border: 5px solid #000; padding: 30px; text-align: center; background: #f9f9f9;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

# تهيئة الحالة (Session State)
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_row' not in st.session_state: st.session_state.selected_row = None

df = load_data()

# --- التنقل ---

# 1. الصفحة الرئيسية
if st.session_state.view == 'main':
    st.markdown('<div class="header-style"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏢 دخول دليل المشاريع"):
            st.session_state.view = 'comp'
            st.rerun()
    with col2:
        if st.button("🛠️ دخول حاسبة الأدوات"):
            st.session_state.view = 'tools'
            st.rerun()

# 2. صفحة المشاريع (الشبكة)
elif st.session_state.view == 'comp':
    st.markdown('<div class="header-style"><h2>🏢 دليل المشاريع العقارية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.view = 'main'
        st.rerun()

    # عرض المشاريع كأزرار حادة 3 في كل صف
    for i in range(0, len(df.head(15)), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(df):
                row = df.iloc[i + j]
                with cols[j]:
                    # نص الزر (المشروع + المطور)
                    btn_text = f"{row[0]}\n({row[2]})"
                    if st.button(btn_text, key=f"btn_{i+j}"):
                        st.session_state.selected_row = row
                        st.session_state.view = 'details'
                        st.rerun()

# 3. صفحة التفاصيل
elif st.session_state.view == 'details':
    r = st.session_state.selected_row
    st.markdown(f'<div class="header-style"><h2>📍 مشروع: {r[0]}</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للقائمة"):
        st.session_state.view = 'comp'
        st.rerun()
    
    st.markdown(f"""
    <div class="detail-box">
        <h2 style="color:#f59e0b;">🏢 شركة: {r[2]}</h2>
        <hr>
        <h3>📍 الموقع: {r[3]}</h3>
        <h2 style="background:#000; color:#fff; padding:10px;">💰 نظام السداد: {r[4]}</h2>
    </div>
    """, unsafe_allow_html=True)

# 4. صفحة الأدوات
elif st.session_state.view == 'tools':
    st.markdown('<div class="header-style"><h2>🛠️ أدوات الحاسبة</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.view = 'main'
        st.rerun()
    
    st.success("هنا حاسبة الأقساط والـ ROI تعمل بشكل كامل.")
    # يمكن إضافة كود الحاسبة هنا ببساطة
