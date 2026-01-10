import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الفاخر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .hero-banner h1 { font-weight: 900; font-size: 2.8rem; margin: 0; color: #f59e0b !important; }

    /* كارت المطور البسيط */
    .dev-card {
        background: #ffffff; border: 4px solid #000; padding: 20px; 
        border-radius: 20px; margin-bottom: 20px; box-shadow: 8px 8px 0px #000;
        height: 150px; display: flex; align-items: center; justify-content: center;
        text-align: center; transition: 0.3s;
    }
    .dev-card:hover { border-color: #f59e0b; box-shadow: 10px 10px 0px #f59e0b; transform: scale(1.02); }
    .dev-name { font-size: 1.6rem; font-weight: 900; color: #000; }

    /* أزرار التنقل (التالي والسابق) */
    div.stButton > button[key^="nav_"] {
        height: 45px !important; width: 120px !important;
        background-color: #ffffff !important; color: #000000 !important;
        border: 3px solid #000000 !important; border-radius: 10px !important;
        box-shadow: 4px 4px 0px #000 !important; font-weight: 900 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        # تنظيف أسماء الأعمدة من أي مسافات زائدة
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame(columns=['Developer'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page' not in st.session_state: st.session_state.page = 0

# تحديد العمود (Developer)
df = st.session_state.data
# التأكد من وجود العمود لتجنب الخطأ
target_col = 'Developer' if 'Developer' in df.columns else df.columns[0]

# --- التطبيق ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<div style='height:80px;'></div>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([0.1, 0.8, 0.1])
    with mid_col:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            if st.button("🏢\nدليل المطورين", key="main_dev"): st.session_state.view = 'comp'; st.rerun()
        with c2:
            if st.button("🛠️\nأدوات البروكر", key="main_tool"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🏢 دليل المطورين العقاريين</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية", key="nav_back"): 
        st.session_state.view = 'main'; st.session_state.page = 0; st.rerun()
    
    # البحث
    search = st.text_input("🔍 ابحث عن اسم المطور...")
    
    # استخراج المطورين الفريدين بناءً على عمود Developer
    unique_devs = df[target_col].dropna().unique()
    
    if search:
        unique_devs = [d for d in unique_devs if search.lower() in str(d).lower()]
    
    # منطق الصفحات (9 كروت)
    items_per_page = 9
    total_items = len(unique_devs)
    start_idx = st.session_state.page * items_per_page
    end_idx = start_idx + items_per_page
    current_devs = unique_devs[start_idx:end_idx]

    # عرض الشبكة 3x3
    for i in range(0, len(current_devs), 3):
        grid_cols = st.columns(3)
        for j in range(3):
            if i + j < len(current_devs):
                dev_name = current_devs[i + j]
                with grid_cols[j]:
                    st.markdown(f"""
                    <div class="dev-card">
                        <div class="dev-name">{dev_name}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # أزرار التنقل في المنتصف
    st.write("<br>", unsafe_allow_html=True)
    _, nav_mid, _ = st.columns([1, 1, 1])
    with nav_mid:
        c_prev, c_next = st.columns(2)
        with c_prev:
            if st.session_state.page > 0:
                if st.button("⬅️ السابق", key="nav_prev"):
                    st.session_state.page -= 1; st.rerun()
        with c_next:
            if end_idx < total_items:
                if st.button("التالي ➡️", key="nav_next"):
                    st.session_state.page += 1; st.rerun()
