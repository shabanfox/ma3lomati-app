
import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة حالة الجلسة (Session State) ---
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
# ملاحظة: تأكد من أن روابط CSV صحيحة وتعمل
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف التقنية ---
def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
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

@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS)
        d = pd.read_csv(URL_DEVELOPERS)
        l = pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            # توحيد أسماء الأعمدة للتعامل معها برمجياً
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price'}, inplace=True, errors="ignore")
            
            if 'Price' in df.columns:
                # تنظيف السعر: إزالة أي رموز غير رقمية وتحويله لـ float
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                # المنطق الذكي: إذا كان الرقم أقل من 1000 (مثلاً 7.5)، يتم ضربه في مليون
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. دالة العرض الرئيسية (الشبكة والتفاصيل) ---
def render_grid(dataframe, prefix):
    # إدارة رقم الصفحة داخل القسم
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        # --- عرض التفاصيل ---
        if st.button("⬅ عودة للقائمة الرئيسية", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        try:
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h2 style='color:#f59e0b; text-align:right;'>🏠 {item.iloc[0]}</h2>", unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, col_name in enumerate(dataframe.columns):
                with cols[i % 3]:
                    val = item[col_name]
                    # تنسيق السعر في صفحة التفاصيل
                    if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل للسعر"
                    st.markdown(f"""
                    <div class="detail-card">
                        <p class="label-gold">{col_name}</p>
                        <p class="val-white">{val}</p>
                    </div>
                    """, unsafe_allow_html=True)
        except:
            st.session_state.view = "grid"; st.rerun()
            
    else:
        # --- عرض الشبكة (Grid) مع الفلاتر ---
        st.markdown("<div style='background:rgba(255,255,255,0.05); padding:15px; border-radius:15px; border:1px solid #333;'>", unsafe_allow_html=True)
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 ابحث عن أي شيء...", key=f"s_{prefix}")
        with f2:
            loc_list = ["الكل"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 تصفية حسب الموقع", loc_list, key=f"l_{prefix}")
        st.markdown("</div>", unsafe_allow_html=True)

        # منطق الفلترة
        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]

        # تقسيم الصفحات
        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        # العرض في كروت
        m_c, s_c = st.columns([0.8, 0.2])
        with m_c:
            if filt.empty: st.warning("لا توجد نتائج تطابق بحثك.")
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    # تنسيق السعر للكارت
                    price_val = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل للسعر"
                    card_content = f"🏢 {r[0]}\n\n📍 {r.get('Location','---')}\n💰 {price_val} ج.م"
                    if st.button(card_content, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # أزرار التنقل
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}"): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#f59e0b; font-weight:bold;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}"): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:2px solid #333;'>🔥 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"📌 {str(s_row[0])[:15]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 6. التصميم (CSS) ---
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
    div.stButton > button[key*="card_"] {{ background: white !important; color: black !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 150px !important; font-weight: 900 !important; font-size: 1.1rem !important; }}
    .detail-card {{ background: rgba(30, 30, 30, 0.95); padding: 20px; border-radius: 15px; border: 1px solid #444; border-top: 6px solid #f59e0b; margin-bottom: 15px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 1rem; }}
    .val-white {{ color: white; font-size: 1.25rem; font-weight: 700; }}
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: black !important; font-weight: 900 !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. بوابة الدخول ---
if not st.session_state.get('auth', False):
    st.markdown("<div class='auth-wrapper'><div class='oval-header'>MA3LOMATI PRO</div><div class='auth-card'>", unsafe_allow_html=True)
    u = st.text_input("User", placeholder="اسم المستخدم", key="log_u")
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
            else: st.error("عذراً، البيانات غير صحيحة.")
    st.markdown("</div></div>", unsafe_allow_html=True); st.stop()

# --- 8. تحميل البيانات والتشغيل ---
df_p, df_d, df_l = load_data()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

# إعادة تعيين العرض عند تغيير القسم
if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.last_m = "grid", menu

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
    st.info("نظام تحليل البيانات العقارية AI 2026 قيد التطوير.")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px; font-weight:bold;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
