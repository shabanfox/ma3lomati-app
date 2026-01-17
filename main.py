import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        # تنظيف الداتا
        p['Project Name'] = p['Project Name'].astype(str).str.strip()
        p = p.drop_duplicates(subset=['Project Name'], keep='first')
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 4. التنسيق (الأساسي والضروري)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .stButton > button { width: 100% !important; border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; }
    /* كروت البيضاء */
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; font-weight: bold !important;
        border: none !important; margin-bottom: 10px !important;
    }
    .smart-box { background: #111; border: 1px solid #333; padding: 20px; border-radius: 15px; border-right: 5px solid #f59e0b; color: white; }
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; margin-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c, _ = st.columns([1,1,1])
    with c:
        if st.text_input("كود الدخول", type="password") == "2026":
            st.session_state.auth = True
            st.rerun()
    st.stop()

# 6. الهيدر
c1, c2, c3 = st.columns([1, 2, 1])
c1.markdown("<h3 style='color:#f59e0b;'>MA3LOMATI</h3>", unsafe_allow_html=True)
c2.markdown(f"<p style='text-align:center; color:gray;'>{datetime.now().strftime('%Y-%m-%d')}</p>", unsafe_allow_html=True)
if c3.button("🚪 خروج"): 
    st.session_state.auth = False
    st.rerun()

# 7. المنيو
menu = option_menu(None, ["المشاريع", "المساعد الذكي", "المطورين", "الأدوات"], 
    icons=["building", "robot", "people", "tools"], orientation="horizontal")

# 8. عرض المحتوى
if st.session_state.selected_item is not None:
    item = st.session_state.selected_item
    if st.button("⬅️ عودة"):
        st.session_state.selected_item = None
        st.rerun()
    
    st.markdown(f"""
    <div class="smart-box">
        <h2 style="color:#f59e0b;">{item['Project Name']}</h2>
        <p><b>🏗️ المطور:</b> {item.get('Developer', '---')}</p>
        <p><b>👤 المالك:</b> {item.get('Owner', '---')}</p>
        <p><b>📍 الموقع:</b> {item.get('Location', '---')}</p>
        <p><b>💰 السعر:</b> {item.get('Starting Price (EGP)', '---')}</p>
        <p><b>💳 السداد:</b> {item.get('Payment Plan', '---')}</p>
        <hr>
        <div style="display:flex; justify-content:space-between;">
            <div style="color:#10b981;">✅ المميزات: موقع استراتيجي، مطور موثوق، طلب عالي.</div>
            <div style="color:#ef4444;">⚠️ العيوب: تأكد من جدول الاستلام ونسبة التحميل.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

elif menu == "المشاريع":
    col_main, col_side = st.columns([0.8, 0.2])
    with col_main:
        search = st.text_input("🔍 ابحث باسم المشروع...")
        dff = df_p[df_p['Project Name'].str.contains(search, case=False)] if search else df_p
        
        # عرض الكروت
        rows_to_show = dff.iloc[st.session_state.p_idx * 6 : (st.session_state.p_idx + 1) * 6]
        for i in range(0, len(rows_to_show), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(rows_to_show):
                    r = rows_to_show.iloc[i+j]
                    if cols[j].button(f"🏢 {r['Project Name']}\n📍 {r['Location']}\n🏗️ {r['Developer']}", key=f"card_p_{i+j}"):
                        st.session_state.selected_item = r
                        st.rerun()
        
        # الترقيم
        p1, _, p2 = st.columns([1,1,1])
        if st.session_state.p_idx > 0:
            if p1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
        if (st.session_state.p_idx + 1) * 6 < len(dff):
            if p2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'><h3>🤖 المساعد الذكي - فلاتر احترافية</h3>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    f_loc = c1.selectbox("المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    f_type = c2.selectbox("نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري"])
    f_sale = c3.selectbox("نوع البيع", ["الكل", "مطور", "ريسيل"])
    
    res = df_p.copy()
    if f_loc != "الكل": res = res[res['Location'] == f_loc]
    if f_type != "الكل": res = res[res['Available Units (Types)'].str.contains(f_type, case=False)]
    if f_sale != "الكل": res = res[res['Sales Type'] == f_sale]
    
    st.write(f"تم إيجاد {len(res)} خيار مناسب")
    for _, r in res.head(5).iterrows():
        if st.button(f"📊 تحليل {r['Project Name']}", key=f"ans_{r['Project Name']}"):
            st.session_state.selected_item = r
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المطورين":
    search_d = st.text_input("🔍 ابحث عن مطور")
    dff_d = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
    for i, r in dff_d.head(10).iterrows():
        if st.button(f"🏗️ {r['Developer']}\n👤 المالك: {r.get('Owner', '---')}", key=f"card_d_{i}"):
            st.write(f"تفاصيل المطور: {r['Developer']}")

elif menu == "الأدوات":
    st.info("🛠️ أدوات الحاسبة العقارية")
    p = st.number_input("السعر", 1000000)
    y = st.slider("السنين", 1, 15, 8)
    st.metric("القسط الشهري التقريبي", f"{p/(y*12):,.0f}")

st.markdown("<p style='text-align:center; color:gray;'>MA3LOMATI PRO 2026</p>", unsafe_allow_html=True)
