import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth, st.session_state.current_user = True, st.query_params["u_session"]
    else: st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف ---
def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

def render_grid(dataframe, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        c1, c2, c3 = st.columns(3)
        cols = dataframe.columns
        for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
            with [c1, c2, c3][i]:
                h = '<div class="detail-card">'
                for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        # --- قسم الفلاتر المطور ---
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; margin-bottom:20px; border:1px solid #333;'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2, 2, 3])
        
        with f1:
            search = st.text_input("🔍 بحث بالإسم...", key=f"search_{prefix}")
        
        # فلتر المنطقة (بشرط وجود عمود Location أو الموقع)
        loc_col = 'Location' if 'Location' in dataframe.columns else ('الموقع' if 'الموقع' in dataframe.columns else None)
        with f2:
            if loc_col:
                areas = ["الكل"] + sorted(dataframe[loc_col].unique().tolist())
                sel_area = st.selectbox("📍 تصفية بالمنطقة", areas, key=f"area_{prefix}")
            else: sel_area = "الكل"

        # فلتر السعر (بشرط وجود عمود Price أو السعر)
        price_col = 'Price' if 'Price' in dataframe.columns else ('السعر' if 'السعر' in dataframe.columns else None)
        with f3:
            if price_col:
                # تحويل السعر لأرقام للتصفية
                dataframe[price_col] = pd.to_numeric(dataframe[price_col].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
                max_p = int(dataframe[price_col].max())
                min_p = int(dataframe[price_col].min())
                price_range = st.slider("💰 نطاق السعر (ج.م)", min_p, max_p, (min_p, max_p), key=f"range_{prefix}")
            else: price_range = None
        st.markdown("</div>", unsafe_allow_html=True)

        # --- تطبيق الفلاتر ---
        filt = dataframe.copy()
        if search:
            filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل" and loc_col:
            filt = filt[filt[loc_col] == sel_area]
        if price_range and price_col:
            filt = filt[(filt[price_col] >= price_range[0]) & (filt[price_col] <= price_range[1])]

        # عرض النتائج
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.76, 0.24])
        with m_c:
            if len(disp) == 0: st.warning("لا توجد نتائج تطابق بحثك")
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if prefix == "dev":
                        owner_val = r.get('Owner', r.get('المالك', '---'))
                        card_text = f"🏗️ {r[0]}\n👤 المالك: {owner_val}"
                    else:
                        p_val = f"{int(r[price_col]):,}" if price_col in r else "---"
                        card_text = f"🏠 {r[0]}\n📍 {r.get(loc_col, '---')}\n💰 يبدأ من: {p_val}"
                    
                    if st.button(card_text, key=f"card_{prefix}_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # التنقل بين الصفحات
            p1, p_info, p2 = st.columns([1, 2, 1])
            with p1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ السابق", key=f"nav_p_{prefix}"): st.session_state.page_num -= 1; st.rerun()
            with p_info: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state.page_num + 1} من {max(1, (len(filt)-1)//ITEMS_PER_PAGE + 1)}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"nav_n_{prefix}"): st.session_state.page_num += 1; st.rerun()
        
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:1px solid #333;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:25]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 5. التصميم CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(0, 0, 0, 0.8) 100%), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 4px solid #f59e0b; padding: 60px 20px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 25px;
    }}
    .royal-header h1 {{ color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }}
    div.stButton > button[key*="card_"] {{ background: #fff !important; color: #1a1a1a !important; border-right: 8px solid #f59e0b !important; border-radius: 12px !important; padding: 15px !important; text-align: right !important; min-height: 120px !important; width: 100% !important; font-weight: bold; }}
    .detail-card {{ background: rgba(30, 30, 30, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; }}
    .val-white {{ color: white; font-size: 1.1rem; border-bottom: 1px solid #333; margin-bottom: 12px; }}
    /* Slider styling */
    .stSlider [data-baseweb="slider"] {{ direction: ltr; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. الدخول والبيانات (نفس الكود السابق) ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/prop?gid=1593482152&single=true&output=csv"
    p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
    return p.fillna("---"), d.fillna("---"), l.fillna("---")

if not st.session_state.auth:
    # (هنا يوضع كود Login الموجود سابقاً)
    st.title("MA3LOMATI PRO Login")
    st.stop()

df_p, df_d, df_l = load_data()

# --- واجهة العرض ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>أهلاً بك يا {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if menu == "المشاريع":
    render_grid(df_p, "proj")
elif menu == "أدوات البروكر":
    # (كود الحاسبة هنا)
    st.write("حاسبات البروكر...")
elif menu == "المطورين":
    render_grid(df_d, "dev")

if st.button("🚪 خروج"): logout()
