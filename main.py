import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# المتغيرات الثابتة لضمان استقرار التطبيق
ITEMS_PER_PAGE = 6
HEADER_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"

# --- 2. دالة تحميل البيانات وتنظيفها ---
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

# --- 3. التصميم (CSS) - خطوط عريضة وتنسيق ملكي ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0px; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    .royal-header {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.4), rgba(0,0,0,0.9)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 5px solid #f59e0b; padding: 50px 20px; text-align: center;
        border-radius: 0 0 40px 40px; margin-bottom: 25px;
    }}
    .royal-header h1 {{ color: #f59e0b; font-size: 3.5rem; font-weight: 900; text-shadow: 2px 2px 10px #000; }}
    
    .stSelectbox label, .stTextInput label, .stSlider label {{ color: #f59e0b !important; font-size: 1.3rem !important; font-weight: 900 !important; }}
    
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #000 !important; border-right: 12px solid #f59e0b !important;
        font-size: 1.25rem !important; font-weight: 900 !important; min-height: 140px !important; text-align: right !important;
    }}
    .detail-card {{ background: rgba(20,20,20,0.98); padding: 25px; border-radius: 20px; border-top: 8px solid #f59e0b; border: 1px solid #444; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1.2rem; }}
    .val-white {{ color: #fff; font-size: 1.4rem; font-weight: 700; margin-bottom: 15px; border-bottom: 1px solid #333; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة العرض والفلترة الذكية ---
def render_grid(dataframe, prefix):
    # إدارة حالة كل قسم (Prefix) لضمان عدم التداخل
    v_key, i_key, p_key = f"v_{prefix}", f"idx_{prefix}", f"pg_{prefix}"
    if v_key not in st.session_state: st.session_state[v_key] = "grid"
    if p_key not in st.session_state: st.session_state[p_key] = 0

    if st.session_state[v_key] == "details":
        if st.button("⬅ عودة للقائمة", key=f"b_{prefix}", use_container_width=True):
            st.session_state[v_key] = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state[i_key]]
        cols = st.columns(3)
        for i, col_name in enumerate(dataframe.columns):
            with cols[i % 3]:
                st.markdown(f"<div class='detail-card'><p class='label-gold'>{col_name}</p><p class='val-white'>{item[col_name]}</p></div>", unsafe_allow_html=True)
    else:
        # استخراج قائمة المناطق الفريدة من الشيت
        if 'Location' in dataframe.columns:
            raw_locs = dataframe['Location'].unique().tolist()
            # تنظيف القائمة من الفراغات والـ "---"
            clean_locs = sorted([str(x).strip() for x in raw_locs if str(x).strip() not in ["---", "nan", ""]])
            area_options = ["الكل"] + clean_locs
        else:
            area_options = ["الكل"]

        # صندوق الفلاتر
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:20px; border:1px solid #444; margin-bottom:25px;'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2, 2, 3])
        with f1: search = st.text_input("🔍 ابحث بالإسم...", key=f"s_{prefix}")
        with f2: sel_area = st.selectbox("📍 تصفية المنطقة", area_options, key=f"l_{prefix}")
        with f3:
            if 'Price' in dataframe.columns and not dataframe.empty:
                min_p, max_p = int(dataframe['Price'].min()), int(dataframe['Price'].max())
                price_range = st.slider("💰 ميزانية العميل", min_p, max_p, (min_p, max_p), key=f"p_{prefix}")
            else: price_range = None
        st.markdown("</div>", unsafe_allow_html=True)

        # منطق الفلترة المتقدم
        filt = dataframe.copy()
        if search: 
            filt = filt[filt.apply(lambda r
