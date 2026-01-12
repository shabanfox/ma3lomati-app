import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - النسخة الموحدة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* هيدر احترافي مع زر خروج مدمج */
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 30px; border-radius: 0 0 20px 20px;
        border-right: 12px solid #f59e0b; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 26px !important; color: #f59e0b; margin: 0; }
    
    /* الكروت الموحدة (المشاريع والمطورين) */
    .unified-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; margin-bottom: 15px; text-align: center; 
        min-height: 200px; display: flex; flex-direction: column; justify-content: center;
        transition: 0.3s ease;
    }
    .unified-card:hover { border-color: #f59e0b; transform: translateY(-5px); box-shadow: 0 5px 15px rgba(245, 158, 11, 0.1); }
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 800; margin-bottom: 8px; }
    
    /* الأدوات والفلاتر (الجهة اليسرى) */
    .side-panel { background: #0d0d0d; border-radius: 15px; padding: 20px; border: 1px solid #222; }
    .tool-card { background: #161616; padding: 15px; border-radius: 10px; margin-bottom: 15px; border-right: 4px solid #f59e0b; }
    .tool-res { color: #f59e0b; font-size: 22px; font-weight: 900; margin-top: 5px; text-align: center; }

    /* أزرار مخصصة */
    .stButton button { width: 100%; background: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; font-weight: bold; }
    .logout-btn button { background: #ff4b4b !important; color: white !important; border: none !important; width: auto !important; padding: 0 20px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# 4. الهيدر العلوي
st.markdown("""
    <div class="header-container">
        <div class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</div>
    </div>
""", unsafe_allow_html=True)

# وضع زر الخروج في مكان محدد باستخدام Streamlit لضمان عمل الـ Callback
cols_top = st.columns([10, 1])
with cols_top[1]:
    if st.button("خروج", key="logout_btn", help="تسجيل الخروج"):
        st.session_state.clear()
        st.rerun()

selected = option_menu(None, ["🏗️ المشاريع", "🏢 المطورين", "🛠️ الأدوات"], 
    icons=["building", "people", "gear"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "2px solid #f59e0b"}})

# إدارة الصفحات
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# --- 🏗️ شاشة المشاريع (التوزيع الجديد) ---
if selected == "🏗️ المشاريع":
    col_main, col_left = st.columns([0.7, 0.3]) # 70% يمين للمشاريع
    
    with col_left:
        st.markdown("<div class='side-panel'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#f59e0b;'>🔍 البحث والفلترة</h4>", unsafe_allow_html=True)
        search_p = st.text_input("اسم المشروع أو المطور")
        area_p = st.selectbox("اختر المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()) if 'Area' in df.columns else ["الكل"])
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main:
        f_df = df.copy()
        if search_p: f_df = f_df[f_df.apply(lambda r: search_p.lower() in r.astype(str).str.lower().values, axis=1)]
        if area_p != "الكل": f_df = f_df[f_df['Area'] == area_p]

        items = 9
        total_p = max(1, math.ceil(len(f_df) / items))
        curr = f_df.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

        for i in range(0, len(curr), 3):
            grid = st.columns(3)
            for j in range(3):
                if i+j < len(curr):
                    row = curr.iloc[i+j]
                    with grid[j]:
                        st.markdown(f"""
                            <div class="unified-card">
                                <div class="card-title">{row.get('Project Name', 'مشروع')}</div>
                                <div style="color:#888; font-size:13px; margin-bottom:10px;">{row.get('Developer', 'مطور')}</div>
                                <div style="text-align:right; font-size:13px; color:#ccc;">
                                    <p>📍 {row.get('Area', '-')}</p>
                                    <p>🏠 {row.get('شقق/فيلات', '-')}</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
        
        # أزرار التنقل
        st.write("---")
        n1, n2, n3 = st.columns([1, 1, 1])
        if n3.button("التالي ⬅️", key="p_n"): st.session_state.p_page += 1; st.rerun()
        n2.markdown(f"<center>{st.session_state.p_page+1} / {total_p}</center>", unsafe_allow_html=True)
        if n1.button("➡️ السابق", key="p_p") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين (بنفس شكل كروت المشاريع) ---
elif selected == "🏢 المطورين":
    devs = df[['Developer', 'Owner']].drop_duplicates().reset_index(drop=True)
    st.markdown("<h3 style='color:#f59e0b;'>🏢 دليل المطورين</h3>", unsafe_allow_html=True)
    
    items = 9
    total_d = max(1, math.ceil(len(devs) / items))
    curr_d = devs.iloc[st.session_state.d_page * items : (st.session_state.d_page + 1) * items]

    for i in range(0, len(curr_d), 3):
        grid = st.columns(3)
        for j in range(3):
            if i+j < len(curr_d):
                row = curr_d.iloc[i+j]
                with grid[j]:
                    st.markdown(f"""
                        <div class="unified-card">
                            <div class="card-title">{row['Developer']}</div>
                            <div style="background:#000; padding:10px; border-radius:8px; margin-top:10px;">
                                <div style="color:#666; font-size:11px;">المالك</div>
                                <div style="color:#fff;">{row['Owner']}</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # تنقل المطورين
    st.write("---")
    d1, d2, d3 = st.columns([1, 1, 1])
    if d3.button("التالي ⬅️", key="d_n"): st.session_state.d_page += 1; st.rerun()
    d2.markdown(f"<center>{st.session_state.d_page+1} / {total_d}</center>", unsafe_allow_html=True)
    if d1.button("➡️ السابق", key="d_p") and st.session_state.d_page > 0: st.session_state.d_page -= 1; st.rerun()

# --- 🛠️ شاشة الأدوات (في جهة اليسار) ---
elif selected == "🛠️ الأدوات":
    st.markdown("<h3 style='color:#f59e0b;'>🛠️ الأدوات الذكية</h3>", unsafe_allow_html=True)
    col_main_tool, col_left_tool = st.columns([0.7, 0.3]) # الأدوات في اليسار كما طلبت

    with col_left_tool:
        st.markdown("<div class='side-panel'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#f59e0b;'>💰 حاسبة القسط</h4>", unsafe_allow_html=True)
        price = st.number_input("السعر", value=1000000)
        years = st.slider("السنوات", 1, 15, 7)
        res = price / (years * 12)
        st.markdown(f"<div class='tool-res'>{res:,.0f} ج.م</div>", unsafe_allow_html=True)
        st.markdown("<hr style='border-color:#222'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#f59e0b;'>📐 المحول</h4>", unsafe_allow_html=True)
        acre = st.number_input("فدان", value=1.0)
        st.markdown(f"<div class='tool-res'>{acre*4200:,.0f} م²</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_main_tool:
        st.markdown("<div class='side-panel' style='min-height:400px;'>", unsafe_allow_html=True)
        st.markdown("<h4 style='color:#f59e0b;'>📝 مفكرة العميل</h4>", unsafe_allow_html=True)
        st.text_area("سجل ملاحظات العميل والطلبات هنا...", height=300)
        st.button("حفظ الملاحظات (نسخ)")
        st.markdown("</div>", unsafe_allow_html=True)
