import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (تقليل المسافات وتوحيد الأبعاد)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border-bottom: 6px solid #f59e0b; font-weight: 900; font-size: 2rem; margin-bottom: 10px;
    }

    /* أزرار الصفحة الرئيسية */
    .home-btn button {
        height: 150px !important; width: 100% !important; font-size: 1.8rem !important; 
        border: 4px solid #000 !important; box-shadow: 8px 8px 0px #f59e0b !important;
        border-radius: 0px !important;
    }

    /* إلغاء المسافات بين أعمدة ستريمليت */
    [data-testid="column"] {
        padding: 2px !important; /* مسافة ضئيلة جداً بين الأزرار */
    }

    /* تصميم أزرار الشبكة المتراصة */
    div.stButton > button {
        width: 100% !important; 
        height: 100px !important; 
        background-color: #ffffff !important; 
        color: #000 !important;
        border: 3px solid #000 !important; 
        border-radius: 0px !important;
        box-shadow: 4px 4px 0px #000 !important; 
        padding: 5px !important;
        margin: 0px !important; /* إزالة الهوامش */
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button:hover {
        background-color: #000 !important;
        color: #f59e0b !important;
        transform: scale(0.98); /* تأثير ضغطة بسيطة */
    }

    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 0.85rem !important;
        line-height: 1.1 !important;
    }
    
    /* إخفاء الفراغات الرأسية الزائدة بين الأسطر */
    [data-testid="stVerticalBlock"] {
        gap: 0.1rem !important;
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

# --- محتوى المنصة ---

if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🏢\nدليل الشركات"): st.session_state.view = 'companies'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المشاريع</div>', unsafe_allow_html=True)
    # زر العودة والبحث في سطر واحد لتوفير المساحة
    b1, b2 = st.columns([1, 4])
    if b1.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
    q = b2.text_input("", placeholder="🔍 ابحث عن مشروع أو مطور...")

    df_f = df
    if q:
        df_f = df[df.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]

    # تقسيم 60% يمين و 40% يسار
    col_grid, col_empty = st.columns([0.6, 0.4])

    with col_grid:
        items_per_page = 9
        start = st.session_state.page * items_per_page
        subset = df_f.iloc[start : start + items_per_page]

        # رسم الشبكة المتراصة
        for i in range(0, len(subset), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(subset):
                    row = subset.iloc[i + j]
                    with grid_cols[j]:
                        if st.button(f"{row.iloc[0]}\n{row.iloc[2]}", key=f"g_{start+i+j}"):
                            st.sidebar.markdown(f"### 📍 {row.iloc[0]}")
                            st.sidebar.info(f"**المطور:** {row.iloc[2]}\n\n**الموقع:** {row.iloc[3]}\n\n**السداد:** {row.iloc[4]}")

        # أزرار التنقل (السابق / التالي)
        st.markdown("<br>", unsafe_allow_html=True)
        nav1, nav2, nav3 = st.columns([1, 1, 1])
        if nav1.button("⬅️") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        nav2.markdown(f"<p style='text-align:center;'>ص {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if nav3.button("➡️") and (start + items_per_page) < len(df_f):
            st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
    # إضافة أدوات البروكر هنا
    t1, t2 = st.tabs(["💰 القسط", "📊 ROI"])
    with t1:
        v = st.number_input("السعر", value=2000000)
        st.write(f"قسط 10 سنوات: {v/120:,.0f} ج.م")
