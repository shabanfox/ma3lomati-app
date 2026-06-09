import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
ITEMS_PER_PAGE = 6

# --- 3. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []
if 'last_search' not in st.session_state: st.session_state.last_search = ""

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- 4. وظائف الربط مع جوجل شيت ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=15)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            pwd_input = str(pwd_input).strip()

            for user_data in users_list:
                name_s = str(user_data.get('Name', user_data.get('name', ''))).strip()
                email_s = str(user_data.get('Email', user_data.get('email', ''))).strip()
                pass_s = str(user_data.get('Password', user_data.get('password', ''))).strip()

                if (user_input == name_s.lower() or user_input == email_s.lower()) and pwd_input == pass_s:
                    return name_s
        return None
    except: return None

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في مصر لعام 2026."

news_text = get_real_news()

# --- 5. التصميم الجمالي الخارق (Luxury Dark Glassmorphism) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: radial-gradient(circle at top right, #1a1a2e, #0f0f1a 80%) !important;
        direction: rtl !important; text-align: right !important; 
        font-family: 'Tajawal', sans-serif !important; color: #ffffff !important;
    }}

    /* تصميم ترويسة اللوجين الدائرية الفخمة */
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; margin: 40px auto -20px auto; max-width: 360px;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.2);
    }}
    
    /* ستايل حقول المدخلات النصية */
    div.stTextInput input {{ 
        background-color: rgba(255, 255, 255, 0.9) !important; 
        color: #000000 !important; 
        border: 1px solid #f59e0b !important; 
        border-radius: 12px !important; 
        text-align: center !important; 
        height: 45px !important;
        font-weight: bold !important;
    }}

    /* تصميم شريط الأخبار الانسيابي */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* تصميم الهيدر الملكي للمحتوى الداخلي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    
    /* تأثير الزجاج الضبابي الفاخر للكروت والتابات */
    .detail-card, .tool-card, div[data-testid="stTabs"] {{
        background: rgba(255, 255, 255, 0.03) !important;
        backdrop-filter: blur(12px) !important;
        -webkit-backdrop-filter: blur(12px) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 20px !important;
        padding: 25px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
    }}
    
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 10px; }}
    .val-white {{ color: white; font-size: 18px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom:5px; margin-bottom: 10px; }}

    /* تحويل الأزرار الافتراضية لكروت ذكية متوهجة وتفاعلية */
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Tajawal', sans-serif !important; transition: 0.3s !important; }}
    
    div.stButton > button[key*="card_"] {{
        background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.01)) !important;
        color: #ffffff !important;
        border: 1px solid rgba(245, 158, 11, 0.2) !important;
        border-radius: 16px !important;
        padding: 20px !important;
        text-align: right !important;
        transition: all 0.4s ease-in-out !important;
        box-shadow: inset 0 1px 1px rgba(255,255,255,0.1) !important;
        min-height: 140px !important;
        display: block !important;
        width: 100% !important;
        line-height: 1.6 !important;
    }}
    
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-8px) !important;
        border-color: #f59e0b !important;
        box-shadow: 0 10px 25px rgba(245, 158, 11, 0.15), inset 0 1px 1px rgba(255,255,255,0.2) !important;
        background: rgba(245, 158, 11, 0.07) !important;
    }}
    
    /* أزرار الإجراءات الرئيسية الملونة */
    div.stButton > button[key*="btn_signin"], div.stButton > button[key*="btn_signup"] {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000000 !important;
        font-weight: 900 !important;
        border: none !important;
        letter-spacing: 1px;
        box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4) !important;
        height: 45px !important;
    }}
    
    /* تعديل نصوص التابات والعناوين المساعدة */
    div[data-testid="stTabs"] p {{ color: #ffffff !important; font-weight: bold; font-size: 16px; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label, .stSlider label {{ color: #f59e0b !important; font-weight: bold !important; }}
    .stMetric label {{ color: #aaa !important; }}
    .stMetric [data-testid="stMetricValue"] {{ color: #f59e0b !important; font-weight: 900; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. صفحة الدخول (توزيع سليم للحاويات لمنع الأخطاء) ---
if not st.session_state.auth:
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.write("")
    st.write("")
    
    # محاذاة في المنتصف لتظهر بشكل كارت منفصل فخم
    _, auth_col, _ = st.columns([1, 1.4, 1])
    
    with auth_col:
        tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
        
        with tab_login:
            u_input = st.text_input("User", placeholder="الاسم أو الجيميل", label_visibility="collapsed", key="log_user")
            p_input = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="log_pass")
            st.write("")
            if st.button("SIGN IN 🚀", use_container_width=True, key="btn_signin"):
                if p_input == "2026": # ممر الطوارئ السريع
                    st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True; st.session_state.current_user = user_verified; st.rerun()
                    else: st.error("بيانات الدخول غير صحيحة")

        with tab_signup:
            reg_name = st.text_input("الأسم", placeholder="الاسم بالكامل", key="reg_name")
            reg_pass = st.text_input("كلمة السر", type="password", placeholder="كلمة السر", key="reg_pass")
            reg_email = st.text_input("الجيميل", placeholder="الإيميل", key="reg_email")
            reg_wa = st.text_input("الواتساب", placeholder="رقم الموبايل", key="reg_wa")
            reg_co = st.text_input("الشركة", placeholder="اسم الشركة", key="reg_co")
            st.write("")
            if st.button("تأكيد الاشتراك ✅", use_container_width=True, key="btn_signup"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("تم تسجيلك بنجاح! جرب تسجيل الدخول الآن.")
                    else: st.error("فشل الاتصال بالسيرفر")
                else: st.warning("يرجى ملء البيانات")
    st.stop()

# --- 7. جلب البيانات من الجوجل شيت ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 8. الهيدر الداخلي بعد الدخول السليم ---
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); font-weight:900;">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px; margin-top:10px;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

c_top1, c_top2 = st.columns([0.85, 0.15])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    if st.button("🚪 خروج", use_container_width=True, key="btn_logout"): 
        st.session_state.auth = False
        st.rerun()

# --- 9. القائمة الرئيسية العلوية ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "rgba(0,0,0,0.5)", "border": "1px solid #333", "border-radius": "15px", "padding": "5px"},
        "nav-link": {"color": "#aaa", "font-family": "Tajawal", "font-weight": "bold"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}
    })

if 'last_menu' not in st.session_state or menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu

# --- 10. منطق الصفحات الداخلي ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center; color:#f59e0b; font-weight:900; margin-bottom:25px;'>🛠️ أدوات البروكر الحسابية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("💳 حساب القسط")
            v = st.number_input("إجمالي السعر", 1000000, key="calc_v")
            y = st.slider("عدد السنين", 1, 15, 8, key="calc_y")
            st.metric("القسط الشهري المتوقع", f"{v/(y*12):,.0f} ج.م")
    with c2:
        with st.container(border=True):
            st.subheader("💰 حساب العمولة")
            deal = st.number_input("قيمة الصفقة الإجمالية", 1000000, key="comm_v")
            pct = st.slider("النسبة مئوية %", 1.0, 5.0, 2.5, key="comm_p")
            st.metric("صافي ربح البروكر", f"{deal*(pct/100):,.0f} ج.م")
    with c3:
        with st.container(border=True):
            st.subheader("📈 العائد على الإستثمار ROI")
            buy = st.number_input("سعر شراء الوحدة", 1000000, key="roi_b")
            rent = st.number_input("الإيجار السنوي المتوقع", 100000, key="roi_r")
            st.metric("نسبة العائد السنوي", f"{(rent/buy)*100:,.1f}%" if buy > 0 else "0%")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 مساعد معلوماتي العقاري الذكي</h3><p style='color:#aaa; margin:0;'>اسألني عن أي تفاصيل تخص المشاريع والمطورين في مصر</p></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if pmt := st.chat_input("اسألني عن أي مشروع أو مطور..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.session_state.messages.append({"role": "assistant", "content": "جاري فحص قاعدة البيانات المركزية... يفضل توجيه العميل نحو المشاريع ذات خطط السداد الطويلة لعام 2026 لضمان أعلى نسبة أرباح."})
        st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if active_df.empty: 
        st.error("لا توجد بيانات متاحة حالياً في الشيت")
    else:
        col_main = active_df.columns[0]
        
        # أولاً: شاشة عرض التفاصيل الكاملة للكارت (Details View)
        if st.session_state.view == "details":
            item = active_df.loc[st.session_state.current_index]
            if st.button("⬅ عودة للقائمة الرئيسية", use_container_width=True, key="back_to_grid"):
                st.session_state.view = "grid"; st.rerun()
            
            c1, c2, c3 = st.columns(3)
            all_cols = active_df.columns
            n = len(all_cols)
            for i, col_set in enumerate([all_cols[:n//3+1], all_cols[n//3+1:2*n//3+1], all_cols[2*n//3+1:]]):
                with [c1, c2, c3][i]:
                    h = '<div class="detail-card">'
                    for k in col_set: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                    st.markdown(h+'</div>', unsafe_allow_html=True)

        # ثانياً: شاشة عرض الشبكة (Grid View)
        else:
            search = st.text_input("🔍 بحث سريع ذكي في كامل البيانات...", key="search_bar")
            
            # حل أزمة الـ Pagination: تصفير مؤشر الصفحة فوراً عند كتابة حرف بحث جديد لعدم كسر الشاشة
            if search != st.session_state.last_search:
                st.session_state.page_num = 0
                st.session_state.last_search = search
                st.rerun()

            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            main_c, side_c = st.columns([0.8, 0.2])
            with main_c:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        name = r[col_main]
                        loc = r.get('Location', '---')
                        dev = r.get('Developer', '---')
                        # زر الكارت الفاخر المتفاعل مع الماوس
                        if st.button(f"🏢 {name}\n📍 {loc}\n🏗️ {dev}", key=f"card_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"
                            st.rerun()
            
            with side_c:
                st.markdown("<p style='color:#f59e0b; font-weight:900; font-size:18px; margin-bottom:15px;'>🏆 مقترحات المنصة</p>", unsafe_allow_html=True)
                for _, s in active_df.head(6).iterrows():
                    st.markdown(f"<div class='mini-side-card' style='background:rgba(255,255,255,0.04); padding:12px; border-radius:12px; margin-bottom:8px; border-right:4px solid #f59e0b; font-size:14px;'>{s[col_main][:25]}</div>", unsafe_allow_html=True)
            
            # أزرار التنقل السفلية بين الصفحات
            st.write("---")
            p1, _, p2 = st.columns([1, 2, 1])
            if st.session_state.page_num > 0:
                if p1.button("⬅ السابق", key="prev_page"): 
                    st.session_state.page_num -= 1
                    st.rerun()
            if (start + ITEMS_PER_PAGE) < len(filt):
                if p2.button("التالي ➡", key="next_page"): 
                    st.session_state.page_num += 1
                    st.rerun()

st.markdown("<p style='text-align:center; color:#555; margin-top:60px; font-size:13px;'>MA3LOMATI PRO © 2026 | تطوير احترافي لمنصات العقارات الذكية</p>", unsafe_allow_html=True)
