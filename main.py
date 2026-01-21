import streamlit as st
import pandas as pd
import requests
import feedparser
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu
from streamlit_autorefresh import st_autorefresh

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# تحديث الصفحة كل 30 ثانية للأخبار والساعة
st_autorefresh(interval=30000, key="fresher")

# 2. الروابط
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# --- وظائف البيانات ---
@st.cache_data(ttl=600)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS).fillna("---")
        d = pd.read_csv(URL_DEVELOPERS).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        # تحويل عمود السعر لرقمي للفحص في المساعد الذكي
        p['Price_Numeric'] = pd.to_numeric(p['Price'].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        news = [item.title for item in feed.entries[:15]]
        return "  •  ".join(news) if news else "MA3LOMATI PRO 2026: السوق العقاري في قمة نشاطه."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى."

def login_user(u, p):
    if p == "2026": return "Admin"
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if res.status_code == 200:
            for user in res.json():
                if (str(user.get('Email')).lower() == u.lower()) and str(user.get('Password')) == p:
                    return user.get('Name')
    except: pass
    return None

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&family=Orbitron:wght@500&display=swap');
    
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* شريط الأخبار البطيء جداً */
    .ticker-wrap {{ background: #000; border-bottom: 2px solid #f59e0b; padding: 15px 0; overflow: hidden; }}
    .ticker {{ display: inline-block; animation: ticker 180s linear infinite; color: #f59e0b; font-weight: 900; font-size: 18px; white-space: nowrap; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* أزرار وكروت */
    div.stButton > button {{ border-radius: 12px !important; font-weight: 900 !important; }}
    .logout-btn button {{ background-color: #ff4b4b !important; color: white !important; height: 35px !important; width: 100px !important; font-size: 14px !important; }}
    
    div.stButton > button[key*="card_"] {{
        background: #111 !important; color: #f59e0b !important; min-height: 120px !important;
        border: 1px solid #222 !important; border-right: 8px solid #f59e0b !important;
        text-align: right !important; margin-bottom: 10px !important;
    }}
    
    .smart-box {{ background: #111; border: 1px solid #222; padding: 25px; border-radius: 20px; border-right: 6px solid #f59e0b; color: white; margin-bottom: 20px; }}
    .tool-card {{ background: #0c0c0c; padding: 20px; border-radius: 15px; border-top: 5px solid #f59e0b; text-align: center; border: 1px solid #222; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:60px;'><h1 style='color:#f59e0b; font-size:80px; font-weight:900;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["SIGN IN", "CREATE ACCOUNT"])
    with t1:
        u = st.text_input("Username / Email")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN TO PLATFORM 🚀"):
            user = login_user(u, p)
            if user:
                st.session_state.auth, st.session_state.current_user = True, user
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# 6. الهيدر العلوي (الساعة + اليوزر + الخروج)
c_h1, c_h2, c_h3 = st.columns([0.4, 0.45, 0.15])
with c_h1:
    st.markdown(f"<p style='color:#f59e0b; font-weight:bold; padding-top:10px;'>👤 {st.session_state.current_user}</p>", unsafe_allow_html=True)
with c_h2:
    st.markdown(f"<p style='color:#888; font-family:Orbitron; padding-top:10px;'>🕒 {egypt_now.strftime('%I:%M %p')} | 📅 {egypt_now.strftime('%d/%m/%Y')}</p>", unsafe_allow_html=True)
with c_h3:
    st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
    if st.button("Logout"): st.session_state.auth = False; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# الهيدر الصوري وشريط الأخبار
st.markdown("""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 150px; background-size: cover; background-position: center; border-radius: 20px; 
                display: flex; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b; margin-bottom:10px;">
        <h1 style="color: white; font-size: 45px; font-weight:900;">MA3LOMATI PRO</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {get_real_news()}</div></div>', unsafe_allow_html=True)

# 7. المنيو والبيانات
df_p, df_d = load_data()
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 8. تفاصيل المشروع المختار
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2><hr>
        <p style='font-size:20px;'>📍 الموقع: {item.get('Location', '---')}</p>
        <p style='font-size:20px;'>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p style='font-size:20px;'>💰 السعر: {item.get('Price', 'تواصل لمعرفة السعر')}</p>
        <p style='background:#222; padding:15px; border-radius:10px;'>📝 تفاصيل: {item.get('Payment Plan', 'خطط سداد متنوعة متوفرة')}</p>
    </div>""", unsafe_allow_html=True)

# --- صفحة المساعد الذكي ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد العقاري الذكي</h3><p>أدخل متطلبات العميل وسأقترح عليك أفضل الخيارات</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    loc = c1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    budget = c2.number_input("💰 الميزانية القصوى (EGP)", 0, 500000000, 5000000)
    dev_filter = c3.selectbox("🏗️ تفضيل مطور معين", ["الكل"] + sorted(df_d['Developer'].unique().tolist()))
    
    if st.button("🎯 توليد الترشيحات"):
        # منطق الفلترة الحقيقي
        results = df_p.copy()
        if loc != "الكل": results = results[results['Location'] == loc]
        if dev_filter != "الكل": results = results[results['Developer'] == dev_filter]
        if budget > 0: results = results[results['Price_Numeric'] <= budget]
        
        if not results.empty:
            st.success(f"تم العثور على {len(results.head(6))} خيارات مطابقة")
            for i in range(0, len(results.head(6)), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i+j < len(results):
                        row = results.iloc[i+j]
                        if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_res_{i+j}"):
                            st.session_state.selected_item = row; st.rerun()
        else: st.warning("لا توجد نتائج مطابقة تماماً، حاول تغيير الفلاتر.")

# --- صفحة المشاريع ---
elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع (بالاسم أو المنطقة)")
    dff = df_p[df_p.apply(lambda row: row.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
    for i in range(0, len(dff.head(10)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row['Developer']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

# --- صفحة المطورين ---
elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن شركة تطوير")
    dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    for i in range(0, len(dfd_f.head(10)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dfd_f):
                row = dfd_f.iloc[i+j]
                if cols[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}", key=f"card_d_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

# --- صفحة أدوات البروكر ---
elif menu == "أدوات البروكر":
    st.title("🛠️ صندوق أدوات البروكر المحترف")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='tool-card'><h3>💳 حاسبة الأقساط</h3>", unsafe_allow_html=True)
        p = st.number_input("قيمة الوحدة", 1000000)
        y = st.slider("مدة السداد (سنوات)", 1, 15, 8)
        st.metric("القسط الشهري", f"{p/(y*12):,.0f} EGP")
    with c2:
        st.markdown("<div class='tool-card'><h3>💰 حاسبة العمولة</h3>", unsafe_allow_html=True)
        d = st.number_input("قيمة الصفقة", 1000000, key="deal")
        r = st.slider("نسبة العمولة %", 0.5, 10.0, 1.5)
        st.metric("صافي الربح", f"{d*(r/100):,.0f} EGP")
    with c3:
        st.markdown("<div class='tool-card'><h3>📈 العائد ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", 1000000, key="roi_b")
        rent = st.number_input("الإيجار السنوي المتوقع", 100000)
        st.metric("نسبة العائد السنوي", f"{(rent/buy)*100:.1f} %")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | Powered by AI</p>", unsafe_allow_html=True)
