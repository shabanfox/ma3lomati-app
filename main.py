import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

# 2. تصميم CSS الفاخر (نفس التصميم اللي بعته مع تعديل بسيط للأزرار)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-banner { 
        background: #000000; color: #f59e0b; padding: 25px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #f59e0b;
        box-shadow: 10px 10px 0px #000;
    }
    .hero-banner h1 { font-weight: 900; font-size: 2.8rem; margin: 0; color: #f59e0b !important; }

    div.stButton > button {
        width: 100% !important; height: 130px !important;
        background-color: #ffffff !important; color: #000000 !important;
        border: 5px solid #000000 !important; border-radius: 25px !important;
        font-size: 1.8rem !important; font-weight: 900 !important;
        box-shadow: 10px 10px 0px 0px #000000 !important;
        transition: 0.2s;
    }

    /* كروت المشاريع (Micro-Cards) */
    .micro-card {
        background: #ffffff; border: 3px solid #000; padding: 12px; 
        border-radius: 18px; margin-bottom: 12px; box-shadow: 6px 6px 0px #000;
        height: 180px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .m-title { font-size: 1.2rem; font-weight: 900; color: #000; line-height: 1.2; }
    .m-dev { color: #f59e0b; font-weight: 900; font-size: 0.9rem; margin-top: 5px; }
    .m-price { 
        background: #000; color: #fff; font-size: 1rem; font-weight: 900; 
        padding: 5px; border-radius: 8px; text-align: center; margin-top: 10px;
    }

    /* أزرار التحكم (التالي والسابق) - تصميم مصغر */
    div.stButton > button[key^="nav_"] {
        height: 45px !important; width: 120px !important;
        font-size: 1rem !important; border-radius: 10px !important;
        box-shadow: 4px 4px 0px #000 !important;
    }

    .admin-panel {
        background: #fcfcfc; border: 4px dashed #000; padding: 20px; 
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page' not in st.session_state: st.session_state.page = 0

# --- التطبيق ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.write("<div style='height:80px;'></div>", unsafe_allow_html=True)
    _, mid_col, _ = st.columns([0.1, 0.8, 0.1])
    with mid_col:
        c1, c2 = st.columns(2, gap="large")
        with c1:
            if st.button("🏢\nدليل المشاريع", key="btn_p"): st.session_state.view = 'comp'; st.rerun()
        with c2:
            if st.button("🛠️\nأدوات البروكر", key="btn_t"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🔍 إدارة المشاريع العقارية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية", key="nav_back_home"): 
        st.session_state.view = 'main'; st.session_state.page = 0; st.rerun()
    
    col_grid, col_admin = st.columns([0.72, 0.28], gap="large")

    with col_grid:
        q = st.text_input("🔍 ابحث عن أي تفاصيل (مشروع، مطور، موقع)...")
        df_f = st.session_state.data
        if q: df_f = df_f[df_f.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]
        
        # --- منطق الصفحات (9 كروت لكل صفحة) ---
        items_per_page = 9
        total_items = len(df_f)
        start_idx = st.session_state.page * items_per_page
        end_idx = start_idx + items_per_page
        current_batch = df_f.iloc[start_idx:end_idx]

        # عرض الكروت 3x3
        for i in range(0, len(current_batch), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_batch):
                    row = current_batch.iloc[i + j]
                    with grid_cols[j]:
                        st.markdown(f"""
                        <div class="micro-card">
                            <div>
                                <div class="m-title">{row[0]}</div>
                                <div class="m-dev">🏢 {row[2]}</div>
                                <div style="font-size:0.8rem; color:#555; margin-top:5px;">📍 {row[3]}</div>
                            </div>
                            <div class="m-price">{row[4]}</div>
                        </div>
                        """, unsafe_allow_html=True)

        # --- أزرار التنقل (التالي والسابق) في المنتصف ---
        st.write("<br>", unsafe_allow_html=True)
        _, nav_mid, _ = st.columns([1, 1, 1])
        with nav_mid:
            c_prev, c_next = st.columns(2)
            with c_prev:
                if st.session_state.page > 0:
                    if st.button("⬅️ السابق", key="nav_prev"):
                        st.session_state.page -= 1; st.rerun()
            with c_next:
                if end_idx < total_items:
                    if st.button("التالي ➡️", key="nav_next"):
                        st.session_state.page += 1; st.rerun()

    with col_admin:
        st.markdown('<div class="admin-panel">', unsafe_allow_html=True)
        st.markdown("### ➕ إضافة مشروع")
        with st.form("add_form", clear_on_submit=True):
            n = st.text_input("اسم المشروع")
            d = st.text_input("اسم المطور")
            l = st.text_input("الموقع الجغرافي")
            p = st.text_input("السعر / نظام السداد")
            if st.form_submit_button("حفظ وإضافة للشبكة"):
                if n:
                    new_r = pd.DataFrame([[n, "", d, l, p]], columns=st.session_state.data.columns)
                    st.session_state.data = pd.concat([new_r, st.session_state.data], ignore_index=True)
                    st.success("تم الحفظ!")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# (بقية كود صفحة الأدوات يبقى كما هو في رسالتك الأصلية...)
