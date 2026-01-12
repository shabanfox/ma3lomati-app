import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة وإزالة أي فراغ علوي
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - المحاذاة لليمين والتصميم الشبكي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إزالة الفراغ الأبيض العلوي */
    .block-container { padding-top: 0rem !important; }
    header { visibility: hidden; height: 0px !important; }
    [data-testid="stHeader"] { display: none; }
    
    [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        direction: RTL; 
        text-align: right; 
        font-family: 'Cairo', sans-serif; 
    }

    /* الهيدر البيضاوي الذهبي */
    .oval-header {
        background-color: #000;
        border: 3px solid #f59e0b;
        border-radius: 60px;
        padding: 15px 40px;
        width: fit-content;
        margin: 0 auto 30px auto;
        text-align: center;
        box-shadow: 0px 5px 20px rgba(245, 158, 11, 0.3);
    }
    .header-title { color: #f59e0b; font-weight: 900; font-size: 30px !important; margin: 0; }

    /* ستايل صفحة الدخول */
    .login-box {
        max-width: 450px;
        margin: 20px auto;
        padding: 40px;
        background: #0a0a0a;
        border-radius: 20px;
        border: 1px solid #222;
        text-align: center;
    }
    div[data-baseweb="input"] { background-color: white !important; border-radius: 10px !important; }
    input { color: black !important; font-weight: 900 !important; text-align: center !important; }

    /* تصميم الكارت الشبكي */
    .pro-card { 
        background: #111; 
        border: 1px solid #222; 
        border-top: 5px solid #f59e0b; 
        border-radius: 15px; 
        padding: 15px; 
        text-align: right; 
        height: 220px;
        margin-bottom: 20px;
    }
    .card-title { color: #f59e0b; font-weight: 900; font-size: 18px; margin-bottom: 5px; }
    
    /* العناوين في الجانب الأيمن */
    .right-title { 
        color: #f59e0b; 
        text-align: right; 
        font-weight: 900; 
        margin-bottom: 20px; 
        border-right: 8px solid #f59e0b; 
        padding-right: 15px;
        font-size: 24px;
    }

    /* الأزرار */
    .stButton button { 
        background-color: #1a1a1a !important; 
        color: #f59e0b !important; 
        border: 1px solid #333 !important;
        border-radius: 8px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. نظام حماية الدخول (باسورد 2026)
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 60px;'>🔒</h1>", unsafe_allow_html=True)
    pwd = st.text_input("", type="password", placeholder="كلمة المرور")
    if st.button("دخول"):
        if pwd == "2026":
            st.session_state.auth = True
            st.rerun()
        else: st.error("❌ خطأ")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# 4. جلب البيانات
@st.cache_data(ttl=60)
def get_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    ]
    dfs = [pd.read_csv(u) for u in urls]
    combined = pd.concat(dfs, ignore_index=True)
    combined.columns = [str(c).strip() for c in combined.columns]
    return combined.fillna("غير متوفر").astype(str)

df = get_data()

# الهيدر وزر الخروج
st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
if st.sidebar.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()

menu = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                  icons=["tools", "building", "person-vcard"], orientation="horizontal")

# --- 🏗️ قسم المشاريع (نظام شبكي 9) ---
if menu == "🏗️ المشاريع":
    st.markdown("<h2 class='right-title'>🏗️ دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
    search = st.text_input("🔍 ابحث عن أي شيء...")
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]

    # إدارة الصفحات
    if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
    size = 9
    total_p = math.ceil(len(dff) / size)
    curr_df = dff.iloc[st.session_state.p_idx*size : (st.session_state.p_idx+1)*size]

    # عرض الشبكة (3 أعمدة)
    for i in range(0, len(curr_df), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(curr_df):
                row = curr_df.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class='pro-card'>
                            <div class='card-title'>{row['Project Name']}</div>
                            <p style='font-size:14px;'>🏢 {row['Developer']}</p>
                            <p style='font-size:13px; color:#f59e0b;'>📍 {row['Area']}</p>
                            <p style='font-size:12px; color:#888;'>👤 المالك: {row['Owner']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    with st.expander("تفاصيل"):
                        st.write(f"👷 {row['Consultant']}")
                        st.write(f"⭐ {row['Competitive Advantage']}")

    # أزرار التنقل (أقصى اليمين)
    st.write("---")
    col_r1, col_r2, _ = st.columns([1, 1, 6])
    if col_r1.button("➡️ السابق") and st.session_state.p_idx > 0:
        st.session_state.p_idx -= 1; st.rerun()
    if col_r2.button("التالي ⬅️") and st.session_state.p_idx < total_p - 1:
        st.session_state.p_idx += 1; st.rerun()
    st.markdown(f"<p style='text-align:right;'>صفحة {st.session_state.p_idx + 1} من {total_p}</p>", unsafe_allow_html=True)

# --- 🏢 قسم المطورين (نظام شبكي 9) ---
elif menu == "🏢 المطورين":
    st.markdown("<h2 class='right-title'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
    
    if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
    total_d = math.ceil(len(devs) / size)
    curr_devs = devs.iloc[st.session_state.d_idx*size : (st.session_state.d_idx+1)*size]

    for i in range(0, len(curr_devs), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(curr_devs):
                row = curr_devs.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class='pro-card'>
                            <div class='card-title'>{row['Developer']}</div>
                            <p>👤 المالك: {row['Owner']}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    with st.expander("الملف"):
                        st.write(row['Detailed_Info'])

    # أزرار تنقل المطورين لليمين
    st.write("---")
    col_d1, col_d2, _ = st.columns([1, 1, 6])
    if col_d1.button("➡️ السابق", key="d1") and st.session_state.d_idx > 0:
        st.session_state.d_idx -= 1; st.rerun()
    if col_d2.button("التالي ⬅️", key="d2") and st.session_state.d_idx < total_d - 1:
        st.session_state.d_idx += 1; st.rerun()

# --- 🛠️ أدوات البروكر ---
elif menu == "🛠️ أدوات البروكر":
    st.markdown("<h2 class='right-title'>🛠️ أدوات العمل</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 💰 حاسبة القسط")
        p = st.number_input("السعر", 1000000)
        y = st.number_input("السنوات", 8)
        st.markdown(f"#### القسط: {p/(y*12):,.0f} ج.م")
    with c2:
        st.markdown("### 📝 المفكرة")
        st.text_area("ملاحظات...", height=200)
