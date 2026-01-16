import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - استلهام روح تصميم Nawy
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #f4f7f6; }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    /* الهيدر العلوي بستايل Nawy */
    .top-bar {
        background: white; padding: 15px 30px; border-bottom: 1px solid #e1e8ed;
        display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;
    }

    /* كروت المطورين (المربعات) بستايل Nawy */
    div.stButton > button[key*="sq_"] {
        background-color: #ffffff !important;
        color: #003049 !important; /* لون أزرق غامق نوي */
        border: 1px solid #e1e8ed !important;
        border-radius: 16px !important; /* حواف دائرية ناعمة */
        width: 180px !important;
        height: 180px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05) !important; /* ظل خفيف جداً */
        transition: all 0.3s ease-in-out !important;
        margin: 10px auto !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button[key*="sq_"]:hover {
        border-color: #f59e0b !important; /* لمسة ذهبية عند الهوفر */
        box-shadow: 0 8px 20px rgba(0,0,0,0.1) !important; /* ظل أقوى عند الهوفر */
        transform: translateY(-5px) !important;
        color: #f59e0b !important;
    }

    /* زر الخروج الصغير */
    div.stButton > button[key*="logout_btn"] {
        background-color: transparent !important; color: #666 !important;
        border: 1px solid #ddd !important; border-radius: 8px !important;
        padding: 5px 15px !important; font-size: 13px !important; height: 35px !important;
    }

    /* أزرار التنقل */
    div.stButton > button[key*="nav_"] {
        background: white !important; color: #003049 !important;
        border: 1px solid #e1e8ed !important; border-radius: 50px !important;
        width: 100px !important; height: 35px !important; font-size: 14px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try: return pd.read_csv(u_d).fillna("").astype(str)
    except: return pd.DataFrame()

df_d = load_data()

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#003049;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("Passcode", type="password", key="main_pass") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر (Nawy Style)
t_col1, t_col2 = st.columns([0.85, 0.15])
with t_col1:
    st.markdown('<p style="color:#003049; font-weight:900; font-size:24px; margin:0;">MA3LOMATI</p>', unsafe_allow_html=True)
with t_col2:
    if st.button("تسجيل خروج", key="logout_btn"):
        st.session_state.auth = False; st.rerun()

# 7. المحتوى
if st.session_state.selected_dev:
    # --- صفحة التفاصيل ---
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    
    if st.button("⬅️ العودة للرئيسية", key="nav_back"):
        st.session_state.selected_dev = None; st.rerun()
    
    st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:20px; border:1px solid #e1e8ed; margin-top:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
            <h1 style="color:#003049; border-right: 5px solid #f59e0b; padding-right:15px;">{dev_name}</h1>
            <p style="color:#666; font-size:20px;">👤 المالك: {dev_info.get('Owner')}</p>
            <hr style="opacity:0.1;">
            <div style="color:#444; font-size:18px; line-height:1.9;">
                {dev_info.get('Detailed_Info')}
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- القائمة الرئيسية ---
    menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
        icons=["tools", "building", "person-vcard"], 
        default_index=2, orientation="horizontal",
        styles={
            "container": {"background-color": "#fff", "border-radius": "10px", "padding": "5px", "border": "1px solid #e1e8ed"},
            "nav-link-selected": {"background-color": "#003049", "color": "#fff"}
        }
    )

    if menu == "المطورين":
        # المساحة 60% يمين كما طلبت
        main_col, empty_col = st.columns([0.6, 0.4])
        with main_col:
            search = st.text_input("🔍 ابحث عن المطور العقاري", placeholder="مثلاً: إعمار، طلعت مصطفى...", key="search_nawy")
            dff = df_d.copy()
            if search: dff = dff[dff['Developer'].str.contains(search, case=False)]
            
            limit = 8
            total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
            items = dff.iloc[st.session_state.d_idx*limit : (st.session_state.d_idx+1)*limit]

            # شبكة المربعات (Nawy Style)
            for i in range(0, len(items), 2):
                cols = st.columns(2)
                with cols[0]:
                    n1 = items.iloc[i].get('Developer')
                    if st.button(n1, key=f"sq_{i}"):
                        st.session_state.selected_dev = n1; st.rerun()
                with cols[1]:
                    if i + 1 < len(items):
                        n2 = items.iloc[i+1].get('Developer')
                        if st.button(n2, key=f"sq_{i+1}"):
                            st.session_state.selected_dev = n2; st.rerun()

            # أزرار التنقل السفلية
            st.write("---")
            nav_c1, nav_c2, nav_c3 = st.columns([1, 2, 1])
            with nav_c1:
                if st.session_state.d_idx > 0:
                    if st.button("السابق", key="nav_prev"): 
                        st.session_state.d_idx -= 1; st.rerun()
            with nav_c2:
                st.markdown(f"<p style='text-align:center; color:#666; font-size:14px;'>{st.session_state.d_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            with nav_c3:
                if (st.session_state.d_idx + 1) * limit < len(dff):
                    if st.button("التالي", key="nav_next"): 
                        st.session_state.d_idx += 1; st.rerun()
