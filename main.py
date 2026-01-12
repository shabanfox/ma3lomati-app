import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS) - ضبط الجهة اليمنى بالكامل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container { padding-top: 0rem !important; margin-top: -20px; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        direction: RTL !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }

    /* الهيدر البيضاوي الذهبي */
    .oval-header {
        background-color: #000;
        border: 3px solid #f59e0b;
        border-radius: 50px;
        padding: 10px 30px;
        width: fit-content;
        margin: 0 auto 20px auto;
        text-align: center;
    }
    .header-title { color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }

    /* ستايل الدخول */
    .login-box {
        max-width: 400px;
        margin: 40px auto;
        padding: 30px;
        background: #111;
        border-radius: 20px;
        border: 1px solid #222;
        text-align: center;
    }
    div[data-baseweb="input"] { background-color: white !important; border-radius: 8px !important; }
    input { color: black !important; font-weight: bold !important; text-align: center !important; }

    /* العناوين في اليمين */
    .right-header {
        color: #f59e0b;
        text-align: right !important;
        font-weight: 900;
        border-right: 10px solid #f59e0b;
        padding-right: 15px;
        margin: 20px 0;
    }

    /* الكروت الشبكية */
    .grid-card {
        background: #111;
        border: 1px solid #222;
        border-top: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 15px;
        height: 180px;
        margin-bottom: 10px;
    }

    /* أزرار التنقل */
    .stButton button { 
        background-color: #1a1a1a !important; 
        color: #f59e0b !important; 
        border: 1px solid #333 !important;
        width: 100% !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام الدخول
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='color:#f59e0b; font-size:50px;'>🔒</h1>", unsafe_allow_html=True)
    pwd = st.text_input("أدخل الباسورد", type="password")
    if st.button("دخول للنظام"):
        if pwd == "2026":
            st.session_state.auth = True
            st.rerun()
        else: st.error("الباسورد خطأ")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. تحميل البيانات
@st.cache_data(ttl=60)
def load_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    ]
    dfs = []
    for u in urls:
        try:
            d = pd.read_csv(u)
            d.columns = [str(c).strip() for c in d.columns]
            dfs.append(d)
        except: continue
    return pd.concat(dfs, ignore_index=True).fillna("غير متوفر").astype(str)

df = load_data()
grid_size = 9

# الهيدر وزر الخروج
st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# جعل المنيو في الجانب الأيمن
col_main, col_nav = st.columns([0.8, 0.2])

with col_nav:
    selected = option_menu(
        menu_title="القائمة",
        options=["🏢 المطورين", "🏗️ المشاريع", "🛠️ الأدوات"],
        icons=["person-vcard", "building", "tools"],
        menu_icon="list",
        default_index=1,
        styles={"container": {"background-color": "#000", "border": "1px solid #222"},
                "nav-link-selected": {"background-color": "#f59e0b"}}
    )
    st.write("---")
    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()

with col_main:
    # --- قسم المشاريع ---
    if selected == "🏗️ المشاريع":
        st.markdown("<h1 class='right-header'>دليل المشاريع العقارية</h1>", unsafe_allow_html=True)
        search = st.text_input("🔍 ابحث في المشاريع...")
        
        dff = df.copy()
        if search: dff = dff[dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]

        if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
        total_p = math.ceil(len(dff) / grid_size)
        curr_df = dff.iloc[st.session_state.p_idx * grid_size : (st.session_state.p_idx + 1) * grid_size]

        for i in range(0, len(curr_df), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_df):
                    row = curr_df.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""<div class='grid-card'>
                            <h3 style='color:#f59e0b;'>{row['Project Name']}</h3>
                            <p>🏢 {row['Developer']}</p>
                            <p style='color:#888; font-size:12px;'>📍 {row['Area']}</p>
                        </div>""", unsafe_allow_html=True)
                        with st.expander("تفاصيل"):
                            st.write(f"👷 {row['Consultant']}")
                            st.write(f"⭐ {row['Competitive Advantage']}")

        # أزرار التنقل (يمين)
        st.write("---")
        n1, n2, _ = st.columns([0.15, 0.15, 0.7])
        if n1.button("التالي ⬅️"):
            if st.session_state.p_idx < total_p - 1:
                st.session_state.p_idx += 1; st.rerun()
        if n2.button("➡️ السابق"):
            if st.session_state.p_idx > 0:
                st.session_state.p_idx -= 1; st.rerun()
        st.markdown(f"<p style='text-align:right;'>صفحة {st.session_state.p_idx + 1} من {total_p}</p>", unsafe_allow_html=True)

    # --- قسم المطورين ---
    elif selected == "🏢 المطورين":
        st.markdown("<h1 class='right-header'>دليل المطورين</h1>", unsafe_allow_html=True)
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
        
        if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
        total_d = math.ceil(len(devs) / grid_size)
        curr_devs = devs.iloc[st.session_state.d_idx * grid_size : (st.session_state.d_idx + 1) * grid_size]

        for i in range(0, len(curr_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_devs):
                    row = curr_devs.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b;'>{row['Developer']}</h3><p>👤 {row['Owner']}</p></div>", unsafe_allow_html=True)
                        with st.expander("الملف"): st.write(row['Detailed_Info'])

        st.write("---")
        dn1, dn2, _ = st.columns([0.15, 0.15, 0.7])
        if dn1.button("التالي ⬅️", key="dn"):
            if st.session_state.d_idx < total_d - 1:
                st.session_state.d_idx += 1; st.rerun()
        if dn2.button("➡️ السابق", key="dp"):
            if st.session_state.d_idx > 0:
                st.session_state.d_idx -= 1; st.rerun()

    # --- قسم الأدوات ---
    elif selected == "🛠️ الأدوات":
        st.markdown("<h1 class='right-header'>أدوات البروكر</h1>", unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            st.markdown("### 💰 حاسبة القسط")
            price = st.number_input("السعر", 1000000)
            st.success(f"القسط التقريبي: {price/96:,.0f} ج.م")
        with t2:
            st.markdown("### 📝 المفكرة")
            st.text_area("سجل ملاحظاتك...", height=200)
