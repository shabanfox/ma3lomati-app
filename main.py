import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (الدخول، الترقيم، واختيار المطور)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None # لحفظ المطور المختار

# 3. التنسيق (CSS) - تحسين كروت المطورين لتكون قابلة للضغط
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; background-color: #f8fafc; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    
    .luxury-header {
        background: #0f172a; border-bottom: 3px solid #f59e0b; padding: 10px 30px;
        display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 20px 20px; margin-bottom: 10px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 22px; }
    
    .dev-card {
        background: white; border: 1px solid #e2e8f0; border-right: 6px solid #3b82f6;
        border-radius: 12px; padding: 20px; margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); transition: 0.3s;
    }
    .dev-card:hover { transform: translateY(-5px); border-color: #3b82f6; cursor: pointer; }
    
    .back-btn {
        background: #0f172a; color: #f59e0b !important; padding: 8px 15px;
        border-radius: 8px; text-decoration: none; font-weight: bold; margin-bottom: 20px; display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# 4. وظائف البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("غير متوفر").astype(str)
        d = pd.read_csv(u_d).fillna("غير متوفر").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_all_data()

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#0f172a;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1,1.5,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر الثابت
col_h1, col_h2 = st.columns([0.8, 0.2])
with col_h1:
    st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div></div>', unsafe_allow_html=True)
with col_h2:
    if st.button("🚪 خروج"):
        st.session_state.auth = False; st.rerun()

# ----------------- المنطق البرمجي لصفحة التفاصيل -----------------

# إذا كان هناك مطور مختار، اعرض صفحته الخاصة
if st.session_state.selected_dev:
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    
    if st.button("⬅️ العودة لقائمة المطورين"):
        st.session_state.selected_dev = None
        st.rerun()
    
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:20px; border:1px solid #e2e8f0; border-top:8px solid #f59e0b;">
            <h1 style="color:#0f172a; margin-bottom:5px;">{dev_info.get('Developer')}</h1>
            <p style="color:#f59e0b; font-weight:bold; font-size:20px;">{dev_info.get('Developer Category', 'الفئة غير محددة')}</p>
            <hr>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div>
                    <h4 style="color:#3b82f6;">👤 صاحب الشركة / Owner</h4>
                    <p style="font-size:18px;">{dev_info.get('Owner', 'غير متوفر')}</p>
                </div>
                <div>
                    <h4 style="color:#3b82f6;">🏗️ عدد المشاريع</h4>
                    <p style="font-size:18px;">{dev_info.get('Number of Projects', '0')}</p>
                </div>
            </div>
            <div style="margin-top:30px;">
                <h4 style="color:#3b82f6;">📖 سابقة الأعمال والتفاصيل</h4>
                <div style="background:#f8fafc; padding:20px; border-radius:10px; line-height:1.8; font-size:16px;">
                    {dev_info.get('Detailed_Info', 'لا توجد معلومات إضافية متوفرة حالياً.')}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # عرض مشاريع هذا المطور فقط
    st.markdown("### 🏗️ مشاريع المطور الحالية")
    dev_projects = df_p[df_p['Developer'] == dev_name]
    if not dev_projects.empty:
        cols = st.columns(2)
        for i, (_, p_row) in enumerate(dev_projects.iterrows()):
            with cols[i % 2]:
                st.info(f"**{p_row.get('Project Name')}**\n\n📍 {p_row.get('Area')}")
    else:
        st.write("لا توجد مشاريع مسجلة لهذا المطور.")

# إذا لم يتم اختيار مطور، اعرض القائمة الرئيسية
else:
    menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
        icons=["tools", "building", "person-vcard"], 
        default_index=1, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#0f172a", "color": "#f59e0b"}}
    )

    if menu == "المشاريع":
        search = st.text_input("🔍 ابحث عن مشروع...")
        dff = df_p.copy()
        if search: dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        limit = 6
        items = dff.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        cols = st.columns(2)
        for i, (idx, row) in enumerate(items.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""<div class="dev-card" style="border-right-color:#f59e0b;">
                    <h3 style="color:#0f172a;">{row.get('Project Name')}</h3>
                    <p>📍 {row.get('Area')}</p>
                    <p style="color:#64748b; font-size:12px;">🏢 {row.get('Developer')}</p>
                </div>""", unsafe_allow_html=True)

    elif menu == "المطورين":
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dff_d = df_d.copy()
        if search_d: dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]
        
        # عرض المطورين كأزرار داخل كروت
        for i, (idx, row) in enumerate(dff_d.iterrows()):
            with st.container():
                col_text, col_btn = st.columns([0.8, 0.2])
                with col_text:
                    st.markdown(f"""<div class="dev-card">
                        <h3 style="margin:0;">{row.get('Developer')}</h3>
                        <p style="margin:0; color:#64748b;">📍 {row.get('Owner')}</p>
                    </div>""", unsafe_allow_html=True)
                with col_btn:
                    st.write("") # للتوسيط
                    if st.button("عرض التفاصيل", key=f"btn_{idx}"):
                        st.session_state.selected_dev = row.get('Developer')
                        st.rerun()

    elif menu == "الأدوات":
        st.subheader("🧮 الأدوات")
        p = st.number_input("السعر", value=1000000); y = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{p/(y*12):,.0f}")
