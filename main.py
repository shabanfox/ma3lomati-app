import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة والحفاظ على الجلسة ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط والثوابت ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف الأساسية ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if user_input == name_s.lower() and str(pwd_input) == pass_s:
                    return name_s
        return None
    except: return None

def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

# --- 5. دالة العرض المحدثة (حل مشكلة كروت التفاصيل) ---
def render_grid(dataframe, prefix):
    # استخدام مفتاح فريد للصفحات لكل قسم
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        # زر العودة بتنسيق واضح
        if st.button("⬅ عودة للقائمة الرئيسية", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        # جلب البيانات المختارة
        try:
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"### 📄 تفاصيل: {item.iloc[0]}")
            
            # توزيع التفاصيل في كروت منظمة (3 أعمدة)
            cols_count = 3
            st_cols = st.columns(cols_count)
            for i, col_name in enumerate(dataframe.columns):
                with st_cols[i % cols_count]:
                    st.markdown(f"""
                    <div class="detail-card">
                        <p class="label-gold">{col_name}</p>
                        <p class="val-white">{item[col_name]}</p>
                    </div>
                    """, unsafe_allow_html=True)
        except Exception as e:
            st.error("عذراً، حدث خطأ في عرض البيانات.")
            st.session_state.view = "grid"
            
    else:
        # --- شريط الفلاتر المطور ---
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border:1px solid #333;'>", unsafe_allow_html=True)
        f1, f2, f3 = st.columns([2, 2, 3])
        
        with f1: search = st.text_input("🔍 بحث بالإسم...", key=f"s_{prefix}")
        with f2:
            loc_list = ["الكل"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 المنطقة", loc_list, key=f"l_{prefix}")
        with f3:
            if 'Price' in dataframe.columns:
                min_p, max_p = int(dataframe['Price'].min()), int(dataframe['Price'].max())
                price_range = st.slider("💰 الميزانية", min_p, max_p + 100, (min_p, max_p + 100), key=f"p_{prefix}")
            else: price_range = None
        st.markdown("</div>", unsafe_allow_html=True)

        # منطق التصفية
        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]
        if price_range: filt = filt[(filt['Price'] >= price_range[0]) & (filt['Price'] <= price_range[1])]

        # العرض والتقسيم
        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.78, 0.22])
        with m_c:
            if filt.empty: st.info("لا توجد نتائج تطابق بحثك")
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    p_val = f"{int(r['Price']):,}" if 'Price' in r else "---"
                    card_content = f"🏠 **{r[0]}**\n\n📍 {r.get('Location','---')}\n💰 {p_val} ج.م"
                    if st.button(card_content, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # أزرار التنقل
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#f59e0b; font-weight:bold;'>{st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}"): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:2px solid #333;'>🔥 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:18]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 6. التنسيق الجمالي (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 50px; }}
    .oval-header {{ background-color: #000; border: 3px solid #f59e0b; border-radius: 60px; padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900; text-align: center; margin-bottom: -30px; min-width: 360px; z-index: 10; }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b; padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 15px; }}
    .royal-header h1 {{ color: #f59e0b; font-size: 3rem; font-weight: 900; margin: 0; }}
    
    /* تنسيق كروت الشبكة */
    div.stButton > button[key*="card_"] {{ 
        background: white !important; color: black !important; 
        border-right: 10px solid #f59e0b !important; border-radius: 15px !important;
        text-align: right !important; min-height: 140px !important; font-weight: 900 !important; 
    }}
    
    /* تنسيق كروت التفاصيل */
    .detail-card {{ 
        background: rgba(30, 30, 30, 0.9); padding: 20px; border-radius: 15px; 
        border: 1px solid #444; border-top: 5px solid #f59e0b; margin-bottom: 15px;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1rem; margin-bottom: 5px; }}
    .val-white {{ color: white; font-size: 1.2rem; font-weight: bold; }}
    
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: black !important; font-weight: 900 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. بوابة تسجيل الدخول ---
if not st.session_state.get('auth', False):
    st.markdown("<div class='auth-wrapper'><div class='oval-header'>MA3LOMATI PRO</div><div class='auth-card'>", unsafe_allow_html=True)
    u = st.text_input("User", placeholder="الأسم", key="log_u")
    p = st.text_input("Pass", type="password", placeholder="كلمة السر", key="log_p")
    if st.button("SIGN IN 🚀", use_container_width=True):
        if p == "2026": 
            st.session_state.auth, st.session_state.current_user = True, "Admin"
            st.query_params["u_session"] = "Admin"; st.rerun()
        else:
            user = login_user(u, p)
            if user:
                st.session_state.auth, st.session_state.current_user = True, user
                st.query_params["u_session"] = user; st.rerun()
            else: st.error("خطأ في البيانات")
    st.markdown("</div></div>", unsafe_allow_html=True); st.stop()

# --- 8. تحميل البيانات ---
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
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 9. الواجهة الرئيسية ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

# إعادة تعيين الحالة عند تغيير المنيو
if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

# --- 10. تنفيذ الأقسام ---
if menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=5000000, step=100000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنين", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>القسط الشهري:</p><p class='val-white'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", value=5000000)
        pct = st.number_input("النسبة %", value=2.5)
        st.markdown(f"<p class='label-gold'>العمولة:</p><p class='val-white'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card'><h3>📈 العائد ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", value=5000000)
        rent = st.number_input("الإيجار", value=40000)
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-gold'>العائد السنوي:</p><p class='val-white'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 اللونشات"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")

elif menu == "المطورين":
    render_grid(df_d, "d")

elif menu == "المساعد الذكي":
    st.info("نظام تحليل البيانات العقارية 2026")

# زر الخروج في السايدبار
if st.sidebar.button("🚪 خروج"): logout()
st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
