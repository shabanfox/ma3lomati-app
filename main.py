import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'd_idx' not in st.session_state: st.session_state.d_idx = 0
if 'selected_dev' not in st.session_state: st.session_state.selected_dev = None

# 3. التنسيق (CSS) - جعل الزرار هو الكارت بالكامل
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl !important; text-align: right; background-color: #ffffff; }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }

    .gold-header {
        background: #000000; color: #f59e0b; padding: 20px;
        text-align: center; font-weight: 900; font-size: 26px;
        border-bottom: 4px solid #f59e0b; margin-bottom: 20px;
    }

    /* استايل الزرار ليتحول لكارت أسود وذهبي */
    div.stButton > button {
        background-color: #000000 !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        border-radius: 12px !important;
        height: 120px !important;
        width: 100% !important;
        font-size: 20px !important;
        font-weight: 900 !important;
        transition: 0.3s !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }

    div.stButton > button:hover {
        background-color: #f59e0b !important;
        color: #000000 !important;
        border: 2px solid #000000 !important;
        transform: translateY(-5px) !important;
    }

    /* إخفاء المسافات الزائدة */
    .block-container { padding-top: 1rem; }
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

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("Passcode", type="password") == "2026": 
            st.session_state.auth = True; st.rerun()
    st.stop()

# 6. الهيدر وزر الخروج فوق عاليسار
h_col1, h_col2 = st.columns([0.9, 0.1])
with h_col1:
    st.markdown('<div class="gold-header">MA3LOMATI PRO 2026</div>', unsafe_allow_html=True)
with h_col2:
    if st.button("🚪 خروج", key="logout"):
        st.session_state.auth = False; st.rerun()

# 7. منطق العرض
if st.session_state.selected_dev:
    # --- صفحة التفاصيل الكاملة ---
    dev_name = st.session_state.selected_dev
    dev_info = df_d[df_d['Developer'] == dev_name].iloc[0]
    
    if st.button("⬅️ عودة للقائمة", key="back"):
        st.session_state.selected_dev = None
        st.rerun()
    
    st.markdown(f"""
        <div style="background:#000; padding:40px; border-radius:20px; border:3px solid #f59e0b; color:white; margin-top:20px;">
            <h1 style="color:#f59e0b; font-size:40px;">{dev_name}</h1>
            <p style="font-size:22px; color:#aaa;">👤 صاحب الشركة: {dev_info.get('Owner')}</p>
            <hr style="border-color:#f59e0b;">
            <div style="font-size:20px; line-height:1.8;">
                {dev_info.get('Detailed_Info')}
            </div>
        </div>
    """, unsafe_allow_html=True)

else:
    # --- القائمة الرئيسية ---
    menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
        icons=["tools", "building", "person-vcard"], 
        default_index=2, orientation="horizontal",
        styles={"nav-link-selected": {"background-color": "#000000", "color": "#f59e0b"}}
    )

    if menu == "المطورين":
        # توزيع 60% يمين و 40% يسار فراغ
        main_col, empty_col = st.columns([0.6, 0.4])
        
        with main_col:
            search = st.text_input("🔍 ابحث عن مطور بالاسم...", placeholder="اكتب هنا...")
            dff = df_d.copy()
            if search:
                dff = dff[dff['Developer'].str.contains(search, case=False)]
            
            # الترقيم (8 مطورين)
            limit = 8
            total_p = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
            start = st.session_state.d_idx * limit
            items = dff.iloc[start : start + limit]

            # شبكة الكروت (2 في كل صف) - الكارت هو الزرار نفسه
            grid_cols = st.columns(2)
            for i, (idx, row) in enumerate(items.iterrows()):
                dev_name = row.get('Developer')
                with grid_cols[i % 2]:
                    # هنا الزرار بياخد ستايل الكارت الأسود والذهبي
                    if st.button(dev_name, key=f"dev_{idx}"):
                        st.session_state.selected_dev = dev_name
                        st.rerun()

            # أزرار التنقل (Next/Prev)
            st.write("---")
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.d_idx > 0:
                    if st.button("السابق", key="prev"):
                        st.session_state.d_idx -= 1; st.rerun()
            with n2:
                st.markdown(f"<p style='text-align:center; font-weight:bold; font-size:18px;'>صفحة {st.session_state.d_idx + 1} من {total_p}</p>", unsafe_allow_html=True)
            with n3:
                if (start + limit) < len(dff):
                    if st.button("التالي", key="next"):
                        st.session_state.d_idx += 1; st.rerun()

    elif menu == "المشاريع":
        st.info("قسم المشاريع سيتم تنفيذه بنفس الستايل عند الطلب.")
    
    elif menu == "الأدوات":
        st.write("حاسبة الأقساط والأدوات...")
