import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- ميزة حماية الموبايل (منع الخروج بزر الرجوع) ---
st.components.v1.html("""
<script>
    window.onbeforeunload = function() { return "هل تريد مغادرة المنصة؟"; };
    history.pushState(null, null, location.href);
    window.onpopstate = function () { history.go(1); };
</script>
""", height=0)

# 2. الرابط الخاص بك
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 4. التنسيق الجمالي (White & Gold Luxury UI)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    
    /* الخلفية الكحلية الداكنة */
    [data-testid="stAppViewContainer"] {{ 
        background-color: #0a192f; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    /* نصوص بيضاء ناصعة وواضحة جداً */
    p, span, label, li, .stWrite, .stMetric div, .stMarkdown, div[data-testid="stExpander"] p {{ 
        color: #ffffff !important; 
        font-weight: 600 !important;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5) !important;
    }}
    
    /* عناوين ذهبية ملكية */
    h1, h2, h3, h4, .stMetric label {{ 
        color: #f59e0b !important; 
        font-weight: 900 !important;
    }}

    /* أزرار النظام (أبيض داخل ذهبي) */
    div.stButton > button {{ 
        border-radius: 12px !important; 
        background-color: #112240 !important;
        color: #ffffff !important;
        border: 2px solid #f59e0b !important;
        transition: 0.3s !important;
        font-weight: bold !important;
    }}
    
    /* كروت المشاريع (تأثير الفخامة) */
    div.stButton > button[key*="card_"], div.stButton > button[key*="ready_"] {{
        background: linear-gradient(145deg, #112240, #0a192f) !important;
        color: #ffffff !important;
        border-right: 8px solid #f59e0b !important;
        min-height: 120px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.4) !important;
    }}

    div.stButton > button:hover {{ 
        background-color: #f59e0b !important; 
        color: #000000 !important; 
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.4) !important;
    }}

    /* صناديق المحتوى المحسنة */
    .smart-box {{ 
        background: #112240; 
        border: 2px solid #233554; 
        padding: 20px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b;
        color: #ffffff !important;
    }}

    /* تحسين شكل خانات الإدخال */
    input, textarea {{ 
        color: white !important; 
        background-color: #0d1e36 !important; 
        border: 1px solid #f59e0b !important; 
    }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ background: #112240; border-bottom: 2px solid #f59e0b; }}
    .ticker {{ color: #f59e0b !important; font-weight: bold; }}
    </style>
""", unsafe_allow_html=True)

# 5. دوال جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p
    except: return pd.DataFrame()

df_p = load_data()

# 6. نظام الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; padding-top:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        u_in = st.text_input("الأسم")
        p_in = st.text_input("كلمة السر", type="password")
        if st.button("دخول للمنصة 🚀"):
            if p_in == "2026":
                st.session_state.auth, st.session_state.current_user = True, "Admin"
                st.rerun()
    st.stop()

# 7. واجهة المنصة الرئيسية
st.markdown(f"""<div class='smart-box' style='text-align:center;'>
    <h1 style='margin:0;'>MA3LOMATI PRO</h1>
    <p style='color:#f59e0b !important; font-size:18px;'>مرحباً {st.session_state.current_user} | {egypt_now.strftime('%I:%M %p')}</p>
</div>""", unsafe_allow_html=True)

menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 8. عرض البيانات
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item['ProjectName']}</h2><p>📍 الموقع: {item['Location']}</p></div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    search = st.text_input("🔍 ابحث عن مشروع...")
    dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
    for i in range(0, len(dff.head(6)), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(dff):
                row = dff.iloc[i+j]
                if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{i+j}"):
                    st.session_state.selected_item = row; st.rerun()

elif menu == "أدوات البروكر":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    v = st.number_input("سعر الوحدة", 1000000)
    st.metric("القسط الشهري (على 8 سنوات)", f"{v/96:,.0f}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; padding:30px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
        transform: translateY(-5px) !important; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.4) !important; 
    }}
    
    /* الصناديق والمحتوى */
    .smart-box {{ 
        background: #112240; 
        border: 1px solid #233554; 
        padding: 25px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b; 
        color: #eeeeee; 
    }}
    .side-card {{ 
        background: #172a45; 
        padding: 15px; 
        border-radius: 15px; 
        border: 1px solid #233554; 
        margin-bottom: 10px; 
        border-right: 4px solid #f59e0b;
    }}
    .tool-card {{ 
        background: #172a45; 
        padding: 20px; 
        border-radius: 15px; 
        border-top: 4px solid #f59e0b; 
        text-align: center; 
        color: white;
    }}
    
    /* ألوان العناوين والمدخلات */
    h1, h2, h3 {{ color: #f59e0b !important; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ 
        color: #f59e0b !important; 
        font-weight: bold !important; 
    }}
    .stTabs [data-baseweb="tab-list"] {{ background-color: transparent !important; }}
    .stTabs [data-baseweb="tab"] {{ color: white !important; font-weight: bold !important; }}
    .stTabs [aria-selected="true"] {{ color: #f59e0b !important; border-bottom-color: #f59e0b !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول والاشتراك
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    tab_login, tab_signup = st.tabs(["🔐 تسجيل دخول", "📝 اشتراك جديد"])
    with tab_login:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            u_input = st.text_input("الأسم أو الجيميل", key="log_user")
            p_input = st.text_input("كلمة السر", type="password", key="log_pass")
            if st.button("دخول للمنصة 🚀"):
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
                    else: st.error("بيانات الدخول غير صحيحة")
    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("الأسم بالكامل")
            reg_pass = st.text_input("كلمة السر المرجوة", type="password")
            reg_email = st.text_input("الجيميل")
            reg_wa = st.text_input("رقم الواتساب")
            reg_co = st.text_input("الشركة")
            if st.button("تأكيد الاشتراك ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("تم تسجيلك بنجاح! اذهب الآن لتبويب تسجيل الدخول.")
                    else: st.error("حدث خطأ في الاتصال بالسيرفر")
                else: st.warning("يرجى ملء الاسم وكلمة السر والإيميل")
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر البصري
st.markdown(f"""
    <div style="background: linear-gradient(rgba(10,25,47,0.8), rgba(10,25,47,0.8)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 200px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات
c_top1, c_top2 = st.columns([0.7, 0.3])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    st.markdown(f"""<div style='text-align: left; padding: 5px; color: #aaa; font-size: 14px;'>
                📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 {egypt_now.strftime('%I:%M %p')} 
                <span style='cursor:pointer; color:#f59e0b; margin-right:15px;' onclick='window.location.reload()'>🔄</span></div>""", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout"): st.session_state.auth = False; st.rerun()

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "#112240"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}
    })

# 10. تفاصيل المشروع
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p>💰 تفاصيل السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
        <hr><p>{item.get('Payment Plan', 'خطط سداد متنوعة متاحة عند التواصل')}</p>
    </div>""", unsafe_allow_html=True)

# 11. المساعد الذكي
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري الذكي")
    col_f1, col_f2, col_f3 = st.columns(3)
    locs = sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else ["الكل"]
    sel_loc = col_f1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + locs)
    sel_type = col_f2.selectbox("🏠 نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري", "إداري", "طبي"])
    sel_budget = col_f3.number_input("💰 المقدم المتاح (EGP)", 0, step=50000)
    client_wa = st.text_input("رقم واتساب العميل (بدون أصفار)")
    if st.button("🎯 استخراج أفضل الترشيحات"):
        res = df_p.copy()
        if sel_loc != "الكل": res = res[res['Location'] == sel_loc]
        if not res.empty:
            st.success(f"تم إيجاد {len(res.head(10))} مشروع مطابق:")
            for idx, r in res.head(6).iterrows():
                with st.container(border=True):
                    c_txt, c_btn = st.columns([0.8, 0.2])
                    c_txt.write(f"🏢 **{r['ProjectName']}** | {r['Developer']}")
                    msg = f"أرشح لك مشروع {r['ProjectName']} في {r['Location']}."
                    c_btn.markdown(f"[📲 إرسال]({f'https://wa.me/{client_wa}?text={urllib.parse.quote(msg)}'})")
    st.markdown("</div>", unsafe_allow_html=True)

# 12. المشاريع
elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(12)
        for i, r in ready.iterrows():
            if st.button(f"✅ {r['ProjectName']}", key=f"ready_{i}"):
                st.session_state.selected_item = r; st.rerun()
    with m_col:
        f1, f2 = st.columns(2)
        search = f1.text_input("🔍 ابحث باسم المشروع")
        area_f = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        if area_f != "الكل": dff = dff[dff['Location'] == area_f]
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()

# 13. المطورين
elif menu == "المطورين":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 أفضل المطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(10).iterrows():
            st.markdown(f"<div class='side-card'><b>{r['Developer']}</b></div>", unsafe_allow_html=True)
    with m_col:
        search_d = st.text_input("🔍 ابحث عن مطور")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        for i, r in dfd_f.head(6).iterrows():
            if st.button(f"🏗️ {r['Developer']}", key=f"card_d_{i}"):
                st.session_state.selected_item = r; st.rerun()

# 14. أدوات البروكر
elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة البروكر")
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    with r1_c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("إجمالي السعر", 1000000, key="t1")
        st.metric("شهري (8 سنين)", f"{v/96:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r1_c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", 1000000, key="t4")
        st.metric("العمولة (1.5%)", f"{deal*0.015:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r1_c3:
        st.markdown("<div class='tool-card'><h3>📈 العائد</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", 1000000, key="t6")
        st.metric("ROI المتوقع", "12%")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)

