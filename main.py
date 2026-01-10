import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أزرار ثلاثية الأبعاد + فلاتر)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 20px; text-align: center;
        border-bottom: 8px solid #f59e0b; font-weight: 900; font-size: 2.5rem; margin-bottom: 0px;
    }

    /* إزالة المسافات بين الأعمدة والصفوف تماماً */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* أزرار 3D للمشاريع */
    div.stButton > button {
        width: 100% !important; 
        height: 140px !important; 
        background-color: #ffffff !important; 
        color: #000 !important;
        border: 2px solid #000 !important; 
        border-radius: 0px !important;
        margin: 0px !important;
        padding: 10px !important;
        transition: all 0.1s ease-out; /* حركة ناعمة */

        /* السحر هنا: ظل ثلاثي الأبعاد */
        box-shadow: 
            5px 5px 0px 0px #f59e0b,  /* ظل ذهبي سفلي */
            10px 10px 0px 0px #000;    /* ظل أسود أعمق */
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button:hover {
        background-color: #000 !important;
        color: #f59e0b !important;
        transform: translate(-3px, -3px); /* حركة للأعلى واليسار عند التمرير */
        box-shadow: 
            8px 8px 0px 0px #f59e0b, 
            15px 15px 0px 0px #000; /* ظل أكبر وأعمق عند التمرير */
        border-color: #f59e0b !important;
    }

    div.stButton > button:active { /* تأثير الضغط */
        transform: translate(2px, 2px);
        box-shadow: 
            2px 2px 0px 0px #f59e0b, 
            5px 5px 0px 0px #000;
    }

    div.stButton > button p {
        font-weight: 900 !important;
        font-size: 1.1rem !important;
        line-height: 1.3 !important;
        text-align: center !important;
    }

    /* أزرار الهوم الرئيسية */
    .home-btn button {
        height: 250px !important; font-size: 2.5rem !important;
        border: 8px solid #000 !important; box-shadow: 15px 15px 0px #f59e0b !important;
        transition: all 0.1s ease-out;
    }
    .home-btn button:hover {
        transform: translate(-5px, -5px);
        box-shadow: 20px 20px 0px #f59e0b !important;
    }
    
    /* فلاتر البحث والفلترة */
    .stTextInput input, .stSelectbox [data-testid="stSelectboxDropdown"] {
        border: 4px solid #000 !important; border-radius: 0px !important; height: 50px !important;
        font-weight: 700 !important;
    }
    .stSelectbox [data-testid="stSelectboxContainer"] label { font-size: 1.1rem !important; }

    /* حاسبة الأدوات */
    .tool-card {
        background: #000; color: #f59e0b; padding: 25px; border: 4px solid #f59e0b;
        text-align: center; font-weight: 900; font-size: 1.8rem; margin-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/sheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv" # تأكد من الرابط
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
        if st.button("🏢\nدليل الشركات والمشاريع"): st.session_state.view = 'companies'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر الذكية"): st.session_state.view = 'tools'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 قائمة المشاريع</div>', unsafe_allow_html=True)
    
    # شريط البحث والفلاتر
    col_back, col_search, col_filter = st.columns([0.8, 3, 2])
    if col_back.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
    
    q = col_search.text_input("", placeholder="🔍 ابحث (مشروع، مطور، موقع)...")
    
    # قائمة المواقع لفلترة
    locations = ["الكل"] + list(df['الموقع'].unique())
    selected_location = col_filter.selectbox("📍 تصفية حسب الموقع", locations)

    df_filtered = df
    if q:
        df_filtered = df_filtered[df_filtered.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]
    if selected_location != "الكل":
        df_filtered = df_filtered[df_filtered['الموقع'] == selected_location]

    # تقسيم المساحة: 60% يمين للشبكة المتلاصقة ثلاثية الأبعاد
    col_grid, col_empty = st.columns([0.6, 0.4])

    with col_grid:
        items_per_page = 9
        start_idx = st.session_state.page * items_per_page
        subset = df_filtered.iloc[start_idx : start_idx + items_per_page]

        # الشبكة 3x3 ثلاثية الأبعاد
        for i in range(0, len(subset), 3):
            grid = st.columns(3)
            for j in range(3):
                if i + j < len(subset):
                    row = subset.iloc[i + j]
                    with grid[j]:
                        label = f"{row.iloc[0]}\n───\n{row.iloc[2]}"
                        if st.button(label, key=f"3d_tile_{start_idx+i+j}"):
                            st.sidebar.markdown(f"## 📌 {row.iloc[0]}")
                            st.sidebar.info(f"**المطور:** {row.iloc[2]}\n\n**الموقع:** {row.iloc[3]}\n\n**السداد:** {row.iloc[4]}")

        # أزرار التنقل (سابق / تالي)
        st.write("")
        nav1, nav2, nav3 = st.columns([1, 1, 1])
        if nav1.button("⬅️ السابق"):
            if st.session_state.page > 0: st.session_state.page -= 1; st.rerun()
        nav2.markdown(f"<p style='text-align:center; font-weight:bold; padding-top:10px;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if nav3.button("التالي ➡️"):
            if (start_idx + items_per_page) < len(df_filtered): st.session_state.page += 1; st.rerun()

elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'home'; st.rerun()
    
    t1, t2 = st.tabs(["💰 حاسبة القسط", "📊 تحليل ROI"])
    with t1:
        price = st.number_input("سعر العقار", value=2000000, step=100000)
        years = st.slider("سنوات السداد", 1, 15, 10)
        monthly_payment = price / (years * 12) if years > 0 else 0
        st.markdown(f'<div class="tool-card">القسط الشهري: {monthly_payment:,.0f} ج.م</div>', unsafe_allow_html=True)
    with t2:
        buy_cost = st.number_input("تكلفة الشراء", value=1500000, step=100000)
        annual_rent = st.number_input("الإيجار السنوي المتوقع", value=150000, step=10000)
        roi_percentage = (annual_rent / buy_cost) * 100 if buy_cost > 0 else 0
        st.markdown(f'<div class="tool-card">العائد السنوي (ROI): %{roi_percentage:.1f}</div>', unsafe_allow_html=True)
