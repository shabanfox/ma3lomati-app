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

if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. الروابط والثوابت ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

HEADER_IMG = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1200&q=80"
ITEMS_PER_PAGE = 6

# --- 4. الوظائف التقنية لربط البيانات ---
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
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1000000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. دالة العرض الذكية المصلحة خطأ الـ KeyError والخط المحدث ---
def render_grid(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    v_key = f"view_{prefix}"
    
    if pg_key not in st.session_state: st.session_state[pg_key] = 0
    if v_key not in st.session_state: st.session_state[v_key] = "grid"

    if st.session_state[v_key] == "details":
        # --- صفحة التفاصيل الفاخرة ---
        if st.button("⬅ عودة للقائمة الرئيسية", key=f"back_{prefix}", use_container_width=True): 
            st.session_state[v_key] = "grid"; st.rerun()
        
        try:
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h2 style='color:#000000; text-align:right; font-weight:900; margin:20px 0;'>🏢 {item.iloc[0]}</h2>", unsafe_allow_html=True)
            
            cols = st.columns(3)
            for i, col_name in enumerate(dataframe.columns):
                with cols[i % 3]:
                    val = item[col_name]
                    if col_name == 'Price': val = f"{int(val):,}" if float(val) > 0 else "اتصل للسعر"
                    st.markdown(f"""
                    <div class="detail-card">
                        <p class="label-gold">{col_name}</p>
                        <p class="val-black">{val}</p>
                    </div>
                    """, unsafe_allow_html=True)
        except:
            st.session_state[v_key] = "grid"; st.rerun()
            
    else:
        # --- شاشة عرض الشبكة (Grid) مع الفلاتر ---
        st.markdown("<div class='filter-box'>", unsafe_allow_html=True)
        f1, f2 = st.columns([2, 1])
        with f1: search = st.text_input("🔍 ابحث عن أي مشروع، مطور، أو تفاصيل...", key=f"s_{prefix}", label_visibility="collapsed", placeholder="اكتب للبحث الفوري...")
        with f2:
            loc_list = ["الكل"] + sorted([str(x).strip() for x in dataframe['Location'].unique() if str(x).strip() not in ["---", "nan", ""]]) if 'Location' in dataframe.columns else ["الكل"]
            sel_area = st.selectbox("📍 تصفية حسب الموقع", loc_list, key=f"l_{prefix}", label_visibility="collapsed")
        st.markdown("</div>", unsafe_allow_html=True)

        filt = dataframe.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل": filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]

        start = st.session_state[pg_key] * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.75, 0.25])
        with m_c:
            if filt.empty: 
                st.warning("لا توجد نتائج تطابق خيارات البحث الحالية.")
            else:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        price_val = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل للسعر"
                        card_content = f"🏢 {r.iloc[0]}\n📍 {r.get('Location','---')}\n💰 {price_val} ج.م"
                        if st.button(card_content, key=f"btn_card_{prefix}_{idx}", use_container_width=True):
                            st.session_state.current_index = idx
                            st.session_state[v_key] = "details"
                            st.rerun()
            
            # أزرار التنقل بين الصفحات
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("⬅ السابق", key=f"prev_{prefix}", use_container_width=True): st.session_state[pg_key] -= 1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#000000; font-weight:900; font-size:16px; margin-top:5px;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", key=f"next_{prefix}", use_container_width=True): st.session_state[pg_key] += 1; st.rerun()

        with s_c:
            st.markdown("<p class='side-title'>⭐ مقترحات المنصة</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(6).iterrows():
                if st.button(f"📌 {str(s_row.iloc[0])[:25]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index = s_idx
                    st.session_state[v_key] = "details"
                    st.rerun()

# --- 6. قوالب الـ CSS المحدثة بالكامل (وضع فاتح فائق الوضوح - خطوط سوداء عريضة) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@600;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 1rem !important; padding-bottom: 1rem !important; }}
    
    /* خلفية بيضاء ناصعة وواضحة جداً */
    [data-testid="stAppViewContainer"] {{
        background-color: #f8fafc !important;
        direction: rtl !important; text-align: right !important; 
        font-family: 'Cairo', sans-serif !important; color: #000000 !important;
    }}
    
    /* إجبار جميع النصوص الافتراضية في ستريمليت لتصبح سوداء عريضة */
    p, span, label, h1, h2, h3, h4, h5, h6 {{
        color: #000000 !important;
        font-weight: 900 !important;
    }}
    
    /* صندوق تسجيل الدخول الفاخر الواضح */
    .login-box {{
        background: #ffffff; border: 3px solid #000000; padding: 40px 30px; 
        border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); margin-top: 40px;
    }}
    .oval-header {{
        background: #000000; border: 2px solid #000000;
        border-radius: 12px; padding: 15px; color: #ffffff !important; font-size: 26px; font-weight: 900;
        text-align: center; margin-bottom: 25px;
    }}
    .oval-header p {{ color: #ffffff !important; }}

    /* هيدر المنصة العلوي */
    .royal-header {{ 
        background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.95)), url('{HEADER_IMG}'); 
        background-size: cover; background-position: center; border-bottom: 4px solid #000000; 
        padding: 45px 20px; text-align: center; border-radius: 15px; margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }}
    .royal-header h1 {{ color: #000000 !important; font-size: 3rem; font-weight: 900; margin: 0; }}
    
    /* صناديق الفلاتر والبحث */
    .filter-box {{ background: #ffffff; padding: 18px; border-radius: 12px; border: 3px solid #000000; margin-bottom: 25px; }}
    
    /* كروت الأزرار الرئيسية - نص أسود غامق عريض وخلفية بيضاء صريحة */
    div.stButton > button {{
        font-family: 'Cairo', sans-serif !important; font-weight: 900 !important;
        border-radius: 12px !important; transition: all 0.2s ease !important;
    }}
    
    div.stButton > button[id*="btn_card_"] {{
        background: #ffffff !important; color: #000000 !important;
        border: 3px solid #000000 !important; border-right: 15px solid #e5a93c !important;
        text-align: right !important; min-height: 140px !important; 
        font-size: 17px !important; line-height: 1.8 !important;
        white-space: pre-line !important; display: block !important; width: 100% !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.03) !important;
    }}
    div.stButton > button[id*="btn_card_"]:hover {{
        background: #f1f5f9 !important; transform: scale(1.01) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important;
    }}
    
    /* كروت تفاصيل المشروع من الداخل */
    .detail-card {{ 
        background: #ffffff; padding: 22px; border-radius: 14px; 
        border: 3px solid #000000; border-top: 8px solid #e5a93c; margin-bottom: 15px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }}
    .label-gold {{ color: #a16207 !important; font-weight: 900 !important; font-size: 15px; margin: 0 0 6px 0; }}
    .val-black {{ color: #000000 !important; font-size: 19px; font-weight: 900 !important; margin: 0; }}
    
    /* القوائم الجانبية والمقترحات */
    .side-title {{ color: #000000 !important; font-weight: 900; border-bottom: 3px solid #000000; padding-bottom: 8px; margin-bottom: 15px; font-size: 17px; }}
    div.stButton > button[id*="side_"] {{ 
        background: #ffffff !important; color: #000000 !important; 
        border: 2px solid #000000 !important; font-size: 14px !important; 
        text-align: right !important; margin-bottom: 8px !important; font-weight: 900 !important;
    }}
    div.stButton > button[id*="side_"]:hover {{ background: #f1f5f9 !important; border-color: #e5a93c !important; }}
    
    /* تعديل مدخلات النصوص لتصبح واضحة جداً بقلم عريض */
    div.stTextInput input, div.stNumberInput input {{ 
        background-color: #ffffff !important; color: #000000 !important; 
        border: 3px solid #000000 !important; border-radius: 10px !important; 
        height: 48px !important; text-align: center !important; font-weight: 900 !important; font-size: 16px !important;
    }}
    
    /* تعديل أزرار التنقل والرجوع واللوجين */
    div.stButton > button[id*="btn_submit_login"], div.stButton > button[id*="back_"], div.stButton > button[id*="prev_"], div.stButton > button[id*="next_"] {{
        background: #000000 !important; color: #ffffff !important;
        font-weight: 900 !important; border: 3px solid #000000 !important; height: 48px !important; font-size: 16px !important;
    }}
    div.stButton > button[id*="btn_submit_login"]:hover, div.stButton > button[id*="back_"]:hover {{ background: #222222 !important; }}
    
    /* التابات (Tabs) */
    .stTabs [data-baseweb="tab"] {{ color: #000000 !important; font-weight: 900 !important; font-size: 16px !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 7. بوابة الدخول الآمنة ---
if not st.session_state.get('auth', False):
    _, auth_col, _ = st.columns([1.1, 1.3, 1.1])
    with auth_col:
        st.markdown("<div class='login-box'>", unsafe_allow_html=True)
        st.markdown("<div class='oval-header'><p style='margin:0; color:#fff;'>MA3LOMATI PRO</p></div>", unsafe_allow_html=True)
        u = st.text_input("User", placeholder="اسم المستخدم", key="log_u", label_visibility="collapsed")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر الأمانية", key="log_p", label_visibility="collapsed")
        st.write("")
        if st.button("تسجيل الدخول للمنصة 🚀", use_container_width=True, key="btn_submit_login"):
            if p == "2026": 
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.query_params["u_session"] = "Admin"; st.rerun()
            else:
                user = login_user(u, p)
                if user:
                    st.session_state.auth, st.session_state.current_user = True, user
                    st.query_params["u_session"] = user; st.rerun()
                else: st.error("عذراً، اسم المستخدم أو كلمة السر غير صحيحة.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 8. تحميل البيانات والتشغيل الداخلي بعد النجاح ---
df_p, df_d, df_l = load_data()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#000000; font-weight:900; font-size:18px; margin-top:10px;">مرحباً بك يا خبير العقارات: {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "#ffffff", "border": "3px solid #000000", "border-radius": "12px", "padding": "3px"},
        "nav-link": {"color": "#000000", "font-family": "Cairo", "font-weight": "900", "font-size": "15px"},
        "nav-link-selected": {"background-color": "#000000", "color": "#ffffff", "font-weight": "900"}
    })

if menu == "أدوات الحساب":
    st.markdown("<h3 style='color:#000000; text-align:center; font-weight:900; margin-bottom:25px;'>🛠️ حزمة أدوات البروكر الحسابية</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h3>💳 حساب القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر الإجمالي", value=5000000, step=100000)
        dp = st.number_input("نسبة مقدم الحجز %", value=10)
        yr = st.number_input("سنوات التقسيط", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>العائد الاستثماري السنوي:</p><p class='val-black'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='detail-card'><h3>📊 حساب نسبة السعي / العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة البيعية", value=5000000)
        pct = st.number_input("نسبة عمولة البروكر %", value=2.5)
        st.markdown(f"<p class='label-gold'>صافي العمولة المستحقة:</p><p class='val-black'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='detail-card'><h3>📈 حساب معدل العائد ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر شراء العقار كاش", value=5000000)
        rent = st.number_input("الإيجار الشهري المتوقع للوحدة", value=40000)
        roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
        st.markdown(f"<p class='label-gold'>العائد الاستثماري السنوي:</p><p class='val-black'>{roi:.2f} %</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ دليل المشاريع الشامل", "🚀 إطلاقات اللونشات الحالية"])
    with t1: render_grid(df_p, "p")
    with t2: render_grid(df_l, "l")

elif menu == "المطورين":
    render_grid(df_d, "d")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 مستشار معلوماتي العقاري AI</h3><p style='color:#000000; font-weight:900;'>قاعدة بيانات تحليل الأسعار وتوقعات عام 2026 قيد الصيانة السريعة لتوفير أدق التفاصيل لعملائك.</p></div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#000000; margin-top:50px; font-size:14px; font-weight:900;'>MA3LOMATI PRO © 2026 | نظام العرض والتحليل العقاري المتقدم</p>", unsafe_allow_html=True)
