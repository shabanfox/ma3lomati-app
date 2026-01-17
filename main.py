import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار (RSS)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "MA3LOMATI PRO: تحديثات السوق العقاري 2026"
    except: return "متابعة مستمرة لآخر أخبار العقارات في مصر."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 2px solid #f59e0b; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* ستايل الكروت */
    div.stButton > button {{ border-radius: 15px !important; font-family: 'Cairo', sans-serif !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 160px !important; text-align: right !important;
        font-weight: bold !important; font-size: 16px !important;
        border: none !important; transition: 0.3s !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 10px solid #f59e0b !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب البيانات وتنظيفها (الدمج الذكي)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        
        # تنظيف النصوص لمنع التكرار
        for col in ['Project Name', 'Developer', 'Owner', 'Location']:
            if col in p.columns: p[col] = p[col].astype(str).str.strip()
            if col in d.columns: d[col] = d[col].astype(str).str.strip()
        
        # حذف المكرر الحقيقي
        p = p.drop_duplicates(subset=['Project Name', 'Developer'], keep='first')
        d = d.drop_duplicates(subset=['Developer'], keep='first')
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 6. نظام الحماية
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 7. الهيدر
h1, h2, h3 = st.columns([1.5, 2, 1])
with h1: st.markdown('<div style="color:#f59e0b; font-weight:900; font-size:28px;">MA3LOMATI PRO</div>', unsafe_allow_html=True)
with h2: st.markdown(f"<div style='text-align:center; color:white;'>📅 {datetime.now().strftime('%Y-%m-%d')} | 🕒 {datetime.now().strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
with h3: 
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "people", "tools"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. توزيع الصفحة
col_main, col_side = st.columns([0.78, 0.22])

with col_side:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
    ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
    for _, row in ready.iterrows():
        st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:10px; border-radius:10px; margin-bottom:8px; font-size:12px; color:white;">{row["Project Name"]}</div>', unsafe_allow_html=True)

with col_main:
    # --- المساعد الذكي المطور ---
    if menu == "المساعد الذكي":
        st.markdown("<div class='smart-box'><h3>🤖 المساعد الذكي (فلترة وتحليل 2026)</h3>", unsafe_allow_html=True)
        f1, f2, f3, f4 = st.columns(4)
        with f1:
            s_name = st.text_input("اسم المشروع")
            s_loc = st.selectbox("الموقع", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
        with f2:
            s_dev = st.selectbox("المطور", ["الكل"] + sorted(df_p['Developer'].unique().tolist()))
            s_owner = st.selectbox("المالك", ["الكل"] + sorted(df_p['Owner'].unique().tolist()))
        with f3:
            s_type = st.selectbox("نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري", "إداري"])
            s_finish = st.selectbox("التشطيب", ["الكل", "تشطيب كامل", "نصف تشطيب"])
        with f4:
            s_sale = st.selectbox("نوع البيع", ["الكل", "مطور", "ريسيل"])
            s_price = st.number_input("الحد الأقصى للسعر", 0)

        # فلترة البيانات
        res = df_p.copy()
        if s_name: res = res[res['Project Name'].str.contains(s_name, case=False)]
        if s_loc != "الكل": res = res[res['Location'] == s_loc]
        if s_dev != "الكل": res = res[res['Developer'] == s_dev]
        if s_owner != "الكل": res = res[res['Owner'] == s_owner]
        if s_finish != "الكل": res = res[res['Finishing Status'] == s_finish]
        if s_sale != "الكل": res = res[res['Sales Type'] == s_sale]
        if s_type != "الكل": res = res[res['Available Units (Types)'].str.contains(s_type, case=False)]

        for i, r in res.head(5).iterrows():
            with st.expander(f"📊 تحليل مشروع: {r['Project Name']}"):
                c_a, c_b = st.columns(2)
                c_a.info(f"✅ المميزات: مطور قوي ({r['Owner']}) - موقع استراتيجي في {r['Location']}")
                c_b.error(f"⚠️ تنبيه للبروكر: تأكد من حالة التسليم {r['Finishing Status']}")
                phone = st.text_input("واتساب العميل", key=f"p_{i}")
                if st.button("إرسال التفاصيل 🚀", key=f"send_{i}"):
                    msg = f"أرشح لك مشروع {r['Project Name']} في {r['Location']}. نظام السداد: {r['Payment Plan']}"
                    st.markdown(f"[فتح واتساب](https://wa.me/{phone}?text={urllib.parse.quote(msg)})")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- المشاريع (كروت) ---
    elif menu == "المشاريع":
        search = st.text_input("🔍 بحث سريع عن مشروع...")
        dff = df_p[df_p['Project Name'].str.contains(search, case=False)] if search else df_p
        
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    r = page.iloc[i+j]
                    if cols[j].button(f"🏢 {r['Project Name']}\n📍 {r['Location']}\n🏗️ {r['Developer']}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = r; st.rerun()
        
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0 and p1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
        if start + 6 < len(dff) and p2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

    # --- المطورين (بنفس شكل كروت المشاريع) ---
    elif menu == "المطورين":
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        for i in range(0, len(dfd.head(10)), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(dfd.head(10)):
                    r = dfd.iloc[i+j]
                    if cols[j].button(f"🏗️ {r['Developer']}\n⭐ المالك: {r.get('Owner', '---')}\n🏢 اضغط للتفاصيل", key=f"card_d_{i+j}"):
                        st.session_state.selected_item = r; st.rerun()

    # --- أدوات البروكر كاملة ---
    elif menu == "أدوات البروكر":
        st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            with st.expander("💳 حاسبة الأقساط"):
                price = st.number_input("السعر الإجمالي", 1000000)
                down = st.number_input("المقدم", 100000)
                years = st.slider("السنين", 1, 15, 8)
                st.metric("القسط الشهري", f"{(price-down)/(years*12):,.0f}")
        with t2:
            with st.expander("💰 حاسبة العمولة"):
                deal = st.number_input("قيمة الصفقة", 1000000)
                comm = st.slider("النسبة %", 0.5, 5.0, 1.5)
                st.metric("عمولتك", f"{deal*(comm/100):,.0f}")
            with st.expander("📏 محول المساحات"):
                mtr = st.number_input("المتر المربع", 100.0)
                st.write(f"تساوي: {mtr * 10.76:,.2f} قدم مربع")
        st.markdown("</div>", unsafe_allow_html=True)

    # --- نافذة التفاصيل (Pop-up style) ---
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        st.markdown("---")
        with st.container(border=True):
            st.header(f"📌 {item.get('Project Name', item.get('Developer'))}")
            st.write(f"**المطور:** {item.get('Developer', '---')} | **المالك:** {item.get('Owner', '---')}")
            st.write(f"**الموقع:** {item.get('Location', '---')} | **السعر:** {item.get('Starting Price (EGP)', '---')}")
            st.write(f"**نظام السداد:** {item.get('Payment Plan', '---')}")
            st.info(f"**حالة التشطيب والوحدات:** {item.get('Finishing Status', '---')} - {item.get('Available Units (Types)', '---')}")
            if st.button("❌ إغلاق التفاصيل"): st.session_state.selected_item = None; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
