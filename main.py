import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار (RSS)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار العقارية..."
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .luxury-header {{
        background: linear-gradient(90deg, #0f0f0f 0%, #1a1a1a 100%);
        border-bottom: 2px solid #f59e0b; padding: 20px 40px;
        display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 30px 30px; margin-bottom: 10px;
    }}
    .logo-main {{ color: #f59e0b; font-weight: 900; font-size: 28px; }}
    
    /* شريط الأخبار المتحرك */
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        border-radius: 15px !important; width: 100% !important;
        min-height: 200px !important; text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        font-weight: bold !important; font-size: 16px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة تسجيل الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": 
            st.session_state.auth = True
            st.rerun()
    st.stop()

# 6. الهيدر وشريط الأخبار
now = datetime.now()
h_col1, h_col2, h_col3 = st.columns([1.5, 2, 1])
with h_col1: st.markdown('<div class="logo-main">MA3LOMATI PRO</div>', unsafe_allow_html=True)
with h_col2:
    st.markdown(f"<div style='text-align:center; color:white;'><b>مرحباً بك يا بروكر المستقبل 👋</b><br><span style='color:#f59e0b; font-size:12px;'>📅 {now.strftime('%Y-%m-%d')} | 🕒 {now.strftime('%I:%M %p')}</span></div>", unsafe_allow_html=True)
with h_col3:
    if st.button("🚪 تسجيل الخروج", use_container_width=True):
        st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 7. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---"); d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip(); d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 8. المنيو الرئيسي
menu = option_menu(None, ["أدوات البروكر", "المشاريع", "المطورين"], 
    icons=["briefcase", "building-up", "person-badge"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

main_col, side_col = st.columns([0.78, 0.22])

# الجانب الجانبي
with side_col:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>⚡ استلام فوري</h4>", unsafe_allow_html=True)
    if not df_p.empty:
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(8)
        for _, row in ready.iterrows():
            st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:8px; border-radius:10px; margin-bottom:5px; font-size:12px; color:white;">{row["Project Name"]}</div>', unsafe_allow_html=True)

# القسم الرئيسي
with main_col:
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"<div style='background:#111; padding:30px; border-radius:20px; border-right:5px solid #f59e0b; color:white;'><h2>{item.get('Project Name', item.get('Developer'))}</h2><hr>{item.get('Project Features', item.get('Detailed_Info', 'لا توجد تفاصيل'))}</div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        f1, f2, f3 = st.columns(3)
        search = f1.text_input("🔍 اسم المشروع")
        area = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Area'].unique().tolist()))
        dev = f3.selectbox("🏗️ المطور", ["الكل"] + sorted(df_p['Developer'].unique().tolist()))
        dff = df_p.copy()
        if search: dff = dff[dff['Project Name'].str.contains(search, case=False)]
        if area != "الكل": dff = dff[dff['Area'] == area]
        if dev != "الكل": dff = dff[dff['Developer'] == dev]
        limit = 6
        start = st.session_state.p_idx * limit
        page = dff.iloc[start:start+limit]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['Project Name']}\n📍 {row['Area']}\n🏗️ {row['Developer']}\n✨ عرض التفاصيل", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        st.markdown("---")
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0:
            if p1.button("⬅️ السابق", key="prev_p"): st.session_state.p_idx -= 1; st.rerun()
        if start + limit < len(dff):
            if p2.button("التالي ➡️", key="next_p"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        limit_d = 6
        start_d = st.session_state.d_idx * limit_d
        page_d = df_d.iloc[start_d:start_d+limit_d]
        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    if cols[j].button(f"🏗️ {row['Developer']}\n⭐ فئة: {row.get('Developer Category','A')}\n📖 سابقة الأعمال", key=f"card_d_{start_d+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        st.markdown("---")
        dp1, _, dp2 = st.columns([1,2,1])
        if st.session_state.d_idx > 0:
            if dp1.button("⬅️ السابق", key="prev_d"): st.session_state.d_idx -= 1; st.rerun()
        if start_d + limit_d < len(df_d):
            if dp2.button("التالي ➡️", key="next_d"): st.session_state.d_idx += 1; st.rerun()

    elif menu == "أدوات البروكر":
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حقيبة البروكر الذكية</h2>", unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            with st.expander("💳 1. حاسبة الأقساط (الأكثر طلباً)"):
                total_p = st.number_input("إجمالي السعر", 1000000)
                down_p = st.number_input("المقدم", 100000)
                years = st.slider("عدد السنين", 1, 15, 8)
                remain = total_p - down_p
                st.info(f"المبلغ المتبقي: {remain:,.0f}")
                st.metric("القسط الشهري", f"{remain/(years*12):,.0f}")
                st.metric("القسط الربع سنوي", f"{remain/(years*4):,.0f}")

            with st.expander("💰 2. حاسبة العمولة"):
                deal = st.number_input("قيمة الصفقة", 1000000, key="comm")
                comm_pct = st.slider("النسبة %", 1.0, 5.0, 1.5)
                st.metric("عمولتك الصافية", f"{deal*(comm_pct/100):,.0f} EGP")

        with t2:
            with st.expander("📈 3. العائد على الاستثمار ROI"):
                buy = st.number_input("سعر الشراء", 1000000, key="roi")
                rent = st.number_input("إيجار شهري متوقع", 5000)
                st.write(f"العائد السنوي: **{((rent*12)/buy)*100:.1f}%**")

            with st.expander("📏 4. محول المساحات"):
                val = st.number_input("القيمة بالمتر", 100.0)
                st.write(f"تساوي: {val * 10.76:.2f} قدم مربع")

        st.markdown("---")
        st.markdown("<h4 style='text-align:center;'>🎯 5. عداد الإنجاز & 🏦 6. تمويل العميل</h4>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        c1.number_input("📞 مكالمات اليوم", 0)
        salary = c2.number_input("دخل العميل الشهري", 10000)
        c2.success(f"أقصى قسط مسموح: {salary*0.4:,.0f}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
