import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (إلغاء الفواصل وجعل الأزرار ضخمة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر */
    .main-header {
        background: #000; color: #f59e0b; padding: 20px; text-align: center;
        border-bottom: 8px solid #f59e0b; font-weight: 900; font-size: 2.5rem; margin-bottom: 0px;
    }

    /* إزالة المسافات بين الأعمدة والصفوف تماماً */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* تصميم أزرار الشركات الضخمة والمتلاصقة */
    div.stButton > button {
        width: 100% !important; 
        height: 140px !important; /* حجم كبير وواضح */
        background-color: #ffffff !important; 
        color: #000 !important;
        border: 2px solid #000 !important; /* حدود رقيقة لتمييز الأزرار المتلاصقة */
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 10px !important;
        transition: 0.2s;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button:hover {
        background-color: #000 !important;
        color: #f59e0b !important;
        z-index: 10;
        position: relative;
        transform: scale(1.02); /* تكبير بسيط عند الوقوف عليه */
        border-color: #f59e0b !important;
    }

    /* النص داخل الأزرار الضخمة */
    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 1.1rem !important; /* خط كبير وواضح */
        line-height: 1.3 !important;
        text-align: center !important;
    }

    /* أزرار الهوم الرئيسية */
    .home-btn button {
        height: 250px !important; font-size: 2.5rem !important;
        border: 8px solid #000 !important; box-shadow: 15px 15px 0px #f59e0b !important;
    }
    
    /* فلاتر البحث */
    .stTextInput input {
        border: 4px solid #000 !important; border-radius: 0px !important; height: 50px !important;
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
        return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0
df = load_data()

# --- المنصة ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🏢\nدليل الشركات"): st.session_state.view = 'companies'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 قائمة المشاريع</div>', unsafe_allow_html=True)
    
    # شريط البحث والعودة
    col_back, col_search = st.columns([1, 5])
    if col_back.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
    q = col_search.text_input("", placeholder="🔍 ابحث عن مشروعك الآن...")

    df_f = df
    if q:
        df_f = df[df.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]

    # تقسيم المساحة: 60% يمين للشبكة المتلاصقة
    col_grid, col_empty = st.columns([0.6, 0.4])

    with col_grid:
        items = 9
        start = st.session_state.page * items
        subset = df_f.iloc[start : start + items]

        # الشبكة المتلاصقة (3x3)
        for i in range(0, len(subset), 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(subset):
                    row = subset.iloc[i + j]
                    with grid[j]:
                        # الزر كبير وواضح بدون فواصل
                        label = f"{row.iloc[0]}\n───\n{row.iloc[2]}"
                        if st.button(label, key=f"tile_{start+i+j}"):
                            st.sidebar.markdown(f"## 📌 {row.iloc[0]}")
                            st.sidebar.info(f"**المطور:** {row.iloc[2]}\n\n**الموقع:** {row.iloc[3]}\n\n**السداد:** {row.iloc[4]}")

        # أزرار التنقل
        st.write("")
        nav1, nav2, nav3 = st.columns([1, 1, 1])
        if nav1.button("⬅️ السابق"):
            if st.session_state.page > 0: st.session_state.page -= 1; st.rerun()
        nav2.markdown(f"<p style='text-align:center; font-weight:bold; padding-top:10px;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if nav3.button("التالي ➡️"):
            if (start + items) < len(df_f): st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات الحاسبة</div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'home'; st.rerun()
    # هنا تضع كود الحاسبات الخاص بك
    st.success("أدوات البروكر جاهزة للاستخدام")
