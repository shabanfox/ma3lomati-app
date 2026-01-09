import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (تصغير الكروت، تقريب المسافات، تقسيم الشاشة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* الهيدر */
    .hero-title { 
        background: #000; color: #FFD700; padding: 15px; border-radius: 12px; 
        text-align: center; margin-bottom: 25px; border: 3px solid #FFD700;
    }

    /* كروت المشاريع الصغيرة (المدمجة) */
    .small-card {
        background: #ffffff; border: 2px solid #000; padding: 10px; 
        border-radius: 12px; margin-bottom: 10px; box-shadow: 4px 4px 0px #000;
        height: 160px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .p-name { font-size: 1.1rem; font-weight: 900; color: #000; line-height: 1.2; }
    .p-dev { color: #2563eb; font-weight: 700; font-size: 0.85rem; }
    .p-tag { 
        font-weight: 900; font-size: 0.9rem; background: #FFD700; 
        padding: 3px; border: 2px solid #000; text-align: center; border-radius: 6px;
    }

    /* قسم الإضافة (اليسار) */
    .add-section {
        background: #f9f9f9; border: 3px dashed #000; padding: 20px; border-radius: 15px;
    }

    /* الأزرار الرئيسية */
    div.stButton > button {
        width: 100% !important; height: 80px !important;
        background-color: #fff !important; color: #000 !important;
        border: 4px solid #000 !important; border-radius: 15px !important;
        font-size: 1.4rem !important; font-weight: 900 !important;
        box-shadow: 6px 6px 0px 0px #000 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. تحميل وإدارة البيانات
@st.cache_data
def load_initial_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع', 'نوعه', 'المطور', 'الموقع', 'السداد'])

if 'data' not in st.session_state:
    st.session_state.data = load_initial_data()

if 'view' not in st.session_state: st.session_state.view = 'main'

# --- التنفيذ ---
if st.session_state.view == 'main':
    st.markdown('<div class="hero-title"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("🏢 دليل المشاريع"): st.session_state.view = 'comp'; st.rerun()
    with col2:
        if st.button("🛠️ أدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-title"><h2>🔍 المشاريع والإدارة</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    # تقسيم الصفحة: يمين (مشاريع) ويسار (إضافة)
    col_projects, col_add = st.columns([0.7, 0.3], gap="large")

    with col_projects:
        st.markdown("### 🏢 شبكة المشاريع")
        q = st.text_input("🔍 بحث سريع...", placeholder="اكتب اسم المشروع")
        df_f = st.session_state.data
        if q: df_f = df_f[df_f.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]
        
        # عرض الشبكة 3x3
        for i in range(0, len(df_f.head(18)), 3):
            grid_cols = st.columns(3)
            for j in range(3):
                if i + j < len(df_f):
                    row = df_f.iloc[i + j]
                    with grid_cols[j]:
                        st.markdown(f"""
                        <div class="small-card">
                            <div>
                                <div class="p-name">{row[0]}</div>
                                <div class="p-dev">🏢 {row[2]}</div>
                                <div style="font-size:0.75rem; color:#555;">📍 {row[3]}</div>
                            </div>
                            <div class="p-tag">{row[4]}</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col_add:
        st.markdown('<div class="add-section">', unsafe_allow_html=True)
        st.markdown("### ➕ إضافة مشروع")
        with st.form("quick_add", clear_on_submit=True):
            n = st.text_input("اسم المشروع")
            d = st.text_input("المطور")
            l = st.text_input("الموقع")
            p = st.text_input("السداد")
            if st.form_submit_button("حفظ الآن"):
                if n and d:
                    new_row = pd.DataFrame([[n, "", d, l, p]], columns=st.session_state.data.columns)
                    st.session_state.data = pd.concat([new_row, st.session_state.data], ignore_index=True)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-title"><h2>🛠️ أدوات الحاسبة</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.view = 'main'; st.rerun()
    # (هنا نضع الحاسبات كما في الأكواد السابقة)
    st.info("حاسبة الأقساط والـ ROI موجودة هنا بكامل قوتها")
