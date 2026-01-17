import streamlit as st
import pandas as pd
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. التوقيت والحالة
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None
if 'current_menu' not in st.session_state: st.session_state.current_menu = "المشاريع"

# 3. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    header, [data-testid="stHeader"] { visibility: hidden; }
    .smart-box { background: #111; border: 1px solid #333; padding: 25px; border-radius: 20px; border-right: 5px solid #f59e0b; color: white; }
    .dev-card { background: white; padding: 20px; border-radius: 15px; border-right: 8px solid #f59e0b; min-height: 200px; color: #111; margin-bottom: 15px; }
    .stButton > button { width: 100% !important; border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; }
    .side-card { background: #1a1a1a; padding: 15px; border-radius: 12px; border-bottom: 2px solid #f59e0b; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        # توحيد المسميات لضمان عمل الفلاتر
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 5. الهيدر العلوي
t1, t2 = st.columns([0.7, 0.3])
with t1: st.markdown("<h1 style='color:#f59e0b; margin:0;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
with t2:
    st.markdown(f"<div style='text-align:left; color:#aaa;'>{egypt_now.strftime('%Y-%m-%d')} | {egypt_now.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

# 6. المنيو الرئيسي مع حل مشكلة التنقل
selected_menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة الأدوات"], 
    icons=["robot", "search", "building", "briefcase"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# *** الكود السحري لحل مشكلة التنقل ***
if selected_menu != st.session_state.current_menu:
    st.session_state.selected_item = None  # تصفير الاختيار عند تغيير الصفحة
    st.session_state.current_menu = selected_menu
    st.rerun()

# 7. عرض المحتوى
if st.session_state.selected_item is not None:
    item = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.selected_item = None
        st.rerun()
    
    # تفاصيل مطور أو مشروع
    st.markdown(f"<div class='smart-box'>", unsafe_allow_html=True)
    if 'Developer' in item and 'ProjectName' not in item: # لو المختار مطور
        st.header(f"🏗️ {item['Developer']}")
        c1, c2 = st.columns(2)
        c1.write(f"👤 **المالك:** {item.get('Owner_Name', '---')}")
        c1.write(f"📅 **تأسست عام:** {item.get('Established_Date', '---')}")
        c2.write(f"🏆 **التصنيف:** {item.get('Category', '---')}")
        c2.write(f"📍 **المقر:** {item.get('Headquarters', '---')}")
        st.write("---")
        st.subheader("📜 سابقة الأعمال والنبذة")
        st.write(item.get('History_Info', 'لا توجد تفاصيل إضافية حالياً'))
    else: # لو المختار مشروع
        st.header(f"🏢 {item['ProjectName']}")
        st.write(f"🏗️ المطور: {item['Developer']} | 📍 الموقع: {item['Location']}")
        st.write(f"📐 المساحات: {item.get('Space_From', '---')} إلى {item.get('Space_To', '---')}")
        st.write(f"💰 السعر يبدأ من: {item.get('Starting_Price', '---')}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- صفحة المطورين (الهيكل المكتمل) ---
elif selected_menu == "المطورين":
    col_main, col_side = st.columns([0.7, 0.3])
    
    with col_side:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 Top 10 Developers</h4>", unsafe_allow_html=True)
        top_10 = df_d.head(10)
        for i, r in top_10.iterrows():
            st.markdown(f"<div class='side-card'><b>{i+1}. {r['Developer']}</b><br><small>Category: {r.get('Category','A')}</small></div>", unsafe_allow_html=True)

    with col_main:
        search_d = st.text_input("🔍 ابحث عن مطور (الاسم أو المالك)")
        dff_d = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        
        start_d = st.session_state.d_idx * 6
        page_d = dff_d.iloc[start_d:start_d+6]
        
        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class='dev-card'>
                            <h3>{row['Developer']}</h3>
                            <p>👤 المالك: {row.get('Owner_Name', '---')}</p>
                            <p>🏆 التصنيف: {row.get('Category', '---')}</p>
                            <p>📅 الخبرة: منذ {row.get('Established_Date', '---')}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        if st.button("عرض الملف الكامل", key=f"card_d_{start_d+i+j}"):
                            st.session_state.selected_item = row
                            st.rerun()

# --- صفحة المشاريع (70/30 مع الاستلام الفوري) ---
elif selected_menu == "المشاريع":
    col_main, col_side = st.columns([0.7, 0.3])
    
    with col_side:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        ready = df_p[df_p['Delivery_Date'].astype(str).str.contains('فوري|جاهز', case=False)].head(10)
        for i, r in ready.iterrows():
            if st.button(f"🏠 {r['ProjectName']}", key=f"ready_{i}"):
                st.session_state.selected_item = r; st.rerun()

    with col_main:
        f1, f2 = st.columns(2)
        s_p = f1.text_input("🔍 ابحث عن مشروع")
        a_p = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
        
        dff_p = df_p[df_p['ProjectName'].str.contains(s_p, case=False)] if s_p else df_p
        if a_p != "الكل": dff_p = dff_p[dff_p['Location'] == a_p]
        
        start_p = st.session_state.p_idx * 6
        page_p = dff_p.iloc[start_p:start_p+6]
        
        for i in range(0, len(page_p), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_p):
                    row = page_p.iloc[i+j]
                    if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row['Developer']}", key=f"card_p_{start_p+i+j}"):
                        st.session_state.selected_item = row; st.rerun()

# --- صفحة المساعد الذكي (100% مساحة) ---
elif selected_menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري 2026")
    c1, c2, c3 = st.columns(3)
    # محرك بحث ذكي بناء على الميزانية والموقع
    budget = c1.number_input("المقدم المتاح عندك", 0)
    target = c2.selectbox("المنطقة المستهدفة", sorted(df_p['Location'].unique().tolist()))
    u_type = c3.selectbox("نوع الوحدة", ["شقق", "فيلات", "تجاري"])
    
    if st.button("🚀 استخراج أفضل الترشيحات المتاحة"):
        st.balloons()
        st.info("جاري فحص قاعدة البيانات لترشيح أفضل مقدم وأطول فترة سداد...")
    st.markdown("</div>", unsafe_allow_html=True)

# --- حقيبة الأدوات ---
elif selected_menu == "حقيبة الأدوات":
    st.title("🛠️ حقيبة البروكر الاحترافية")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("💳 حاسبة الأقساط")
            price = st.number_input("السعر", 1000000)
            st.write(f"القسط الشهري (8 سنين): {(price*0.9)/(8*12):,.0f}")
    with c2:
        with st.container(border=True):
            st.subheader("💰 العمولات")
            deal = st.number_input("الصفقة", 1000000)
            st.write(f"العمولة (1.5%): {deal*0.015:,.0f}")
    with c3:
        with st.container(border=True):
            st.subheader("📐 المساحات")
            m2 = st.number_input("متر", 100.0)
            st.write(f"قدم مربع: {m2*10.76:,.0f}")
