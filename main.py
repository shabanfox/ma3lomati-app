import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار (RSS)
@st.cache_data(ttl=600)
def get_real_news():
    try:
        rss_url = "https://www.skynewsarabia.com/rss/v1/business.xml" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:20]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار..."
    except:
        return "سوق العقارات المصري يشهد طفرة إنشائية كبيرة • استقرار أسعار الصرف • العاصمة الإدارية الوجهة الاستثمارية الأولى."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS الكامل)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* الهيدر */
    .luxury-header {{
        background: rgba(15, 15, 15, 0.95); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 10px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 10px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; }}

    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #000; padding: 12px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #f59e0b; margin-bottom: 15px; }}
    .ticker {{ display: inline-block; padding-right: 100%; animation: ticker 60s linear infinite; color: #f59e0b; font-size: 18px; font-weight: 700; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* ستايل الكروت الكبير (نوي) */
    div.stButton > button[key*="card_"] {{
        background-color: white !important;
        color: #111 !important;
        border: 1px solid #eee !important;
        border-radius: 15px !important;
        width: 100% !important;
        min-height: 280px !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: flex-start !important;
        padding: 20px !important;
        transition: 0.3s !important;
        text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        white-space: pre-wrap !important;
    }}
    div.stButton > button[key*="card_"]:hover {{
        border-right: 8px solid #f59e0b !important;
        transform: translateY(-5px) !important;
    }}

    /* زر الخروج */
    div.stButton > button[key="logout_top"] {{
        background-color: #ef4444 !important; color: white !important;
        height: 35px !important; border: none !important; border-radius: 8px !important;
    }}
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

# 6. الهيدر وزر الخروج
header_main, header_btn = st.columns([0.88, 0.12])
with st.container():
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI <span style="color:white; font-size:14px;">PRO</span></div><div></div></div>', unsafe_allow_html=True)
    with header_btn:
        st.markdown("<div style='margin-top:-60px; text-align:left;'>", unsafe_allow_html=True)
        if st.button("🚪 خروج", key="logout_top"):
            st.session_state.auth = False; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# عرض شريط الأخبار
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔴 عاجل: {news_text}</div></div>', unsafe_allow_html=True)

# 7. تحميل البيانات من الروابط الأصلية
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

# 8. القائمة الرئيسية
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

main_col, side_col = st.columns([0.75, 0.25])

# القائمة الجانبية (استلام فوري)
with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    st.markdown("<div style='background:#0d0d0d; border-radius:15px; padding:10px; border-top:3px solid #10b981;'>", unsafe_allow_html=True)
    ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(15)
    for _, row in ready.iterrows():
        st.markdown(f'<div style="background:#161616; padding:8px; border-right:3px solid #10b981; margin-bottom:5px; border-radius:5px;"><div style="color:#f59e0b; font-size:12px; font-weight:bold;">{row.get("Project Name")}</div><div style="color:#666; font-size:10px;">{row.get("Area")}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# الجزء الرئيسي (المحتوى)
with main_col:
    # --- عرض التفاصيل ---
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        st.markdown(f"""
            <div style='background:#111; padding:30px; border-radius:15px; border-right:8px solid #f59e0b; color:white;'>
                <h1 style='color:#f59e0b;'>{item.get('Project Name', item.get('Developer'))}</h1>
                <hr style='opacity:0.2;'>
                <div style='font-size:18px; line-height:1.8;'>
                    {item.get('Project Features', item.get('Detailed_Info', 'لا توجد بيانات إضافية.'))}
                </div>
            </div>
        """, unsafe_allow_html=True)

    # --- صفحة المشاريع ---
    elif menu == "المشاريع":
        # الفلاتر والبحث
        c1, c2, c3 = st.columns([1.5, 1, 1])
        search_p = c1.text_input("🔍 ابحث باسم المشروع أو المطور...")
        area_list = ["الكل"] + sorted(df_p['Area'].unique().tolist())
        filter_area = c2.selectbox("📍 تصفية حسب المنطقة", area_list)
        dev_list = ["الكل"] + sorted(df_p['Developer'].unique().tolist())
        filter_dev = c3.selectbox("🏗️ تصفية حسب المطور", dev_list)

        dff = df_p.copy()
        if search_p: dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search_p, case=False).any(), axis=1)]
        if filter_area != "الكل": dff = dff[dff['Area'] == filter_area]
        if filter_dev != "الكل": dff = dff[dff['Developer'] == filter_dev]

        limit = 6
        items = dff.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        
        for i in range(0, len(items), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(items):
                    row = items.iloc[i+j]
                    with cols[j]:
                        label = f"🏢 {row.get('Project Name')}\n📍 الموقع: {row.get('Area')}\n━━━━━━━━━━━━\n🏗️ المطور: {row.get('Developer')}\n📐 المساحة: {row.get('Project Area')}"
                        if st.button(label, key=f"card_p_{i+j}"): st.session_state.selected_item = row; st.rerun()
        
        st.write("---")
        n1, _, n2 = st.columns([1, 2, 1])
        if n1.button("السابق ⬅️", key="p_p") and st.session_state.p_idx > 0: st.session_state.p_idx -= 1; st.rerun()
        if n2.button("التالي ➡️", key="p_n") and (st.session_state.p_idx+1)*limit < len(dff): st.session_state.p_idx += 1; st.rerun()

    # --- صفحة المطورين ---
    elif menu == "المطورين":
        search_d = st.text_input("🔍 ابحث عن اسم المطور...")
        dff_d = df_d.copy()
        if search_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]

        limit_d = 6
        items_d = dff_d.iloc[st.session_state.d_idx*limit_d : (st.session_state.d_idx+1)*limit_d]

        for i in range(0, len(items_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(items_d):
                    row = items_d.iloc[i+j]
                    with cols[j]:
                        label = f"🏗️ {row.get('Developer')}\n⭐ فئة المطور: {row.get('Developer Category')}\n━━━━━━━━━━━━\n👤 المالك/الإدارة: {row.get('Owner')}\n🏢 عدد المشاريع: {row.get('Number of Projects')}"
                        if st.button(label, key=f"card_d_{i+j}"): st.session_state.selected_item = row; st.rerun()

        st.write("---")
        nd1, _, nd2 = st.columns([1, 2, 1])
        if nd1.button("السابق ⬅️", key="d_p") and st.session_state.d_idx > 0: st.session_state.d_idx -= 1; st.rerun()
        if nd2.button("التالي ➡️", key="d_n") and (st.session_state.d_idx+1)*limit_d < len(dff_d): st.session_state.d_idx += 1; st.rerun()

    # --- صفحة الأدوات (محسنة بالكامل) ---
    elif menu == "الأدوات":
        st.markdown("<h3 style='color:#f59e0b;'>🛠️ الأدوات والآلات الحاسبة</h3>", unsafe_allow_html=True)
        t1, t2 = st.tabs(["🧮 حاسبة القسط الاحترافية", "📐 محول المساحات"])
        
        with t1:
            cc1, cc2 = st.columns(2)
            total_price = cc1.number_input("إجمالي السعر (ج.م)", min_value=0, value=5000000, step=100000)
            down_payment_pct = cc2.slider("نسبة المقدم (%)", 0, 50, 10)
            
            cc3, cc4 = st.columns(2)
            years = cc3.number_input("سنوات التقسيط", 1, 20, 8)
            interest = cc4.number_input("الفائدة السنوية % (إن وجد)", 0.0, 30.0, 0.0)
            
            down_val = total_price * (down_payment_pct / 100)
            remaining = total_price - down_val
            
            # حساب القسط (مع فائدة بسيطة)
            total_with_int = remaining * (1 + (interest/100 * years))
            monthly = total_with_int / (years * 12)
            
            st.markdown(f"""
            <div style='background:#111; padding:20px; border-radius:10px; border:1px solid #f59e0b;'>
                <h4 style='color:#f59e0b; margin-top:0;'>النتائج:</h4>
                <p>💵 قيمة المقدم: <b>{down_val:,.0f} ج.م</b></p>
                <p>📅 القسط الشهري: <b style='font-size:24px; color:#10b981;'>{monthly:,.0f} ج.م</b></p>
                <p>💰 المبلغ المتبقي: <b>{remaining:,.0f} ج.م</b></p>
            </div>
            """, unsafe_allow_html=True)

        with t2:
            st.info("قم بالتحويل السريع بين وحدات القياس")
            m2 = st.number_input("المساحة بالمتر المربع (M²)", value=100.0)
            st.write(f"📐 بالقدم المربع: **{m2 * 10.764:,.2f} ft²**")
            st.write(f"🚜 بالفدان: **{m2 / 4200:,.4f} فدان**")
