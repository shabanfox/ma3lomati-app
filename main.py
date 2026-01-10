import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أزرار ميكرو، محاذاة يمين، تصميم حاد)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* هيدر المنصة */
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border-bottom: 6px solid #f59e0b; font-weight: 900; font-size: 1.8rem; margin-bottom: 20px;
    }

    /* أزرار ميكرو نانو (Micro-Nano Buttons) */
    div.stButton > button {
        width: 100% !important;
        height: 75px !important; /* حجم مدمج جداً */
        background-color: #ffffff !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #000 !important;
        transition: 0.1s;
        margin-bottom: 5px !important;
    }
    div.stButton > button:hover {
        background-color: #000 !important;
        color: #f59e0b !important;
        box-shadow: 2px 2px 0px #f59e0b !important;
    }
    div.stButton > button p { font-weight: 900 !important; font-size: 0.85rem !important; line-height: 1.1; }

    /* أزرار التنقل (السابق والتالي) */
    .nav-btn button {
        background-color: #f59e0b !important;
        color: #000 !important;
        height: 40px !important;
        font-size: 1rem !important;
    }

    /* صناديق أدوات البروكر */
    .broker-tool-box {
        background: #000; color: #fff; padding: 20px;
        border: 4px solid #f59e0b; text-align: center; margin-top: 10px;
    }
    .tool-val { font-size: 2rem; font-weight: 900; color: #f59e0b; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

# تهيئة المتغيرات
if 'page' not in st.session_state: st.session_state.page = 0
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'selected_row' not in st.session_state: st.session_state.selected_row = None

df = load_data()
items_per_page = 9 # 3x3

# --- المحتوى الرئيسي ---

if st.session_state.view == 'main':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    
    # تقسيم المساحة: 60% يمين (الأزرار)، 40% يسار (فارغ/أدوات)
    col_right, col_left = st.columns([0.6, 0.4], gap="large")

    with col_right:
        st.markdown("<h4 style='font-weight:900;'>🏢 دليل المشاريع (3x3)</h4>", unsafe_allow_html=True)
        
        # عرض الشبكة 3x3
        start_idx = st.session_state.page * items_per_page
        end_idx = start_idx + items_per_page
        current_df = df.iloc[start_idx:end_idx]

        for i in range(0, len(current_df), 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(current_df):
                    row = current_df.iloc[i + j]
                    with grid[j]:
                        if st.button(f"{row[0]}\n{row[2]}", key=f"p_{start_idx+i+j}"):
                            st.session_state.selected_row = row
                            st.session_state.view = 'details'
                            st.rerun()

        # أزرار التنقل (السابق والتالي)
        st.markdown("<br>", unsafe_allow_html=True)
        nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
        with nav_col1:
            if st.button("⬅️ السابق") and st.session_state.page > 0:
                st.session_state.page -= 1
                st.rerun()
        with nav_col2:
            st.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        with nav_col3:
            if st.button("التالي ➡️") and end_idx < len(df):
                st.session_state.page += 1
                st.rerun()

    with col_left:
        st.markdown("<h4 style='font-weight:900;'>🛠️ أدوات البروكر</h4>", unsafe_allow_html=True)
        with st.expander("💰 حاسبة القسط السريع", expanded=True):
            price = st.number_input("سعر الوحدة", value=2000000, step=100000)
            years = st.slider("سنوات السداد", 1, 15, 8)
            monthly = price / (years * 12) if years > 0 else 0
            st.markdown(f"""<div class="broker-tool-box">
                <span style="font-size:0.9rem;">القسط الشهري</span><br>
                <span class="tool-val">{monthly:,.0f} ج.م</span>
            </div>""", unsafe_allow_html=True)

elif st.session_state.view == 'details':
    r = st.session_state.selected_row
    st.markdown(f'<div class="main-header">📍 تفاصيل: {r[0]}</div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للقائمة"): st.session_state.view = 'main'; st.rerun()
    
    st.markdown(f"""
        <div style="border:6px solid #000; padding:30px; background:#fff; box-shadow: 10px 10px 0px #f59e0b;">
            <h2 style="font-weight:900;">شركة: {r[2]}</h2>
            <p style="font-size:1.3rem;"><b>📍 الموقع:</b> {r[3]}</p>
            <div style="background:#000; color:#fff; padding:15px; font-weight:900; font-size:1.5rem;">
                💰 نظام السداد: {r[4]}
            </div>
        </div>
    """, unsafe_allow_html=True)
