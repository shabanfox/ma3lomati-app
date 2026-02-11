import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. الإعدادات وتنسيق الـ CSS (الخطوط العريضة Bold)
st.set_page_config(page_title="MA3LOMATI PRO 2026", layout="wide", initial_sidebar_state="collapsed")

ITEMS_PER_PAGE = 6
BG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"
HDR = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0px; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.4), rgba(0,0,0,0.9)), url('{HDR}');
        background-size: cover; border-bottom: 5px solid #f59e0b; padding: 50px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 25px;
    }}
    .royal-header h1 {{ color: #f59e0b; font-size: 3rem; font-weight: 900; }}
    .stSelectbox label, .stTextInput label {{ color: #f59e0b !important; font-weight: 900 !important; font-size: 1.2rem !important; }}
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #000 !important; border-right: 12px solid #f59e0b !important;
        font-size: 1.2rem !important; font-weight: 900 !important; min-height: 130px !important; text-align: right !important;
    }}
    .detail-card {{ background: rgba(20,20,20,0.98); padding: 20px; border-radius: 20px; border-top: 6px solid #f59e0b; border: 1px solid #444; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; }}
    .val-white {{ color: #fff; font-size: 1.3rem; font-weight: 700; border-bottom: 1px solid #333; }}
    </style>
""", unsafe_allow_html=True)

# 2. تحميل البيانات
@st.cache_data(ttl=60)
def load_data():
    u = {
        "p": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "d": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
        "l": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    }
    try:
        p, d, l = pd.read_csv(u["p"]), pd.read_csv(u["d"]), pd.read_csv(u["l"])
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# 3. دالة العرض والفلترة
def render_grid(df, px):
    vk, ik, pk = f"v_{px}", f"i_{px}", f"p_{px}"
    if vk not in st.session_state: st.session_state[vk] = "grid"
    if pk not in st.session_state: st.session_state[pk] = 0

    if st.session_state[vk] == "details":
        if st.button("⬅ عودة", key=f"b_{px}", use_container_width=True):
            st.session_state[vk] = "grid"; st.rerun()
        item = df.iloc[st.session_state[ik]]
        c = st.columns(3)
        for i, col in enumerate(df.columns):
            with c[i%3]: st.markdown(f"<div class='detail-card'><p class='label-gold'>{col}</p><p class='val-white'>{item[col]}</p></div>", unsafe_allow_html=True)
    else:
        # فلتر المناطق الديناميكي
        locs = ["الكل"] + sorted([str(x) for x in df['Location'].unique() if str(x) != "---"]) if 'Location' in df.columns else ["الكل"]
        
        with st.container():
            f1, f2 = st.columns(2)
            search = f1.text_input("🔍 بحث بالإسم", key=f"s_{px}")
            area = f2.selectbox("📍 المنطقة", locs, key=f"l_{px}")
        
        filt = df.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(area, case=False, na=False)]

        start = st.session_state[pk] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start+ITEMS_PER_PAGE]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                txt = f"🏠 {r[0]}\n📍 {r.get('Location','---')}\n💰 {int(r['Price']):,} ج.م" if 'Price' in r else f"🏢 {r[0]}"
                if st.button(txt, key=f"card_{px}_{idx}", use_container_width=True):
                    st.session_state[ik], st.session_state[vk] = idx, "details"; st.rerun()
        
        # أزرار الصفحة
        c1, c2, c3 = st.columns([1,2,1])
        if st.session_state[pk] > 0:
            if c1.button("⬅ السابق", key=f"pr_{px}"): st.session_state[pk]-=1; st.rerun()
        if (start+ITEMS_PER_PAGE) < len(filt):
            if c3.button("التالي ➡", key=f"nx_{px}"): st.session_state[pk]+=1; st.rerun()

# 4. التنفيذ
df_p, df_d, df_l = load_data()
st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>2026</p></div>', unsafe_allow_html=True)

m = option_menu(None, ["المطورين", "المشاريع", "المساعد"], icons=["building", "house", "robot"], orientation="horizontal")

if m == "المشاريع":
    t1, t2 = st.tabs(["🏗️ الكل", "🚀 جديد"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")
elif m == "المطورين": render_grid(df_d, "d")
elif m == "المساعد": st.info("AI 2026 Ready")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
