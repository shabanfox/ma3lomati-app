import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى لعام 2026."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 1rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 2px solid #f59e0b; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #aaa; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; width: 100% !important; }}
    div.stButton > button[key*="card_"] {{ background-color: white !important; color: #111 !important; min-height: 140px !important; text-align: right !important; font-weight: bold !important; border: none !important; margin-bottom: 15px !important; }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 10px solid #f59e0b !important; box-shadow: 0 10px 20px rgba(245,158,11,0.2) !important; }}
    .smart-box {{ background: #111; border: 1px solid #333; padding: 30px; border-radius: 20px; border-right: 8px solid #f59e0b; color: white; margin-bottom: 20px; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; margin-bottom: 15px; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. نظام الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات وتصحيح الأعمدة (حل مشكلة الـ KeyError)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        # توحيد اسم عمود الموقع لتجنب الخطأ
        if 'Area' in p.columns and 'Location' not in p.columns: p.rename(columns={'Area': 'Location'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر
h_c1, h_c2, h_c3 = st.columns([1.5, 2, 1])
with h_c1: st.markdown('<div style="color:#f59e0b; font-weight:900; font-size:28px;">MA3LOMATI PRO</div>', unsafe_allow_html=True)
with h_c2: st.markdown(f"<div style='text-align:center; color:white;'>📅 {datetime.now().strftime('%Y-%m-%d')} | 🕒 {datetime.now().strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
with h_c3: 
    if st.button("🚪 تسجيل الخروج"): st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "دليل المشاريع", "المطورين", "حقيبة الأدوات"], 
    icons=["robot", "search", "people", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 9. عرض المحتوى
if st.session_state.selected_item is not None:
    if st.button("⬅️ العودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2 style='color:#f59e0b;'>{item.get('Project Name', 'تفاصيل الكيان')}</h2>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
            <div>
                <p>📍 <b>الموقع:</b> {item.get('Location', '---')}</p>
                <p>🏗️ <b>المطور:</b> {item.get('Developer', '---')}</p>
                <p>👤 <b>المالك:</b> {item.get('Owner', '---')}</p>
            </div>
            <div>
                <p>💰 <b>السعر:</b> {item.get('Starting Price (EGP)', '---')}</p>
                <p>💳 <b>السداد:</b> {item.get('Payment Plan', '---')}</p>
                <p>🏠 <b>الوحدات:</b> {item.get('Available Units (Types)', '---')}</p>
            </div>
        </div>
        <hr style='border-color:#333'>
        <div style='display:flex; gap:20px;'>
            <div style='flex:1; background:#064e3b; padding:15px; border-radius:10px;'>✅ <b>المميزات:</b> موقع استراتيجي - مطور ذو سابقة أعمال قوية - عوائد استثمارية متوقعة.</div>
            <div style='flex:1; background:#7f1d1d; padding:15px; border-radius:10px;'>⚠️ <b>تنبيه البروكر:</b> تأكد من نسبة التحميل في العقار وجدية جدول التنفيذ.</div>
        </div>
    </div>""", unsafe_allow_html=True)

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد الذكي للربط العقاري")
    st.write("فلترة متقدمة للوصول لأفضل ترشيح لعميلك:")
    
    col_f1, col_f2, col_f3, col_f4 = st.columns(4)
    with col_f1: 
        loc_list = sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else []
        m_loc = st.selectbox("المنطقة", ["الكل"] + loc_list)
    with col_f2:
        m_dev = st.selectbox("المطور", ["الكل"] + sorted(df_p['Developer'].unique().tolist()))
    with col_f3:
        m_type = st.selectbox("نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري", "إداري"])
    with col_f4:
        m_sale = st.selectbox("نوع البيع", ["الكل", "مطور", "ريسيل"])

    client_num = st.text_input("رقم واتساب العميل (إرسال مباشر)")
    
    matches = df_p.copy()
    if m_loc != "الكل": matches = matches[matches['Location'] == m_loc]
    if m_dev != "الكل": matches = matches[matches['Developer'] == m_dev]
    if m_type != "الكل": matches = matches[matches['Available Units (Types)'].str.contains(m_type, case=False)]
    if m_sale != "الكل": matches = matches[matches['Sales Type'] == m_sale]

    st.success(f"وجدنا {len(matches.head(10))} خيارات مطابقة")
    for _, r in matches.head(5).iterrows():
        with st.container(border=True):
            col_a, col_b = st.columns([0.8, 0.2])
            col_a.write(f"**{r['Project Name']}** | {r['Location']} | {r['Starting Price (EGP)']}")
            msg = f"أرشح لك مشروع {r['Project Name']} في {r['Location']}. المطور: {r['Developer']}. تواصل معي للتفاصيل."
            link = f"https://wa.me/{client_num}?text={urllib.parse.quote(msg)}"
            col_b.markdown(f"[📲 واتساب]({link})")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "دليل المشاريع":
    s_col1, s_col2 = st.columns([2,1])
    search_q = s_col1.text_input("🔍 ابحث عن اسم المشروع...")
    loc_list = sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else []
    loc_q = s_col2.selectbox("📍 فلتر بالمنطقة", ["الكل"] + loc_list)
    
    filtered_p = df_p.copy()
    if search_q: filtered_p = filtered_p[filtered_p['Project Name'].str.contains(search_q, case=False)]
    if loc_q != "الكل": filtered_p = filtered_p[filtered_p['Location'] == loc_q]
    
    start_idx = st.session_state.p_idx * 6
    page_p = filtered_p.iloc[start_idx : start_idx + 6]
    
    for i in range(0, len(page_p), 2):
        c_row = st.columns(2)
        for j in range(2):
            if i+j < len(page_p):
                row = page_p.iloc[i+j]
                if c_row[j].button(f"🏢 {row['Project Name']}\n📍 {row.get('Location','---')}\n🏗️ {row['Developer']}", key=f"card_p_{start_idx+i+j}"):
                    st.session_state.selected_item = row; st.rerun()
    
    st.markdown("---")
    nav1, nav2, nav3 = st.columns([1,2,1])
    if st.session_state.p_idx > 0:
        if nav1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
    if start_idx + 6 < len(filtered_p):
        if nav3.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

elif menu == "حقيبة الأدوات":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حقيبة البروكر الشاملة</h2>", unsafe_allow_html=True)
    
    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💳 القسط الشهري")
        tp = st.number_input("السعر الإجمالي", 1000000)
        dp = st.number_input("المقدم", 100000)
        yr = st.slider("السنين", 1, 15, 8)
        st.metric("القسط", f"{(tp-dp)/(yr*12):,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)
    with t_c2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💰 عمولة الصفقة")
        deal = st.number_input("قيمة البيع", 1000000)
        pct = st.slider("النسبة %", 0.5, 5.0, 1.5)
        st.metric("عمولتك", f"{deal*(pct/100):,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)
    with t_c3:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📐 تحويل المساحة")
        m2 = st.number_input("بالمتر المربع", 100.0)
        st.write(f"القدم المربع: {m2 * 10.76:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)

    t_c4, t_c5 = st.columns(2)
    with t_c4:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📈 العائد الاستثماري ROI")
        buy = st.number_input("سعر الشراء", 1000000)
        rent = st.number_input("الإيجار الشهري", 10000)
        st.metric("العائد السنوي", f"{(rent*12/buy)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with t_c5:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📝 رسوم التسجيل")
        val = st.number_input("قيمة العقد", 1000000)
        st.write(f"ضريبة تصرفات (2.5%): {val*0.025:,.0f} ج.م")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المطورين":
    search_dev = st.text_input("🔍 ابحث عن مطور...")
    f_devs = df_d[df_d['Developer'].str.contains(search_dev, case=False)] if search_dev else df_d
    for i, row in f_devs.head(10).iterrows():
        if st.button(f"🏗️ {row['Developer']} | المالك: {row.get('Owner','---')}", key=f"card_d_{i}"):
            st.session_state.selected_item = row; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
