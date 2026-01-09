import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (تحويل الزر إلى كارت احترافي حاد)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* العنوان الرئيسي العلوي */
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border-bottom: 6px solid #f59e0b; font-weight: 900; font-size: 2.5rem; margin-bottom: 20px;
    }

    /* السحر هنا: تحويل زر Streamlit لشكل كارت حاد ومربّع */
    div.stButton > button {
        width: 100% !important;
        height: 220px !important; /* طول الكارت */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 4px solid #000000 !important;
        border-radius: 0px !important; /* حواف حادة جداً */
        box-shadow: 8px 8px 0px #000 !important; /* ظل حاد أسود */
        padding: 0px !important;
        transition: 0.2s;
        display: block !important;
    }

    div.stButton > button:hover {
        border-color: #f59e0b !important;
        box-shadow: 8px 8px 0px #f59e0b !important;
        transform: translate(-3px, -3px);
    }

    /* تنسيق النصوص داخل الزر يدويًا عبر CSS (لجعلها تشبه الصورة) */
    /* بما أن زر ستريمليت لا يقبل HTML داخله، سنلعب بتنسيق النص الافتراضي */
    div.stButton > button p {
        font-family: 'Cairo', sans-serif;
        font-weight: 900 !important;
        font-size: 1.4rem !important; /* اسم المشروع */
        line-height: 1.4;
        margin: 10px !important;
        color: #000;
    }
    
    /* فلاتر البحث والمدخلات */
    .stTextInput input {
        border: 3px solid #000 !important;
        border-radius: 0px !important;
        font-weight: 900 !important;
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

# --- محتوى المنصة ---

if st.session_state.view == 'main':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 استعراض دليل المشاريع"):
            st.session_state.view = 'comp'
            st.rerun()
    with c2:
        if st.button("🛠️ فتح حاسبة الأدوات"):
            st.session_state.view = 'tools'
            st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="main-header">🏢 دليل المشاريع</div>', unsafe_allow_html=True)
    
    # شريط البحث والعودة
    col_back, col_search = st.columns([1, 3])
    with col_back:
        if st.button("🔙 عودة"):
            st.session_state.view = 'main'
            st.rerun()
    with col_search:
        q = st.text_input("🔍 ابحث عن مشروع أو مطور...")

    # فلترة البيانات
    df_f = df
    if q:
        df_f = df[df.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]

    st.markdown("---")

    # عرض الشبكة 3x3 (الأزرار التي تشبه الكروت)
    for i in range(0, len(df_f.head(15)), 3):
        grid = st.columns(3)
        for j in range(3):
            if i + j < len(df_f):
                row = df_f.iloc[i + j]
                with grid[j]:
                    # نص الزر منسق ليعطي إيحاء الكارت
                    # (اسم المشروع) + (المطور) + (السعر)
                    card_content = f"📌 {row[0]}\n───\n🏢 {row[2]}\n───\n💰 {row[4]}"
                    if st.button(card_content, key=f"p_{i+j}"):
                        st.session_state.selected_row = row
                        st.session_state.view = 'details'
                        st.rerun()

elif st.session_state.view == 'details':
    r = st.session_state.selected_row
    st.markdown(f'<div class="main-header">📍 تفاصيل {r[0]}</div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للشبكة"):
        st.session_state.view = 'comp'
        st.rerun()

    # تصميم صفحة التفاصيل بشكل حاد ونظيف
    st.markdown(f"""
    <div style="border:10px solid #000; padding:40px; background:#fff; text-align:center;">
        <h1 style="font-size:3.5rem; font-weight:900;">{r[0]}</h1>
        <h2 style="color:#f59e0b; font-size:2.5rem;">المطور: {r[2]}</h2>
        <hr style="border:2px solid #000">
        <h3 style="font-size:2rem;">الموقع: {r[3]}</h3>
        <div style="background:#000; color:#f59e0b; padding:20px; font-size:2.2rem; font-weight:900; margin-top:20px;">
            {r[4]}
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات الحاسبة</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.view = 'main'
        st.rerun()
    st.write("أضف هنا كود الحاسبة الذي تريده")
