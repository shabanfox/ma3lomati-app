import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* زر الخروج */
    .stButton > button[key="logout_btn"] {
        background-color: #ff4b4b !important; color: white !important;
        border: none !important; padding: 5px 20px !important; border-radius: 5px !important;
    }

    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; margin-bottom: 10px; text-align: center;
        min-height: 250px; display: flex; flex-direction: column; justify-content: center;
    }
    .card-main-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; margin-top: 8px; color: #ccc; border-bottom: 1px solid #1a1a1a; padding-bottom: 5px; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    
    /* أزرار التنقل */
    .stButton button { width: 100%; background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. شريط الخروج العلوي
t_col1, t_col2 = st.columns([10, 1])
with t_col2:
    if st.button("خروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

# 4. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        data = data.fillna("غير متوفر").astype(str)
        return data
    except: return pd.DataFrame()

df = load_data()

# 5. القائمة
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], icons=["tools", "building", "person-badge"], orientation="horizontal", styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# تهيئة العدادات في الـ Session State
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c1, c2 = st.columns([0.7, 0.3])
        with c1:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع...")
            with f2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))
            
            dff = df.copy()
            name_col = 'Project Name' if 'Project Name' in df.columns else 'Projects'
            if s_p: dff = dff[dff[name_col].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff['Area'] == a_p]

            items = 9
            total_p = max(1, math.ceil(len(dff) / items))
            curr = dff.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

            for i in range(0, len(curr), 3):
                cols = st.columns(3)
                for j in range(len(cols)):
                    if i+j < len(curr):
                        row = curr.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><div class="card-main-title">{row.get(name_col)}</div><div style="color:#888;">{row.get("Developer")}</div><div class="stat-row">📍 {row.get("Area")}</div></div>', unsafe_allow_html=True)
            
            # أزرار تنقل المشاريع
            st.write("---")
            b1, b2, b3 = st.columns([1, 2, 1])
            with b3:
                if (st.session_state.p_page + 1) < total_p:
                    if st.button("التالي ⬅️", key="pn"): st.session_state.p_page += 1; st.rerun()
            with b2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_p}</p>", unsafe_allow_html=True)
            with b1:
                if st.session_state.p_page > 0:
                    if st.button("➡️ السابق", key="pp"): st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين (تمت إضافة أزرار التنقل) ---
elif selected == "🏢 المطورين":
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        c1, c2 = st.columns([0.7, 0.3])
        with c1:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين العقاريين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False)]
            
            items = 9
            total_d = max(1, math.ceil(len(devs) / items))
            curr_devs = devs.iloc[st.session_state.d_page * items : (st.session_state.d_page + 1) * items]

            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(len(cols)):
                    if i+j < len(curr_devs):
                        row = curr_devs.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><div class="card-main-title">{row["Developer"]}</div><p>👤 {row["Owner"]}</p></div>', unsafe_allow_html=True)
            
            # أزرار تنقل المطورين (تمت إعادتها)
            st.write("---")
            d1, d2, d3 = st.columns([1, 2, 1])
            with d3:
                if (st.session_state.d_page + 1) < total_d:
                    if st.button("التالي ⬅️", key="dn"): st.session_state.d_page += 1; st.rerun()
            with d2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_page + 1} من {total_d}</p>", unsafe_allow_html=True)
            with d1:
                if st.session_state.d_page > 0:
                    if st.button("➡️ السابق", key="dp"): st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ شاشة أدوات البروكر ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=1000000)
        yr = st.number_input("السنين", value=7, min_value=1)
        st.subheader(f"{pr/(yr*12):,.0f} ج/شهري")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='pro-card'><h3>📏 المحول</h3>", unsafe_allow_html=True)
        ac = st.number_input("فدان", value=1.0)
        st.subheader(f"{ac*4200:,.0f} متر مربع")
        st.markdown("</div>", unsafe_allow_html=True)
    st.text_area("📝 مسودة ملاحظات العميل...")
