import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# المتغيرات الثابتة لضمان استقرار التطبيق
ITEMS_PER_PAGE = 6
HEADER_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"

# --- 2. دالة تحميل البيانات ---
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

# --- 3. التصميم (CSS) - خطوط عريضة وتنسيق موبايل ---
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
    .royal-header h1 {{ color: #f59e0b; font-size: 3.2rem; font-weight: 900; }}
    
    .stSelectbox label, .stTextInput label, .stSlider label {{ color: #f59e0b !important; font-size: 1.2rem !important; font-weight: 900 !important; }}
    
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #000 !important; border-right: 12px solid #f59e0b !important;
        font-size: 1.2rem !important; font-weight: 900 !important; min-height: 130px !important; text-align: right !important;
    }}
    .detail-card {{ background: rgba(20,20,20,0.98); padding: 20px; border-radius: 20px; border-top: 6px solid #f59e0b; border: 1px solid #444; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1.1rem; }}
    .val-white {{ color: #fff; font-size: 1.3rem; font-weight: 700; margin-bottom: 10px; border-bottom: 1px solid #333; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. دالة العرض والفلترة ---
def render_grid(dataframe, prefix):
    # إدارة الحالة لكل قسم بشكل منفصل
    v_key, i_key, p_key = f"v_{prefix}", f"idx_{prefix}", f"pg_{prefix}"
    if v_key not in st.session_state: st.session_state[v_key] = "grid"
    if p_key not in st.session_state: st.session_state[p_key] = 0

    if st.session_state[v_key] == "details":
        if st.button("⬅ عودة للقائمة", key=f"b_{prefix}", use_container_width=True):
            st.session_state[v_key] = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state[i_key]]
        cols = st.columns(3)
        for i, col in enumerate(dataframe.columns):
            with cols[i % 3]:
                st.markdown(f"<div class='detail-card'><p class='label-gold'>{col}</p><p class='val-white'>{item[col]}</p></div>", unsafe_allow_html=True)
    else:
        # استخراج المناطق الفريدة أوتوماتيكياً من الشيت
        if 'Location' in dataframe.columns:
            unique_locs = sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() != "---"])
            area_options = ["الكل"] + unique_locs
        else:
            area_options = ["الكل"]

        # شريط الفلاتر
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border:1px solid #444; margin-bottom:20px;'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2, 2, 3])
        with f1: search = st.text_input("🔍 بحث بالإسم", key=f"s_{prefix}")
        with f2: sel_area = st.selectbox("📍 اختيار المنطقة", area_options, key=f"l_{prefix}")
        with f3:
            if 'Price' in dataframe.columns and not dataframe.empty:
                min_p, max_p = int(dataframe['Price'].min()), int(dataframe['Price'].max())
                price_range = st.slider("💰 ميزانية العميل", min_p, max_p, (min_p, max_p), key=f"p_{prefix}")
            else: price_range = None
        st.markdown("</div>", unsafe_allow_html=True)

        # منطق الفلترة
        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]
        if price_range: filt = filt[(filt['Price'] >= price_range[0]) & (filt['Price'] <= price_range[1])]

        # العرض
        start = st.session_state[p_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_val = f"{int(r['Price']):,}" if 'Price' in r else "---"
                    txt = f"🏠 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_val} ج.م"
                    if st.button(txt, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state[i_key], st.session_state[v_key] = idx, "details"; st.rerun()
            
            # التنقل
            st.write("")
            p1, px, p2 = st.columns([1, 2, 1])
            with p1:
                if st.session_state[p_key] > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state[p_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#f59e0b; font-weight:900;'>صفحة {st.session_state[p_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}"): st.session_state[p_key] += 1; st.rerun()
        
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:900; border-bottom:2px solid #f59e0b;'>⭐ مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"📌 {str(s_row[0])[:15]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state[i_key], st.session_state[v_key] = s_idx, "details"; st.rerun()

# --- 5. تشغيل التطبيق ---
df_p, df_d, df_l = load_data()
st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>النسخة الاحترافية 2026</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["building", "house", "robot"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ قاعدة المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")
elif menu == "المطورين":
    render_grid(df_d, "dev")
elif menu == "المساعد الذكي":
    st.info("نظام تحليل البيانات بالذكاء الاصطناعي 2026")

st.markdown("<p style='text-align:center; color:#555; font-weight:900; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
