import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار العقارية
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار العقارية..."
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."

news_text = get_real_news()

# 4. التنسيق الجمالي الموحد (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    div.stButton > button {{
        background-color: white !important; color: #111 !important;
        border-radius: 15px !important; width: 100% !important;
        text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        font-weight: bold !important;
    }}
    .stSelectbox label, .stTextInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    .project-card-custom {{
        background: #111; border-right: 5px solid #f59e0b; padding: 20px; border-radius: 15px; color: white; margin-bottom: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة تسجيل الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات (دمج الشيتات الـ 3 اللي بعت روابطهم)
@st.cache_data(ttl=60)
def load_data():
    # الرابط الموحد (بما أنك بعت نفس الرابط لـ 3 حاجات، الكود هيقرأ منه ويفلتر)
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url).fillna("---")
        df.columns = df.columns.str.strip()
        # شيت المشاريع هو الأساس
        return df
    except: return pd.DataFrame()

df_all = load_data()

# 7. الهيدر وشريط الأخبار
now = datetime.now()
h_col1, h_col2, h_col3 = st.columns([1.5, 2, 1])
with h_col1: st.markdown('<div style="color:#f59e0b; font-weight:900; font-size:28px;">MA3LOMATI PRO</div>', unsafe_allow_html=True)
with h_col2:
    st.markdown(f"<div style='text-align:center; color:white;'><b>مرحباً بك يا بروكر المستقبل 👋</b><br><span style='color:#f59e0b; font-size:12px;'>📅 {now.strftime('%Y-%m-%d')} | 🕒 {now.strftime('%I:%M %p')}</span></div>", unsafe_allow_html=True)
with h_col3:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "building-up", "person-badge", "briefcase"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

main_col, side_col = st.columns([0.78, 0.22])

# الجانب الجانبي (استلام فوري ريسيل)
with side_col:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>⚡ صفقات ريسيل</h4>", unsafe_allow_html=True)
    if not df_all.empty and 'Sales Type' in df_all.columns:
        resale = df_all[df_all['Sales Type'].str.contains('ريسيل', na=False)].head(5)
        for _, row in resale.iterrows():
            st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:8px; border-radius:10px; margin-bottom:5px; font-size:12px; color:white;">{row["Project Name"]}<br><span style="color:#aaa;">{row["Starting Price (EGP)"]}</span></div>', unsafe_allow_html=True)

# القسم الرئيسي
with main_col:
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"""
        <div class="project-card-custom">
            <h2>{item.get('Project Name', 'تفاصيل')}</h2>
            <hr>
            <p>🏗️ <b>المطور:</b> {item.get('Developer', '---')}</p>
            <p>📍 <b>الموقع:</b> {item.get('Location', '---')}</p>
            <p>💰 <b>السعر:</b> {item.get('Starting Price (EGP)', '---')}</p>
            <p>🏠 <b>الوحدات:</b> {item.get('Available Units (Types)', '---')}</p>
            <p>🏗️ <b>التشطيب:</b> {item.get('Finishing Status', '---')}</p>
            <p>💳 <b>السداد:</b> {item.get('Payment Plan', '---')}</p>
        </div>
        """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        f1, f2, f3 = st.columns(3)
        s_name = f1.text_input("🔍 اسم المشروع")
        s_loc = f2.selectbox("📍 الموقع", ["الكل"] + sorted(df_all['Location'].unique().tolist()) if 'Location' in df_all.columns else ["الكل"])
        s_dev = f3.selectbox("🏗️ المطور", ["الكل"] + sorted(df_all['Developer'].unique().tolist()) if 'Developer' in df_all.columns else ["الكل"])
        
        dff = df_all.copy()
        if s_name: dff = dff[dff['Project Name'].str.contains(s_name, case=False)]
        if s_loc != "الكل": dff = dff[dff['Location'] == s_loc]
        if s_dev != "الكل": dff = dff[dff['Developer'] == s_dev]

        # عرض الكروت (نظام 2 في كل صف)
        limit = 6
        start = st.session_state.p_idx * limit
        page = dff.iloc[start:start+limit]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['Project Name']}\n💰 {row['Starting Price (EGP)']}\n🏗️ {row['Developer']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        
        # Pagination
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0:
            if p1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
        if start + limit < len(dff):
            if p2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المساعد الذكي":
        st.markdown("<h3 style='color:#f59e0b;'>🤖 ربط ميزانية العميل بالمشاريع</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            client_budget = st.text_input("ميزانية العميل (مقدم)")
            target_type = st.selectbox("نوع الوحدة المطلوب", ["شقق", "فيلات", "تاون هاوس", "دوبلكس"])
        with c2:
            whatsapp_num = st.text_input("رقم العميل (WhatsApp)")
            if st.button("📤 توليد عرض سعر"):
                msg = f"أهلاً بك.. بناءً على طلبك لوحدة {target_type}، أرشح لك أقوى مشاريع التجمع المتاحة حالياً."
                st.markdown(f"[إرسال العرض عبر الواتساب](https://wa.me/{whatsapp_num}?text={urllib.parse.quote(msg)})")

    elif menu == "أدوات البروكر":
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حاسبة العقارات الذكية</h2>", unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            with st.expander("💳 حاسبة الأقساط"):
                total = st.number_input("إجمالي السعر", 1000000)
                down = st.number_input("المقدم", 100000)
                yrs = st.slider("السنين", 1, 15, 8)
                st.metric("القسط الشهري", f"{(total-down)/(yrs*12):,.0f}")
        with t2:
            with st.expander("📏 محول المساحات"):
                m2 = st.number_input("المتر المربع", 100.0)
                st.write(f"تساوي: {m2 * 10.76:.2f} قدم مربع")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
