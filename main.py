import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الوقت بتوقيت مصر
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 4. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى لعام 2026."

news_text = get_real_news()

# 5. التنسيق الجمالي (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 2px solid #f59e0b; margin-bottom: 10px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #aaa; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* ستايل الكروت */
    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; width: 100% !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; border: none !important; margin-bottom: 15px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 10px solid #f59e0b !important; box-shadow: 0 10px 20px rgba(245,158,11,0.2) !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; margin-bottom: 15px; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; height: 100%; border-top: 4px solid #f59e0b; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# 6. الهيدر البصري (صورة احترافية)
st.markdown("""
    <div style="position: relative; height: 200px; border-radius: 0 0 30px 30px; overflow: hidden; margin-bottom: 20px;">
        <img src="https://images.unsplash.com/photo-1582407947304-fd86f028f716?ixlib=rb-4.0.3&auto=format&fit=crop&w=1500&q=80" style="width: 100%; height: 100%; object-fit: cover; opacity: 0.5;">
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center; width: 100%;">
            <h1 style="color: #f59e0b; font-weight: 900; font-size: 50px; text-shadow: 2px 2px 10px rgba(0,0,0,0.8);">MA3LOMATI PRO</h1>
            <p style="color: white; font-size: 18px;">المساعد العقاري الذكي والبيانات اللحظية لسوق مصر</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# 7. نظام الدخول
if not st.session_state.auth:
    _, c2, _ = st.columns([1,1,1])
    with c2:
        st.markdown("<h3 style='text-align:center; color:white;'>برجاء إدخال كود الوصول</h3>", unsafe_allow_html=True)
        if st.text_input("كود الدخول", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 8. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        if 'Area' in p.columns and 'Location' not in p.columns: p.rename(columns={'Area': 'Location'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 9. شريط المعلومات العلوي
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
inf1, inf2, inf3 = st.columns(3)
inf1.markdown(f"<p style='color:#aaa;'>🕒 توقيت القاهرة: {egypt_now.strftime('%I:%M %p')}</p>", unsafe_allow_html=True)
inf2.markdown(f"<p style='text-align:center; color:#aaa;'>📅 التاريخ: {egypt_now.strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
if inf3.button("🚪 خروج آمن"): st.session_state.auth = False; st.rerun()

# 10. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "دليل المشاريع", "كبار المطورين", "حقيبة الأدوات"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 11. تفاصيل الوحدة (Pop-up style)
if st.session_state.selected_item is not None:
    if st.button("⬅️ العودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2 style='color:#f59e0b;'>{item.get('Project Name', 'تفاصيل')}</h2>
        <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
            <div><p>📍 الموقع: {item.get('Location', '---')}</p><p>🏗️ المطور: {item.get('Developer', '---')}</p></div>
            <div><p>💰 السعر: {item.get('Starting Price (EGP)', '---')}</p><p>💳 السداد: {item.get('Payment Plan', '---')}</p></div>
        </div>
    </div>""", unsafe_allow_html=True)

# ---------------------------------------------------------
# المساعد الذكي (100% المساحة)
# ---------------------------------------------------------
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري الذكي")
    st.write("أدخل متطلبات عميلك وسأقوم بتحليل البيانات لإعطائك أفضل ترشيح.")
    
    c1, c2, c3, c4 = st.columns(4)
    with c1: f_loc = st.selectbox("المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    with c2: f_type = st.selectbox("النوع", ["الكل", "شقق", "فيلات", "تجاري", "إداري"])
    with c3: f_bud = st.number_input("المقدم المتاح (EGP)", 0)
    with c4: f_pay = st.selectbox("سنوات القسط", ["الكل", "5 سنوات", "7 سنوات", "8 سنوات", "10 سنوات"])
    
    client_phone = st.text_input("رقم واتساب العميل (لإرسال المقترح فوراً)")
    
    if st.button("🚀 تحليل واقتراح"):
        res = df_p.copy()
        if f_loc != "الكل": res = res[res['Location'] == f_loc]
        if f_type != "الكل": res = res[res['Available Units (Types)'].str.contains(f_type, case=False)]
        
        st.subheader("💡 الترشيحات الذكية")
        if res.empty: st.warning("لا يوجد تطابق دقيق حالياً.")
        else:
            for _, r in res.head(3).iterrows():
                with st.container(border=True):
                    col_info, col_btn = st.columns([0.8, 0.2])
                    col_info.write(f"**{r['Project Name']}** | المطور: {r['Developer']} | السعر: {r['Starting Price (EGP)']}")
                    msg = f"تحية طيبة.. أرشح لك مشروع {r['Project Name']} في {r['Location']} كأفضل خيار لميزانيتك."
                    link = f"https://wa.me/{client_phone}?text={urllib.parse.quote(msg)}"
                    col_btn.markdown(f"[📲 إرسال المقترح]({link})")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------
# دليل المشاريع (مع الاستلام الفوري)
# ---------------------------------------------------------
elif menu == "دليل المشاريع":
    col_main, col_side = st.columns([0.7, 0.3])
    
    with col_side:
        st.markdown("<div class='smart-box' style='border-right-color:#10b981;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 فرص الاستلام الفوري</h4>", unsafe_allow_html=True)
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(8)
        for _, row in ready.iterrows():
            if st.button(f"🏠 {row['Project Name']}", key=f"ready_{row['Project Name']}"):
                st.session_state.selected_item = row; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        search = st.text_input("🔍 ابحث عن اسم المشروع...")
        dff = df_p[df_p['Project Name'].str.contains(search, case=False)] if search else df_p
        
        start = st.session_state.p_idx * 4
        page = dff.iloc[start:start+4]
        for i, r in page.iterrows():
            if st.button(f"🏢 {r['Project Name']} | 📍 {r['Location']} | 🏗️ {r['Developer']}", key=f"card_p_{i}"):
                st.session_state.selected_item = r; st.rerun()
        
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0 and p1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
        if start + 4 < len(dff) and p2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

# ---------------------------------------------------------
# كبار المطورين
# ---------------------------------------------------------
elif menu == "كبار المطورين":
    col_dev, col_top = st.columns([0.7, 0.3])
    
    with col_top:
        st.markdown("<div class='smart-box' style='border-right-color:#f59e0b;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 أفضل 10 مطورين</h4>", unsafe_allow_html=True)
        # عرض أول 10 مطورين كقائمة سريعة
        for i, row in df_d.head(10).iterrows():
            st.markdown(f"<p style='font-size:14px;'>{i+1}- {row['Developer']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_dev:
        st.title("🏗️ دليل المطورين الشامل")
        for i, r in df_d.head(20).iterrows():
            if st.button(f"🏗️ {r['Developer']} | المالك: {r.get('Owner', '---')}", key=f"card_d_{i}"):
                st.session_state.selected_item = r; st.rerun()

# ---------------------------------------------------------
# حقيبة الأدوات (6 أدوات احترافية)
# ---------------------------------------------------------
elif menu == "حقيبة الأدوات":
    st.title("🛠️ حقيبة الأدوات الاحترافية للبروكر")
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    
    with r1_c1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💳 حاسبة الأقساط")
        price = st.number_input("إجمالي السعر", 1000000)
        down = st.number_input("المقدم", 100000)
        years = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{(price-down)/(years*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    with r1_c2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💰 حاسبة العمولات")
        deal = st.number_input("قيمة الصفقة", 1000000, key="deal")
        comm = st.slider("النسبة %", 0.5, 5.0, 1.5)
        st.metric("صافي عمولتك", f"{deal*(comm/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)

    with r1_c3:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📈 حاسبة ROI")
        buy_p = st.number_input("سعر الشراء", 1000000, key="roi_buy")
        rent = st.number_input("الإيجار السنوي المتوقع", 100000)
        st.metric("العائد الاستثماري السنوي", f"{(rent/buy_p)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_c1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📏 محول المساحات")
        m2 = st.number_input("بالمتر المربع", 100.0)
        st.write(f"القدم المربع: **{m2 * 10.76:,.2f}**")
        st.write(f"الفدان: **{m2 / 4200:,.4f}**")
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_c2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📝 رسوم التسجيل")
        prop_v = st.number_input("قيمة العقار", 1000000, key="reg")
        st.write(f"ضريبة التصرفات (2.5%): **{prop_v*0.025:,.0f}**")
        st.write(f"رسوم الشهر العقاري تقريباً: **5,000 ج.م**")
        st.markdown("</div>", unsafe_allow_html=True)

    with r2_c3:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("🏦 التمويل العقاري")
        loan = st.number_input("مبلغ القرض", 500000)
        interest = st.slider("الفائدة السنوية %", 1.0, 25.0, 10.0)
        # حاسبة بسيطة للفائدة
        total_pay = loan + (loan * (interest/100) * 10)
        st.write(f"الإجمالي بعد 10 سنوات: **{total_pay:,.0f}**")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
