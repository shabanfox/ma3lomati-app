import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- إدارة الحالة (Session State) ---
# التأكد من تعريف المتغيرات الأساسية مرة واحدة فقط
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None
if 'view' not in st.session_state:
    st.session_state.view = "grid"
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'page_num' not in st.session_state:
    st.session_state.page_num = 0
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'last_m' not in st.session_state:
    st.session_state.last_m = "المشاريع" # القيمة الافتراضية

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف النظام (تم تحسين الاستجابة) ---
def signup_user(name, pwd, email, wa, comp):
    payload = {"name": name, "password": pwd, "email": email, "whatsapp": wa, "company": comp}
    try:
        response = requests.post(SCRIPT_URL, json=payload, timeout=10)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # إضافة عامل زمن لمنع الكاش وضمان جلب أحدث البيانات
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

def logout():
    # تفريغ الجلسة بالكامل عند الخروج
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# --- 4. التصميم الجمالي CSS ---
# (يبقى كما هو في كودك الأصلي لأنه ممتاز)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; justify-content: flex-start; width: 100%; padding-top: 50px; }}
    .oval-header {{
        background-color: #000; border: 3px solid #f59e0b; border-radius: 60px;
        padding: 15px 50px; color: #f59e0b; font-size: 24px; font-weight: 900;
        text-align: center; z-index: 10; margin-bottom: -30px; min-width: 360px;
    }}
    .auth-card {{ background-color: #ffffff; width: 380px; padding: 55px 35px 30px 35px; border-radius: 30px; text-align: center; box-shadow: 0 20px 50px rgba(0,0,0,0.3); }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"] {{
        background: linear-gradient(145deg, #ffffff, #f9f9f9) !important;
        color: #1a1a1a !important; border-right: 6px solid #f59e0b !important;
        border-radius: 15px !important; padding: 20px !important;
        text-align: right !important; line-height: 1.7 !important;
        min-height: 180px !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
        transition: all 0.3s ease !important; white-space: pre-line !important;
        margin-bottom: 10px !important; font-family: 'Cairo', sans-serif !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        transform: translateY(-5px) !important;
        box-shadow: 0 8px 20px rgba(245, 158, 11, 0.4) !important;
        background: #fff !important;
    }}
    div.stButton > button[key*="nav_"] {{
        background-color: #f59e0b !important; color: #000 !important;
        font-weight: 900 !important; border-radius: 12px !important;
        border: none !important; margin-top: 5px !important;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; margin-top: 5px; }}
    .val-white {{ color: white; font-size: 16px; border-bottom: 1px solid #333; padding-bottom:5px; margin-bottom: 8px; }}
    div.stButton > button[key*="side_"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #eee !important; border: none !important;
        border-right: 3px solid #f59e0b !important;
        text-align: right !important; font-size: 13px !important;
        margin-bottom: 5px !important; border-radius: 8px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول والحفاظ على الجلسة ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'>", unsafe_allow_html=True)
    st.markdown("<div class='oval-header'>MA3LOMATI PRO</div>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    col_lang, _ = st.columns([0.45, 0.55])
    with col_lang: st.button("🌐 EN / AR", key="login_lang", use_container_width=True)
    
    tab_login, tab_signup = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_login:
        u = st.text_input("User", placeholder="الأسم أو الإيميل", label_visibility="collapsed", key="u_input")
        p = st.text_input("Pass", type="password", placeholder="كلمة السر", label_visibility="collapsed", key="p_input")
        if st.button("SIGN IN 🚀", use_container_width=True, key="signin_btn"):
            if p == "2026": 
                st.session_state.auth = True
                st.session_state.current_user = "Admin"
                st.rerun()
            else:
                user = login_user(u, p)
                if user:
                    st.session_state.auth = True
                    st.session_state.current_user = user
                    st.rerun()
                else:
                    st.error("خطأ في بيانات الدخول")
                    
    with tab_signup:
        n = st.text_input("الاسم", key="sig_n")
        pw = st.text_input("السر", type="password", key="sig_p")
        em = st.text_input("الايميل", key="sig_e")
        if st.button("إتمام التسجيل", use_container_width=True, key="signup_btn"):
            if signup_user(n, pw, em, "", ""): 
                st.success("تم التسجيل! يمكنك الدخول الآن.")
            else: 
                st.error("فشل الاتصال بالقاعدة")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# --- 6. جلب البيانات (مع استخدام الكاش) ---
@st.cache_data(ttl=300) # زيادة الوقت لـ 5 دقائق لتقليل استهلاك الكاش وتحسين الأداء
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

# --- 7. واجهة المنصة ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; margin:0; font-size:40px;">MA3LOMATI PRO</h1><p style="color:#f59e0b; font-weight:bold;">مرحباً {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

_, c_ex = st.columns([0.88, 0.12])
with c_ex:
    if st.button("🚪 خروج", key="logout_nav", use_container_width=True): logout()

# القائمة العلوية
selected_menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], 
    default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}},
    key="main_menu_navigator")

# تحديث الحالة عند تغيير القائمة
if selected_menu != st.session_state.last_m:
    st.session_state.view = "grid"
    st.session_state.page_num = 0
    st.session_state.last_m = selected_menu

# --- 8. تشغيل الأقسام بناءً على الحالة المحفوظة ---
menu = st.session_state.last_m

if menu == "أدوات البروكر":
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("💳 القسط")
            v = st.number_input("السعر", value=1000000, key="calc_v")
            dp = st.number_input("مقدم %", 0, 100, 10, key="calc_dp")
            y = st.number_input("سنين", 1, 20, 8, key="calc_y")
            st.metric("الشهري", f"{(v-(v*dp/100))/(y*12):,.0f}")
    # ... (باقي كود الحسابات يبقى كما هو)

elif menu == "المساعد الذكي":
    # سيظل محتوى الرسائل محفوظاً لأنه مرتبط بـ st.session_state.messages
    st.info("اسألني عن أي مشروع أو قارن بين المطورين...")
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
    
    if prompt := st.chat_input("اكتب سؤالك هنا..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # هنا يمكنك استدعاء API للذكاء الاصطناعي مستقبلاً
        st.session_state.messages.append({"role": "assistant", "content": f"بناءً على بيانات 2026 لـ '{prompt}'، الخيار الأفضل هو..."})
        st.rerun()

else:
    # منطق عرض الجداول (المشاريع، المطورين، Launches)
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if active_df.empty:
        st.warning("جاري جلب البيانات أو القاعدة فارغة...")
    else:
        col_main = active_df.columns[0]
        
        if st.session_state.view == "details":
            if st.button("⬅ عودة للقائمة", use_container_width=True, key="back_btn"): 
                st.session_state.view = "grid"
                st.rerun()
            
            item = active_df.iloc[st.session_state.current_index]
            # عرض التفاصيل (كما في كودك الأصلي)
            c1, c2, c3 = st.columns(3)
            cols = active_df.columns
            for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
                with [c1, c2, c3][i]:
                    h = '<div class="detail-card">'
                    for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                    st.markdown(h+'</div>', unsafe_allow_html=True)

        else:
            # واجهة الشبكة (Grid) مع البحث
            search = st.text_input("🔍 بحث ذكي...", key="search_input")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            main_c, side_c = st.columns([0.76, 0.24])
            with main_c:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        name = r[col_main]
                        loc = r.get('Location', 'غير محدد')
                        dev = r.get('Developer', '---')
                        price = r.get('Starting Price', r.get('Price', 'تواصل للتفاصيل'))
                        card_text = f"🏠 {name}\n🏗️ المطور: {dev}\n📍 الموقع: {loc}\n💰 السعر: {price}"
                        if st.button(card_text, key=f"card_{idx}_{menu}"):
                            st.session_state.current_index = idx
                            st.session_state.view = "details"
                            st.rerun()

                # أزرار التنقل الصفحي
                st.markdown("---")
                p1, p_info, p2 = st.columns([1, 2, 1])
                with p1:
                    if st.session_state.page_num > 0:
                        if st.button("⬅ السابق", key="prev_pg"):
                            st.session_state.page_num -= 1
                            st.rerun()
                with p_info:
                    st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
                with p2:
                    if (start + ITEMS_PER_PAGE) < len(filt):
                        if st.button("التالي ➡", key="next_pg"):
                            st.session_state.page_num += 1
                            st.rerun()

            with side_c:
                st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:1px solid #333;'>🏆 مقترحات سريعة</p>", unsafe_allow_html=True)
                for s_idx, s_row in active_df.head(10).iterrows():
                    if st.button(f"📌 {str(s_row[col_main])[:28]}", key=f"side_{s_idx}_{menu}", use_container_width=True):
                        st.session_state.current_index = s_idx
                        st.session_state.view = "details"
                        st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px; font-size:12px;'>MA3LOMATI PRO © 2026 | Powered by AI</p>", unsafe_allow_html=True)
