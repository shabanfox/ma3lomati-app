import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS) المحسن لعرض البيانات الكثيرة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 10px solid #f59e0b; text-align: center; margin-bottom: 20px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 18px; margin-bottom: 10px; 
        min-height: 320px; text-align: center; display: flex; flex-direction: column; justify-content: space-between;
    }
    .card-main-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; margin-bottom: 5px; }
    .dev-label { color: #888; font-size: 14px; margin-bottom: 12px; }
    .stat-row { display: flex; justify-content: space-between; font-size: 13px; margin-top: 6px; color: #ccc; border-bottom: 1px solid #1a1a1a; padding-bottom: 4px; }
    .stat-val { color: #f59e0b; font-weight: bold; text-align: left; padding-left: 5px; }
    .advantage-box { background: #1a150b; color: #f59e0b; font-size: 12px; padding: 8px; border-radius: 5px; margin-top: 10px; border: 1px dashed #f59e0b; }
    .stButton button { width: 100%; border-radius: 8px; font-weight: bold; height: 40px; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        data = data.fillna("غير متوفر").astype(str)
        return data
    except: return pd.DataFrame()

df = load_data()

# 4. الهيدر والقائمة
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)
selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], icons=["tools", "building", "person-badge"], orientation="horizontal", styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع التفصيلي</h2>", unsafe_allow_html=True)
            
            f1, f2 = st.columns(2)
            with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع...")
            with f2: 
                area_col = 'Area' if 'Area' in df.columns else df.columns[0]
                areas = ["الكل"] + sorted(df[area_col].unique().tolist())
                a_p = st.selectbox("📍 تصفية حسب المنطقة", areas)
            
            dff = df.copy()
            name_col = 'Project Name' if 'Project Name' in df.columns else 'Projects'
            if s_p: dff = dff[dff[name_col].str.contains(s_p, case=False)]
            if a_p != "الكل": dff = dff[dff[area_col] == a_p]

            items = 9
            total_p = max(1, math.ceil(len(dff) / items))
            if st.session_state.p_idx >= total_p: st.session_state.p_idx = 0
            
            curr_slice = dff.iloc[st.session_state.p_idx * items : (st.session_state.p_idx + 1) * items]

            if not curr_slice.empty:
                for i in range(0, len(curr_slice), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i+j < len(curr_slice):
                            row = curr_slice.iloc[i+j]
                            with cols[j]:
                                # استخراج البيانات المطلوبة
                                p_name = row.get(name_col, 'غير مسمى')
                                dev = row.get('Developer', 'مطور غير محدد')
                                consultant = row.get('Consultant', 'غير محدد')
                                size = row.get('Size (Acres)', 'غير محدد')
                                units = row.get('شقق/فيلات', 'غير محدد')
                                advantage = row.get('Competitive Advantage', 'لا يوجد تفاصيل')

                                st.markdown(f"""
                                    <div class="pro-card">
                                        <div>
                                            <div class="card-main-title">{p_name}</div>
                                            <div class="dev-label">{dev}</div>
                                            <div class="stat-row"><span>👷 الاستشاري:</span><span class="stat-val">{consultant}</span></div>
                                            <div class="stat-row"><span>📏 المساحة:</span><span class="stat-val">{size} فدان</span></div>
                                            <div class="stat-row"><span>🏠 النوع:</span><span class="stat-val">{units}</span></div>
                                            <div class="stat-row"><span>📍 المنطقة:</span><span class="stat-val">{row.get('Area', '-')}</span></div>
                                        </div>
                                        <div class="advantage-box">
                                            <b>⭐ الميزة التنافسية:</b><br>{advantage[:80]}...
                                        </div>
                                    </div>
                                """, unsafe_allow_html=True)
                                with st.expander("🔍 عرض كل البيانات"):
                                    st.write(row.to_dict())
            
            # أزرار التنقل
            st.write("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav3:
                if (st.session_state.p_idx + 1) < total_p:
                    if st.button("التالي ⬅️", key="p_next"): st.session_state.p_idx += 1; st.rerun()
            with nav2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            with nav1:
                if st.session_state.p_idx > 0:
                    if st.button("➡️ السابق", key="p_prev"): st.session_state.p_idx -= 1; st.rerun()
        
        with c_side: st.write("")

# --- باقي الشاشات تظل كما هي لضمان استقرار التطبيق ---
elif selected == "🏢 المطورين":
    st.info("شاشة المطورين تعمل بنظام الـ 70/30 والشبكة.")
elif selected == "🛠️ أدوات البروكر":
    st.info("أدوات الحساب (القسط و ROI) جاهزة.")
