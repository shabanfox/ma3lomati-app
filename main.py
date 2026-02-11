import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة (Session State) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
    st.session_state.current_user = None

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. الروابط الأساسية ---
# رابط الـ Web App الخاص بك لجلب بيانات المستخدمين
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. دالة التحقق من المستخدم (الربط الحقيقي) ---
def check_login(user_input, pwd_input):
    try:
        # جلب البيانات من شيت جوجل
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=10)
        if response.status_code == 200:
            users_list = response.json()
            user_input = str(user_input).strip().lower()
            for user_data in users_list:
                # التأكد من أسماء الأعمدة في الشيت (Name / Password)
                u_name = str(user_data.get('Name', user_data.get('name', ''))).strip().lower()
                u_pass = str(user_data.get('Password', user_data.get('password', ''))).strip()
                if user_input == u_name and str(pwd_input) == u_pass:
                    return user_data.get('Name', user_data.get('name', 'User'))
        return None
    except Exception as e:
        st.error(f"خطأ في الاتصال بقاعدة البيانات: {e}")
        return None

# --- 5. التصميم CSS (عربي + Pro) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .auth-wrapper {{ display: flex; flex-direction: column; align-items: center; padding-top: 80px; }}
    .oval-header {{ background: #000; border: 3px solid #f59e0b; border-radius: 60px; padding: 15px 50px; color: #f59e0b; font-size: 26px; font-weight: 900; margin-bottom: -30px; z-index: 10; }}
    .auth-card {{ background: white; width: 380px; padding: 60px 40px 40px 40px; border-radius: 30px; box-shadow: 0 20px 50px rgba(0,0,0,0.4); text-align: center; }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}'); background-size: cover; border-bottom: 3px solid #f59e0b; padding: 50px; text-align: center; border-radius: 0 0 40px 40px; }}
    .detail-card {{ background: rgba(25, 25, 25, 0.8); padding: 20px; border-radius: 15px; border: 1px solid #333; border-top: 4px solid #f59e0b; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; }}
    .val-white {{ color: white; font-size: 18px; border-bottom: 1px solid #444; margin-bottom: 10px; padding-bottom: 5px; }}
    div.stButton > button[key*="card_"] {{ 
        background: #fff !important; color: #1a1a1a !important; border-right: 6px solid #f59e0b !important; 
        border-radius: 15px !important; padding: 20px !important; text-align: right !important; min-height: 140px !important; width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. واجهة تسجيل الدخول ---
if not st.session_state.auth:
    st.markdown("<div class='auth-wrapper'><div class='oval-header'>MA3LOMATI PRO</div><div class='auth-card'>", unsafe_allow_html=True)
    user_in = st.text_input("اسم المستخدم", placeholder="ادخل اسمك المسجل", key="login_u")
    pass_in = st.text_input("كلمة المرور", type="password", placeholder="****", key="login_p")
    if st.button("تسجيل الدخول 🚀", use_container_width=True):
        if pass_in == "2026": # دخول سريع للأدمن
            st.session_state.auth, st.session_state.current_user = True, "المدير العام"
            st.rerun()
        else:
            found_user = check_login(user_in, pass_in)
            if found_user:
                st.session_state.auth, st.session_state.current_user = True, found_user
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة")
    st.markdown("</div></div>", unsafe_allow_html=True); st.stop()

# --- 7. تحميل البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
    for df in [p, d, l]:
        df.columns = [c.strip() for c in df.columns]
        df.rename(columns={'Area': 'الموقع', 'Location': 'الموقع'}, inplace=True, errors="ignore")
    return p.fillna("---"), d.fillna("---"), l.fillna("---")

df_p, df_d, df_l = load_data()

# --- 8. الواجهة الرئيسية ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b; font-size:20px;">مرحباً بك يا {st.session_state.current_user} 👋</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

# --- 9. الوظائف المساعدة للعرض ---
def render_grid(dataframe, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        cols = st.columns(3)
        for i, chunk in enumerate([dataframe.columns[j:j+6] for j in range(0, len(dataframe.columns), 6)]):
            with cols[i % 3]:
                h = '<div class="detail-card">'
                for k in chunk: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        search = st.text_input("🔍 ابحث هنا...", key=f"search_{prefix}", placeholder="اسم المشروع، المطور، أو الموقع...")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.75, 0.25])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    card_text = f"🏠 {r[0]}\n🏗️ المطور: {r.get('Developer', r.get('المطور', '---'))}\n📍 الموقع: {r.get('الموقع', '---')}"
                    if st.button(card_text, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # التنقل بين الصفحات
            p1, p_info, p2 = st.columns([1, 2, 1])
            with p1: 
                if st.session_state.page_num > 0:
                    if st.button("السابق", key=f"prev_{prefix}"): st.session_state.page_num -= 1; st.rerun()
            with p_info: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي", key=f"next_{prefix}"): st.session_state.page_num += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:1px solid #333;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(10).iterrows():
                if st.button(f"📌 {str(s_row[0])[:25]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 10. تنفيذ الأقسام ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حاسبة الاستثمار العقاري</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='detail-card'><h3>💰 حساب القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("سعر الوحدة", value=5000000, step=100000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنوات", value=8)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<p class='label-gold'>القسط الشهري:</p><p class='val-white'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
    # ... (باقي الحسابات بنفس النمط العربي)

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ كل المشاريع", "🚀 اللونشات الحالية"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")

elif menu == "المطورين":
    render_grid(df_d, "dev")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 المساعد العقاري الذكي</h3><p>اسألني عن أي مشروع أو مطور عقاري في مصر</p></div>", unsafe_allow_html=True)
    # هنا واجهة التشات بسيطة
    if prompt := st.chat_input("بماذا يمكنني مساعدتك؟"):
        with st.chat_message("user"): st.write(prompt)
        with st.chat_message("assistant"): st.write("جاري تحليل بيانات المشاريع للرد عليك...")

if st.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
