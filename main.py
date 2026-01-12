import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    .stButton > button[key="logout_btn"] { background-color: #ff4b4b !important; color: white !important; border: none !important; padding: 5px 20px !important; border-radius: 8px !important; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 20px; border-radius: 0 0 20px 20px; border-right: 15px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 32px !important; color: #f59e0b; margin: 0; }
    .pro-card { background: #111; border: 1px solid #222; border-top: 5px solid #f59e0b; border-radius: 15px; padding: 20px; margin-bottom: 15px; text-align: center; height: 100%; }
    .stat-value { color: #f59e0b; font-weight: bold; }
    .stSelectbox div[data-baseweb="select"] { background-color: #111 !important; }
    .stTextInput input { background-color: #111 !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات مع تنظيف أسماء الأعمدة
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        # تنظيف أسماء الأعمدة من المسافات المخفية
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# وظيفة مساعدة للحصول على القيمة حتى لو اسم العمود اختلف
def get_val(row, target_names, default="غير متوفر"):
    for name in target_names:
        if name in row: return row[name]
    return default

# 4. واجهة المستخدم
t_c1, t_c2 = st.columns([10, 1.5])
with t_c2:
    if st.button("تسجيل الخروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

st.markdown('<div class="main-header"><h1 class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ الأدوات", "🏗️ المشاريع", "🏢 المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal", 
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

if 'p_page' not in st.session_state: st.session_state.p_page = 0

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    search_q = col1.text_input("🔍 ابحث عن مشروع أو مطور...")
    
    # التأكد من وجود عمود المنطقة
    area_col = 'Area' if 'Area' in df.columns else (df.columns[0] if not df.empty else None)
    areas = ["كل المناطق"] + sorted(df[area_col].unique().tolist()) if area_col else ["الكل"]
    area_f = col2.selectbox("📍 المنطقة", areas)

    filtered_df = df.copy()
    if search_q:
        # بحث مرن في كل الأعمدة المتاحة
        filtered_df = filtered_df[filtered_df.apply(lambda r: search_q.lower() in r.astype(str).str.lower().values, axis=1)]
    if area_f != "كل المناطق" and area_col:
        filtered_df = filtered_df[filtered_df[area_col] == area_f]

    # عرض الكروت
    items = 6
    total_pages = max(1, math.ceil(len(filtered_df) / items))
    if st.session_state.p_page >= total_pages: st.session_state.p_page = 0
    
    curr = filtered_df.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

    for i in range(0, len(curr), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(curr):
                row = curr.iloc[i+j]
                with cols[j]:
                    # جلب القيم بأمان بغض النظر عن اسم العمود في الشيت
                    p_name = get_val(row, ['Project Name', 'Project', 'المشروع', 'Projects'])
                    dev_name = get_val(row, ['Developer', 'المطور', 'Company'])
                    area_name = get_val(row, ['Area', 'المنطقة', 'Location'])
                    unit_type = get_val(row, ['شقق/فيلات', 'Type', 'النوع', 'unit type'])
                    size = get_val(row, ['Size (Acres)', 'المساحة', 'Size'])

                    st.markdown(f"""
                        <div class="pro-card">
                            <h3 style="color:#f59e0b;">{p_name}</h3>
                            <p style="color:#888;">{dev_name}</p>
                            <hr style="border-color:#222">
                            <div style="text-align:right; font-size:14px;">
                                <p>📍 المنطقة: <span class="stat-value">{area_name}</span></p>
                                <p>🏠 النوع: <span class="stat-value">{unit_type}</span></p>
                                <p>📏 المساحة: <span class="stat-value">{size}</span></p>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

    # التنقل
    st.write("---")
    n1, n2, n3 = st.columns([1, 2, 1])
    if n3.button("الصفحة التالية ⬅️") and st.session_state.p_page < total_pages -1:
        st.session_state.p_page += 1
        st.rerun()
    n2.markdown(f"<p style='text-align:center;'>{st.session_state.p_page + 1} / {total_pages}</p>", unsafe_allow_html=True)
    if n1.button("➡️ الصفحة السابقة") and st.session_state.p_page > 0:
        st.session_state.p_page -= 1
        st.rerun()

elif selected == "🏢 المطورين":
    st.info("قسم المطورين جاهز.")
elif selected == "🛠️ الأدوات":
    st.info("الأدوات جاهزة.")
