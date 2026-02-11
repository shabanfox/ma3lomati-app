import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة ---
if 'auth' not in st.session_state:
    st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. الروابط والثوابت ---
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
DEFAULT_LOGO = "https://cdn-icons-png.flaticon.com/512/609/609803.png" # أيقونة افتراضية فخمة
ITEMS_PER_PAGE = 6

# --- 4. تحميل ومعالجة البيانات ---
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
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price', 'Logo': 'Image', 'صورة': 'Image'}, inplace=True, errors="ignore")
            
            # معالجة الأسعار (الملايين)
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. دالة العرض مع الصور المصغرة ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"### 📄 {item.iloc[0]}")
        cols = st.columns(3)
        for i, col in enumerate(dataframe.columns):
            if col == 'Image': continue # لا نعرض رابط الصورة كنص
            with cols[i % 3]:
                val = item[col]
                if col == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل"
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
    else:
        # البحث والفلترة
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 بحث...", key=f"s_{prefix}")
        with f2:
            locs = ["الكل"] + sorted([str(x) for x in dataframe['Location'].unique() if str(x) != "---"]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 المنطقة", locs, key=f"l_{prefix}")

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False)]

        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                p_val = f"{int(r['Price']):,}" if r['Price'] > 0 else "اتصل للسعر"
                img_url = r['Image'] if ('Image' in r and str(r['Image']) != "---") else DEFAULT_LOGO
                
                # تصميم الكارت الذي يحتوي على الصورة والاسم
                # نستخدم Markdown لعرض الصورة فوق الزر مباشرة لإعطاء مظهر احترافي
                st.markdown(f"""
                <div style="margin-bottom:-45px; margin-right:20px; position:relative; z-index:99;">
                    <img src="{img_url}" style="width:50px; height:50px; border-radius:50%; border:2px solid #f59e0b; background:white; object-fit:contain;">
                </div>
                """, unsafe_allow_html=True)
                
                card_text = f"🏢 {r[0]}\n\n📍 {r.get('Location','---')}\n💰 {p_val} ج.م"
                if st.button(card_text, key=f"card_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- 6. التنسيق (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{ background: #000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; border-bottom: 3px solid #f59e0b; padding: 40px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px; }}
    div.stButton > button[key*="card_"] {{ 
        background: white !important; color: black !important; 
        border-right: 12px solid #f59e0b !important; border-radius: 20px !important; 
        text-align: right !important; min-height: 160px !important; 
        font-weight: 900 !important; padding-top: 30px !important;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.2) !important;
    }}
    .detail-card {{ background: #111; padding: 15px; border-radius: 12px; border-top: 4px solid #f59e0b; border: 1px solid #333; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; margin:0; }}
    .val-white {{ color: white; font-size: 1.1rem; margin:0; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. التشغيل ---
df_p, df_d, df_l = load_data()

if not st.session_state.auth:
    # واجهة الدخول المختصرة
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    p = st.text_input("كلمة السر", type="password")
    if st.button("دخول"):
        if p == "2026": st.session_state.auth = True; st.rerun()
else:
    st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)
    menu = option_menu(None, ["المطورين", "المشاريع", "اللونشات"], icons=["building", "search", "rocket"], orientation="horizontal")
    
    if menu == "المشاريع": render_grid(df_p, "p")
    elif menu == "اللونشات": render_grid(df_l, "l")
    else: render_grid(df_d, "d")
