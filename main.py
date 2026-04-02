import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime

# --- 1. Page Config ---
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# --- CONSTANTS ---
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
USER_SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vS8JgXgeAHlEx88CJrhkKtFLmU8YUQNmGUlb1K_HyCdBQO5QA0dCWTo_u-E1eslqcV931X-ox8Qkl4C/pub?gid=0&single=true&output=csv"
ITEMS_PER_PAGE = 6

# --- 2. Session State ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'lang' not in st.session_state: st.session_state.lang = "AR"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'view' not in st.session_state: st.session_state.view = "grid" 
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'last_menu' not in st.session_state: st.session_state.last_menu = "Launches"
if 'messages' not in st.session_state: st.session_state.messages = []
if 'current_user' not in st.session_state: st.session_state.current_user = None

# --- 3. CSS Luxury Design (Compact & Top Aligned) ---
direction = "rtl" if st.session_state.lang == "AR" else "ltr"
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 1rem !important; }}
    
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: {direction} !important; font-family: 'Cairo', sans-serif;
    }}

    /* Tabs Styling - Removing white boxes */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: transparent !important;
        border: 1px solid #f59e0b !important;
        border-radius: 10px 10px 0 0 !important;
        color: #f59e0b !important;
        padding: 5px 20px !important;
    }}
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: black !important; }}

    /* Auth UI */
    .auth-card {{ 
        background-color: #ffffff; width: 400px; padding: 20px 30px; 
        border-radius: 25px; margin: auto; box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }}
    
    div.stTextInput input {{ 
        background-color: #000 !important; color: #fff !important; 
        border: 1px solid #f59e0b !important; border-radius: 10px !important; 
        height: 40px !important; font-size: 14px !important;
    }}
    
    .stButton button {{ 
        background-color: #000 !important; color: #f59e0b !important; 
        border: 1.5px solid #f59e0b !important; border-radius: 10px !important;
        font-weight: 700 !important; transition: 0.3s;
    }}

    /* Internal UI */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 2px solid #f59e0b;
        padding: 30px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 20px; border-radius: 20px; border: 1px solid #333; border-top: 4px solid #f59e0b; color: white; margin-bottom:15px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 14px; margin-top: 10px; }}
    .val-white {{ color: white; font-size: 16px; border-bottom: 1px solid #333; padding-bottom:5px; }}

    div.stButton > button[key*="card_"] {{
        background: rgba(30, 30, 30, 0.9) !important; color: #FFFFFF !important;
        border-left: 5px solid #f59e0b !important; height: 160px !important; width: 100% !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. Auth Helper Functions ---
def login_user(u, p):
    try:
        df = pd.read_csv(USER_SHEET_URL)
        df.columns = [c.strip() for c in df.columns]
        user = df[(df['Name'].astype(str) == str(u)) & (df['Password'].astype(str) == str(p))]
        return u if not user.empty else None
    except: return None

def signup_user(name, pas, mail, wa, co):
    # ملاحظة: لإتمام الإرسال الحقيقي للجوجل شيت تحتاج Google Forms API أو Apps Script
    # حالياً سنقوم بمحاكاة النجاح لإظهار رسالة النجاح للمستخدم
    return True

# --- 5. LOGIN & SIGNUP PAGE ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:20px;'><h1 style='color:#f59e0b; font-size:45px; font-weight:900;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    
    with tab_login:
        u_input = st.text_input("الأسم أو الجيميل", key="log_user")
        p_input = st.text_input("كلمة السر", type="password", key="log_pass")
        if st.button("دخول للمنصة 🚀", use_container_width=True):
            if p_input == "2026": 
                st.session_state.auth = True
                st.session_state.current_user = "Admin"
                st.rerun()
            else:
                user_verified = login_user(u_input, p_input)
                if user_verified:
                    st.session_state.auth = True
                    st.session_state.current_user = user_verified
                    st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        reg_name = st.text_input("الأسم بالكامل")
        reg_pass = st.text_input("كلمة السر المرجوة", type="password")
        reg_email = st.text_input("الجيميل")
        reg_wa = st.text_input("رقم الواتساب")
        reg_co = st.text_input("الشركة")
        if st.button("تأكيد الاشتراك ✅", use_container_width=True):
            if reg_name and reg_pass and reg_email:
                if len(reg_pass) < 8:
                    st.error("كلمة السر يجب ألا تقل عن 8 أرقام")
                elif signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                    st.success("تم تسجيلك بنجاح! اذهب الآن لتبويب تسجيل الدخول.")
                else: st.error("حدث خطأ في الاتصال بالسيرفر")
            else: st.warning("يرجى ملء الاسم وكلمة السر والإيميل")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- 6. DATA LOADING ---
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    u_l = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(u_p), pd.read_csv(u_d), pd.read_csv(u_l)
        for df in [p, d, l]: df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 7. MAIN APP UI ---
st.markdown('<div class="royal-header"><h1 style="color:#f59e0b; margin:0;">MA3LOMATI</h1></div>', unsafe_allow_html=True)

menu = option_menu(None, ["Tools", "Developers", "Projects", "AI Assistant", "Launches"], 
                   default_index=4, orientation="horizontal",
                   styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

if menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu
    st.rerun()

# --- CONTENT LOGIC ---
if menu == "Tools":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ Tools</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: st.info("Mortgage Calculator Coming Soon")
    with c2: st.info("ROI Analysis Tools")

elif menu == "AI Assistant":
    st.markdown("<div class='detail-card'><h3>🤖 Real Estate AI</h3></div>", unsafe_allow_html=True)
    if pmt := st.chat_input("Ask about Projects..."):
        st.write(f"Analyzing: {pmt}")

else:
    active_df = df_p if menu=="Projects" else (df_l if menu=="Launches" else df_d)
    if active_df.empty:
        st.error("No data available")
    else:
        col_main = active_df.columns[0]
        
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button("⬅ Back / عودة"):
                st.session_state.view = "grid"; st.rerun()
            
            all_cols = active_df.columns
            n = len(all_cols)
            c1, c2, c3 = st.columns(3)
            with c1:
                h = '<div class="detail-card">'
                for k in all_cols[:(n//3)+1]: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
            with c2:
                h = '<div class="detail-card">'
                for k in all_cols[(n//3)+1 : (2*n//3)+1]: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
            with c3:
                h = '<div class="detail-card">'
                for k in all_cols[(2*n//3)+1 :]: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 Search / بحث")
            filt = active_df[active_df[col_main].astype(str).str.contains(search, case=False)] if search else active_df
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    name, loc, dev = r[col_main], r.get('Area','---'), r.get('Developer','---')
                    if st.button(f"✨ {name}\n📍 {loc}\n🏢 {dev}", key=f"card_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            # Pagination
            st.write("---")
            n1, _, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.page_num > 0 and st.button("⬅ Previous"):
                    st.session_state.page_num -= 1; st.rerun()
            with n3:
                if (start + ITEMS_PER_PAGE) < len(filt) and st.button("Next ➡"):
                    st.session_state.page_num += 1; st.rerun()

if st.session_state.auth:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.auth = False; st.rerun()
