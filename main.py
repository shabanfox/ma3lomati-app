import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (التنسيق الملكي الموحد)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }
    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border-bottom: 6px solid #f59e0b; font-weight: 900; font-size: 2rem; margin-bottom: 30px;
    }
    /* أزرار القائمة الرئيسية (كبيرة وفخمة) */
    .main-btn button {
        height: 200px !important; font-size: 2rem !important; border-radius: 0px !important;
        border: 5px solid #000 !important; box-shadow: 10px 10px 0px #f59e0b !important;
    }
    /* أزرار الشركات نانو (3x3) */
    .nano-btn button {
        height: 80px !important; font-size: 0.9rem !important; border-radius: 0px !important;
        border: 3px solid #000 !important; box-shadow: 4px 4px 0px #000 !important;
        background-color: #fff !important; color: #000 !important;
    }
    .nano-btn button:hover { background-color: #f59e0b !important; border-color: #000 !important; }
    
    /* أدوات البروكر */
    .calc-card {
        background: #000; color: #f59e0b; padding: 20px; border: 4px solid #f59e0b;
        text-align: center; font-weight: 900; font-size: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظائف البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

# الحالة البرمجية
if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0
df = load_data()

# --- التنقل بين الصفحات ---

# أ. الصفحة الرئيسية (الزرين الأساسيين)
if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("🏢\nقائمة الشركات والمشاريع"):
            st.session_state.view = 'companies'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="main-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر الذكية"):
            st.session_state.view = 'tools'
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ب. صفحة الشركات (الشبكة 3x3)
elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل الشركات والمشاريع</div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'home'; st.rerun()
    
    # البحث والفلاتر
    col_search, col_filter = st.columns([2, 1])
    search_q = col_search.text_input("🔍 ابحث باسم المشروع أو المطور...")
    filter_loc = col_filter.selectbox("📍 تصفية بالموقع", ["الكل"] + list(df['الموقع'].unique()))
    
    filtered_df = df
    if search_q:
        filtered_df = filtered_df[filtered_df.apply(lambda r: search_q.lower() in r.astype(str).str.lower().values, axis=1)]
    if filter_loc != "الكل":
        filtered_df = filtered_df[filtered_df['الموقع'] == filter_loc]

    # تقسيم 60% يمين و 40% يسار
    c_right, c_left = st.columns([0.6, 0.4])
    
    with c_right:
        items_per_page = 9
        start = st.session_state.page * items_per_page
        current_batch = filtered_df.iloc[start:start+items_per_page]
        
        for i in range(0, len(current_batch), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_batch):
                    row = current_batch.iloc[i + j]
                    with cols[j]:
                        st.markdown('<div class="nano-btn">', unsafe_allow_html=True)
                        if st.button(f"{row[0]}\n({row[2]})", key=f"btn_{start+i+j}"):
                            st.info(f"تفاصيل: {row[0]} - {row[4]}")
                        st.markdown('</div>', unsafe_allow_html=True)
        
        # أزرار التالي والسابق
        st.markdown("---")
        n1, n2, n3 = st.columns([1,1,1])
        if n1.button("⬅️ السابق") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        n2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if n3.button("التالي ➡️") and start + items_per_page < len(filtered_df):
            st.session_state.page += 1; st.rerun()

# ج. صفحة أدوات البروكر
elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر العقاري</div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'home'; st.rerun()
    
    t1, t2 = st.tabs(["💰 حاسبة التمويل", "📊 تحليل ROI"])
    with t1:
        p = st.number_input("سعر العقار", value=1000000)
        y = st.slider("سنوات السداد", 1, 15, 10)
        res = p / (y * 12)
        st.markdown(f'<div class="calc-card">القسط الشهري: {res:,.0f} ج.م</div>', unsafe_allow_html=True)
    with t2:
        buy = st.number_input("سعر الشراء", value=1000000)
        rent = st.number_input("الإيجار السنوي المتوقع", value=100000)
        st.markdown(f'<div class="calc-card">العائد السنوي: {(rent/buy)*100:.1f}%</div>', unsafe_allow_html=True)
