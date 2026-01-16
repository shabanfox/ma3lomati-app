import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعداد الصفحة
st.set_page_config(page_title="BrokerEdge", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Auth & Selection)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0

# 3. التنسيق (CSS) لمحاكاة التصميم اللي بعته بالضبط
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #f9fafb; }
    
    header, [data-testid="stHeader"] { visibility: hidden; }

    /* الهيدر الأزرق الكبير (Hero Section) */
    .hero {
        background-color: #1e3a8a; padding: 40px 20px; text-align: center;
        color: white; border-radius: 0 0 20px 20px; margin-bottom: 30px;
    }

    /* تصميم الكارت المربع (1*1) بستايل BrokerEdge */
    div.stButton > button[key*="dev_"] {
        background-color: white !important;
        color: #1e3a8a !important; /* لون الخط أزرق غامق */
        border: 1px solid #e5e7eb !important;
        border-right: 6px solid #3b82f6 !important; /* الخط الأزرق الجانبي */
        border-radius: 12px !important;
        width: 100% !important;
        height: 180px !important; /* مربع 1:1 تقريباً */
        font-size: 20px !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
        transition: 0.3s !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    div.stButton > button[key*="dev_"]:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1) !important;
        border-color: #3b82f6 !important;
        background-color: #f0f7ff !important;
    }

    /* زر الخروج الصغير */
    div.stButton > button[key="logout"] {
        background-color: #ef4444 !important; color: white !important;
        border: none !important; border-radius: 8px !important;
        height: 35px !important; width: 80px !important; font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data
def load_data():
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    return pd.read_csv(u_d).fillna("").astype(str)

df_d = load_data()

# 5. البار العلوي
c1, c2 = st.columns([0.9, 0.1])
with c1: st.markdown('<div style="font-size:28px; font-weight:bold; color:#1e3a8a;">Broker<span style="color:#3b82f6;">Edge</span></div>', unsafe_allow_html=True)
with c2: 
    if st.button("خروج", key="logout"): st.session_state.auth = False; st.rerun()

# 6. Hero Section
st.markdown("""
    <div class="hero">
        <h1 style="font-size:32px; font-weight:bold;">كل داتا السوق في جيبك</h1>
        <p style="color:#bfdbfe; font-size:18px;">ابحث عن المطورين، واحصل على الزتونة فوراً</p>
    </div>
""", unsafe_allow_html=True)

# 7. منطق العرض (المساحة 60% يمين)
if st.session_state.selected_dev:
    # صفحة التفاصيل
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.selected_dev = None; st.rerun()
    
    st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:15px; border-right:8px solid #3b82f6; box-shadow:0 4px 6px rgba(0,0,0,0.05);">
            <h2 style="color:#1e3a8a;">{dev_name}</h2>
            <hr>
            <p style="font-size:18px; line-height:1.8;">{dev_info.get('Detailed_Info')}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # القائمة الرئيسية (60% يمين)
    col_main, col_empty = st.columns([0.6, 0.4])
    
    with col_main:
        search = st.text_input("🔍 ابحث عن مطور...", placeholder="اسم المطور العقاري")
        dff = df_d.copy()
        if search: dff = dff[dff['Developer'].str.contains(search, case=False)]
        
        limit = 8
        total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
        items = dff.iloc[st.session_state.d_idx*limit : (st.session_state.d_idx+1)*limit]

        # عرض المربعات 1:1 بستايل BrokerEdge (2 في كل صف)
        for i in range(0, len(items), 2):
            cols = st.columns(2)
            with cols[0]:
                n1 = items.iloc[i].get('Developer')
                if st.button(n1, key=f"dev_{i}"):
                    st.session_state.selected_dev = n1; st.rerun()
            with cols[1]:
                if i + 1 < len(items):
                    n2 = items.iloc[i+1].get('Developer')
                    if st.button(n2, key=f"dev_{i+1}"):
                        st.session_state.selected_dev = n2; st.rerun()

        # أزرار التنقل
        st.write("---")
        n1, n2, n3 = st.columns([1, 2, 1])
        if n1.button("السابق", key="prev") and st.session_state.d_idx > 0:
            st.session_state.d_idx -= 1; st.rerun()
        with n2: st.markdown(f"<p style='text-align:center;'>{st.session_state.d_idx + 1} / {total_p}</p>", unsafe_allow_html=True)
        if n3.button("التالي", key="next") and (st.session_state.d_idx + 1) * limit < len(dff):
            st.session_state.d_idx += 1; st.rerun()
