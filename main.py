import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة (Session State) ---
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. الروابط والثوابت ---
ITEMS_PER_PAGE = 6
HEADER_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"

# --- 4. دالة تحميل البيانات وتنظيفها ---
@st.cache_data(ttl=60)
def load_data():
    urls = {
        "p": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "d": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
        "l": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    }
    try:
        p, d, l = pd.read_csv(urls["p"]), pd.read_csv(urls["d"]), pd.read_csv(urls["l"])
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. التصميم الملكي (CSS) - خطوط عريضة Bold ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0px; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.3), rgba(0,0,0,0.9)), url('{HEADER_IMG}');
        background-size: cover; border-bottom: 5px solid #f59e0b; padding: 50px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}
    .royal-header h1 {{ color: #f59e0b; font-size: 3.5rem; font-weight: 900; margin: 0; }}
    .stSelectbox label, .stTextInput label, .stSlider label {{ color: #f59e0b !important; font-size: 1.2rem !important; font-weight: 900 !important; }}
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #000 !important; border-right: 12px solid #f59e0b !important;
        font-size: 1.2rem !important; font-weight: 900 !important; min-height: 140px !important; text-align: right !important;
    }}
    .detail-card {{ background: rgba(20,20,20,0.98); padding: 25px; border-radius: 20px; border: 1px solid #444; border-top: 6px solid #f59e0b; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1.1rem; }}
    .val-white {{ color: #fff; font-size: 1.3rem; font-weight: 700; border-bottom: 1px solid #333; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. دالة العرض مع فلاتر المناطق الديناميكية ---
def render_grid(dataframe, prefix):
    # إدارة الصفحة لكل قسم
    pg_key = f"page_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        cols = dataframe.columns
        c1, c2, c3 = st.columns(3)
        for i, col_name in enumerate(cols):
            with [c1, c2, c3][i % 3]:
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col_name}</p><p class="val-white">{item[col_name]}</p></div>', unsafe_allow_html=True)
    else:
        # --- صندوق الفلاتر الذكي ---
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:20px; border:1px solid #444;'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2, 2, 3])
        
        with f1: search = st.text_input("🔍 بحث بالإسم", key=f"s_{prefix}")
        
        with f2:
            # استخراج المناطق من الشيت مباشرة (بدون تكرار)
            if 'Location' in dataframe.columns:
                areas = ["الكل"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan"]])
            else: areas = ["الكل"]
            sel_area = st.selectbox("📍 اختار المنطقة", areas, key=f"l_{prefix}")
        
        with f3:
            if 'Price' in dataframe.columns and not dataframe.empty:
                min_v, max_v = int(dataframe['Price'].min()), int(dataframe['Price'].max())
                if min_v == max_v: max_v += 1
                price_range = st.slider("💰 الميزانية (ج.م)", min_v, max_v, (min_v, max_v), key=f"p_{prefix}")
            else: price_range = None
        st.markdown("</div>", unsafe_allow_html=True)

        # منطق التصفية
        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]
        if price_range: filt = filt[(filt['Price'] >= price_range[0]) & (filt['Price'] <= price_range[1])]

        # العرض والتقسيم لصفحات
        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_val = f"{int(r['Price']):,}" if 'Price' in r else "---"
                    txt = f"🏠 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_val} ج.م"
                    if st.button(txt, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # أزرار الصفحات
            st.write("")
            p1, px, p2 = st.columns([1, 2, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#f59e0b; font-weight:900;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}"): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:900; border-bottom:2px solid #f59e0b;'>⭐ مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"📌 {str(s_row[0])[:15]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 7. تشغيل التطبيق ---
df_p, df_d, df_l = load_data()
st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>النسخة الملكية 2026</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الحاسبة", "المطورين", "المشاريع", "المساعد AI"], 
    icons=["calculator", "building", "house", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if menu == "الحاسبة":
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("<div class='detail-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("إجمالي السعر", value=5000000, step=100000)
        down = st.number_input("المقدم %", value=10)
        years = st.number_input("سنين التقسيط", value=8)
        res = (price - (price * down/100)) / (years * 12) if years > 0 else 0
        st.markdown(f"<p class='label-gold'>القسط الشهري:</p><h2>{res:,.0f} ج.م</h2></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h3>📊 حاسبة العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", value=5000000, step=100000)
        comm = st.number_input("نسبة العمولة %", value=2.5, step=0.1)
        st.markdown(f"<p class='label-gold'>صافي عمولتك:</p><h2>{deal*(comm/100):,.0f} ج.م</h2></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ قاعدة المشاريع", "🚀 لانش جديد"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")

elif menu == "المطورين":
    render_grid(df_d, "dev")

st.markdown("<p style='text-align:center; color:#555; font-weight:900; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
