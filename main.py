import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. نظام إدارة اللغات
if 'lang' not in st.session_state:
    st.session_state.lang = 'Arabic'

# قاموس الواجهة (Interface Dictionary)
ui_texts = {
    'Arabic': {
        'title': "منصة معلوماتي العقارية",
        'logout': "🚪 خروج",
        'projects': "🏗️ المشاريع",
        'devs': "🏢 المطورين",
        'tools': "🛠️ أدوات البروكر",
        'search_label': "🔍 ابحث بأي لغة (عربي/EN)...",
        'area_label': "📍 المنطقة",
        'details_btn': "🔎 التفاصيل",
        'next': "التالي ⬅️",
        'prev': "➡️ السابق",
        'dir': "rtl",
        'align': "right",
        'flex_dir': "row"
    },
    'English': {
        'title': "Ma3lomati Real Estate",
        'logout': "🚪 Logout",
        'projects': "🏗️ Projects",
        'devs': "🏢 Developers",
        'tools': "🛠️ Broker Tools",
        'search_label': "🔍 Search (Arabic/EN)...",
        'area_label': "📍 Area",
        'details_btn': "🔎 Details",
        'next': "Next ➡️",
        'prev': "⬅️ Prev",
        'dir': "ltr",
        'align': "left",
        'flex_dir': "row-reverse"
    }
}

T = ui_texts[st.session_state.lang]

# 3. التنسيق (CSS) المتفاعل مع اللغة
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; margin-top: -10px; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; 
        direction: {T['dir']} !important; 
        text-align: {T['align']} !important; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 50px; padding: 10px 30px; width: fit-content; margin: 10px auto 20px auto; text-align: center; }}
    .header-title {{ color: #f59e0b; font-weight: 900; font-size: 26px !important; margin: 0; }}
    .grid-card {{ background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; border-radius: 12px; padding: 15px; height: 165px; margin-bottom: 10px; }}
    .stButton button {{ background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; }}
    .logout-btn button {{ background-color: #ff4b4b !important; color: white !important; border: none !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات (تلقائي)
@st.cache_data(ttl=60)
def load_data():
    u1 = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(u1)
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("").astype(str)
    except:
        return pd.DataFrame()

df = load_data()

# 5. نظام الدخول (Password: 2026)
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)
    pwd = st.text_input("Password / كلمة المرور", type="password")
    if st.button("Login / دخول"):
        if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- واجهة المستخدم بعد الدخول ---

# شريط التحكم العلوي (خروج وتبديل لغة)
top_col1, top_col2 = st.columns([1, 1])
with top_col1:
    if st.button(T['logout'], key="logout"):
        st.session_state.auth = False; st.rerun()
with top_col2:
    btn_label = "🇺🇸 Switch to English" if st.session_state.lang == 'Arabic' else "🇪🇬 التغيير للعربية"
    if st.button(btn_label):
        st.session_state.lang = 'English' if st.session_state.lang == 'Arabic' else 'Arabic'
        st.rerun()

st.markdown(f'<div class="oval-header"><h1 class="header-title">{T["title"]}</h1></div>', unsafe_allow_html=True)

menu = option_menu(None, [T['projects'], T['devs'], T['tools']], 
                  icons=["building", "person-vcard", "tools"], 
                  orientation="horizontal")

# توزيع المساحة 70% حسب اتجاه اللغة
if st.session_state.lang == 'Arabic':
    main_col, empty_col = st.columns([0.7, 0.3])
else:
    empty_col, main_col = st.columns([0.3, 0.7])

with main_col:
    if menu == T['projects']:
        st.markdown(f"<h2 class='right-header'>{T['projects']}</h2>", unsafe_allow_html=True)
        
        # الفلاتر
        f1, f2 = st.columns([0.6, 0.4])
        with f1: search = st.text_input(T['search_label'], placeholder="..." )
        with f2: 
            areas = ["All/الكل"] + sorted(df['Area'].unique().tolist())
            sel_area = st.selectbox(T['area_label'], areas)

        # منطق الفلترة (يبحث في كل اللغات)
        dff = df.copy()
        if search:
            # يبحث في كل خانات الشيت سواء الاسم بالعربي أو الإنجليزي
            mask = dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)
            dff = dff[mask]
        if sel_area != "All/الكل":
            dff = dff[dff['Area'] == sel_area]

        # الشبكة 3×3
        grid_limit = 9
        if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
        total_pages = math.ceil(len(dff) / grid_limit)
        curr_page = dff.iloc[st.session_state.p_idx * grid_limit : (st.session_state.p_idx + 1) * grid_limit]

        for i in range(0, len(curr_page), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_page):
                    row = curr_page.iloc[i + j]
                    with cols[j]:
                        # عرض البيانات (يفضل تسمية الأعمدة في الشيت بأسماء واضحة)
                        st.markdown(f"""<div class='grid-card'>
                            <h3 style='color:#f59e0b; font-size:16px;'>{row.get('Project Name', 'Project')}</h3>
                            <p style='font-size:13px;'>🏢 {row.get('Developer', '')}</p>
                            <p style='font-size:12px; color:#888;'>📍 {row.get('Area', '')}</p>
                        </div>""", unsafe_allow_html=True)
                        with st.expander(T['details_btn']):
                            # يعرض كل بيانات الصف المتاحة في الشيت
                            for col_name, value in row.to_dict().items():
                                st.write(f"**{col_name}:** {value}")

        # أزرار التنقل
        st.write("---")
        b1, b2, _ = st.columns([0.2, 0.2, 0.6])
        if b1.button(T['next']):
            if st.session_state.p_idx < total_pages -1: st.session_state.p_idx += 1; st.rerun()
        if b2.button(T['prev']):
            if st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()

    elif menu == T['tools']:
        st.markdown(f"<h2>{T['tools']}</h2>", unsafe_allow_html=True)
        # أدوات البروكر هنا...
        st.info("حاسبة الأقساط قيد التشغيل...")
