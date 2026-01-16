import streamlit as st
import pandas as pd
import feedparser
import time
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'r_idx' not in st.session_state: st.session_state.r_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار
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
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .luxury-header {
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 10px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 10px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 22px; }
    
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important; border: 1px solid #eee !important;
        border-radius: 12px !important; width: 100% !important; min-height: 200px !important;
        padding: 15px !important; transition: 0.3s !important; text-align: right !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; white-space: pre-wrap !important;
    }
    
    div.stButton > button[key="logout_top"] {
        background-color: #dc2626 !important; color: white !important; border-radius: 8px !important;
        padding: 5px 15px !important; font-size: 14px !important;
    }
    
    div.stButton > button[key="refresh_btn"] {
        background-color: #10b981 !important; color: white !important; border-radius: 8px !important;
        margin-top: 28px !important; width: 100% !important;
    }

    .sidebar-box { background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 10px; border-top: 3px solid #10b981; }
    .ready-card { background: #161616; border-right: 3px solid #10b981; padding: 8px; border-radius: 5px; margin-bottom: 5px; font-size: 13px; color: #eee; }
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    .info-label { color: #f59e0b; font-weight: bold; margin-left: 5px; }
    .detail-card { background:#111; padding:25px; border-radius:15px; border-right:5px solid #f59e0b; color:white; line-height:1.8; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# الهيدر وزر الخروج
h_col1, h_col2 = st.columns([0.85, 0.15])
with h_col1:
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)
with h_col2:
    if st.button("🚪 خروج", key="logout_top"):
        st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 6. جلب البيانات (تحديث تلقائي كل 200 ثانية + كسر التخزين المؤقت)
@st.cache_data(ttl=200)
def load_all_data(timestamp):
    # إضافة الوقت للرابط لضمان عدم سحب نسخة قديمة من جوجل
    u_p = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv&t={timestamp}"
    u_d = f"https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv&t={timestamp}"
    try:
        p = pd.read_csv(u_p).fillna("جاري تحديث البيانات...").astype(str)
        d = pd.read_csv(u_d).fillna("جاري تحديث البيانات...").astype(str)
        
        # تنظيف شامل لكل أنواع الـ None المحتملة
        def clean(val):
            v = str(val).strip()
            if v.lower() in ["none", "nan", "", "null", "undefined"]:
                return "جاري تحديث البيانات..."
            return v
            
        p = p.applymap(clean)
        d = d.applymap(clean)
        return p, d
    except Exception as e:
        return pd.DataFrame(), pd.DataFrame()

# نستخدم الوقت الحالي كمفتاح للتحديث
df_p, df_d = load_all_data(int(time.time() / 200))

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

main_col, side_col = st.columns([0.75, 0.25])

# --- القائمة الجانبية (6 عناصر استلام فوري) ---
with side_col:
    st.markdown("<p style='color:#10b981; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    if not df_p.empty:
        ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        r_limit = 6
        curr_ready = ready_df.iloc[st.session_state.r_idx*r_limit : (st.session_state.r_idx+1)*r_limit]
        st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
        for _, row in curr_ready.iterrows():
            st.markdown(f'<div class="ready-card"><b>{row.get("Project Name")}</b><br><small>📍 {row.get("Area")}</small></div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        rc1, rc2 = st.columns(2)
        if st.session_state.r_idx > 0 and rc1.button("السابق", key="r_prev"): st.session_state.r_idx -= 1; st.rerun()
        if (st.session_state.r_idx + 1) * r_limit < len(ready_df) and rc2.button("التالي", key="r_next"): st.session_state.r_idx += 1; st.rerun()

# --- الجزء الرئيسي ---
with main_col:
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        
        st.markdown('<div class="detail-card">', unsafe_allow_html=True)
        if 'Project Name' in item:
            st.markdown(f"<h2>🏢 {item.get('Project Name')}</h2><hr style='opacity:0.2;'>")
            st.markdown(f"<p><span class='info-label'>📍 المنطقة:</span> {item.get('Area')}</p>")
            st.markdown(f"<p><span class='info-label'>🏗️ المطور:</span> {item.get('Developer')}</p>")
            st.markdown(f"<p><span class='info-label'>📐 المساحة:</span> {item.get('Project Area')}</p>")
            st.markdown(f"<div style='background:#1a1a1a; padding:15px; border-radius:10px; margin-top:15px;'>")
            st.markdown(f"<h4>✨ تفاصيل المشروع:</h4><p>{item.get('Project Features')}</p></div>")
        else:
            st.markdown(f"<h2>🏗️ {item.get('Developer')}</h2><hr style='opacity:0.2;'>")
            st.markdown(f"<p><span class='info-label'>👤 المالك:</span> {item.get('Owner')}</p>")
            st.markdown(f"<p><span class='info-label'>📍 المقر:</span> {item.get('Headquarters Address')}</p>")
            st.markdown(f"<div style='background:#1a1a1a; padding:15px; border-radius:10px; margin-top:15px;'>")
            st.markdown(f"<h4>📖 معلومات تفصيلية:</h4><p>{item.get('Detailed_Info')}</p></div>")
            st.markdown(f"<p style='margin-top:15px;'><span class='info-label'>📚 سابقة الأعمال:</span> {item.get('Previous Projects')}</p>")
        st.markdown('</div>', unsafe_allow_html=True)

    elif menu == "المشاريع":
        f1, f2, f3, f4 = st.columns([1, 1, 1, 0.4])
        s_area = f1.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Area'].unique().tolist()))
        s_dev = f2.selectbox("🏗️ المطور", ["الكل"] + sorted(df_p['Developer'].unique().tolist()))
        s_search = f3.text_input("🔍 اسم المشروع")
        if f4.button("🔄", key="refresh_btn"):
            st.cache_data.clear()
            st.rerun()

        dff_p = df_p.copy()
        if s_area != "الكل": dff_p = dff_p[dff_p['Area'] == s_area]
        if s_dev != "الكل": dff_p = dff_p[dff_p['Developer'] == s_dev]
        if s_search: dff_p = dff_p[dff_p['Project Name'].str.contains(s_search, case=False)]

        p_limit = 6
        curr_p = dff_p.iloc[st.session_state.p_idx*p_limit : (st.session_state.p_idx+1)*p_limit]
        for i in range(0, len(curr_p), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_p):
                    row = curr_p.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n📐 {row.get('Project Area')}"
                        if st.button(lbl, key=f"card_p_{i+j}"): st.session_state.selected_item = row; st.rerun()
        
        st.markdown("---")
        pc1, pc2 = st.columns(2)
        if st.session_state.p_idx > 0 and pc1.button("⬅️ السابق", key="p_prev"): st.session_state.p_idx -= 1; st.rerun()
        if (st.session_state.p_idx + 1) * p_limit < len(dff_p) and pc2.button("التالي ➡️", key="p_next"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        s_d = st.text_input("🔍 ابحث عن مطور...")
        dff_d = df_d.copy()
        if s_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(s_d, case=False).any(), axis=1)]
        
        d_limit = 6
        curr_d = dff_d.iloc[st.session_state.d_idx*d_limit : (st.session_state.d_idx+1)*d_limit]
        for i in range(0, len(curr_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_d):
                    row = curr_d.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏗️ {row.get('Developer')}\n👑 المالك: {row.get('Owner')}\n⭐ فئة {row.get('Developer Category')}\n🏢 مشاريع: {row.get('Number of Projects')}"
                        if st.button(lbl, key=f"card_d_{i+j}"): st.session_state.selected_item = row; st.rerun()
        
        st.markdown("---")
        dc1, dc2 = st.columns(2)
        if st.session_state.d_idx > 0 and dc1.button("⬅️ السابق", key="d_prev"): st.session_state.d_idx -= 1; st.rerun()
        if (st.session_state.d_idx + 1) * d_limit < len(dff_d) and dc2.button("التالي ➡️", key="d_next"): st.session_state.d_idx += 1; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات PRO</h2>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📐 محول المساحات"])
        with t1:
            c1, c2 = st.columns(2)
            total = c1.number_input("إجمالي السعر", value=2000000)
            down = c2.number_input("المقدم", value=200000)
            years = st.slider("سنين التقسيط", 1, 15, 7)
            rem = total - down
            st.metric("المبلغ المتبقي", f"{rem:,.0f} ج.م")
            st.metric("القسط الشهري", f"{rem/(years*12):,.0f} ج.م")
        with t2:
            sqm = st.number_input("المساحة بالمتر المربع", value=100.0)
            st.info(f"القدم المربع: {sqm * 10.76:,.2f}")
            st.info(f"الفدان: {sqm / 4200:,.4f}")
