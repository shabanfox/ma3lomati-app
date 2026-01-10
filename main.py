import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (أزرار 3D ضخمة متلاصقة + تنسيق احترافي)
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

    /* إزالة الفواصل تماماً لجعل الأزرار متلاصقة */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stVerticalBlock"] { gap: 0px !important; }
    .stHorizontalBlock { gap: 0px !important; }

    /* أزرار المشاريع ثلاثية الأبعاد (3D) */
    div.stButton > button {
        width: 100% !important; 
        height: 150px !important; /* حجم كبير */
        background-color: #ffffff !important; 
        color: #000 !important;
        border: 2px solid #000 !important; 
        border-radius: 0px !important;
        margin: 0px !important;
        transition: 0.1s;
        
        /* تأثير الـ 3D الحاد */
        box-shadow: 6px 6px 0px #f59e0b, 12px 12px 0px #000;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button:hover {
        background-color: #000 !important;
        color: #f59e0b !important;
        transform: translate(-4px, -4px); /* حركة البروز للأمام */
        box-shadow: 10px 10px 0px #f59e0b, 18px 18px 0px #333;
        z-index: 10;
        position: relative;
    }

    div.stButton > button p {
        font-weight: 900 !important; font-size: 1.1rem !important; line-height: 1.3;
    }

    /* أزرار الصفحة الرئيسية الضخمة */
    .home-btn button {
        height: 280px !important; font-size: 2.8rem !important;
        border: 10px solid #000 !important;
        box-shadow: 15px 15px 0px #f59e0b !important;
    }

    /* صناديق الحاسبة */
    .calc-box {
        background: #000; color: #f59e0b; padding: 30px; border: 5px solid #f59e0b;
        text-align: center; font-weight: 900; font-size: 2rem;
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
        return pd.DataFrame(columns=['المشروع','المطور','الموقع','السداد'])

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0
df = load_data()

# --- محرك العرض ---

# أ. الصفحة الرئيسية (القرارين الأساسيين)
if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🏢\nدليل الشركات"): st.session_state.view = 'companies'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ب. صفحة الشركات (هنا أزرار المشاريع 3x3)
elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المشاريع والمطورين</div>', unsafe_allow_html=True)
    
    # الفلاتر والبحث
    b1, b2, b3 = st.columns([1, 3, 2])
    if b1.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
    search_q = b2.text_input("", placeholder="🔍 ابحث عن مشروع أو مطور...")
    loc_filter = b3.selectbox("📍 الموقع", ["الكل"] + list(df['الموقع'].unique() if 'الموقع' in df.columns else []))

    # تطبيق الفلترة
    df_f = df
    if search_q:
        df_f = df_f[df_f.apply(lambda r: search_q.lower() in r.astype(str).str.lower().values, axis=1)]
    if loc_filter != "الكل":
        df_f = df_f[df_f['الموقع'] == loc_filter]

    st.markdown("---")
    
    # تقسيم 60% يمين (الأزرار) و 40% يسار
    col_grid, col_empty = st.columns([0.6, 0.4])

    with col_grid:
        items_per_page = 9
        start = st.session_state.page * items_per_page
        subset = df_f.iloc[start : start + items_per_page]

        # رسم شبكة الأزرار 3D (3 أزرار في السطر)
        for i in range(0, len(subset), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(subset):
                    row = subset.iloc[i + j]
                    with cols[j]:
                        # محتوى الزر
                        btn_txt = f"{row.iloc[0]}\n───\n{row.iloc[1]}" # اسم المشروع والمطور
                        if st.button(btn_txt, key=f"3d_{start+i+j}"):
                            st.sidebar.markdown(f"### 📋 تفاصيل المشروع")
                            st.sidebar.info(f"**المشروع:** {row.iloc[0]}\n\n**المطور:** {row.iloc[1]}")

        # أزرار التنقل (السابق / التالي)
        st.write("")
        n1, n2, n3 = st.columns([1, 1, 1])
        if n1.button("⬅️ السابق") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        n2.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if n3.button("التالي ➡️") and (start + items_per_page) < len(df_f):
            st.session_state.page += 1; st.rerun()

# ج. صفحة الأدوات
elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ الحاسبات المالية</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'home'; st.rerun()
    
    # حاسبة بسيطة
    price = st.number_input("سعر الوحدة", value=1000000)
    st.markdown(f'<div class="calc-box">القسط الشهري (10 سنوات): {price/120:,.0f} ج.م</div>', unsafe_allow_html=True)
