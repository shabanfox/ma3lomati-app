import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# --- 1. إعدادات الصفحة والتصميم الفخم ---
st.set_page_config(page_title="منصة معلوماتي PRO 2026", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* الهيدر وزر الخروج */
    .stButton > button[key="logout_btn"] { background-color: #ff4b4b !important; color: white !important; border: none !important; padding: 5px 20px !important; border-radius: 8px !important; width: auto !important; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 20px 20px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .header-title { font-weight: 900; font-size: 32px !important; color: #f59e0b; margin: 0; }

    /* الكروت الاحترافية */
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 5px solid #f59e0b; 
        border-radius: 15px; padding: 20px; margin-bottom: 10px; text-align: center; 
        min-height: 260px; display: flex; flex-direction: column; justify-content: space-between;
        transition: 0.3s ease-in-out;
    }
    .pro-card:hover { transform: translateY(-5px); border-color: #f59e0b; box-shadow: 0 0 20px rgba(245, 158, 11, 0.2); }
    .card-title { color: #f59e0b; font-size: 20px !important; font-weight: 900; margin-bottom: 10px; }
    
    /* تفاصيل المطور المنسدلة */
    .dev-box { background: #0d0d0d; border: 2px solid #f59e0b; border-radius: 15px; padding: 25px; margin-bottom: 25px; animation: fadeIn 0.5s; }
    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }

    .stat-row { display: flex; justify-content: space-between; border-bottom: 1px solid #1a1a1a; padding: 8px 0; font-size: 14px; }
    .stat-label { color: #888; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    
    /* الأزرار والمدخلات */
    .stButton button { background: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; border-radius: 8px; }
    .stButton button:hover { background: #f59e0b !important; color: #000 !important; }
    div[data-baseweb="select"], input { background-color: #111 !important; color: white !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# --- 2. محرك البيانات الذكي ---
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# وظائف مساعدة للتعامل مع الأعمدة
def get_c(row, names):
    for n in names:
        if n in row: return row[n]
    return "غير متوفر"

# --- 3. الهيدر وزر الخروج ---
top_col1, top_col2 = st.columns([10, 1.5])
with top_col2:
    if st.button("تسجيل الخروج", key="logout_btn"):
        st.session_state.clear()
        st.rerun()

st.markdown('<div class="main-header"><h1 class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)

# --- 4. القائمة الرئيسية ---
selected = option_menu(
    menu_title=None, 
    options=["🛠️ الأدوات", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building-fill", "person-badge-fill"], 
    orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# إدارة الـ State
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'active_dev' not in st.session_state: st.session_state.active_dev = None

# --- 🏗️ شاشة المشاريع (مع تحديث زر المنطقة) ---
if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    
    # الفلاتر
    f_c1, f_c2 = st.columns([2, 1])
    search_q = f_c1.text_input("🔍 ابحث (مشروع/مطور)...", placeholder="ادخل نص البحث هنا...")
    
    area_col_name = 'Area' if 'Area' in df.columns else ('المنطقة' if 'المنطقة' in df.columns else None)
    if area_col_name:
        unique_areas = ["الكل"] + sorted(df[area_col_name].unique().tolist())
        area_choice = f_c2.selectbox("📍 فلتر المنطقة", unique_areas)
    else:
        area_choice = "الكل"

    # معالجة الفلترة
    filtered_df = df.copy()
    if search_q:
        filtered_df = filtered_df[filtered_df.apply(lambda r: search_q.lower() in r.astype(str).str.lower().values, axis=1)]
    if area_choice != "الكل" and area_col_name:
        filtered_df = filtered_df[filtered_df[area_col_name] == area_choice]

    # العرض بنظام الكروت
    items = 6
    total_p = max(1, math.ceil(len(filtered_df) / items))
    if st.session_state.p_page >= total_p: st.session_state.p_page = 0
    
    curr = filtered_df.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

    for i in range(0, len(curr), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(curr):
                row = curr.iloc[i+j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="pro-card">
                            <div>
                                <div class="card-title">{get_c(row, ['Project Name', 'المشروع'])}</div>
                                <div style="color:#666; font-size:13px; margin-bottom:15px;">{get_c(row, ['Developer', 'المطور'])}</div>
                                <div class="stat-row"><span class="stat-label">📍 المنطقة:</span><span class="stat-val">{get_c(row, ['Area', 'المنطقة'])}</span></div>
                                <div class="stat-row"><span class="stat-label">🏠 النوع:</span><span class="stat-val">{get_c(row, ['شقق/فيلات', 'النوع'])}</span></div>
                                <div class="stat-row"><span class="stat-label">📏 المساحة:</span><span class="stat-val">{get_c(row, ['Size (Acres)', 'المساحة'])} فدان</span></div>
                            </div>
                            <div style="background:rgba(245,158,11,0.1); padding:10px; border-radius:8px; font-size:11px; color:#f59e0b; margin-top:10px; border:1px dashed #f59e0b;">
                                ⭐ {get_c(row, ['Competitive Advantage', 'المميزات'])[:75]}...
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
    
    # التنقل
    st.write("---")
    n1, n2, n3 = st.columns([1, 2, 1])
    if n3.button("التالي ⬅️", key="p_next"): st.session_state.p_page += 1; st.rerun()
    n2.markdown(f"<p style='text-align:center;'>{st.session_state.p_page + 1} / {total_p}</p>", unsafe_allow_html=True)
    if n1.button("➡️ السابق", key="p_prev") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    devs_list = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    
    if st.session_state.active_dev:
        info = devs_list[devs_list['Developer'] == st.session_state.active_dev].iloc[0]
        st.markdown(f"""
            <div class="dev-box">
                <h2 style="color:#f59e0b;">🏢 {info['Developer']}</h2>
                <p><b>👤 رئيس مجلس الإدارة:</b> {info['Owner']}</p>
                <hr style="border-color:#333">
                <p style="color:#ccc; line-height:1.7;">{info['Detailed_Info']}</p>
                <button onclick="window.location.reload()" style="background:#f59e0b; color:#000; border:none; padding:5px 15px; border-radius:5px; cursor:pointer; font-weight:bold;">إغلاق التفاصيل</button>
            </div>
        """, unsafe_allow_html=True)
        if st.button("❌ إغلاق ملف الشركة"): st.session_state.active_dev = None; st.rerun()

    st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    search_d = st.text_input("🔍 ابحث عن شركة مطورة...")
    if search_d: devs_list = devs_list[devs_list['Developer'].str.contains(search_d, case=False)]

    for i in range(0, len(devs_list), 3):
        cols = st.columns(3)
        for j in range(3):
            if i+j < len(devs_list):
                row = devs_list.iloc[i+j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="pro-card" style="min-height:150px;">
                            <div class="card-title">{row['Developer']}</div>
                            <div style="color:#888; font-size:14px;">المالك: {row['Owner']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"🔍 فتح ملف {row['Developer']}", key=f"dev_{row['Developer']}"):
                        st.session_state.active_dev = row['Developer']; st.rerun()

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ الأدوات":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حزمة أدوات البروكر</h2>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["💰 حاسبة الأقساط", "📐 محول المساحة"])
    
    with t1:
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        p = st.number_input("سعر الوحدة الإجمالي", value=2000000)
        y = st.slider("سنوات التقسيط", 1, 15, 7)
        st.markdown(f"<h1 style='color:#f59e0b; text-align:center;'>{p/(y*12):,.0f} ج.م / شهري</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with t2:
        st.markdown("<div class='pro-card'>", unsafe_allow_html=True)
        acre = st.number_input("المساحة بالفدان", value=1.0)
        st.markdown(f"<h1 style='color:#f59e0b; text-align:center;'>{acre*4200:,.0f} متر مربع</h1>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
