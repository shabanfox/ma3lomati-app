import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_option_menu import option_menu
from streamlit_javascript import st_javascript

# 1. إعدادات الصفحة والتصميم
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    .stMarkdown, div, p, h1, h2, h3 { direction: rtl !important; text-align: right !important; color: white; }
    .launch-card { background: linear-gradient(145deg, #1a1a1a, #000); border-right: 8px solid #f59e0b; padding: 20px; border-radius: 15px; margin-bottom: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }
    .dev-card { background: #111; border: 1px solid #333; padding: 15px; border-radius: 12px; margin-bottom: 10px; transition: 0.3s; }
    .dev-card:hover { border-color: #f59e0b; transform: translateY(-5px); }
    .status-badge { background: #f59e0b; color: black; padding: 2px 12px; border-radius: 20px; font-weight: bold; font-size: 14px; }
    .stButton button { width: 100%; border-radius: 10px !important; background: #f59e0b !important; color: black !important; font-weight: bold !important; border: none !important; }
    </style>
""", unsafe_allow_html=True)

# 2. روابط البيانات (تأكد من تفعيل النشر لـ CSV لكل شيت)
U_PROJECTS = "رابط_شيت_المشاريع_CSV"
U_DEVS = "رابط_شيت_المطورين_CSV"
U_LAUNCHES = "رابط_شيت_اللونشات_CSV"

@st.cache_data(ttl=60)
def load_all_data():
    try:
        p = pd.read_csv(U_PROJECTS).fillna("---")
        d = pd.read_csv(U_DEVS).fillna("---")
        l = pd.read_csv(U_LAUNCHES).fillna("---")
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# 3. إدارة الحالة (الدخول وصفحات العرض)
if 'auth' not in st.session_state: st.session_state.auth = True # للتجربة فقط
if 'page' not in st.session_state: st.session_state.page = "main"
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 4. القائمة الجانبية أو العلوية
with st.sidebar:
    st.image("https://via.placeholder.com/150x50.png?text=MA3LOMATI+PRO", use_column_width=True)
    menu = option_menu("الرئيسية", ["اللونشات 🚀", "المطورين 🏗️", "دليل المشاريع 🏢", "المساعد الذكي 🤖"], 
        icons=['rocket-takeoff', 'building', 'search', 'robot'], menu_icon="cast", default_index=0)

# --- قسم اللونشات (الصفحة الجديدة) ---
if menu == "اللونشات 🚀":
    st.markdown("<h1 style='color:#f59e0b;'>🚀 رادار اللونشات الحالية</h1>", unsafe_allow_html=True)
    st.write("تابع أحدث الفرص قبل الإعلان الرسمي لجمع الـ EOIs")
    
    if df_l.empty:
        st.info("لا توجد لونشات مسجلة حالياً.. انتظر تحديث الإدارة.")
    else:
        for i, row in df_l.iterrows():
            st.markdown(f"""
            <div class="launch-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <h2 style="color:#f59e0b; margin:0;">{row['Launch_Name']}</h2>
                    <span class="status-badge">{row['Status']}</span>
                </div>
                <p style="font-size:18px; margin:10px 0;">🏗️ <b>المطور:</b> {row['Developer']} | 📍 <b>المنطقة:</b> {row['Location']}</p>
                <div style="background:#222; padding:15px; border-radius:10px; border:1px dashed #f59e0b;">
                    <p style="margin:0;">💰 <b>مبلغ جدية الحجز (EOI):</b> <span style="color:#00ff00; font-weight:bold;">{row['EOI_Amount']}</span></p>
                    <p style="margin:5px 0 0 0; color:#ddd; font-style:italic;">🔥 {row['Hot_Note']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            msg = f"فرصة لونش جديد! {row['Launch_Name']} بشركة {row['Developer']}. الحجز بدأ بـ {row['EOI_Amount']}. تحب أحجزلك ميعاد؟"
            st.markdown(f"[📲 إرسال التنبيه لعميلك على الواتساب](https://wa.me/?text={urllib.parse.quote(msg)})")

# --- قسم المطورين (المطور بالصور والقصص) ---
elif menu == "المطورين 🏗️":
    if st.session_state.selected_item is None:
        st.title("🏗️ موسوعة المطورين")
        search = st.text_input("🔍 ابحث عن مطور...")
        
        filtered_d = df_d[df_d['Developer'].str.contains(search, case=False)] if search else df_d
        
        for i, row in filtered_d.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="dev-card">
                    <div style="display:flex; align-items:center; gap:15px;">
                        <img src="{row.get('Logo_URL', 'https://via.placeholder.com/50')}" width="50" style="border-radius:5px;">
                        <div>
                            <h3 style="margin:0; color:#f59e0b;">{row['Developer']}</h3>
                            <p style="margin:0; font-size:14px; color:#aaa;">⭐ الفئة: {row.get('Category','A')}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"عرض قصة نجاح {row['Developer']} 📖", key=f"dev_{i}"):
                    st.session_state.selected_item = row.to_dict()
                    st.rerun()
    else:
        # صفحة المطور التفصيلية
        dev = st.session_state.selected_item
        if st.button("⬅️ العودة للقائمة"):
            st.session_state.selected_item = None
            st.rerun()
        
        st.image(dev.get('Hero_Image', 'https://via.placeholder.com/800x300'), use_column_width=True)
        st.header(f"🏗️ {dev['Developer']}")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("🌟 قصة النجاح وسر القوة")
            st.write(dev.get('Success_Story', 'معلومات قادمة قريباً...'))
            st.subheader("🏗️ سابقة الأعمال")
            st.info(dev.get('Flagship_Projects', '---'))
        with col2:
            st.markdown(f"""
            <div style="background:#1a1a1a; padding:15px; border-radius:10px;">
                <p>👤 <b>رئيس مجلس الإدارة:</b><br>{dev.get('Owner', '---')}</p>
                <p>📅 <b>التأسيس:</b> {dev.get('Establishment', '---')}</p>
                <p>🎯 <b>نصيحة المنصة:</b><br>{dev.get('USP', '---')}</p>
            </div>
            """, unsafe_allow_html=True)

# --- باقي الأقسام (تكملة للهيكل) ---
elif menu == "دليل المشاريع 🏢":
    st.title("🏢 محرك بحث المشاريع")
    st.write("هنا تظهر المشاريع المربوطة بالمطورين...")
    # كود البحث في df_p

elif menu == "المساعد الذكي 🤖":
    st.title("🤖 المساعد العقاري الذكي")
    st.write("قريباً: اسألني عن أفضل استثمار في التجمع أو زايد!")
