import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. جلب الوقت بتوقيت مصر
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 4. التنسيق الجمالي (CSS) - النسخة الموحدة
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 2px solid #f59e0b; margin-bottom: 10px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #aaa; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; width: 100% !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 120px !important; text-align: right !important;
        font-weight: bold !important; border: none !important; margin-bottom: 10px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 10px solid #f59e0b !important; box-shadow: 0 10px 20px rgba(245,158,11,0.2) !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 8px solid #f59e0b; color: white; margin-bottom: 20px; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; height: 100%; border-top: 4px solid #f59e0b; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى لعام 2026."

news_text = get_real_news()

# 6. الهيدر البصري
st.markdown("""
    <div style="height: 160px; background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1500&q=80'); background-size: cover; background-position: center; border-radius: 0 0 30px 30px; display: flex; align-items: center; justify-content: center; flex-direction: column;">
        <h1 style="color: #f59e0b; font-size: 40px; margin: 0; font-weight:900;">MA3LOMATI PRO</h1>
        <p style="color: white; font-size: 16px;">المساعد العقاري الذكي والبيانات اللحظية لسوق مصر</p>
    </div>
""", unsafe_allow_html=True)

# 7. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        # توحيد الأسماء
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Available Units (Types)': 'UnitType', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 8. شريط المعلومات
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
c_inf1, c_inf2, c_inf3 = st.columns(3)
c_inf1.write(f"🕒 توقيت القاهرة: {egypt_now.strftime('%I:%M %p')}")
c_inf2.write(f"📅 التاريخ: {egypt_now.strftime('%Y-%m-%d')}")
if c_inf3.button("🚪 تسجيل الخروج"): st.session_state.auth = False; st.rerun()

# 9. المنيو
menu = option_menu(None, ["المساعد الذكي", "دليل المشاريع", "كبار المطورين", "حقيبة الأدوات"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 10. تفاصيل المشروع (عند الضغط)
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', 'التفاصيل')}</h2><p>📍 {item.get('Location', '---')}</p><p>🏗️ {item.get('Developer', '---')}</p><p>💰 السعر: {item.get('Starting Price (EGP)', '---')}</p></div>", unsafe_allow_html=True)

# --- 11. المساعد الذكي (100% من المساحة) ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري الذكي")
    c1, c2, c3 = st.columns(3)
    with c1: f_loc = st.selectbox("المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    with c2: f_type = st.selectbox("نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري", "إداري"])
    with c3: f_bud = st.number_input("المقدم المتاح (EGP)", 0)
    
    c_wa = st.text_input("رقم واتساب العميل (بدون أصفار)")
    
    if st.button("🚀 عرض الترشيحات"):
        res = df_p.copy()
        if f_loc != "الكل": res = res[res['Location'] == f_loc]
        for idx, r in res.head(5).iterrows():
            with st.container(border=True):
                col_txt, col_btn = st.columns([0.8, 0.2])
                col_txt.write(f"🏢 **{r['ProjectName']}** | {r['Location']} | {r['Developer']}")
                msg = f"أرشح لك مشروع {r['ProjectName']} في {r['Location']}."
                link = f"https://wa.me/{c_wa}?text={urllib.parse.quote(msg)}"
                col_btn.markdown(f"[📲 واتساب]({link})")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 12. دليل المشاريع (30% استلام فوري) ---
elif menu == "دليل المشاريع":
    col_main, col_ready = st.columns([0.7, 0.3])
    with col_ready:
        st.markdown("<div class='smart-box' style='border-right-color:#10b981;'><h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(8)
        for i, r in ready.iterrows():
            # حل مشكلة Duplicate Key بإضافة الرقم التسلسلي i
            if st.button(f"✅ {r['ProjectName']}", key=f"ready_btn_{i}"):
                st.session_state.selected_item = r; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    with col_main:
        search = st.text_input("🔍 ابحث عن مشروع...")
        filt = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        for i, r in filt.head(6).iterrows():
            if st.button(f"🏢 {r['ProjectName']} | {r['Location']} | {r['Developer']}", key=f"card_p_{i}"):
                st.session_state.selected_item = r; st.rerun()

# --- 13. كبار المطورين (30% توب 10) ---
elif menu == "كبار المطورين":
    col_d, col_top = st.columns([0.7, 0.3])
    with col_top:
        st.markdown("<div class='smart-box'><h4 style='color:#f59e0b; text-align:center;'>🏆 أفضل 10 مطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(10).iterrows():
            st.write(f"{i+1}. {r['Developer']}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_d:
        for i, r in df_d.iterrows():
            if st.button(f"🏗️ {r['Developer']} | المالك: {r.get('Owner','---')}", key=f"card_d_{i}"):
                st.session_state.selected_item = r; st.rerun()

# --- 14. حقيبة الأدوات (6 أدوات احترافية) ---
elif menu == "حقيبة الأدوات":
    st.title("🛠️ حقيبة البروكر الاحترافية")
    r1_1, r1_2, r1_3 = st.columns(3)
    r2_1, r2_2, r2_3 = st.columns(3)
    
    with r1_1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💳 الأقساط")
        p = st.number_input("السعر", 1000000)
        d = st.number_input("المقدم", 100000)
        y = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r1_2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💰 العمولة")
        v = st.number_input("الصفقة", 1000000)
        pct = st.slider("النسبة %", 0.5, 5.0, 1.5)
        st.metric("صافي الربح", f"{v*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r1_3:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📈 ROI")
        b = st.number_input("الشراء", 1000000, key="roi")
        r = st.number_input("الإيجار سنوي", 100000)
        st.metric("العائد", f"{(r/b)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2_1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📏 المساحة")
        m2 = st.number_input("متر", 100.0)
        st.write(f"قدم مربع: {m2 * 10.76:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2_2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📝 الضرائب")
        t_v = st.number_input("قيمة العقار", 1000000, key="tax")
        st.write(f"تصرفات (2.5%): {t_v*0.025:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with r2_3:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("🏦 تمويل عقاري")
        loan = st.number_input("القرض", 500000)
        st.write(f"فائدة تقديرية: {loan*0.20:,.0f}/سنوياً")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
