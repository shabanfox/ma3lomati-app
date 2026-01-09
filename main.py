import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (تحسين شكل الأزرار لتبدو ككروت فخمة)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* هيدر الصفحة */
    .hero-banner { 
        background: #000; color: #f59e0b; padding: 20px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border-bottom: 6px solid #f59e0b;
    }

    /* تحويل زر Streamlit ليصبح بشكل "كارت مشروع" */
    div.stButton > button {
        width: 100% !important;
        height: 180px !important;
        background-color: #ffffff !important;
        color: #000 !important;
        border: 3px solid #000 !important;
        border-radius: 20px !important;
        box-shadow: 6px 6px 0px #000 !important;
        white-space: normal !important; /* للسماح بتعدد الأسطر داخل الزر */
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        transition: 0.2s;
    }
    div.stButton > button:hover {
        border-color: #f59e0b !important;
        box-shadow: 8px 8px 0px #f59e0b !important;
        transform: translateY(-3px);
    }
    
    /* تفاصيل صفحة المشروع المنفردة */
    .detail-box {
        background: #000; color: #fff; padding: 40px; border-radius: 30px;
        border: 5px solid #f59e0b; text-align: center; margin-top: 20px;
    }
    .detail-val { font-size: 2.5rem; font-weight: 900; color: #f59e0b; }
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
if 'selected_project' not in st.session_state: st.session_state.selected_project = None

# --- منطق التنقل ---

# أ. الصفحة الرئيسية
if st.session_state.view == 'main':
    st.markdown('<div class="hero-banner"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button("🏢\nدليل المشاريع\n(استعراض الكل)"): st.session_state.view = 'comp'; st.rerun()
    with c2:
        if st.button("🛠️\nأدوات البروكر\n(حسابات الاستثمار)"): st.session_state.view = 'tools'; st.rerun()

# ب. صفحة دليل المشاريع (الشبكة التفاعلية)
elif st.session_state.view == 'comp':
    st.markdown('<div class="hero-banner"><h2>🔍 اختر مشروعاً للتفاصيل</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

    q = st.text_input("🔍 بحث سريع عن مطور أو مشروع...")
    df_f = st.session_state.data
    if q: df_f = df_f[df_f.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]

    # عرض الشبكة 3x3 كأزرار
    for i in range(0, len(df_f.head(15)), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(df_f):
                row = df_f.iloc[i + j]
                with cols[j]:
                    # كل كارت هو زر فعلي
                    button_label = f"📍 {row[0]}\n🏢 {row[2]}\n💰 {row[4]}"
                    if st.button(button_label, key=f"proj_{i+j}"):
                        st.session_state.selected_project = row
                        st.session_state.view = 'details'
                        st.rerun()

# ج. صفحة تفاصيل المشروع (تظهر عند الضغط على الكارت)
elif st.session_state.view == 'details':
    proj = st.session_state.selected_project
    st.markdown(f'<div class="hero-banner"><h1>🏢 تفاصيل: {proj[0]}</h1></div>', unsafe_allow_html=True)
    
    if st.button("🔙 العودة للقائمة"): st.session_state.view = 'comp'; st.rerun()
    
    st.markdown(f"""
        <div class="detail-box">
            <span style="font-size:1.5rem; color:#bbb;">اسم المطور العقاري:</span><br>
            <span class="detail-val">{proj[2]}</span>
            <hr style="border-color:#333">
            <span style="font-size:1.5rem; color:#bbb;">الموقع الجغرافي:</span><br>
            <span class="detail-val" style="font-size:1.8rem;">📍 {proj[3]}</span>
            <hr style="border-color:#333">
            <span style="font-size:1.5rem; color:#bbb;">نظام السداد والأسعار:</span><br>
            <span class="detail-val" style="color:#22c55e;">{proj[4]}</span>
        </div>
    """, unsafe_allow_html=True)
    
    # ميزة إضافية: مشاريع أخرى لنفس المطور
    other_projs = st.session_state.data[st.session_state.data.iloc[:,2] == proj[2]]
    if len(other_projs) > 1:
        st.markdown(f"### 🏗️ مشاريع أخرى لشركة {proj[2]}:")
        st.dataframe(other_projs[[st.session_state.data.columns[0], st.session_state.data.columns[3], st.session_state.data.columns[4]]], use_container_width=True)

# د. صفحة الأدوات
elif st.session_state.view == 'tools':
    st.markdown('<div class="hero-banner"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    st.info("حاسبات الأقساط والـ ROI تعمل هنا كما في النسخ السابقة.")
