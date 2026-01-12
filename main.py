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
    
    .stButton > button[key="logout_btn"] { background-color: #ff4b4b !important; color: white !important; border: none !important; padding: 5px 20px !important; border-radius: 5px !important; }
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 0 0 15px 15px; border-right: 12px solid #f59e0b; text-align: center; margin-bottom: 25px; }
    .header-title { font-weight: 900; font-size: 30px !important; color: #f59e0b; margin: 0; }

    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 20px; text-align: center; height: 100%; min-height: 200px;
    }
    .detail-box {
        background: #0d0d0d; border-right: 6px solid #f59e0b; border-radius: 12px;
        padding: 25px; color: #eee; height: 100%; border: 1px solid #222; border-right: 6px solid #f59e0b;
    }
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; margin-bottom: 10px; }
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; font-weight: bold; }
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

# 4. الهيدر
t_c1, t_c2 = st.columns([10, 1.2])
with t_c2:
    if st.button("خروج", key="logout_btn"): st.session_state.clear(); st.rerun()
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-badge"], orientation="horizontal",
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

# إدارة الحالات
if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'active_dev_idx' not in st.session_state: st.session_state.active_dev_idx = None

# --- 🏢 شاشة المطورين (إصلاح الـ NameError ونظام التفاصيل) ---
if selected == "🏢 المطورين":
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    
    search_d = st.text_input("🔍 ابحث عن مطور...", placeholder="اكتب اسم الشركة هنا...")
    if search_d: devs = devs[devs['Developer'].str.contains(search_d, case=False)]

    items = 9
    total_d = max(1, math.ceil(len(devs) / items))
    start_idx = st.session_state.d_page * items
    end_idx = start_idx + items
    curr_devs = devs.iloc[start_idx:end_idx].reset_index()

    # معالجة العرض
    for i in range(0, len(curr_devs), 3):
        # التحقق إذا كان أحد العناصر في هذا الصف مفتوحاً
        row_indices = curr_devs['index'].iloc[i:i+3].tolist()
        
        active_in_row = st.session_state.active_dev_idx in row_indices
        
        if active_in_row:
            # عرض العنصر المفتوح فقط في هذا الصف بتنسيق (كارت + تفاصيل)
            target_idx = st.session_state.active_dev_idx
            row_data = devs.iloc[target_idx]
            proj_list = df[df['Developer'] == row_data['Developer']]['Project Name'].unique()
            
            st.markdown("---")
            c_card, c_desc = st.columns([0.3, 0.7])
            with c_card:
                st.markdown(f"""
                    <div class="pro-card">
                        <div class="card-title">{row_data['Developer']}</div>
                        <p style="color:#888; font-size:14px;">{row_data['Owner']}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("⬅️ إغلاق التفاصيل", key=f"cls_{target_idx}"):
                    st.session_state.active_dev_idx = None
                    st.rerun()
            with c_desc:
                st.markdown(f"""
                    <div class="detail-box">
                        <h3 style="color:#f59e0b; margin-top:0;">🏢 ملف شركة {row_data['Developer']}</h3>
                        <p><b>👤 المالك:</b> {row_data['Owner']}</p>
                        <p><b>📜 النبذة:</b> {row_data['Detailed_Info']}</p>
                        <p style="background:#1a150b; padding:10px; border-radius:8px; border:1px dashed #f59e0b;">
                        <b>🏗️ المشاريع:</b> {', '.join(proj_list)}
                        </p>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
        else:
            # العرض العادي (3 كروت في الصف)
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(curr_devs):
                    item = curr_devs.iloc[i + j]
                    idx_original = item['index']
                    with cols[j]:
                        st.markdown(f"""
                            <div class="pro-card">
                                <div class="card-title">{item['Developer']}</div>
                                <div style="color:#888; font-size:13px; margin:10px 0;">{item['Owner'][:50]}...</div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("🔍 عرض التفاصيل", key=f"btn_{idx_original}"):
                            st.session_state.active_dev_idx = idx_original
                            st.rerun()

    # أزرار التنقل
    st.write("---")
    d1, d2, d3 = st.columns([1, 1, 1])
    if d3.button("التالي ⬅️") and st.session_state.d_page < total_d-1: 
        st.session_state.d_page += 1; st.session_state.active_dev_idx = None; st.rerun()
    d2.markdown(f"<center>صفحة {st.session_state.d_page+1} من {total_d}</center>", unsafe_allow_html=True)
    if d1.button("➡️ السابق") and st.session_state.d_page > 0: 
        st.session_state.d_page -= 1; st.session_state.active_dev_idx = None; st.rerun()

# --- بقية الأقسام ---
elif selected == "🏗️ المشاريع":
    st.info("قسم المشاريع جاهز.")
elif selected == "🛠️ أدوات البروكر":
    st.info("قسم الأدوات جاهز.")
