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
        border-radius: 12px; padding: 20px; text-align: center; height: 100%;
    }
    .detail-box {
        background: #0d0d0d; border-right: 4px solid #f59e0b; border-radius: 10px;
        padding: 20px; color: #eee; height: 100%; animation: slideIn 0.3s ease-out;
    }
    @keyframes slideIn { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
    
    .card-title { color: #f59e0b; font-size: 19px !important; font-weight: 900; }
    .stButton button { background-color: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; border-radius: 8px; }
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

# 4. زر الخروج والهيدر
t_c1, t_c2 = st.columns([10, 1])
with t_c2:
    if st.button("خروج", key="logout_btn"): st.session_state.clear(); st.rerun()

st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
                       icons=["tools", "building", "person-badge"], orientation="horizontal",
                       styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}})

if 'd_page' not in st.session_state: st.session_state.d_page = 0
if 'active_dev_id' not in st.session_state: st.session_state.active_dev_id = None

# --- 🏢 شاشة المطورين (التفاصيل بجانب الكارت) ---
if selected == "🏢 المطورين":
    devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
    st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين</h2>", unsafe_allow_html=True)
    
    search_d = st.text_input("🔍 ابحث عن مطور...")
    if search_d: devs = devs[devs['Developer'].str.contains(search_d, case=False)]

    items = 9
    total_d = max(1, math.ceil(len(devs) / items))
    curr_devs = devs.iloc[st.session_state.d_page * items : (st.session_state.d_page + 1) * items]

    for idx, row in curr_devs.iterrows():
        # إذا كان هذا المطور هو النشط، نفتح تقسيم خاص (كارت + تفاصيل)
        if st.session_state.active_dev_id == idx:
            st.markdown("---")
            c_card, c_desc = st.columns([0.3, 0.7]) # الكارت 30% والتفاصيل 70% بجانبه
            with c_card:
                st.markdown(f"""
                    <div class="pro-card">
                        <div class="card-title">{row['Developer']}</div>
                        <p style="color:#888;">{row['Owner']}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("⬅️ إغلاق", key=f"close_{idx}"):
                    st.session_state.active_dev_id = None
                    st.rerun()
            with c_desc:
                # جلب مشاريع هذا المطور من الجدول الرئيسي
                proj_list = df[df['Developer'] == row['Developer']]['Project Name'].unique()
                st.markdown(f"""
                    <div class="detail-box">
                        <h3 style="color:#f59e0b; margin-top:0;">🏢 تفاصيل شركة {row['Developer']}</h3>
                        <p><b>👤 رئيس مجلس الإدارة:</b> {row['Owner']}</p>
                        <p><b>📜 نبذة عن الشركة:</b><br>{row['Detailed_Info']}</p>
                        <p><b>🏗️ أهم المشاريع:</b> {', '.join(proj_list)}</p>
                    </div>
                """, unsafe_allow_html=True)
            st.markdown("---")
        
        # إذا لم يكن نشطاً، يتم عرضه في الشبكة العادية (3 في الصف)
        else:
            # نفتح صف جديد كل 3 عناصر
            if idx % 3 == 0:
                cols = st.columns(3)
            
            with cols[int(idx % 3)]:
                st.markdown(f"""
                    <div class="pro-card" style="margin-bottom:15px;">
                        <div class="card-title">{row['Developer']}</div>
                        <div style="background:#000; padding:10px; border-radius:8px; margin:10px 0;">
                            <small style="color:#666;">المالك</small><br>
                            <span style="color:#fff;">{row['Owner']}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("🔍 عرض التفاصيل", key=f"btn_{idx}"):
                    st.session_state.active_dev_id = idx
                    st.rerun()

    # أزرار التنقل
    st.write("---")
    d1, d2, d3 = st.columns([1, 1, 1])
    if d3.button("التالي ⬅️") and st.session_state.d_page < total_d-1: st.session_state.d_page += 1; st.rerun()
    d2.markdown(f"<center>{st.session_state.d_page+1} / {total_d}</center>", unsafe_allow_html=True)
    if d1.button("➡️ السابق") and st.session_state.d_page > 0: st.session_state.d_page -= 1; st.rerun()

# --- باقي الأقسام (المشاريع والأدوات) تظل كما هي ---
elif selected == "🏗️ المشاريع":
    st.info("قسم المشاريع يعمل بنظام الشبكة 9.")
elif selected == "🛠️ أدوات البروكر":
    st.info("قسم الأدوات يعمل بنظام 70/30.")
