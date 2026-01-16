import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - التحكم الدقيق في الأحجام والمواقع
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #ffffff; }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    /* هيدر ثابت مع زر خروج صغير عاليسار */
    .top-bar {
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 10px 20px; border-bottom: 3px solid #f59e0b;
        border-radius: 0 0 15px 15px; margin-bottom: 20px;
    }
    .logo-title { color: #f59e0b; font-weight: 900; font-size: 20px; margin: 0; }

    /* زر الخروج الصغير */
    .stButton > button[kind="secondary"] {
        padding: 2px 10px !important; height: 30px !important; width: 60px !important;
        font-size: 12px !important; background-color: #ff4b4b !important; color: white !important;
        border: none !important; border-radius: 5px !important;
    }

    /* المربعات الكبيرة (المطورين) */
    div.stButton > button[kind="primary"] {
        background-color: #000 !important; color: #f59e0b !important;
        border: 2px solid #f59e0b !important; border-radius: 12px !important;
        width: 180px !important; height: 180px !important;
        font-size: 18px !important; font-weight: 900 !important;
        transition: 0.3s !important; margin: 10px auto !important;
    }
    div.stButton > button[kind="primary"]:hover {
        background-color: #f59e0b !important; color: #000 !important; transform: scale(1.05);
    }

    /* أزرار التنقل الصغيرة (التالي والسابق) */
    .nav-btn > div.stButton > button {
        height: 30px !important; width: 80px !important; font-size: 12px !important;
        padding: 0 !important; background: #f8fafc !important; color: #000 !important;
        border: 1px solid #e2e8f0 !important;
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
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. البار العلوي (لوجو + خروج)
t_col1, t_col2 = st.columns([0.9, 0.1])
with t_col1:
    st.markdown('<p class="logo-title">MA3LOMATI PRO 2026</p>', unsafe_allow_html=True)
with t_col2:
    if st.button("خروج", kind="secondary"):
        st.session_state.auth = False; st.rerun()

# 7. المحتوى
if st.session_state.selected_dev:
    # صفحة التفاصيل
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    if st.button("⬅️ عودة", kind="primary"):
        st.session_state.selected_dev = None; st.rerun()
    
    st.markdown(f"""
        <div style="background:#000; padding:25px; border-radius:15px; border:2px solid #f59e0b; color:white;">
            <h2 style="color:#f59e0b;">{dev_name}</h2>
            <hr style="border-color:#f59e0b;">
            <p style="font-size:18px;">{dev_info.get('Detailed_Info')}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
        icons=["tools", "building", "person-vcard"], 
        default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#000", "color": "#f59e0b"}}
    )

    if menu == "المطورين":
        main_col, empty_col = st.columns([0.6, 0.4])
        with main_col:
            search = st.text_input("🔍 بحث...")
            dff = df_d.copy()
            if search: dff = dff[dff['Developer'].str.contains(search, case=False)]
            
            limit = 8
            total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
            items = dff.iloc[st.session_state.d_idx*limit : (st.session_state.d_idx+1)*limit]

            # شبكة المربعات 2 في الصف
            for i in range(0, len(items), 2):
                cols = st.columns(2)
                with cols[0]:
                    n1 = items.iloc[i].get('Developer')
                    if st.button(n1, key=f"sq_{i}", kind="primary"):
                        st.session_state.selected_dev = n1; st.rerun()
                with cols[1]:
                    if i + 1 < len(items):
                        n2 = items.iloc[i+1].get('Developer')
                        if st.button(n2, key=f"sq_{i+1}", kind="primary"):
                            st.session_state.selected_dev = n2; st.rerun()

            # أزرار التنقل الصغيرة أسفل المحتوى
            st.write("---")
            nav_col1, nav_col2, nav_col3 = st.columns([1, 2, 1])
            with nav_col1:
                st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
                if st.session_state.d_idx > 0:
                    if st.button("السابق", key="prev_sm"): st.session_state.d_idx -= 1; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with nav_col2:
                st.markdown(f"<p style='text-align:center; font-size:12px; color:#666;'>صفحة {st.session_state.d_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            with nav_col3:
                st.markdown('<div class="nav-btn">', unsafe_allow_html=True)
                if (st.session_state.d_idx + 1) * limit < len(dff):
                    if st.button("التالي", key="next_sm"): st.session_state.d_idx += 1; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
