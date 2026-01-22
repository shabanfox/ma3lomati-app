import streamlit as st
import pandas as pd
import requests
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. روابط البيانات (تم تحديث رابط اللونشات) ---
# ملاحظة: تم تحويل رابط الـ HTML إلى CSV ليتمكن الكود من قراءته
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

# --- 3. وظائف جلب البيانات ---
@st.cache_data(ttl=60)
def load_launch_data():
    try:
        df = pd.read_csv(URL_LAUNCHES).fillna("---")
        # تنظيف أسماء الأعمدة من أي فراغات
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

# --- 4. التنسيق الجمالي (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    /* تصميم كارت اللونش */
    .launch-card {
        background: #161616;
        border: 1px solid #333;
        padding: 20px;
        border-radius: 15px;
        border-top: 5px solid #f59e0b;
        margin-bottom: 20px;
        transition: 0.3s;
    }
    .launch-card:hover { border-color: #fff; transform: translateY(-5px); }
    .dev-name { color: #f59e0b; font-size: 14px; font-weight: bold; margin-bottom: 5px; }
    .proj-name { color: #fff; font-size: 20px; font-weight: 900; margin-bottom: 10px; }
    .info-tag { background: #333; color: #eee; padding: 4px 10px; border-radius: 5px; font-size: 12px; display: inline-block; margin-left: 5px; }
    
    .update-box { background: #111; border: 1px dashed #f59e0b; padding: 40px; border-radius: 20px; text-align: center; color: #888; }
    </style>
""", unsafe_allow_html=True)

# --- 5. إدارة الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    _, col_mid, _ = st.columns([1, 1.2, 1])
    with col_mid:
        st.markdown("<br><br><br><h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور", type="password")
        if st.button("دخول", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
            else: st.error("خطأ!")
    st.stop()

# --- 6. القائمة العلوية ---
col_out, col_user = st.columns([0.2, 0.8])
with col_out:
    if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "اللونشات"], 
    icons=["briefcase", "building", "search", "robot", "rocket"], 
    default_index=4, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# --- 7. محتوى الأقسام ---
if menu == "اللونشات":
    st.markdown("<h2 style='text-align:center; color:white;'>🚀 دليل اللونشات الحديثة 2026</h2>", unsafe_allow_html=True)
    df_launch = load_launch_data()
    
    if df_launch.empty:
        st.warning("برجاء التأكد من وجود بيانات في الشيت (الورقة المحددة)")
    else:
        # عرض البيانات في شبكة (Grid)
        cols = st.columns(3)
        for index, row in df_launch.iterrows():
            with cols[index % 3]:
                # افترضنا أسماء الأعمدة في الشيت: المطور، المشروع، الموقع، التفاصيل
                # يمكنك تعديل المسميات حسب الشيت الفعلي
                dev = row.get('Developer', row.get('المطور', 'مطور غير معروف'))
                proj = row.get('Project', row.get('المشروع', 'مشروع جديد'))
                loc = row.get('Location', row.get('الموقع', '---'))
                eoi = row.get('EOI', row.get('الجدية', '---'))
                
                st.markdown(f"""
                    <div class="launch-card">
                        <div class="dev-name">🏢 {dev}</div>
                        <div class="proj-name">{proj}</div>
                        <div class="info-tag">📍 {loc}</div>
                        <div class="info-tag">💰 EOI: {eoi}</div>
                        <p style="color:#888; font-size:13px; margin-top:15px;">{row.get('Notes', row.get('ملاحظات', ''))}</p>
                    </div>
                """, unsafe_allow_html=True)

elif menu == "المشاريع" or menu == "المطورين":
    st.markdown("<br><div class='update-box'><h1>🔄 جاري التحديث</h1><p>يتم الآن رفع قاعدة البيانات الجديدة لعام 2026</p></div>", unsafe_allow_html=True)

elif menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    # الأدوات الستة...

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
