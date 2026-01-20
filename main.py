import streamlit as st
import pandas as pd
import requests
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (Midnight & Gold Design)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 1rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #0a192f; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    h1, h2, h3 { color: #f59e0b !important; }
    p, span, label { color: #ccd6f6 !important; font-weight: bold; }
    div.stButton > button {
        background: linear-gradient(145deg, #112240, #0a192f) !important;
        color: #ffffff !important; border: 1px solid #233554 !important;
        border-right: 5px solid #f59e0b !important; border-radius: 12px !important;
        min-height: 100px !important; width: 100% !important; transition: 0.3s all ease !important;
    }
    div.stButton > button:hover { border-color: #f59e0b !important; transform: translateY(-5px) !important; }
    .smart-box { background: #112240; border: 1px solid #233554; padding: 20px; border-radius: 15px; border-right: 6px solid #f59e0b; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الحالة والرابط
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None

# الرابط الخاص بك (Apps Script)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# --- وظائف الربط الفعلي مع جوجل شيت ---
def signup_user(name, pwd, email):
    payload = {"name": name, "password": pwd, "email": email}
    try:
        # إرسال البيانات للجوجل شيت لحفظ مستخدم جديد
        response = requests.post(SCRIPT_URL, json=payload)
        return response.text == "Success"
    except: return False

def login_user(user_input, pwd_input):
    try:
        # جلب قائمة المستخدمين والتحقق منهم
        response = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if response.status_code == 200:
            users = response.json()
            for u in users:
                n, p, e = str(u.get('Name','')), str(u.get('Password','')), str(u.get('Email',''))
                if (user_input.strip().lower() in [n.lower(), e.lower()]) and str(pwd_input) == p:
                    return n
        return None
    except: return None

# 4. نظام الدخول والاشتراك (المرتبط بالشيت)
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    tab_log, tab_sign = st.tabs(["🔐 دخول", "📝 اشتراك"])
    
    with tab_log:
        u_in = st.text_input("الأسم أو الجيميل")
        p_in = st.text_input("كلمة السر", type="password")
        if st.button("دخول 🚀"):
            if p_in == "2026": # كود طوارئ
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
            else:
                user = login_user(u_in, p_in)
                if user:
                    st.session_state.auth, st.session_state.current_user = True, user
                    st.rerun()
                else: st.error("خطأ في البيانات أو المستخدم غير مسجل")

    with tab_sign:
        reg_n = st.text_input("الأسم الكامل")
        reg_e = st.text_input("الجيميل")
        reg_p = st.text_input("كلمة السر الجديدة", type="password")
        if st.button("تأكيد التسجيل ✅"):
            if reg_n and reg_e and reg_p:
                if signup_user(reg_n, reg_p, reg_e):
                    st.success("تم تسجيلك! يمكنك الآن الدخول.")
                else: st.error("حدث خطأ في الاتصال بالشيت")
    st.stop()

# 5. تحميل بيانات المشاريع والمطورين
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.rename(columns={'Area':'Location','الموقع':'Location','Project Name':'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 6. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "calculator"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 7. الأقسام
if menu == "المشاريع":
    st.title("🏢 دليل المشاريع")
    search = st.text_input("🔍 ابحث عن مشروع")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i, r in dff.head(8).iterrows():
        if st.button(f"🏢 {r['ProjectName']} | {r['Location']}", key=f"p_{i}"):
            st.session_state.selected_item = r
    
elif menu == "المساعد الذكي":
    st.title("🤖 مساعد المبيعات")
    wa = st.text_input("رقم واتساب العميل")
    loc = st.selectbox("📍 المنطقة", sorted(df_p['Location'].unique()))
    if st.button("🎯 ترشيح وإرسال"):
        res = df_p[df_p['Location'] == loc].head(3)
        for _, r in res.iterrows():
            msg = f"أهلاً.. أرشح لك {r['ProjectName']}."
            st.markdown(f"[📲 إرسال الواتساب لبـ {r['ProjectName']}](https://wa.me/{wa}?text={urllib.parse.quote(msg)})")

elif menu == "أدوات البروكر":
    st.title("🛠️ حسابات مالية")
    price = st.number_input("إجمالي السعر", value=1000000)
    st.metric("القسط الشهري (على 8 سنين)", f"{(price*0.9)/(8*12):,.0f}")

st.markdown(f"<p style='text-align:center; margin-top:50px;'>أهلاً بك يا {st.session_state.current_user} | 2026</p>", unsafe_allow_html=True)
    item = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.selected_item = None; st.rerun()
    
    st.markdown(f"""
    <div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <hr style='border-color:#233554;'>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p>💰 السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
        <p>📝 نظام السداد: {item.get('Payment Plan', 'خطط متنوعة متاحة')}</p>
    </div>
    """, unsafe_allow_html=True)

# 7. الأقسام الرئيسية
elif menu == "المساعد الذكي":
    st.title("🤖 المساعد الذكي")
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    loc = c1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    wa = c2.text_input("رقم واتساب العميل")
    
    if st.button("🎯 توليد المقترح الإحترافي"):
        res = df_p[df_p['Location'] == loc] if loc != "الكل" else df_p
        if not res.empty:
            for _, r in res.head(3).iterrows():
                msg = f"أهلاً بك.. أرشح لك مشروع {r['ProjectName']} في {r['Location']}."
                st.write(f"🏢 {r['ProjectName']} - {r['Developer']}")
                st.markdown(f"[📲 إرسال المقترح للعميل](https://wa.me/{wa}?text={urllib.parse.quote(msg)})")
        else: st.warning("لا توجد مشاريع في هذه المنطقة حالياً")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن اسم المشروع...")
    area_f = st.selectbox("📍 تصفية حسب المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    if area_f != "الكل": dff = dff[dff['Location'] == area_f]
    
    start = st.session_state.p_idx * 6
    page = dff.iloc[start:start+6]
    
    for i, r in page.iterrows():
        if st.button(f"🏢 {r['ProjectName']}\n📍 {r['Location']}\n🏗️ {r['Developer']}", key=f"card_p_{i}"):
            st.session_state.selected_item = r; st.rerun()
            
    p1, _, p2 = st.columns([1,2,1])
    if st.session_state.p_idx > 0:
        if p1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
    if start + 6 < len(dff):
        if p2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن المطور...")
    dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    
    for i, r in dfd_f.head(10).iterrows():
        if st.button(f"🏗️ {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}\n💼 المالك: {r.get('Owner','---')}", key=f"card_d_{i}"):
            st.session_state.selected_item = r; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة البروكر")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("<div class='tool-card'><h3>💳 حساب القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("إجمالي السعر", value=1000000)
        down = st.number_input("المقدم", value=100000)
        years = st.slider("عدد السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{(price-down)/(years*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col2:
        st.markdown("<div class='tool-card'><h3>💰 حساب العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", value=2000000)
        pct = st.slider("النسبة %", 0.5, 5.0, 1.5)
        st.metric("صافي الربح", f"{deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

# 8. الفوتر
st.markdown("<br><hr style='border-color:#233554;'><p style='text-align:center; color:#4f5b7d;'>MA3LOMATI PRO © 2026 | النسخة الاحترافية</p>", unsafe_allow_html=True)

