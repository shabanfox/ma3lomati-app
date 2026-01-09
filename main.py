import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أزرار نانو متقاربة - نظام ملكي)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* العنوان العلوي */
    .nano-header {
        background: #000; color: #f59e0b; padding: 10px 25px; text-align: right;
        border-right: 10px solid #f59e0b; font-weight: 900; font-size: 1.8rem; margin-bottom: 20px;
    }

    /* تصميم أزرار النانو (Nano Buttons) */
    div.stButton > button {
        width: 100% !important;
        height: 100px !important; /* حجم صغير جداً */
        background-color: #000000 !important;
        color: #ffffff !important;
        border: 2px solid #f59e0b !important;
        border-radius: 0px !important; /* حواف حادة */
        padding: 5px !important;
        transition: 0.3s;
        display: block !important;
        margin-bottom: 0px !important;
    }

    div.stButton > button:hover {
        background-color: #f59e0b !important;
        color: #000000 !important;
        border-color: #000 !important;
        transform: scale(0.98);
    }

    /* تنسيق النص داخل زر النانو */
    div.stButton > button p {
        font-family: 'Cairo', sans-serif;
        font-weight: 900 !important;
        font-size: 0.9rem !important; /* نص صغير مدمج */
        line-height: 1.2;
        margin: 0px !important;
    }

    /* تقليل المسافات بين الأعمدة */
    [data-testid="column"] {
        padding: 5px !important;
    }
    
    /* صندوق التفاصيل */
    .detail-card {
        border: 4px solid #000; padding: 20px; background: #fff;
        box-shadow: 10px 10px 0px #f59e0b;
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
    st.markdown('<div class="nano-header">🏠 منصة معلوماتى | التحكم</div>', unsafe_allow_html=True)
    
    # تقسيم الصفحة: يمين (أزرار النانو)، يسار (مساحة فارغة أو تفاصيل)
    col_right, col_left = st.columns([0.6, 0.4])

    with col_right:
        st.markdown("<p style='font-weight:900;'>🏢 دليل المشاريع السريع (3x3)</p>", unsafe_allow_html=True)
        # عرض 9 أزرار فقط في شبكة 3x3
        for i in range(0, 9, 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    with grid[j]:
                        # محتوى الزر نانو (اسم المشروع + المطور)
                        nano_content = f"{row[0]}\n{row[2]}"
                        if st.button(nano_content, key=f"nano_{i+j}"):
                            st.session_state.selected_row = row
                            st.session_state.view = 'details'
                            st.rerun()
        
        # زر إضافي للأدوات أسفل الشبكة
        if st.button("🛠️ أدوات البروكر المستثمر", key="tools_btn"):
            st.session_state.view = 'tools'
            st.rerun()

    with col_left:
        st.info("💡 اضغط على أي كارت نانو من جهة اليمين لاستعراض كامل البيانات فوراً.")

elif st.session_state.view == 'details':
    r = st.session_state.selected_row
    st.markdown(f'<div class="nano-header">📍 {r[0]}</div>', unsafe_allow_html=True)
    
    col_back, col_content = st.columns([0.2, 0.8])
    with col_back:
        if st.button("🔙 عودة"):
            st.session_state.view = 'main'
            st.rerun()
    
    with col_content:
        st.markdown(f"""
        <div class="detail-card">
            <h1 style="font-weight:900; color:#000; border-bottom:3px solid #f59e0b; padding-bottom:10px;">{r[0]}</h1>
            <p style="font-size:1.5rem; font-weight:700;">🏢 المطور: <span style="color:#f59e0b;">{r[2]}</span></p>
            <p style="font-size:1.2rem;">📍 الموقع: {r[3]}</p>
            <div style="background:#000; color:#fff; padding:15px; font-weight:900; font-size:1.4rem;">
                💰 السداد: {r[4]}
            </div>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="nano-header">🛠️ حاسبة الاستثمار</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.view = 'main'
        st.rerun()
    st.success("تم تفعيل الحاسبة بنجاح.")
