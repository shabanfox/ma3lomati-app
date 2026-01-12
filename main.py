import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - تحسين شكل الفلاتر
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 20px; border-radius: 0 0 20px 20px; border-right: 15px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 32px !important; color: #f59e0b; margin: 0; }

    /* استايل الفلاتر المحدث */
    .stSelectbox label, .stTextInput label { color: #f59e0b !important; font-weight: bold !important; margin-bottom: 8px !important; }
    div[data-baseweb="select"] { background-color: #111 !important; border: 1px solid #333 !important; border-radius: 10px !important; }
    div[data-baseweb="select"]:hover { border-color: #f59e0b !important; }
    input { background-color: #111 !important; color: white !important; border-radius: 10px !important; }

    .pro-card { background: #111; border: 1px solid #222; border-top: 5px solid #f59e0b; border-radius: 15px; padding: 20px; margin-bottom: 15px; text-align: center; height: 100%; transition: 0.3s; }
    .pro-card:hover { border-color: #f59e0b; transform: translateY(-5px); }
    .stat-label { color: #888; font-size: 13px; }
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

# دوال مساعدة للبحث الآمن عن الأعمدة
def find_column(df, possible_names):
    for name in possible_names:
        if name in df.columns: return name
    return None

def get_row_val(row, possible_names):
    for name in possible_names:
        if name in row: return row[name]
    return "غير متوفر"

# 4. الواجهة الرئيسية
st.markdown('<div class="main-header"><h1 class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ الأدوات", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-vcard"], 
                       orientation="horizontal", 
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

if 'p_page' not in st.session_state: st.session_state.p_page = 0

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    st.markdown("<h3 style='color:#f59e0b; margin-bottom:20px;'>🏗️ دليل المشاريع العقارية</h3>", unsafe_allow_html=True)
    
    # تحديد عمود المنطقة
    area_col = find_column(df, ['Area', 'المنطقة', 'الموقع', 'Location'])
    
    # صف البحث والفلاتر
    f_col1, f_col2 = st.columns([2, 1])
    with f_col1:
        search_q = st.text_input("🔍 ابحث باسم المشروع أو المطور...", placeholder="اكتب للبحث...")
    
    with f_col2:
        if area_col:
            unique_areas = ["الكل"] + sorted(df[area_col].unique().tolist())
            area_choice = st.selectbox("📍 تصفية حسب المنطقة", unique_areas)
        else:
            area_choice = "الكل"
            st.warning("عمود المنطقة غير موجود")

    # تطبيق الفلترة
    filtered_df = df.copy()
    if search_q:
        filtered_df = filtered_df[filtered_df.apply(lambda r: search_q.lower() in r.astype(str).str.lower().values, axis=1)]
    if area_choice != "الكل" and area_col:
        filtered_df = filtered_df[filtered_df[area_col] == area_choice]

    # عرض النتائج
    items_per_page = 6
    total_pages = max(1, math.ceil(len(filtered_df) / items_per_page))
    
    # تصفير الصفحة عند تغيير الفلتر
    if st.session_state.p_page >= total_pages: st.session_state.p_page = 0

    curr_items = filtered_df.iloc[st.session_state.p_page * items_per_page : (st.session_state.p_page + 1) * items_per_page]

    if not curr_items.empty:
        for i in range(0, len(curr_items), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_items):
                    row = curr_items.iloc[i+j]
                    with cols[j]:
                        p_name = get_row_val(row, ['Project Name', 'Project', 'المشروع'])
                        dev_name = get_row_val(row, ['Developer', 'المطور'])
                        loc_name = get_row_val(row, ['Area', 'المنطقة'])
                        type_name = get_row_val(row, ['شقق/فيلات', 'النوع', 'Type'])
                        
                        st.markdown(f"""
                            <div class="pro-card">
                                <h3 style="color:#f59e0b; margin-bottom:5px;">{p_name}</h3>
                                <p style="color:#666; font-size:14px;">{dev_name}</p>
                                <hr style="border-color:#222">
                                <div style="text-align:right;">
                                    <p><span class="stat-label">📍 المنطقة:</span> <span class="stat-value">{loc_name}</span></p>
                                    <p><span class="stat-label">🏠 النوع:</span> <span class="stat-value">{type_name}</span></p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
        
        # أزرار التنقل
        st.write("---")
        n1, n2, n3 = st.columns([1, 2, 1])
        if n3.button("التالي ⬅️"): 
            st.session_state.p_page += 1
            st.rerun()
        n2.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_page + 1} من {total_pages}</p>", unsafe_allow_html=True)
        if n1.button("➡️ السابق") and st.session_state.p_page > 0: 
            st.session_state.p_page -= 1
            st.rerun()
    else:
        st.error("❌ لا توجد نتائج تطابق بحثك.")

elif selected == "🏢 المطورين":
    st.info("قسم المطورين جاهز.")
elif selected == "🛠️ الأدوات":
    st.info("قسم الأدوات جاهز.")
