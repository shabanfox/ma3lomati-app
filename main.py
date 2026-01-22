import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الفخمة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
URL_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
URL_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'last_menu' not in st.session_state: st.session_state.last_menu = "اللونشات"

# --- 4. التنسيق الجمالي المتطور (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* خلفية الموقع الكاملة */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
        url('https://images.unsplash.com/photo-1449824913935-59a10b8d2000?ixlib=rb-1.2.1&auto=format&fit=crop&w=1920&q=80');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    /* الهيدر الزجاجي */
    .glass-header {
        background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);
        border-radius: 0 0 30px 30px; padding: 30px; text-align: center;
        border-bottom: 2px solid #f59e0b; margin-bottom: 20px;
    }

    /* تصميم الكروت */
    div.stButton > button[key*="card_"] {
        background: rgba(20, 20, 20, 0.9) !important; color: white !important;
        border: 1px solid #333 !important; border-top: 4px solid #f59e0b !important;
        border-radius: 15px !important; min-height: 140px !important; transition: 0.4s !important;
    }
    div.stButton > button:hover { transform: scale(1.02); border-color: #f59e0b !important; box-shadow: 0 10px 20px rgba(245, 158, 11, 0.2); }

    /* المساعد الذكي */
    .ai-box { background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; border-radius: 20px; padding: 20px; }
    
    .stMetric { background: rgba(255,255,255,0.05); padding: 15px; border-radius: 15px; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

# --- 5. وظائف الداتا ---
@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(URL_P).fillna("---")
        d = pd.read_csv(URL_D).fillna("---")
        l = pd.read_csv(URL_L).fillna("---")
        for df in [p, d, l]: df.columns = df.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def login_user(u, p):
    if p == "2026": return "Admin"
    try:
        r = requests.get(f"{SCRIPT_URL}?nocache={time.time()}")
        if r.status_code == 200:
            for user in r.json():
                if (u.lower() == str(user.get('Email','')).lower() or u == str(user.get('Name',''))) and str(p) == str(user.get('Password','')):
                    return user.get('Name','User')
    except: pass
    return None

# --- 6. الصفحة الافتتاحية (Login) ---
if not st.session_state.auth:
    _, col_login, _ = st.columns([1, 1.2, 1])
    with col_login:
        st.markdown("""
            <div style='background: rgba(0,0,0,0.6); padding: 40px; border-radius: 30px; border: 1px solid #f59e0b; text-align: center; margin-top: 50px;'>
                <h1 style='color: #f59e0b; font-size: 45px; margin-bottom: 10px;'>MA3LOMATI PRO</h1>
                <p style='color: #ccc; font-size: 18px;'>الجيل القادم من منصات إدارة العقارات</p>
                <hr style='border-color: #333;'>
            </div>
        """, unsafe_allow_html=True)
        u = st.text_input("اسم المستخدم")
        p = st.text_input("كلمة المرور", type="password")
        if st.button("دخول للمنصة الملكية 👑", use_container_width=True):
            user = login_user(u, p)
            if user: st.session_state.auth = True; st.session_state.current_user = user; st.rerun()
            else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- 7. واجهة المنصة بعد الدخول ---
df_p, df_d, df_l = load_all_data()

# الهيدر السينمائي
st.markdown(f"""
    <div class="glass-header">
        <h1 style="color: white; margin: 0; letter-spacing: 2px;">MA3LOMATI <span style="color:#f59e0b;">PRO</span></h1>
        <p style="color: #aaa; margin-top: 10px;">أهلاً بك يا {st.session_state.current_user} | {datetime.now().strftime('%Y-%m-%d')}</p>
    </div>
""", unsafe_allow_html=True)

# زر الخروج والمنيو
c_ex, c_menu = st.columns([0.15, 0.85])
with c_ex:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()
with c_menu:
    menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
        icons=["briefcase", "building", "search", "robot", "rocket"], 
        default_index=4, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

if menu != st.session_state.last_menu:
    st.session_state.selected_item = None
    st.session_state.last_menu = menu

# --- 8. الأقسام المتطورة ---

# 1. المساعد الذكي (تم التعديل ليعمل بقوة)
if menu == "المساعد الذكي":
    st.markdown("<div class='ai-box'><h2>🤖 مساعد الربط العقاري الذكي</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    loc = c1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
    bud = c2.number_input("💰 المقدم المتاح (EGP)", 0, step=100000)
    typ = c3.selectbox("🏠 نوع الوحدات", ["سكني", "تجاري", "إداري", "الكل"])
    
    if st.button("تحليل ومطابقة البيانات 🎯", use_container_width=True):
        with st.spinner("جاري فحص قاعدة البيانات..."):
            time.sleep(1)
            results = df_p.copy()
            if loc != "الكل": results = results[results['Location'] == loc]
            # هنا يمكنك إضافة فلترة الميزانية لو الشيت يحتوي على خانة "المقدم"
            
            if not results.empty:
                st.success(f"تم إيجاد {len(results.head(6))} ترشيحات مثالية لعميلك:")
                grid = st.columns(3)
                for i, r in results.head(6).reset_index().iterrows():
                    with grid[i % 3]:
                        st.markdown(f"""<div style='background:rgba(0,0,0,0.5); padding:15px; border-radius:10px; border-right:4px solid #f59e0b;'>
                            <h4 style='margin:0;'>{r['ProjectName']}</h4>
                            <p style='color:#f59e0b; font-size:12px;'>{r['Developer']}</p>
                        </div>""", unsafe_allow_html=True)
            else:
                st.warning("لم نجد نتائج مطابقة تماماً، جرب تغيير الفلاتر.")
    st.markdown("</div>", unsafe_allow_html=True)

# 2. أدوات البروكر (تعمل بقوة الآن)
elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center;'>🛠️ الحقيبة الحسابية الاحترافية</h2>", unsafe_allow_html=True)
    t1, t2, t3 = st.tabs(["💳 حاسبة الأقساط", "💰 حاسبة العمولة", "📐 تحويل المساحات"])
    
    with t1:
        cc1, cc2 = st.columns(2)
        total = cc1.number_input("إجمالي سعر الوحدة", 1000000, step=50000)
        down = cc2.number_input("قيمة المقدم", 100000, step=10000)
        years = st.slider("عدد سنوات التقسيط", 1, 15, 8)
        
        rem = total - down
        monthly = rem / (years * 12)
        quarterly = rem / (years * 4)
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_res1, col_res2 = st.columns(2)
        col_res1.metric("القسط الشهري", f"{monthly:,.0f} EGP")
        col_res2.metric("القسط الربع سنوي", f"{quarterly:,.0f} EGP")

    with t2:
        deal = st.number_input("قيمة الصفقة الإجمالية", 1000000)
        comm = st.slider("نسبة العمولة %", 0.5, 10.0, 2.5)
        tax = st.checkbox("خصم ضرائب (14%)")
        
        net = deal * (comm / 100)
        if tax: net = net * 0.86
        
        st.metric("صافي الربح المتوقع", f"{net:,.0f} EGP")

    with t3:
        m2 = st.number_input("المساحة بالمتر المربع (M²)", 100)
        st.info(f"المساحة بالقدم المربع: {m2 * 10.76:,.2f} Ft²")
        st.info(f"المساحة بالفدان: {m2 / 4200:,.4f} فدان")

# باقي الأقسام (المشاريع، المطورين، اللونشات) بنفس منطق "التفاصيل" القوي
elif st.session_state.selected_item is not None:
    it = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    st.markdown(f"""
        <div style='background: rgba(20,20,20,0.8); padding: 30px; border-radius: 20px; border: 1px solid #f59e0b;'>
            <h1 style='color:#f59e0b;'>{it.get('ProjectName', it.get('Project', it.get('Developer')))}</h1>
            <hr>
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 20px;'>
                <div><p style='color:#aaa;'>📍 الموقع</p><h3>{it.get('Location','---')}</h3></div>
                <div><p style='color:#aaa;'>🏢 المطور</p><h3>{it.get('Developer','---')}</h3></div>
                <div><p style='color:#aaa;'>💰 السعر/السداد</p><h3>{it.get('Price & Payment','---')}</h3></div>
                <div><p style='color:#aaa;'>⭐ الفئة</p><h3>{it.get('Developer Category','---')}</h3></div>
            </div>
            <br>
            <p style='color:#f59e0b; font-weight:bold;'>🌟 نقاط القوة (USP):</p>
            <p style='font-size:18px;'>{it.get('Unique Selling Points (USP)', it.get('Notes','---'))}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # عرض الشبكة (Grid) لباقي الأقسام
    if menu == "اللونشات":
        st.markdown("<h2 style='text-align:center; color:white;'>🚀 حصريات 2026</h2>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, r in df_l.iterrows():
            with cols[i % 3]:
                if st.button(f"🔥 {r['Developer']}\n{r['Project']}\n📍 {r['Location']}", key=f"card_l_{i}"):
                    st.session_state.selected_item = r; st.rerun()
    
    elif menu == "المشاريع":
        search = st.text_input("🔍 ابحث في قاعدة بيانات مشاريع مصر...")
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        grid = st.columns(3)
        for i, r in dff.head(12).reset_index().iterrows():
            with grid[i % 3]:
                if st.button(f"🏗️ {r['ProjectName']}\n📍 {r['Location']}", key=f"card_p_{i}"):
                    st.session_state.selected_item = r; st.rerun()

    elif menu == "المطورين":
        search_d = st.text_input("🔍 ابحث عن مطور...")
        dfd = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        grid = st.columns(3)
        for i, r in dfd.head(12).reset_index().iterrows():
            with grid[i % 3]:
                if st.button(f"🏆 {r['Developer']}\n⭐ الفئة: {r.get('Developer Category','A')}", key=f"card_d_{i}"):
                    st.session_state.selected_item = r; st.rerun()

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026 | THE FUTURE OF REAL ESTATE</p>", unsafe_allow_html=True)
