import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "الإطلاقات الجديدة"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 3. CSS Luxury Design (Arabic Optimized) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}

    /* تصميم واجهة الدخول المحدثة */
    .auth-container {{
        display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
        padding-top: 50px; width: 100%;
    }}
    .brand-glow {{
        color: #f59e0b; font-size: 45px; font-weight: 900; margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
    }}
    .brand-sub {{ color: #ffffff; font-size: 18px; margin-bottom: 30px; opacity: 0.8; }}
    
    .stTabs [data-baseweb="tab-list"] {{
        background-color: rgba(255,255,255,0.05) !important;
        border-radius: 15px; justify-content: center !important; gap: 20px;
    }}
    .stTabs [data-baseweb="tab"] {{ color: #fff !important; font-size: 18px !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom: 2px solid #f59e0b !important; }}

    div.stTextInput input {{
        background-color: rgba(0,0,0,0.5) !important; color: #fff !important;
        border: 1px solid #444 !important; border-radius: 12px !important;
        text-align: center !important; height: 50px !important;
    }}

    /* الأزرار الذهبية */
    div.stButton > button {{
        background: linear-gradient(90deg, #f59e0b, #d97706) !important;
        color: #000 !important; font-weight: 900 !important;
        border-radius: 12px !important; border: none !important; height: 50px !important;
    }}

    /* التصميم الداخلي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; padding: 40px; text-align: center;
        border-radius: 0 0 40px 40px; border-bottom: 3px solid #f59e0b; margin-bottom: 30px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.95); padding: 25px; border-radius: 20px; border: 1px solid #333; border-top: 4px solid #f59e0b; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; margin-top: 15px; font-size: 15px; }}
    .val-white {{ color: white; font-size: 17px; border-bottom: 1px solid #222; padding-bottom: 5px; }}
    
    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #fff !important;
        border-right: 6px solid #f59e0b !important; border-left: none !important;
        height: 150px !important; width: 100% !important; text-align: right !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Logic Functions ---
def check_auth(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        return not df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))].empty
    except: return False

@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. AUTHENTICATION INTERFACE ---
if not st.session_state.auth:
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    st.markdown("<p class='brand-glow'>MA3LOMATI PRO</p>", unsafe_allow_html=True)
    st.markdown("<p class='brand-sub'>منصة معلوماتي العقارية الذكية</p>", unsafe_allow_html=True)
    
    auth_col = st.columns([1, 1.5, 1])[1]
    with auth_col:
        tab_login, tab_reg = st.tabs(["🔐 تسجيل الدخول", "📝 طلب اشتراك"])
        
        with tab_login:
            st.write("")
            u_in = st.text_input("اسم المستخدم", placeholder="User", label_visibility="collapsed", key="log_u")
            p_in = st.text_input("كلمة السر", type="password", placeholder="Pass", label_visibility="collapsed", key="log_p")
            if st.button("دخول للمنصة", use_container_width=True):
                if check_auth(u_in, p_in): st.session_state.auth = True; st.rerun()
                else: st.error("عذراً، البيانات غير صحيحة")
        
        with tab_reg:
            st.write("")
            st.text_input("الأسم الكامل", placeholder="Full Name", label_visibility="collapsed")
            st.text_input("رقم الواتساب", placeholder="WhatsApp Number", label_visibility="collapsed")
            if st.button("إرسال طلب الانضمام", use_container_width=True):
                st.success("تم إرسال طلبك للإدارة، سنتواصل معك قريباً")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. MAIN APPLICATION ---
df_p, df_d, df_l = load_data()
MENU_ITEMS = ["الأدوات", "المطورين", "المشاريع", "المساعد الذكي", "الإطلاقات الجديدة"]

st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; font-weight:900;">MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)

m_col, o_col = st.columns([0.85, 0.15])
with m_col:
    menu = option_menu(None, MENU_ITEMS, default_index=4, orientation="horizontal", 
                       styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})
with o_col:
    if st.button("🚪 خروج", use_container_width=True): st.session_state.auth = False; st.rerun()

if menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu
    st.rerun()

# --- 7. CONTENT LOGIC ---
if menu == "الأدوات":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ أدوات العقاري المحترف</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("🧮 التمويل العقاري")
            val = st.number_input("سعر الوحدة", value=2000000)
            yrs = st.slider("عدد السنوات", 1, 20, 10)
            st.warning(f"القسط الشهري التقريبي: {val/(yrs*12):,.0f}")
    with c2:
        with st.container(border=True):
            st.subheader("📈 حساب العائد ROI")
            cost = st.number_input("التكلفة الإجمالية", value=1000000)
            rent = st.number_input("الإيجار السنوي", value=100000)
            st.warning(f"نسبة العائد: {(rent/cost)*100:.1f}%")
    with c3:
        with st.container(border=True):
            st.subheader("💰 حساب العمولة")
            deal = st.number_input("قيمة الصفقة", value=1000000)
            st.info(f"عمولتك (2.5%): {deal*0.025:,.0f}")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 مساعد العقارات الذكي</h3></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if pmt := st.chat_input("اسألني عن السوق العقاري..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.session_state.messages.append({"role": "assistant", "content": "جاري تحليل البيانات... السوق حالياً يشهد طلباً متزايداً في منطقة التجمع الخامس ومستقبل سيتي."})
        st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="الإطلاقات الجديدة" else df_d)
    if active_df.empty: st.error("لا توجد بيانات حالياً")
    else:
        col_main = active_df.columns[0]
        
        # --- VIEW: DETAILS ---
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button("⬅ عودة للقائمة", use_container_width=True):
                st.session_state.view = "grid"; st.rerun()
            
            all_cols = active_df.columns
            n = len(all_cols)
            c1, c2, c3 = st.columns(3)
            
            for i, col_group in enumerate([all_cols[:n//3+1], all_cols[n//3+1 : 2*n//3+1], all_cols[2*n//3+1:]]):
                with [c1, c2, c3][i]:
                    h = '<div class="detail-card">'
                    for k in col_group:
                        h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                    st.markdown(h+'</div>', unsafe_allow_html=True)

        # --- VIEW: GRID ---
        else:
            search = st.text_input("🔍 ابحث هنا بالاسم...")
            filt = active_df[active_df[col_main].astype(str).str.contains(search, case=False)] if search else active_df
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            main_c, side_c = st.columns([0.8, 0.2])
            with main_c:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        name = r[col_main]
                        loc = r.get('Area', r.get('Location', '---'))
                        dev = r.get('Developer', '---')
                        if st.button(f"🏢 {name}\n📍 {loc}\n🏗️ {dev}", key=f"card_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            with side_c:
                st.markdown("<p style='color:#f59e0b; font-weight:bold;'>⭐ ترشيحاتنا</p>", unsafe_allow_html=True)
                for _, s in active_df.head(6).iterrows():
                    st.markdown(f"<div style='background:rgba(255,255,255,0.05); padding:10px; border-radius:10px; margin-bottom:5px; border-right:3px solid #f59e0b;'>💎 {s[col_main][:25]}</div>", unsafe_allow_html=True)
            
            # Pagination
            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.page_num > 0:
                    if st.button("السابق", use_container_width=True): st.session_state.page_num -= 1; st.rerun()
            with n3:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي", use_container_width=True): st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © جميع الحقوق محفوظة 2026</p>", unsafe_allow_html=True)
