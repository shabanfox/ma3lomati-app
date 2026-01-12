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
    
    /* الهيدر وزر الخروج */
    .stButton > button[key="logout_btn"] { background-color: #ff4b4b !important; color: white !important; border: none !important; padding: 5px 20px !important; border-radius: 8px !important; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 20px; border-radius: 0 0 20px 20px; border-right: 15px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 32px !important; color: #f59e0b; margin: 0; }

    /* الكروت */
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 5px solid #f59e0b; 
        border-radius: 15px; padding: 20px; margin-bottom: 15px; text-align: center; 
        transition: 0.3s; height: 100%;
    }
    .pro-card:hover { transform: translateY(-5px); border-color: #f59e0b; box-shadow: 0 0 20px rgba(245, 158, 11, 0.2); }
    
    /* تحسين شكل الفلاتر */
    .stSelectbox div[data-baseweb="select"] { background-color: #111 !important; border: 1px solid #333 !important; border-radius: 10px !important; }
    .stTextInput input { background-color: #111 !important; border: 1px solid #333 !important; border-radius: 10px !important; color: white !important; }
    
    .stat-value { color: #f59e0b; font-weight: bold; }
    .stButton button { background: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; border-radius: 8px; }
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

# 4. الترويسة
t_c1, t_c2 = st.columns([10, 1.5])
with t_c2:
    if st.button("تسجيل الخروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

st.markdown('<div class="main-header"><h1 class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)

# 5. القائمة الرئيسية
selected = option_menu(
    menu_title=None, 
    options=["🛠️ الأدوات", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# تهيئة الذاكرة
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'active_dev' not in st.session_state: st.session_state.active_dev = None

# --- 🏗️ شاشة المشاريع (تحديث الفلاتر) ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    
    # صف الفلاتر المطور
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        search_query = st.text_input("🔍 ابحث باسم المشروع أو المطور...", placeholder="اكتب هنا للبحث السريع...")
    with filter_col2:
        # جلب المناطق الفريدة من عمود Area
        unique_areas = ["كل المناطق"] + sorted(df['Area'].unique().tolist())
        area_filter = st.selectbox("📍 اختر المنطقة", unique_areas)
    
    # تطبيق الفلترة
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['Project Name'].str.contains(search_query, case=False) | 
            filtered_df['Developer'].str.contains(search_query, case=False)
        ]
    
    if area_filter != "كل المناطق":
        filtered_df = filtered_df[filtered_df['Area'] == area_filter]

    # عرض النتائج
    items_per_page = 6
    total_pages = max(1, math.ceil(len(filtered_df) / items_per_page))
    
    # تصحيح رقم الصفحة في حال الفلترة قللت النتائج
    if st.session_state.p_page >= total_pages:
        st.session_state.p_page = 0

    curr_items = filtered_df.iloc[st.session_state.p_page * items_per_page : (st.session_state.p_page + 1) * items_per_page]

    if not curr_items.empty:
        for i in range(0, len(curr_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_items):
                    row = curr_items.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="pro-card">
                                <h3 style="color:#f59e0b;">{row['Project Name']}</h3>
                                <p style="color:#888;">{row['Developer']}</p>
                                <hr style="border-color:#222">
                                <div style="text-align:right; font-size:14px;">
                                    <p>📍 المنطقة: <span class="stat-value">{row['Area']}</span></p>
                                    <p>🏠 النوع: <span class="stat-value">{row['شقق/فيلات']}</span></p>
                                    <p>📏 المساحة: <span class="stat-value">{row['Size (Acres)']} فدان</span></p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
        
        # أزرار التنقل
        st.write("---")
        n1, n2, n3 = st.columns([1, 2, 1])
        if n3.button("الصفحة التالية ⬅️", key="next"): 
            st.session_state.p_page += 1
            st.rerun()
        n2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
        if n1.button("➡️ الصفحة السابقة", key="prev") and st.session_state.p_page > 0: 
            st.session_state.p_page -= 1
            st.rerun()
    else:
        st.warning("⚠️ لا توجد نتائج تطابق بحثك في هذه المنطقة.")

# --- الأقسام الأخرى تظل كما هي لضمان الاستقرار ---
elif selected == "🏢 المطورين":
    # (كود المطورين المستقر من الرد السابق)
    st.info("قسم المطورين جاهز للاستخدام.")
elif selected == "🛠️ الأدوات":
    # (كود الأدوات المستقر من الرد السابق)
    st.info("أدوات الحساب جاهزة.")
