import streamlit as st
import pandas as pd
import urllib.parse
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    .stMarkdown, div, p, h1, h2, h3 { direction: rtl !important; text-align: right !important; }
    
    /* ستايل كارت اللونش */
    .launch-card {
        background: linear-gradient(145deg, #1e1e1e, #000000);
        border-right: 10px solid #f59e0b;
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 25px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    .launch-title { color: #f59e0b; font-size: 28px; font-weight: 900; margin-bottom: 10px; }
    .eoi-box { background: #333; padding: 10px 20px; border-radius: 10px; border: 1px dashed #f59e0b; display: inline-block; margin-top: 10px; }
    
    .stButton button { width: 100%; border-radius: 10px !important; background: #f59e0b !important; color: black !important; font-weight: bold !important; border: none !important; height: 45px; }
    </style>
""", unsafe_allow_html=True)

# 3. الروابط (استبدلها بروابط الـ CSV الخاصة بك)
U_PROJECTS = "https://docs.google.com/spreadsheets/d/e/YOUR_LINK/pub?gid=0&single=true&output=csv"
U_DEVS = "https://docs.google.com/spreadsheets/d/e/YOUR_LINK/pub?gid=2031754026&single=true&output=csv"
U_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/YOUR_LINK/pub?gid=YOUR_LAUNCH_GID&single=true&output=csv"

@st.cache_data(ttl=60)
def load_data():
    try:
        # ملاحظة: إذا لم تتوفر الداتا حالياً سنصنع داتا تجريبية لتشغيل الشكل
        l_df = pd.read_csv(U_LAUNCHES).fillna("---")
        return l_df
    except:
        # داتا وهمية فقط لكي ترى "قسم اللونشات" شغال أمامك الآن
        data = {
            'Launch_Name': ['مشروع نايل تاور الجديد', 'ماونتن فيو زايد الجديدة'],
            'Developer': ['Nile Development', 'Mountain View'],
            'Location': ['العاصمة الإدارية', 'الشيخ زايد'],
            'EOI_Amount': ['50,000 EGP', '100,000 EGP'],
            'Status': ['قريباً جداً', 'جمع EOIs'],
            'Hot_Note': ['أطول برج سكني في أفريقيا، فرصة استثمارية خرافية.', 'موقع استراتيجي بجوار مطار سفنكس مباشرة.']
        }
        return pd.DataFrame(data)

df_launches = load_data()

# 4. القائمة الرئيسية (Navigation)
selected = option_menu(
    menu_title=None,
    options=["اللونشات 🚀", "المطورين 🏗️", "المشاريع 🏢"],
    icons=["rocket-takeoff", "building", "search"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#111"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"},
    }
)

# --- منطق الصفحات ---

if selected == "اللونشات 🚀":
    st.markdown("<h1 style='color:#f59e0b; text-align:center;'>🎯 رادار اللونشات الحصرية</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:18px;'>كن أول من يعلم وأول من يحجز لعملائك في أقوى الفرص القادمة</p>", unsafe_allow_html=True)
    st.write("---")

    if df_launches.empty:
        st.info("لا توجد لونشات مسجلة حالياً.")
    else:
        for i, row in df_launches.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="launch-card">
                    <div style="display:flex; justify-content:space-between; align-items:start;">
                        <div>
                            <div class="launch-title">{row['Launch_Name']}</div>
                            <div style="font-size:20px; color:#ccc;">🏗️ المطور: <b>{row['Developer']}</b></div>
                            <div style="font-size:18px; color:#aaa;">📍 الموقع: {row['Location']}</div>
                        </div>
                        <div style="background:#f59e0b; color:black; padding:5px 15px; border-radius:8px; font-weight:bold;">
                            {row['Status']}
                        </div>
                    </div>
                    <div class="eoi-box">
                        <span style="color:#f59e0b; font-weight:bold;">💰 مبلغ الحجز (EOI):</span> 
                        <span style="font-size:20px;">{row['EOI_Amount']}</span>
                    </div>
                    <div style="margin-top:15px; color:#eee; font-style:italic; border-top:1px solid #333; padding-top:10px;">
                        💡 <b>توصية المنصة:</b> {row['Hot_Note']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # زر الواتساب لإرسال اللونش للعميل
                msg = f"مساء الخير يا فندم، فيه لونش شغال حالياً لشركة {row['Developer']} في {row['Location']}. مبلغ الحجز {row['EOI_Amount']} ومسترد بالكامل. لو حابب أحجزلك مكان في أول يوم تواصل معايا."
                st.markdown(f"[📲 أرسل تفاصيل اللونش لعميلك الآن](https://wa.me/?text={urllib.parse.quote(msg)})")

elif selected == "المطورين 🏗️":
    st.title("🏗️ قسم المطورين")
    st.write("هنا سيظهر شيت المطورين بالصور والقصص اللي عملناه...")

elif selected == "المشاريع 🏢":
    st.title("🏢 دليل المشاريع")
    st.write("هنا تظهر محرك بحث المشاريع...")
