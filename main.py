import streamlit as st
import pandas as pd
import math
import feedparser
from streamlit_option_menu import option_menu 
from datetime import datetime

# 1. إعدادات الصفحة (أداء عالي)
st.set_page_config(page_title="Ma3lomati PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. تحميل البيانات مع تخزين مؤقت ذكي للسرعة
@st.cache_data(ttl=300) # تحديث كل 5 دقائق لضمان السرعة
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 3.CSS المطور (خفيف وسريع)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] { background-color: #050505; color: white; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif; }
    .block-container { padding-top: 0rem !important; }
    header { visibility: hidden; }
    
    /* هيدر جذاب وخفيف */
    .header-box {
        background: linear-gradient(90deg, #000, #111);
        border-bottom: 2px solid #f59e0b;
        padding: 15px 30px; display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 20px 20px; margin-bottom: 15px;
    }
    .logo { color: #f59e0b; font-weight: 900; font-size: 26px; }

    /* منطقة الاستلام الفوري الجانبية */
    .ready-sidebar {
        background: #0f0f0f; border: 1px solid #222; border-radius: 15px; padding: 15px;
        height: 80vh; overflow-y: auto;
    }
    .ready-item {
        background: #161616; border-right: 4px solid #10b981;
        padding: 10px; border-radius: 8px; margin-bottom: 10px;
    }

    /* كروت المشاريع */
    .project-card {
        background: #111; border: 1px solid #222; border-radius: 12px;
        padding: 15px; margin-bottom: 15px; border-top: 3px solid #f59e0b;
    }
    </style>
""", unsafe_allow_html=True)

# 4. التحقق من الدخول
if 'auth' not in st.session_state: st.session_state.auth = False
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; margin-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("كلمة المرور", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- الهيدر المطور ---
st.markdown(f"""
    <div class="header-box">
        <div class="logo">MA3LOMATI <span style="color:white; font-size:12px;">PRO 2026</span></div>
        <div style="color:#aaa;">{datetime.now().strftime("%Y-%m-%d")}</div>
    </div>
""", unsafe_allow_html=True)

# المنيو
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], orientation="horizontal",
    styles={"container": {"background-color": "#000"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- تقسيم الشاشة 70% و 30% ---
col_main, col_side = st.columns([0.7, 0.3])

# --- الـ 30% الجانبية: استلام فوري فقط ---
with col_side:
    st.markdown("<h3 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h3>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    
    # فلترة المشاريع (نبحث عن كلمة فوري أو جاهز في أي مكان في بيانات المشروع)
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    
    if not ready_df.empty:
        for _, row in ready_df.iterrows():
            st.markdown(f"""
                <div class="ready-item">
                    <b style="color:#f59e0b;">{row['Project Name']}</b><br>
                    <small>📍 {row['Area']}</small><br>
                    <small>🏢 {row['Developer']}</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("لا توجد مشاريع استلام فوري حالياً")
    st.markdown("</div>", unsafe_allow_html=True)

# --- الـ 70% الرئيسية ---
with col_main:
    if menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل كافة المشاريع</h2>", unsafe_allow_html=True)
        search = st.text_input("🔍 بحث في كل المشاريع (الاسم، المطور، المنطقة)...")
        
        display_df = df_p.copy()
        if search:
            display_df = display_df[display_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        # عرض البيانات بشكل كامل (شبكة 2 في الصف)
        for i in range(0, len(display_df), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(display_df):
                    row = display_df.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="project-card">
                                <h4 style="color:#f59e0b; margin:0;">{row['Project Name']}</h4>
                                <p style="font-size:13px; margin:5px 0;">
                                📍 {row['Area']} | 📐 {row['Project Area']}<br>
                                🏢 المطور: {row['Developer']}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("تفاصيل إضافية"):
                            st.info(f"✨ المميزات: {row['Project Features']}")
                            st.warning(f"⚠️ العيوب: {row['Project Flaws']}")

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين العقاريين</h2>", unsafe_allow_html=True)
        for _, row in df_d.iterrows():
            with st.expander(f"🏢 {row['Developer']} - المالك: {row['Owner']}"):
                st.write(f"📝 {row['Detailed_Info']}")
                st.success(f"🏆 الميزة التنافسية: {row['Competitive Advantage']}")

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ حاسبات البروكر</h2>", unsafe_allow_html=True)
        t1, t2, t3, t4, t5, t6 = st.tabs(["الأقساط", "العمولة", "المساحة", "ROI", "الفائدة", "نوت"])
        with t1:
            p = st.number_input("السعر", 1000000); d = st.number_input("المقدم", p*0.1); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط شهرياً", f"{(p-d)/(y*12):,.0f} ج.م")
        with t2: r = st.number_input("النسبة %", 1.5); st.metric("العمولة", f"{p*(r/100):,.0f} ج.م")
        with t3: sq = st.number_input("المتر المربع", 100.0); st.write(f"القدم المربع: {sq*10.76:,.2f}")
        with t4: rent = st.number_input("الإيجار", 10000); st.metric("ROI السنوي", f"{(rent*12/p)*100:.2f}%")
        with t5: f = st.slider("الفائدة السنوية %", 1, 30, 20); st.write(f"الإجمالي بالفوائد: {p*(1+(f/100)*y):,.0f}")
        with t6: st.text_area("سجل ملاحظاتك هنا...")

# زر الخروج في ذيل الصفحة بشكل أنيق
if st.button("🚪 تسجيل الخروج"):
    st.session_state.auth = False
    st.rerun()
