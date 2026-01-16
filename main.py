import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - جعل الأزرار مربعة 1*1
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #ffffff; }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    .gold-header {
        background: #000000; color: #f59e0b; padding: 15px;
        text-align: center; font-weight: 900; font-size: 24px;
        border-bottom: 4px solid #f59e0b; border-radius: 0 0 15px 15px; margin-bottom: 25px;
    }

    /* تحويل الأزرار لمربعات 1*1 */
    div.stButton > button {
        background-color: #000000 !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        border-radius: 10px !important;
        
        /* تثبيت الحجم المربع */
        aspect-ratio: 1 / 1 !important; 
        width: 100% !important;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        
        font-size: 16px !important; /* حجم خط مناسب للمربع */
        font-weight: 800 !important;
        transition: 0.3s !important;
        padding: 10px !important;
        white-space: normal !important; /* للسماح بنزول النص سطر جديد لو طويل */
        line-height: 1.2 !important;
    }

    div.stButton > button:hover {
        background-color: #f59e0b !important;
        color: #000000 !important;
        transform: scale(1.05) !important;
    }

    /* ضبط المسافات بين المربعات */
    [data-testid="column"] {
        padding: 8px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        d = pd.read_csv(u_d).fillna("").astype(str)
        return d
    except: return pd.DataFrame()

df_d = load_data()

# 5. الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر
st.markdown('<div class="gold-header">MA3LOMATI PRO 2026</div>', unsafe_allow_html=True)

# 7. منطق العرض
if st.session_state.selected_dev:
    # صفحة التفاصيل
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    if st.button("⬅️ عودة لقائمة المطورين"):
        st.session_state.selected_dev = None
        st.rerun()
    
    st.markdown(f"""
        <div style="background:#000; padding:30px; border-radius:15px; border:2px solid #f59e0b; color:white;">
            <h1 style="color:#f59e0b;">{dev_name}</h1>
            <p>👤 صاحب الشركة: {dev_info.get('Owner')}</p>
            <hr style="border-color:#f59e0b;">
            <p style="font-size:18px;">{dev_info.get('Detailed_Info')}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # القائمة الرئيسية
    menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
        icons=["tools", "building", "person-vcard"], 
        default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#000", "color": "#f59e0b"}}
    )

    if menu == "المطورين":
        # توزيع 60% يمين و 40% يسار فراغ
        main_col, empty_col = st.columns([0.6, 0.4])
        
        with main_col:
            search = st.text_input("🔍 بحث عن مطور...", placeholder="اكتب الاسم هنا")
            dff = df_d.copy()
            if search:
                dff = dff[dff['Developer'].str.contains(search, case=False)]
            
            # الترقيم (8 مطورين)
            limit = 8
            total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
            start = st.session_state.d_idx * limit
            items = dff.iloc[start : start + limit]

            # شبكة المربعات (2 في كل صف داخل الـ 60%)
            for i in range(0, len(items), 2):
                cols = st.columns(2)
                with cols[0]:
                    name1 = items.iloc[i].get('Developer')
                    if st.button(name1, key=f"sq_{i}"):
                        st.session_state.selected_dev = name1
                        st.rerun()
                with cols[1]:
                    if i + 1 < len(items):
                        name2 = items.iloc[i+1].get('Developer')
                        if st.button(name2, key=f"sq_{i+1}"):
                            st.session_state.selected_dev = name2
                            st.rerun()

            # أزرار التنقل
            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            if n1.button("السابق") and st.session_state.d_idx > 0:
                st.session_state.d_idx -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            if n3.button("التالي") and (start + limit) < len(dff):
                st.session_state.d_idx += 1; st.rerun()

if st.sidebar.button("🚪 خروج"):
    st.session_state.auth = False; st.rerun()
