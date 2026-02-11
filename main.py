import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"
HEADER_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"

# --- 3. تحميل البيانات بدقة ---
@st.cache_data(ttl=60)
def load_data():
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            # توحيد مسميات الأعمدة للفلترة
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'Price ': 'Price'}, inplace=True, errors="ignore")
            # تنظيف عمود السعر ليكون أرقام فقط
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 4. تصميم الواجهة (CSS) ---
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
        background-size: cover; border-bottom: 5px solid #f59e0b; padding: 60px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 25px;
    }}
    .royal-header h1 {{ color: #f59e0b; font-size: 3.8rem; font-weight: 900; margin: 0; }}
    .stSelectbox label, .stTextInput label, .stSlider label {{ color: #f59e0b !important; font-size: 1.2rem !important; font-weight: 900 !important; }}
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #000 !important; border-right: 10px solid #f59e0b !important;
        font-size: 1.2rem !important; font-weight: 900 !important; min-height: 130px !important; text-align: right !important;
    }}
    .detail-card {{ background: rgba(20,20,20,0.98); padding: 25px; border-radius: 20px; border-top: 6px solid #f59e0b; border-left: 1px solid #444; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1.1rem; }}
    .val-white {{ color: #fff; font-size: 1.3rem; font-weight: 700; border-bottom: 1px solid #333; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. دالة العرض والفلترة الدقيقة ---
def render_grid(dataframe, prefix):
    if st.session_state.get(f"view_{prefix}") == "details":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state[f"view_{prefix}"] = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state[f"idx_{prefix}"]]
        c1, c2, c3 = st.columns(3)
        cols = dataframe.columns
        for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
            with [c1, c2, c3][i]:
                h = '<div class="detail-card">'
                for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        # --- صندوق الفلاتر الذكي ---
        with st.container():
            st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:20px; border:1px solid #444; margin-bottom:20px;'>", unsafe_allow_html=True)
            f1, f2, f3 = st.columns([2, 2, 3])
            
            with f1: search = st.text_input("🔍 بحث بالإسم...", key=f"s_{prefix}")
            
            with f2:
                # قائمة المناطق المطلوبة بدقة
                target_areas = [
                    "الكل", "العاصمة الإدارية", "التجمع الخامس", "مستقبل سيتي", 
                    "الساحل الشمالي", "البحر الأحمر", "المعادي", "مدينة نصر",
                    "الشيخ زايد", "6 أكتوبر", "الشروق", "هليوبوليس"
                ]
                sel_area = st.selectbox("📍 تصفية حسب المنطقة", target_areas, key=f"l_{prefix}")
            
            with f3:
                if 'Price' in dataframe.columns:
                    min_p = int(dataframe['Price'].min())
                    max_p = int(dataframe['Price'].max())
                    price_range = st.slider("💰 نطاق السعر (ج.م)", min_p, max_p, (min_p, max_p), key=f"p_{prefix}")
                else: price_range = None
            st.markdown("</div>", unsafe_allow_html=True)

        # --- عملية الفلترة الدقيقة ---
        filt = dataframe.copy()
        if search:
            filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        if sel_area != "الكل":
            # فلترة دقيقة: تبحث عن اسم المنطقة المختارة داخل عمود الموقع (Location)
            filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]
        
        if price_range:
            filt = filt[(filt['Price'] >= price_range[0]) & (filt['Price'] <= price_range[1])]

        # --- العرض ---
        start = st.session_state.get(f"page_{prefix}", 0) * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            if filt.empty: st.warning("⚠️ لا توجد نتائج تطابق هذه الفلاتر")
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if prefix == "dev":
                        owner = r.get('Owner', r.get('المالك', '---'))
                        txt = f"🏢 {r[0]}\n👤 المالك: {owner}"
                    else:
                        p_txt = f"{int(r['Price']):,}" if 'Price' in r else "---"
                        txt = f"🏠 {r[0]}\n📍 {r.get('Location','---')}\n💰 يبدأ من: {p_txt} ج.م"
                    
                    if st.button(txt, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state[f"idx_{prefix}"] = idx
                        st.session_state[f"view_{prefix}"] = "details"
                        st.rerun()
            
            # التنقل
            st.write("")
            c_p1, c_px, c_p2 = st.columns([1, 2, 1])
            with c_p1:
                if st.session_state.get(f"page_{prefix}", 0) > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}"): 
                        st.session_state[f"page_{prefix}"] = st.session_state.get(f"page_{prefix}", 0) - 1
                        st.rerun()
            with c_px: st.markdown(f"<p style='text-align:center; font-weight:900; color:#f59e0b; font-size:1.4rem;'>صفحة {st.session_state.get(f"page_{prefix}", 0) + 1}</p>", unsafe_allow_html=True)
            with c_p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}"):
                        st.session_state[f"page_{prefix}"] = st.session_state.get(f"page_{prefix}", 0) + 1
                        st.rerun()
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:900; font-size:1.3rem; border-bottom:3px solid #f59e0b;'>⭐ مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:15]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state[f"idx_{prefix}"] = s_idx
                    st.session_state[f"view_{prefix}"] = "details"
                    st.rerun()

# --- 6. تشغيل التطبيق ---
df_p, df_d, df_l = load_data()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>دليلك العقاري الأذكى لعام 2026</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "house", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; font-weight:900;'>🛠️ حاسبات البروكر الاحترافية</h2>", unsafe_allow_html=True)
    # (هنا توضع كود الحاسبات كما في النسخ السابقة)
elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ قاعدة المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")
elif menu == "المطورين":
    render_grid(df_d, "dev")
elif menu == "المساعد الذكي":
    st.info("نظام تحليل البيانات بالذكاء الاصطناعي جاري تحديثه...")

st.markdown("<p style='text-align:center; color:#444; font-weight:900; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
