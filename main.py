import streamlit as st
import pandas as pd
import feedparser
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

# 4. التنسيق الجمالي المحسن
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
    
    /* أزرار الكروت البيضاء */
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important; border: 1px solid #eee !important;
        border-radius: 12px !important; width: 100% !important; min-height: 200px !important;
        padding: 15px !important; transition: 0.3s !important; text-align: right !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important; white-space: pre-wrap !important;
    }
    div.stButton > button[key*="card_"]:hover { border-color: #f59e0b !important; transform: translateY(-3px) !important; }
    
    /* زر الخروج العلوي */
    div.stButton > button[key="logout_top"] {
        background-color: #dc2626 !important; color: white !important; border-radius: 8px !important;
        padding: 5px 15px !important; font-size: 14px !important;
    }

    .sidebar-box { background: #0d0d0d; border: 1px solid #222; border-radius: 15px; padding: 10px; border-top: 3px solid #10b981; }
    .ready-card { background: #161616; border-right: 3px solid #10b981; padding: 8px; border-radius: 5px; margin-bottom: 5px; font-size: 13px; color: #eee; }
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

# --- الهيدر العلوي مع زر الخروج ---
h_col1, h_col2 = st.columns([0.8, 0.2])
with h_col1:
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)
with h_col2:
    st.write("") # موازنة
    if st.button("🚪 خروج", key="logout_top"):
        st.session_state.auth = False; st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# القائمة الرئيسية
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

# تحميل البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

main_col, side_col = st.columns([0.75, 0.25])

# --- القائمة الجانبية (استلام فوري) ---
with side_col:
    st.markdown("<p style='color:#10b981; font-weight:bold; margin-bottom:5px;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    r_limit = 6
    curr_ready = ready_df.iloc[st.session_state.r_idx*r_limit : (st.session_state.r_idx+1)*r_limit]
    
    st.markdown("<div class='sidebar-box'>", unsafe_allow_html=True)
    for _, row in curr_ready.iterrows():
        st.markdown(f'<div class="ready-card"><b>{row.get("Project Name")}</b><br><small>📍 {row.get("Area")}</small></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    c_r1, c_r2 = st.columns(2)
    if st.session_state.r_idx > 0:
        if c_r1.button("السابق", key="r_prev"): st.session_state.r_idx -= 1; st.rerun()
    if (st.session_state.r_idx + 1) * r_limit < len(ready_df):
        if c_r2.button("التالي", key="r_next"): st.session_state.r_idx += 1; st.rerun()

# --- المحتوى الرئيسي ---
with main_col:
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        st.markdown(f'<div style="background:#111; padding:25px; border-radius:15px; border-right:5px solid #f59e0b; color:white;"><h2>{item.get("Project Name", item.get("Developer"))}</h2><hr opacity="0.1"><p style="line-height:1.8;">{item.get("Project Features", item.get("Detailed_Info", "لا يوجد بيانات"))}</p></div>', unsafe_allow_html=True)

    elif menu == "المشاريع":
        # الفلاتر
        f1, f2, f3 = st.columns([1,1,1.5])
        with f1: area_list = ["الكل"] + sorted(df_p['Area'].unique().tolist())
        s_area = f1.selectbox("📍 تصفية بالمنطقة", area_list)
        with f2: dev_list = ["الكل"] + sorted(df_p['Developer'].unique().tolist())
        s_dev = f2.selectbox("🏗️ تصفية بالمطور", dev_list)
        with f3: s_search = st.text_input("🔍 ابحث بالاسم...")

        dff_p = df_p.copy()
        if s_area != "الكل": dff_p = dff_p[dff_p['Area'] == s_area]
        if s_dev != "الكل": dff_p = dff_p[dff_p['Developer'] == s_dev]
        if s_search: dff_p = dff_p[dff_p['Project Name'].str.contains(s_search, case=False)]

        limit = 6
        curr_p = dff_p.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        for i in range(0, len(curr_p), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(curr_p):
                    row = curr_p.iloc[i+j]
                    with cols[j]:
                        lbl = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n📐 {row.get('Project Area')}"
                        if st.button(lbl, key=f"card_p_{i+j}"): st.session_state.selected_item = row; st.rerun()
        
        # أزرار التنقل
        st.markdown("---")
        pc1, pc2 = st.columns(2)
        if st.session_state.p_idx > 0:
            if pc1.button("⬅️ السابق", key="p_prev"): st.session_state.p_idx -= 1; st.rerun()
        if (st.session_state.p_idx + 1) * limit < len(dff_p):
            if pc2.button("التالي ➡️", key="p_next"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        s_d = st.text_input("🔍 ابحث عن مطور عقاري، مالك، أو عنوان...")
        dff_d = df_d.copy()
        if s_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(s_d, case=False).any(), axis=1)]

        limit = 6
        curr_d = dff_d.iloc[st.session_state.d_idx*limit : (st.session_state.d_idx+1)*limit]
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
        if st.session_state.d_idx > 0:
            if dc1.button("⬅️ السابق", key="d_prev"): st.session_state.d_idx -= 1; st.rerun()
        if (st.session_state.d_idx + 1) * limit < len(dff_d):
            if dc2.button("التالي ➡️", key="d_next"): st.session_state.d_idx += 1; st.rerun()

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات العقارية PRO</h2>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📐 محول المساحات"])
        
        with t1:
            col_a, col_b = st.columns(2)
            price = col_a.number_input("سعر الوحدة الإجمالي (ج.م)", value=5000000, step=100000)
            down = col_b.number_input("المقدم المدفوع (ج.م)", value=500000, step=50000)
            years = st.slider("فترة التقسيط (سنوات)", 1, 15, 8)
            
            remaining = price - down
            monthly = remaining / (years * 12)
            quarterly = remaining / (years * 4)
            
            st.success(f"المبلغ المتبقي للتقسيط: {remaining:,.2f} ج.م")
            st.metric("القسط الشهري", f"{monthly:,.0f} ج.م")
            st.metric("القسط الربع سنوي", f"{quarterly:,.0f} ج.م")
            
        with t2:
            st.info("قم بإدخال المساحة بالمتر المربع للتحويل")
            sqm = st.number_input("المساحة بالمتر المربع (m²)", value=100.0)
            c1, c2, c3 = st.columns(3)
            c1.metric("بالقدم المربع", f"{sqm * 10.76:,.2f}")
            c2.metric("بالفدان", f"{sqm / 4200:,.4f}")
            c3.metric("بالقيراط", f"{sqm / 175:,.2f}")
