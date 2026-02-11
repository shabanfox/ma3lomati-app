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

# --- 3. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. تحميل البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. التصميم الملكي (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إزالة المساحة العلوية تماماً */
    header, [data-testid="stHeader"] {{ visibility: hidden; height: 0px; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.94), rgba(0,0,0,0.94)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}

    /* الهيدر المطور */
    .royal-header {{
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.3), rgba(0,0,0,0.9)), url('{HEADER_IMG}');
        background-size: cover; background-position: center;
        border-bottom: 5px solid #f59e0b; padding: 60px 20px; text-align: center;
        border-radius: 0 0 50px 50px; margin-bottom: 30px;
    }}
    .royal-header h1 {{ color: #f59e0b; font-size: 4.5rem; font-weight: 900; margin: 0; text-shadow: 4px 4px 15px #000; }}
    
    /* تكبير خطوط الأزرار والقوائم */
    .stSelectbox label, .stTextInput label, .stSlider label {{ color: #f59e0b !important; font-size: 1.3rem !important; font-weight: 900 !important; }}
    div.stButton > button {{ font-size: 1.3rem !important; font-weight: 900 !important; border-radius: 12px !important; }}
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #000 !important; border-right: 12px solid #f59e0b !important;
        min-height: 150px !important; text-align: right !important; transition: 0.4s;
    }}
    div.stButton > button:hover {{ transform: translateY(-5px); box-shadow: 0 10px 20px rgba(245,158,11,0.3) !important; }}

    /* تفاصيل الكروت */
    .detail-card {{ background: rgba(20,20,20,0.98); padding: 30px; border-radius: 25px; border: 1px solid #444; border-top: 8px solid #f59e0b; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1.2rem; }}
    .val-white {{ color: #fff; font-size: 1.4rem; font-weight: 700; border-bottom: 1px solid #333; padding-bottom: 10px; margin-bottom: 15px; }}
    
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: #000 !important; font-weight: 900 !important; font-size: 1.2rem !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. دالة العرض مع فلاتر المناطق المحددة ---
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
        # تصميم الفلاتر
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:20px; border-radius:20px; border:1px solid #444;'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2, 2, 3])
        
        with f1: search = st.text_input("🔍 بحث سـريع بالإسم...", key=f"s_{prefix}")
        
        with f2:
            # قائمة المناطق المحددة والمضافة
            custom_areas = [
                "الكل", "العاصمة الإدارية", "التجمع الخامس", "مستقبل سيتي", 
                "الساحل الشمالي", "البحر الأحمر", "المعادي", "مدينة نصر",
                "الشيخ زايد", "6 أكتوبر", "هليوبوليس", "القاهرة الجديدة"
            ]
            sel_area = st.selectbox("📍 اختار المنطقة", custom_areas, key=f"l_{prefix}")
        
        with f3:
            price_col = 'Price' if 'Price' in dataframe.columns else None
            if price_col:
                dataframe[price_col] = pd.to_numeric(dataframe[price_col].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
                price_range = st.slider("💰 ميزانية العميل (ج.م)", int(dataframe[price_col].min()), int(dataframe[price_col].max()), (int(dataframe[price_col].min()), int(dataframe[price_col].max())), key=f"p_{prefix}")
            else: price_range = None
        st.markdown("</div>", unsafe_allow_html=True)

        # التصفية
        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل":
            # دعم البحث عن كلمات مشابهة في عمود الموقع
            filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False)]
        if price_range: filt = filt[(filt[price_col] >= price_range[0]) & (filt[price_col] <= price_range[1])]

        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if prefix == "dev":
                        owner = r.get('Owner', r.get('المالك', '---'))
                        txt = f"🏢 {r[0]}\n👤 المالك: {owner}"
                    else:
                        p_txt = f"{int(r['Price']):,}" if 'Price' in r else "---"
                        txt = f"🏠 {r[0]}\n📍 {r.get('Location','---')}\n💰 السعر: {p_txt} ج.م"
                    if st.button(txt, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # أزرار التنقل
            st.markdown("<br>", unsafe_allow_html=True)
            p1, p_info, p2 = st.columns([1, 2, 1])
            with p1: 
                if st.session_state.page_num > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state.page_num -= 1; st.rerun()
            with p_info: st.markdown(f"<p style='text-align:center; color:#f59e0b; font-weight:900; font-size:1.5rem;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}"): st.session_state.page_num += 1; st.rerun()
        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:900; font-size:1.4rem; border-bottom:3px solid #f59e0b; padding-bottom:5px;'>⭐ الأكثر طلباً</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:15]}...", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 7. سير العمل ---
df_p, df_d, df_l = load_data()

# الهيدر الملكي الصافي
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p>النسخة الاحترافية 2026</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "house", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900", "font-size": "1.3rem"}})

if menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; font-weight:900;'>🛠️ حاسبات البروكر الذكية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("إجمالي السعر", 5000000, step=100000, key="ca1")
        dp = st.number_input("المقدم %", 10, key="ca2")
        yr = st.number_input("السنين", 8, key="ca3")
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>القسط الشهري:</p><p class='val-white'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", 5000000, step=100000, key="cb1")
        pct = st.number_input("النسبة %", 2.5, step=0.1, key="cb2")
        st.markdown(f"<p class='label-gold'>العمولة الصافية:</p><p class='val-white'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card'><h3>📈 العائد ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", 5000000, key="cc1")
        rent = st.number_input("الإيجار الشهري", 40000, key="cc2")
        st.markdown(f"<p class='label-gold'>العائد السنوي:</p><p class='val-white'>{((rent*12)/buy)*100:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ كل المشاريع", "🚀 المشاريع الجديدة"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")

elif menu == "المطورين":
    render_grid(df_d, "dev")

elif menu == "المساعد الذكي":
    st.info("نظام AI متطور لعام 2026 قيد التحليل")

st.markdown("<p style='text-align:center; color:#555; font-weight:900; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
