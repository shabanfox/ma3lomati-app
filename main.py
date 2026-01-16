import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة حالة الجلسة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. التنسيق الجمالي المتقدم (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .luxury-header {
        background: linear-gradient(90deg, #0f0f0f 0%, #1a1a1a 100%);
        border-bottom: 2px solid #f59e0b; padding: 20px 40px;
        display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 30px 30px; margin-bottom: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .welcome-text { color: white; font-size: 18px; font-weight: bold; }
    .datetime-text { color: #f59e0b; font-size: 14px; }
    .logo-main { color: #f59e0b; font-weight: 900; font-size: 28px; letter-spacing: 1px; }
    
    .tool-card {
        background: #111; border: 1px solid #222; padding: 20px;
        border-radius: 15px; transition: 0.3s; margin-bottom: 15px;
    }
    .tool-card:hover { border-color: #f59e0b; transform: translateY(-3px); }
    
    div.stButton > button[key*="card_"] {
        background-color: white !important; color: #111 !important;
        border-radius: 15px !important; width: 100% !important;
        min-height: 200px !important; text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
        font-weight: bold !important; font-size: 16px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. شاشة تسجيل الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        passcode = st.text_input("كود الدخول المباشر", type="password")
        if passcode == "2026": 
            st.session_state.auth = True
            st.rerun()
    st.stop()

# 5. الهيدر الترحيبي (الاسم، الوقت، التاريخ، زر الخروج)
now = datetime.now()
h_col1, h_col2, h_col3 = st.columns([1.5, 2, 1])

with h_col1:
    st.markdown(f'<div class="logo-main">MA3LOMATI PRO</div>', unsafe_allow_html=True)

with h_col2:
    st.markdown(f"""
        <div style='text-align:center;'>
            <div class='welcome-text'>مرحباً بك يا بروكر المستقبل 👋</div>
            <div class='datetime-text'>📅 {now.strftime('%Y-%m-%d')} | 🕒 {now.strftime('%I:%M %p')}</div>
        </div>
    """, unsafe_allow_html=True)

with h_col3:
    if st.button("🚪 تسجيل الخروج", use_container_width=True):
        st.session_state.auth = False
        st.rerun()

# 6. جلب البيانات وتأمينها
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---"); d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip(); d.columns = d.columns.str.strip()
        # تأمين الأعمدة الأساسية
        for c in ['Project Name', 'Area', 'Developer']: 
            if c not in p.columns: p[c] = "---"
        for c in ['Developer', 'Developer Category']: 
            if c not in d.columns: d[c] = "---"
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. المنيو الرئيسي
menu = option_menu(None, ["أدوات البروكر", "المشاريع", "المطورين"], 
    icons=["briefcase", "building-up", "person-badge"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# تقسيم الصفحة
main_col, side_col = st.columns([0.78, 0.22])

# الجانب الجانبي (استلام فوري)
with side_col:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>⚡ استلام فوري</h4>", unsafe_allow_html=True)
    if not df_p.empty:
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(8)
        for _, row in ready.iterrows():
            st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:10px; border-radius:10px; margin-bottom:8px; font-size:13px; color:white;">{row["Project Name"]}</div>', unsafe_allow_html=True)

# القسم الرئيسي
with main_col:
    if st.session_state.selected_item is not None:
        if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
        item = st.session_state.selected_item
        st.markdown(f"<div style='background:#111; padding:30px; border-radius:20px; border-right:5px solid #f59e0b; color:white;'><h2>{item.get('Project Name', item.get('Developer'))}</h2><hr>{item.get('Project Features', item.get('Detailed_Info', 'لا توجد تفاصيل إضافية حالياً'))}</div>", unsafe_allow_html=True)

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
                    btn_text = f"🏢 {row['Project Name']}\n📍 {row['Area']}\n🏗️ {row['Developer']}\n✨ عرض كامل البيانات"
                    if cols[j].button(btn_text, key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row
                        st.rerun()
        
        # التنقل
        st.markdown("---")
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0:
            if p1.button("⬅️ السابق", key="prev_p"): st.session_state.p_idx -= 1; st.rerun()
        if start + limit < len(dff):
            if p2.button("التالي ➡️", key="next_p"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        fd1, fd2 = st.columns(2)
        s_dev = fd1.text_input("🔍 ابحث عن المطور")
        cat = fd2.selectbox("⭐ الفئة", ["الكل"] + sorted(df_d['Developer Category'].unique().tolist()))

        dfd = df_d.copy()
        if s_dev: dfd = dfd[dfd['Developer'].str.contains(s_dev, case=False)]
        if cat != "الكل": dfd = dfd[dfd['Developer Category'] == cat]

        limit_d = 6
        start_d = st.session_state.d_idx * limit_d
        page_d = dfd.iloc[start_d:start_d+limit_d]

        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    btn_txt = f"🏗️ {row['Developer']}\n⭐ فئة: {row['Developer Category']}\n👤 المالك: {row.get('Owner','---')}\n📖 سابقة الأعمال"
                    if cols[j].button(btn_txt, key=f"card_d_{start_d+i+j}"):
                        st.session_state.selected_item = row
                        st.rerun()

        st.markdown("---")
        dp1, _, dp2 = st.columns([1,2,1])
        if st.session_state.d_idx > 0:
            if dp1.button("⬅️ السابق", key="prev_d"): st.session_state.d_idx -= 1; st.rerun()
        if start_d + limit_d < len(dfd):
            if dp2.button("التالي ➡️", key="next_d"): st.session_state.d_idx += 1; st.rerun()

    elif menu == "أدوات البروكر":
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حقيبة أدوات البروكر الذكية</h2>", unsafe_allow_html=True)
        
        t1, t2 = st.columns(2)
        
        with t1:
            with st.expander("💰 1. حاسبة العمولة الصافية"):
                deal = st.number_input("قيمة الصفقة (EGP)", 1000000)
                comm_pct = st.slider("نسبة عمولتك (%)", 0.5, 5.0, 1.5)
                tax = st.checkbox("خصم ضرائب (14%)")
                total = deal * (comm_pct/100)
                if tax: total = total * 0.86
                st.metric("صافي ربحك المتوقع", f"{total:,.0f} EGP")

            with st.expander("📈 2. حاسبة العائد على الاستثمار (ROI)"):
                buy_price = st.number_input("سعر الشراء", 1000000, key="roi_buy")
                rent = st.number_input("الإيجار الشهري المتوقع", 5000)
                yearly_roi = ((rent * 12) / buy_price) * 100
                st.write(f"نسبة العائد السنوي: **{yearly_roi:.1f}%**")
                st.progress(min(yearly_roi/15, 1.0))

        with t2:
            with st.expander("📏 3. محول المساحات السريع"):
                val = st.number_input("القيمة", 1.0)
                unit = st.selectbox("من", ["متر مربع", "قدم مربع", "فدان"])
                if unit == "متر مربع": st.write(f"تساوي: {val * 10.76:.2f} قدم مربع")
                elif unit == "فدان": st.write(f"تساوي: {val * 4200:.0f} متر مربع")

            with st.expander("🏦 4. حاسبة أقصى تمويل للعميل"):
                salary = st.number_input("دخل العميل الشهري", 5000)
                limit_ratio = 0.40
                max_installment = salary * limit_ratio
                st.warning(f"أقصى قسط مسموح للعميل: {max_installment:,.0f} EGP")

        st.markdown("---")
        st.markdown("<h4 style='text-align:center;'>🎯 5. عداد الإنجاز اليومي</h4>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.number_input("📞 مكالمات اليوم", 0)
        c2.number_input("🤝 زيارات الموقع", 0)
        c3.number_input("📑 عقود مغلقة", 0)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 - الإصدار المتقدم</p>", unsafe_allow_html=True)
