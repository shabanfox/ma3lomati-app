import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - توحيد أحجام الأزرار تماماً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #ffffff; }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    /* الهيدر الذهبي */
    .gold-header {
        background: #000000; color: #f59e0b; padding: 15px;
        text-align: center; font-weight: 900; font-size: 24px;
        border-bottom: 4px solid #f59e0b; border-radius: 0 0 15px 15px; margin-bottom: 25px;
    }

    /* توحيد حجم الأزرار (الكروت) */
    div.stButton > button {
        background-color: #000000 !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        border-radius: 10px !important;
        
        /* تثبيت الحجم هنا */
        height: 100px !important; 
        width: 100% !important;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        
        font-size: 18px !important;
        font-weight: 800 !important;
        transition: 0.3s !important;
        margin-bottom: 5px !important;
    }

    div.stButton > button:hover {
        background-color: #f59e0b !important;
        color: #000000 !important;
        transform: scale(1.02) !important;
    }

    /* جعل المسافات بين الأعمدة متناسقة */
    [data-testid="column"] {
        padding: 5px !important;
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

# 6. الهيدر
st.markdown('<div class="gold-header">MA3LOMATI PRO 2026</div>', unsafe_allow_html=True)

# 7. منطق العرض
if st.session_state.selected_dev:
    # --- صفحة التفاصيل (100% عرض) ---
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    
    if st.button("⬅️ عودة للقائمة"):
        st.session_state.selected_dev = None
        st.rerun()
    
    st.markdown(f"""
        <div style="background:#000; padding:30px; border-radius:15px; border:2px solid #f59e0b; color:white;">
            <h1 style="color:#f59e0b;">{dev_name}</h1>
            <p style="font-size:20px;">👤 صاحب الشركة: {dev_info.get('Owner')}</p>
            <hr style="border-color:#f59e0b;">
            <p style="font-size:18px; line-height:1.6;">{dev_info.get('Detailed_Info')}</p>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- القائمة الرئيسية ---
    menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
        icons=["tools", "building", "person-vcard"], 
        default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#000", "color": "#f59e0b"}}
    )

    if menu == "المطورين":
        # توزيع 60% يمين للفعل و 40% يسار فراغ
        main_col, empty_col = st.columns([0.6, 0.4])
        
        with main_col:
            search = st.text_input("🔍 بحث...", placeholder="اكتب اسم المطور")
            dff = df_d.copy()
            if search:
                dff = dff[dff['Developer'].str.contains(search, case=False)]
            
            # الترقيم (8 مطورين)
            limit = 8
            total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
            start = st.session_state.d_idx * limit
            items = dff.iloc[start : start + limit]

            # عرض الشبكة (2 في كل صف) - أزرار متساوية الحجم
            for i in range(0, len(items), 2):
                cols = st.columns(2)
                # العنصر الأول في الصف
                with cols[0]:
                    name1 = items.iloc[i].get('Developer')
                    if st.button(name1, key=f"btn_{i}"):
                        st.session_state.selected_dev = name1
                        st.rerun()
                # العنصر الثاني في الصف (إذا وجد)
                with cols[1]:
                    if i + 1 < len(items):
                        name2 = items.iloc[i+1].get('Developer')
                        if st.button(name2, key=f"btn_{i+1}"):
                            st.session_state.selected_dev = name2
                            st.rerun()

            # أزرار التنقل في الأسفل
            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.d_idx > 0:
                    if st.button("السابق"): st.session_state.d_idx -= 1; st.rerun()
            with n2:
                st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.d_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            with n3:
                if (start + limit) < len(dff):
                    if st.button("التالي"): st.session_state.d_idx += 1; st.rerun()

if st.sidebar.button("🚪 خروج"):
    st.session_state.auth = False; st.rerun()
