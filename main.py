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
    
    .ticker-wrap {{ width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 180px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; transition: 0.3s !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border: 2px solid #f59e0b !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; margin-top: 10px; }}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:60px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر
h_col1, h_col2, h_col3 = st.columns([1.5, 2, 1])
with h_col1: st.markdown('<div class="logo-main">MA3LOMATI PRO</div>', unsafe_allow_html=True)
with h_col2:
    st.markdown(f"<div style='text-align:center; color:white;'><b>مرحباً بك يا بروكر المستقبل 👋</b><br><span style='color:#f59e0b; font-size:12px;'>🕒 {datetime.now().strftime('%I:%M %p')} | {datetime.now().strftime('%Y-%m-%d')}</span></div>", unsafe_allow_html=True)
with h_col3:
    if st.button("🚪 خروج", use_container_width=True): st.session_state.auth = False; st.rerun()

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

# 8. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "people", "tools"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# --- التحكم في عرض الصفحة (Layout Control) ---
if menu == "المساعد الذكي":
    main_container = st.container()
    show_side_panel = False
else:
    col_main, col_side = st.columns([0.78, 0.22])
    main_container = col_main
    show_side_panel = True

# --- عرض القائمة الجانبية (فقط في الصفحات العادية) ---
if show_side_panel:
    with col_side:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        if not df_p.empty:
            ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
            for _, row in ready.iterrows():
                st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:10px; border-radius:10px; margin-bottom:8px; font-size:12px; color:white;">{row["Project Name"]}</div>', unsafe_allow_html=True)

# --- عرض المحتوى الرئيسي ---
with main_container:
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"<div class='smart-box'><h2>{item.get('Project Name', item.get('Developer'))}</h2><hr>{item.get('Project Features', item.get('Detailed_Info', 'لا توجد تفاصيل'))}</div>", unsafe_allow_html=True)

    elif menu == "المساعد الذكي":
        st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🤖 مساعد المبيعات الذكي (عرض كامل)</h2>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#aaa; margin-bottom:30px;'>واجهة مخصصة للتركيز على ميزانية العميل وإرسال البيانات فوراً</p>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        with c1:
            m_down = st.number_input("المقدم المتاح لدى العميل (EGP)", 0)
            m_area = st.selectbox("اختر المنطقة", ["الكل"] + sorted(df_p['Area'].unique().tolist()))
        with c2:
            m_monthly = st.number_input("القسط الشهري المتاح", 0)
            m_type = st.selectbox("تصنيف الوحدة", ["الكل", "سكني", "تجاري", "إداري", "طبي"])
        with c3:
            broker_name = st.text_input("اسمك (المرسل)", "بروكر Ma3lomati")
            client_phone = st.text_input("رقم واتساب العميل (بدون صفر)")

        st.markdown("<hr style='border: 0.1px solid #333;'>", unsafe_allow_html=True)
        
        res_col, msg_col = st.columns([0.65, 0.35])
        
        with res_col:
            st.markdown("#### 🎯 الترشيحات المقترحة")
            filtered_aid = df_p[df_p['Area'] == m_area] if m_area != "الكل" else df_p
            if filtered_aid.empty:
                st.info("قم بتغيير الفلاتر أعلاه لعرض النتائج")
            else:
                for _, r in filtered_aid.head(5).iterrows():
                    with st.expander(f"🏢 {r['Project Name']} | {r['Developer']}"):
                        st.write(f"📍 المنطقة: {r['Area']}")
                        st.write(f"✨ المميزات: {r['Project Features']}")
                        if st.button(f"رؤية التفاصيل: {r['Project Name']}", key=f"btn_{r['Project Name']}"):
                            st.session_state.selected_item = r; st.rerun()

        with msg_col:
            st.markdown("#### 💬 التواصل السريع")
            msg_opt = st.radio("اختر نمط الرسالة", ["تفاصيل مشروع", "حجز موعد", "ترحيب عام"])
            
            text_map = {
                "تفاصيل مشروع": f"تحية طيبة يا فندم، معك {broker_name}. بناءً على تواصلنا، أرشح لك مشروع مميز في {m_area} يتوافق مع ميزانيتك.",
                "حجز موعد": f"أهلاً يا فندم، متاح معاينة للموقع في {m_area} غداً. هل يناسبك الموعد؟",
                "ترحيب عام": f"أهلاً بك يا فندم، معك {broker_name}. يسعدني مساعدتك في إيجاد أفضل وحدة عقارية."
            }
            
            final_msg = st.text_area("تعديل الرسالة", text_map[msg_opt], height=150)
            
            if st.button("🚀 إرسال لواتساب العميل", use_container_width=True):
                if client_phone:
                    link = f"https://wa.me/{client_phone}?text={urllib.parse.quote(final_msg)}"
                    st.markdown(f'<a href="{link}" target="_blank" style="background-color:#25d366; color:white; padding:12px; text-decoration:none; border-radius:10px; display:block; text-align:center; font-weight:bold;">✅ اضغط لفتح المحادثة</a>', unsafe_allow_html=True)
                else: st.warning("يجب إدخال رقم هاتف")
        st.markdown("</div>", unsafe_allow_html=True)

    elif menu == "المشاريع":
        f1, f2, f3 = st.columns(3)
        search = f1.text_input("🔍 بحث")
        area_f = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Area'].unique().tolist()), key="p_area")
        dev_f = f3.selectbox("🏗️ المطور", ["الكل"] + sorted(df_p['Developer'].unique().tolist()), key="p_dev")
        
        dff = df_p.copy()
        if search: dff = dff[dff['Project Name'].str.contains(search, case=False)]
        if area_f != "الكل": dff = dff[dff['Area'] == area_f]
        if dev_f != "الكل": dff = dff[dff['Developer'] == dev_f]
        
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['Project Name']}\n📍 {row['Area']}\n🏗️ {row['Developer']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        
        st.markdown("---")
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0 and p1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
        if start + 6 < len(dff) and p2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        start_d = st.session_state.d_idx * 6
        page_d = df_d.iloc[start_d:start_d+6]
        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    if cols[j].button(f"🏗️ {row['Developer']}\n⭐ فئة: {row.get('Developer Category','A')}", key=f"card_d_{start_d+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        
        st.markdown("---")
        dp1, _, dp2 = st.columns([1,2,1])
        if st.session_state.d_idx > 0 and dp1.button("⬅️ السابق"): st.session_state.d_idx -= 1; st.rerun()
        if start_d + 6 < len(df_d) and dp2.button("التالي ➡️"): st.session_state.d_idx += 1; st.rerun()

    elif menu == "أدوات البروكر":
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حقيبة الأدوات</h2>", unsafe_allow_html=True)
        t1, t2 = st.columns(2)
        with t1:
            with st.expander("💳 حاسبة الأقساط"):
                tp = st.number_input("السعر", 1000000); dp = st.number_input("المقدم", 100000); y = st.slider("السنين", 1, 15, 8)
                st.metric("القسط الشهري", f"{(tp-dp)/(y*12):,.0f}")
            with st.expander("💰 حاسبة العمولة"):
                val = st.number_input("الصفقة", 1000000); pct = st.slider("%", 1.0, 5.0, 1.5)
                st.metric("العمولة", f"{val*(pct/100):,.0f}")
        with t2:
            with st.expander("📏 محول المساحات"):
                m = st.number_input("المتر", 100.0)
                st.write(f"تساوي: {m * 10.76:.2f} قدم")
            with st.expander("🏦 تمويل"):
                s = st.number_input("الدخل", 10000)
                st.success(f"القسط المسموح: {s*0.4:,.0f}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | Full Layout Assistant Enabled</p>", unsafe_allow_html=True)
