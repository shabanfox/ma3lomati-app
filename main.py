import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - الأسود والذهبي والـ 60% يمين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #ffffff; }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    /* الهيدر */
    .gold-header {
        background: #000000; color: #f59e0b; padding: 20px;
        text-align: center; font-weight: 900; font-size: 26px;
        border-bottom: 4px solid #f59e0b; margin-bottom: 20px;
    }

    /* كارت المطور - أسود في ذهبي */
    .dev-grid-card {
        background: #000000; /* خلفية سوداء */
        border: 2px solid #f59e0b; /* إطار ذهبي */
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        transition: 0.3s;
        height: 100px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }
    .dev-grid-card:hover {
        background: #f59e0b; /* يقلب ذهبي عند التمرير */
        cursor: pointer;
    }
    .dev-name {
        color: #f59e0b; /* النص ذهبي */
        font-weight: 900;
        font-size: 18px;
        margin: 0;
    }
    .dev-grid-card:hover .dev-name {
        color: #000000; /* النص يقلب أسود عند التمرير */
    }

    /* أزرار التصفح */
    .stButton>button {
        background-color: #000000 !important;
        color: #f59e0b !important;
        border: 1px solid #f59e0b !important;
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 5. الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الواجهة
st.markdown('<div class="gold-header">MA3LOMATI PRO 2026</div>', unsafe_allow_html=True)

if st.session_state.selected_dev:
    # --- صفحة التفاصيل (100% عرض) ---
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    if st.button("⬅️ عودة"):
        st.session_state.selected_dev = None
        st.rerun()
    
    st.markdown(f"""
        <div style="background:#000; padding:30px; border-radius:15px; border:2px solid #f59e0b; color:white;">
            <h1 style="color:#f59e0b;">{dev_name}</h1>
            <p>👤 المالك: {dev_info.get('Owner')}</p>
            <hr style="border-color:#f59e0b;">
            <p style="font-size:18px;">{dev_info.get('Detailed_Info')}</p>
        </div>
    """, unsafe_allow_html=True)
else:
    # --- الصفحة الرئيسية ---
    menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
        icons=["tools", "building", "person-vcard"], 
        default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#000000", "color": "#f59e0b"}}
    )

    if menu == "المطورين":
        # تقسيم الشاشة: 60% يمين للكروت، 40% يسار فراغ
        main_col, empty_col = st.columns([0.6, 0.4])
        
        with main_col:
            search = st.text_input("🔍 بحث...", placeholder="اكتب اسم المطور")
            dff = df_d.copy()
            if search: dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
            
            # الترقيم (8 مطورين)
            limit = 8
            total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
            start = st.session_state.d_idx * limit
            items = dff.iloc[start : start + limit]

            # شبكة الكروت (2 في كل صف داخل الـ 60%)
            grid_cols = st.columns(2)
            for i, (idx, row) in enumerate(items.iterrows()):
                with grid_cols[i % 2]:
                    st.markdown(f"""<div class="dev-grid-card"><p class="dev-name">{row.get('Developer')}</p></div>""", unsafe_allow_html=True)
                    if st.button("عرض الزتونة", key=f"btn_{idx}", use_container_width=True):
                        st.session_state.selected_dev = row.get('Developer')
                        st.rerun()

            # التنقل
            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            if n1.button("السابق") and st.session_state.d_idx > 0:
                st.session_state.d_idx -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.d_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            if n3.button("التالي") and (start + limit) < len(dff):
                st.session_state.d_idx += 1; st.rerun()

    elif menu == "المشاريع":
        st.write("قسم المشاريع")
    elif menu == "الأدوات":
        st.write("قسم الأدوات")

if st.sidebar.button("🚪 خروج"):
    st.session_state.auth = False; st.rerun()
