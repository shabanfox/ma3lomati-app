import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - محاكاة Nawy بالحرف
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #f0f2f5; }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    /* زر الخروج الصغير في أعلى اليسار */
    .stButton > button[key="logout_btn"] {
        position: fixed; top: 10px; left: 10px; z-index: 1000;
        height: 30px !important; width: 80px !important; font-size: 12px !important;
        background: white !important; color: red !important; border: 1px solid #ddd !important;
    }

    /* تصميم الكارت المربع 1:1 بستايل Nawy */
    div.stButton > button[key*="sq_"] {
        background-color: white !important;
        border: 1px solid #e1e8ed !important;
        border-radius: 12px !important;
        width: 220px !important; /* حجم ثابت للمربع */
        height: 220px !important; /* حجم ثابت للمربع */
        display: block !important;
        padding: 0 !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease !important;
        margin: 10px auto !important;
    }

    div.stButton > button[key*="sq_"]:hover {
        transform: translateY(-8px) !important;
        box-shadow: 0 12px 24px rgba(0,0,0,0.1) !important;
        border-color: #003049 !important;
    }

    /* تنسيق اسم المطور داخل الكارت */
    div.stButton > button[key*="sq_"] p {
        color: #003049 !important;
        font-weight: 700 !important;
        font-size: 18px !important;
        margin-top: 80px !important; /* لجعله في المنتصف تقريباً */
    }

    /* أزرار التنقل الصغيرة */
    div.stButton > button[key*="nav_"] {
        height: 35px !important; width: 90px !important; font-size: 13px !important;
        background: white !important; border-radius: 20px !important;
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

# 5. زر الخروج الثابت
if st.session_state.auth:
    if st.button("تسجيل خروج", key="logout_btn"):
        st.session_state.auth = False; st.rerun()

# 6. الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#003049;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("Passcode", type="password", key="p_in") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 7. المنطق الرئيسي
if st.session_state.selected_dev:
    # صفحة التفاصيل (Nawy Style)
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    
    if st.button("⬅️ عودة للقائمة", key="nav_back"):
        st.session_state.selected_dev = None; st.rerun()
    
    st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:20px; border:1px solid #e1e8ed; margin-top:20px;">
            <h1 style="color:#003049; border-bottom:3px solid #f59e0b; display:inline-block;">{dev_name}</h1>
            <p style="margin-top:20px; font-size:20px; color:#555;">{dev_info.get('Detailed_Info')}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # القائمة بستايل Nawy
    st.markdown('<h2 style="color:#003049; text-align:right; margin-bottom:20px;">المطورين العقاريين</h2>', unsafe_allow_html=True)
    
    # 60% يمين
    main_col, empty_col = st.columns([0.6, 0.4])
    
    with main_col:
        search = st.text_input("🔍 ابحث عن مطورك المفضل...", key="s_nawy")
        dff = df_d.copy()
        if search: dff = dff[dff['Developer'].str.contains(search, case=False)]
        
        limit = 8
        total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
        items = dff.iloc[st.session_state.d_idx*limit : (st.session_state.d_idx+1)*limit]

        # شبكة المربعات 1x1
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

        # أزرار التنقل صغيرة جداً
        st.write("---")
        n_c1, n_c2, n_c3 = st.columns([1, 2, 1])
        with n_c1:
            if st.session_state.d_idx > 0:
                if st.button("السابق", key="nav_p"): st.session_state.d_idx -= 1; st.rerun()
        with n_c2:
            st.markdown(f"<p style='text-align:center; font-size:12px;'>{st.session_state.d_idx + 1} / {total_p}</p>", unsafe_allow_html=True)
        with n_c3:
            if (st.session_state.d_idx + 1) * limit < len(dff):
                if st.button("التالي", key="nav_n"): st.session_state.d_idx += 1; st.rerun()
