import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة وإزالة أي فراغ علوي
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - تصميم مخصص حسب طلبك
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إزالة الفراغ الأبيض العلوي تماماً */
    .block-container { padding-top: 0rem !important; padding-bottom: 0rem !important; }
    header { visibility: hidden; height: 0px !important; }
    footer { visibility: hidden; }
    [data-testid="stHeader"] { display: none; }
    
    /* الخلفية والمحاذاة */
    [data-testid="stAppViewContainer"] { 
        background-color: #050505; 
        direction: RTL; 
        text-align: right; 
        font-family: 'Cairo', sans-serif; 
    }

    /* الهيدر البيضاوي (في منتصف الصفحة وبدون فراغ علوي) */
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
    .header-title { color: #f59e0b; font-weight: 900; font-size: 32px !important; margin: 0; }

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
    
    /* جعل مكان الكتابة (Input) أسود على خلفية بيضاء */
    div[data-baseweb="input"] {
        background-color: white !important;
        border-radius: 10px !important;
        border: 2px solid #f59e0b !important;
    }
    input {
        color: black !important;
        font-weight: 900 !important;
        text-align: center !important;
        font-size: 20px !important;
    }

    /* كروت المشاريع والمطورين */
    .pro-card { 
        background: #111; 
        border: 1px solid #222; 
        border-top: 5px solid #f59e0b; 
        border-radius: 15px; 
        padding: 20px; 
        text-align: right; 
        transition: 0.3s;
    }
    .pro-card:hover { border-color: #f59e0b; transform: translateY(-5px); }
    
    /* العناوين الجانبية لليمين */
    .right-title { 
        color: #f59e0b; 
        text-align: right; 
        font-weight: 900; 
        margin-bottom: 25px; 
        border-right: 8px solid #f59e0b; 
        padding-right: 15px; 
    }
    
    /* زر الخروج والتنقل */
    .stButton button { 
        background-color: #1a1a1a !important; 
        color: #f59e0b !important; 
        border: 1px solid #333 !important; 
        border-radius: 10px; 
        font-weight: bold; 
    }
    .logout-container { text-align: left; padding: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. نظام حماية الدخول
if 'auth' not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    # عرض الهيدر البيضاوي في صفحة الدخول
    st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
    
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size: 80px; color: #f59e0b; margin-bottom:10px;'>🔒</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: white;'>تسجيل دخول الوكيل</h3>", unsafe_allow_html=True)
    
    # خانة الباسورد (خلفية بيضاء، خط أسود)
    pwd = st.text_input("", type="password", placeholder="أدخل كلمة المرور")
    
    if st.button("دخول إلى النظام"):
        if pwd == "2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("❌ كلمة المرور غير صحيحة")
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# --- الكود بعد تسجيل الدخول الناجح ---

# 4. جلب ودمج البيانات من الروابط
@st.cache_data(ttl=60)
def get_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    ]
    dfs = []
    for u in urls:
        try:
            d = pd.read_csv(u)
            d.columns = [str(c).strip() for c in d.columns]
            dfs.append(d)
        except: continue
    return pd.concat(dfs, ignore_index=True).fillna("غير متوفر").astype(str)

df = get_data()

# الهيدر وزر الخروج
st.markdown('<div class="oval-header"><h1 class="header-title">منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

col_out, _ = st.columns([1, 5])
with col_out:
    if st.button("🚪 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

# المنيو الرئيسي
menu = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                  icons=["tools", "building", "person-vcard"], orientation="horizontal",
                  styles={"container": {"background-color": "#000", "padding": "5px"}})

# --- 🏗️ قسم المشاريع ---
if menu == "🏗️ المشاريع":
    st.markdown("<h2 class='right-title'>🏗️ دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 ابحث عن (مشروع، منطقة، مطور)...")
    dff = df.copy()
    if search:
        dff = dff[dff.apply(lambda r: search.lower() in r.astype(str).str.lower().values, axis=1)]

    # Pagination
    if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
    size = 6
    total_p = math.ceil(len(dff) / size)
    curr_df = dff.iloc[st.session_state.p_idx*size : (st.session_state.p_idx+1)*size]

    for idx, row in curr_df.iterrows():
        st.markdown(f"""
            <div class='pro-card'>
                <h3 style='color:#f59e0b;'>{row['Project Name']}</h3>
                <p>🏢 {row['Developer']} | 📍 {row['Area']}</p>
                <p style='font-size:14px; color:#aaa;'>👤 المالك: {row['Owner']}</p>
            </div>
        """, unsafe_allow_html=True)
        with st.expander("📝 عرض كامل التفاصيل الفنية"):
            st.info(f"👷 الاستشاري: {row['Consultant']}")
            st.warning(f"⭐ الميزة: {row['Competitive Advantage']}")
            st.write(f"📜 نبذة: {row['Detailed_Info']}")

    # أزرار التنقل
    st.write("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    if c3.button("التالي ⬅️") and st.session_state.p_idx < total_p - 1:
        st.session_state.p_idx += 1; st.rerun()
    c2.markdown(f"<center>صفحة {st.session_state.p_idx + 1} من {total_p}</center>", unsafe_allow_html=True)
    if c1.button("➡️ السابق") and st.session_state.p_idx > 0:
        st.session_state.p_idx -= 1; st.rerun()

# --- 🏢 قسم المطورين ---
elif menu == "🏢 المطورين":
    st.markdown("<h2 class='right-title'>🏢 دليل المطورين العقاريين</h2>", unsafe_allow_html=True)
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
    
    for idx, row in devs.head(15).iterrows():
        st.markdown(f"<div class='pro-card'><h3 style='color:#f59e0b;'>{row['Developer']}</h3><p>👤 المالك: {row['Owner']}</p></div>", unsafe_allow_html=True)
        with st.expander("📂 بروفايل الشركة"):
            st.write(row['Detailed_Info'])

# --- 🛠️ حقيبة الأدوات (كاملة) ---
elif menu == "🛠️ أدوات البروكر":
    st.markdown("<h2 class='right-title'>🛠️ حقيبة أدوات البروكر</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 💰 حاسبة القسط")
        total = st.number_input("سعر الوحدة", 1000000)
        dp = st.slider("المقدم %", 0, 50, 10)
        yrs = st.number_input("سنوات التقسيط", 1, 15, 8)
        calc_res = (total - (total * dp/100)) / (yrs * 12)
        st.markdown(f"<h2 style='color:#f59e0b;'>{calc_res:,.0f} ج.م/شهري</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 📏 محول المساحة")
        fadan = st.number_input("المساحة بالفدان", 1.0)
        st.markdown(f"<h2 style='color:#f59e0b;'>{fadan * 4200:,.0f} متر مربع</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='tool-container'>", unsafe_allow_html=True)
        st.markdown("### 📝 مفكرة العميل")
        st.text_area("سجل تفاصيل المكالمة والملاحظات هنا...", height=350)
        st.button("💾 حفظ الملاحظات")
        st.markdown("</div>", unsafe_allow_html=True)
