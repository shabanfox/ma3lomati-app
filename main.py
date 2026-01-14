import streamlit as st
import pandas as pd
import math
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297"
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار..."
    except: return "سوق العقارات المصري: متابعة مستمرة."

news_text = get_real_news()

# 4. التنسيق الجمالي المطور
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 40px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 10px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; }}
    .ticker-wrap {{ width: 100%; background: #111; padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #ccc; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .grid-card {{ background: #111; border: 1px solid #222; border-right: 5px solid #f59e0b; border-radius: 12px; padding: 15px; margin-bottom: 15px; }}
    .ready-sidebar {{ background: #0f0f0f; border: 1px solid #222; border-radius: 15px; padding: 15px; height: 80vh; overflow-y: auto; border-top: 4px solid #10b981; }}
    .ready-item {{ background: #161616; border-right: 4px solid #10b981; padding: 10px; border-radius: 8px; margin-bottom: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 5. تسجيل الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; padding-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات (معالجة ذكية للأعمدة لضمان عدم حدوث KeyError)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        # تنظيف أسماء الأعمدة من المسافات المخفية
        p.columns = [c.strip() for c in p.columns]
        d.columns = [c.strip() for c in d.columns]
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# الهيدر وشريط الأخبار
now = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#f59e0b;">⌚ {now}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

col_main, col_side = st.columns([0.7, 0.3])

# --- الجانب الأيمن (30%): استلام فوري ---
with col_side:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري فقط</h4>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    
    # البحث عن كلمة "فوري" أو "جاهز" في أي عمود لضمان المرونة
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    
    for _, row in ready_df.iterrows():
        # استخدام .get لضمان عدم حدوث KeyError لو الاسم اتغير في الشيت
        p_name = row.get('Project Name', row.get('اسم المشروع', 'مشروع غير مسمى'))
        p_area = row.get('Area', row.get('المنطقة', 'الموقع غير محدد'))
        p_dev = row.get('Developer', row.get('المطور', 'مطور مجهول'))
        
        st.markdown(f"""
            <div class="ready-item">
                <b style="color:#f59e0b;">{p_name}</b><br>
                <small>📍 {p_area}</small><br>
                <small>🏢 {p_dev}</small>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الأيسر (70%): المحتوى ---
with col_main:
    if menu == "المشاريع":
        search = st.text_input("🔍 بحث في المشاريع...")
        filtered = df_p.copy()
        if search: filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        limit = 6
        page = filtered.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    r = page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <h4 style="color:#f59e0b;">{r.get('Project Name', 'اسم المشروع')}</h4>
                                <p>📍 {r.get('Area', 'المنطقة')} | 📐 {r.get('Project Area', 'المساحة')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔎 كامل المواصفات"):
                            st.write(f"✨ المميزات: {r.get('Project Features', 'لا يوجد')}")
        
        st.write("---")
        c1, c2 = st.columns(2)
        if c1.button("التالي ⬅️"): st.session_state.p_idx += 1; st.rerun()
        if c2.button("➡️ السابق"): st.session_state.p_idx = max(0, st.session_state.p_idx-1); st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات والبحث الذكي</h2>", unsafe_allow_html=True)
        radar = st.text_input("🕵️ رادار البحث (عن أي مشروع خارج الشيت)...")
        if radar:
            st.link_button(f"🔍 ابحث عن {radar} في جوجل", f"https://www.google.com/search?q={urllib.parse.quote(radar + ' عقارات مصر')}")
        
        t1, t2, t3 = st.tabs(["🧮 حاسبة القسط", "📈 ROI", "📐 مساحات"])
        with t1:
            price = st.number_input("السعر", 1000000)
            st.metric("القسط (على 8 سنين بدون مقدم)", f"{price/(8*12):,.0f} ج.م")
        with t2:
            rent = st.number_input("الإيجار", 10000)
            st.metric("العائد السنوي", f"{(rent*12/price)*100:.2f}%")
        with t3:
            m = st.number_input("المتر المربع", 100.0)
            st.write(f"القدم المربع: {m*10.76:,.2f}")

    elif menu == "المطورين":
        for _, r in df_d.iterrows():
            with st.expander(f"🏢 {r.get('Developer', 'شركة تطوير')}"):
                st.write(r.get('Detailed_Info', 'لا توجد بيانات'))

if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()
