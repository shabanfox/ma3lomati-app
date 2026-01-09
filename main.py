import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أزرار نانو حادة + حاسبات فخمة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border-bottom: 6px solid #f59e0b; font-weight: 900; font-size: 2rem; margin-bottom: 20px;
    }

    /* أزرار نانو: صغيرة، حادة، وظل قوي */
    div.stButton > button {
        width: 100% !important;
        height: 80px !important; /* حجم نانو */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        border-radius: 0px !important;
        box-shadow: 5px 5px 0px #000 !important;
        margin-bottom: 10px !important;
        transition: 0.1s;
    }

    div.stButton > button:hover {
        background-color: #000 !important;
        color: #f59e0b !important;
        box-shadow: 5px 5px 0px #f59e0b !important;
    }

    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 0.9rem !important;
        line-height: 1.1;
    }

    /* صناديق الحاسبة (Calc-Box) */
    .calc-box {
        background: #000; color: #fff; padding: 20px;
        border: 4px solid #f59e0b; text-align: center;
        box-shadow: 10px 10px 0px #000; margin-top: 10px;
    }
    .calc-val { font-size: 2.2rem; font-weight: 900; color: #f59e0b; }
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

# --- التنقل المحتوى ---

if st.session_state.view == 'main':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى</div>', unsafe_allow_html=True)
    
    col_right, col_left = st.columns([0.5, 0.5])
    
    with col_right:
        st.markdown("<h3 style='font-weight:900;'>🏢 دليل المشاريع (نانو)</h3>", unsafe_allow_html=True)
        # شبكة 2 زر في السطر و 3 أسطر (إجمالي 6 أزرار نانو)
        for i in range(0, 6, 2):
            cols = st.columns(2)
            for j in range(2):
                if i + j < len(df):
                    row = df.iloc[i + j]
                    with cols[j]:
                        if st.button(f"{row[0]}\n{row[2]}", key=f"n_{i+j}"):
                            st.session_state.selected_row = row
                            st.session_state.view = 'details'
                            st.rerun()
        
        if st.button("🛠️ الدخول للأدوات والحاسبات", key="goto_tools"):
            st.session_state.view = 'tools'
            st.rerun()

elif st.session_state.view == 'details':
    r = st.session_state.selected_row
    st.markdown(f'<div class="main-header">📍 {r[0]}</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة"):
        st.session_state.view = 'main'
        st.rerun()
    
    st.markdown(f"""
    <div style="border:5px solid #000; padding:25px; background:#fff;">
        <h2 style="font-weight:900;">المطور: <span style="color:#f59e0b;">{r[2]}</span></h2>
        <p style="font-size:1.2rem; font-weight:700;">الموقع: {r[3]}</p>
        <div style="background:#000; color:#fff; padding:15px; font-weight:900;">
            نظام السداد: {r[4]}
        </div>
    </div>
    """, unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر العقاري</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"):
        st.session_state.view = 'main'
        st.rerun()
    
    t1, t2 = st.tabs(["💰 حاسبة القسط", "📈 ROI الاستثماري"])
    
    with t1:
        c1, c2 = st.columns(2)
        price = c1.number_input("سعر الوحدة", value=1000000)
        years = c2.number_input("سنوات التقسيط", value=10)
        monthly = price / (years * 12) if years > 0 else 0
        st.markdown(f"""
        <div class="calc-box">
            <p>القسط الشهري المتوقع</p>
            <div class="calc-val">{monthly:,.0f} ج.م</div>
        </div>
        """, unsafe_allow_html=True)

    with t2:
        c1, c2 = st.columns(2)
        cost = c1.number_input("تكلفة الشراء", value=1000000)
        rent = c2.number_input("الإيجار السنوي", value=100000)
        roi = (rent / cost) * 100 if cost > 0 else 0
        st.markdown(f"""
        <div class="calc-box" style="border-color:#fff;">
            <p>نسبة العائد السنوي (ROI)</p>
            <div class="calc-val">%{roi:.1f}</div>
        </div>
        """, unsafe_allow_html=True)
