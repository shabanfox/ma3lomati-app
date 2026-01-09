import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS المتكامل (تباين عالي - خطوط واضحة جداً - بدون فواصل)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية لستريمليت */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* كروت البوابة الرئيسية */
    .main-gate-card {
        background: white; border-radius: 20px; padding: 30px; text-align: center;
        border: 2px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: 0.3s ease; height: 260px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; width: 100%;
    }
    .main-gate-card:hover { transform: translateY(-10px); border-color: #001a33; }
    .card-companies { border-top: 12px solid #001a33; }
    .card-tools { border-top: 12px solid #f59e0b; }
    .gate-icon { font-size: 4rem; margin-bottom: 10px; }
    .gate-title { font-size: 2.2rem; font-weight: 900; color: #000000; }

    /* الهيدر الموحد لصفحات المحتوى */
    .hero-section {
        background: #001a33; padding: 30px 20px; border-radius: 0 0 30px 30px;
        margin-bottom: 25px; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .hero-tools { background: #f59e0b; color: #000000; border-bottom: 5px solid #b45309; }

    /* الكروت الـ 9 (Premium Nano) */
    .premium-nano-card {
        background: #ffffff; border: 1px solid #cbd5e1; border-right: 8px solid #001a33;
        border-radius: 12px; padding: 15px; margin-bottom: 10px; min-height: 135px;
        display: flex; flex-direction: column; justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .c-dev { color: #000000 !important; font-size: 1.25rem; font-weight: 900; line-height: 1.2; }
    .c-proj { color: #1d4ed8 !important; font-size: 1rem; font-weight: 700; }
    .c-price { color: #15803d !important; font-size: 1.4rem; font-weight: 900; margin: 5px 0; }
    .c-meta { color: #1e293b; font-size: 0.95rem; font-weight: 700; background: #f1f5f9; padding: 4px 10px; border-radius: 6px; }

    /* حاسبة البروكر - خط واضح جداً */
    .calc-box {
        background: #ffffff; padding: 30px; border-radius: 20px; 
        border: 4px solid #001a33; box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    .result-card { padding: 20px; border-radius: 12px; margin-bottom: 15px; border: 2px solid #eee; }
    .label-big { color: #000000; font-size: 1.3rem; font-weight: 900; display: block; }
    .value-huge { font-size: 2.3rem; font-weight: 900; display: block; color: #000; }

    /* تنسيق أزرار ستريمليت */
    div.stButton > button {
        background: #001a33 !important; color: white !important;
        font-size: 1rem !important; font-weight: 900 !important;
        height: 45px !important; border-radius: 10px !important; width: 100%;
    }
    /* أزرار العودة باللون الأسود */
    .back-btn div.stButton > button { background: #000 !important; }

    /* تباين الفلاتر */
    label { color: black !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    .hero-section label { color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. وظائف معالجة البيانات
def extract_num(text):
    if pd.isna(text): return 0
    res = re.findall(r'\d+', str(text).replace(',', ''))
    return int(res[0]) if res else 0

@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        df['p_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return None

df = get_data()

# 4. إدارة حالة التنقل (Session State)
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page_idx' not in st.session_state: st.session_state.page_idx = 0

if df is not None:
    
    # --- أ. الصفحة الرئيسية (البوابة) ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; margin:60px 0; font-weight:900; font-size:3rem;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        col_gate1, col_gate2 = st.columns(2)
        with col_gate1:
            st.markdown('<div class="main-gate-card card-companies"><div class="gate-icon">🏢</div><div class="gate-title">الشركات</div><p style="color:#64748b; font-weight:700;">دليل المطورين والمشاريع</p></div>', unsafe_allow_html=True)
            if st.button("دخول قسم الشركات", key="go_comp"):
                st.session_state.view = 'companies'; st.rerun()
        with col_gate2:
            st.markdown('<div class="main-gate-card card-tools"><div class="gate-icon">🛠️</div><div class="gate-title">أدوات البروكر</div><p style="color:#64748b; font-weight:700;">الحاسبات والأدوات الذكية</p></div>', unsafe_allow_html=True)
            if st.button("دخول أدوات البروكر", key="go_tools"):
                st.session_state.view = 'tools'; st.rerun()

    # --- ب. صفحة الشركات (الفلاتر + الكروت الـ 9) ---
    elif st.session_state.view == 'companies':
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        st.markdown('<div class="back-btn">', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية", key="back_home"):
            st.session_state.view = 'main'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<h1 style="text-align:center; margin-bottom:20px; color:white;">🔍 دليل الشركات والمشاريع</h1>', unsafe_allow_html=True)
        
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1: sq = st.text_input("بحث بالاسم", placeholder="اكتب اسم المطور أو المشروع...", label_visibility="collapsed")
        with f_col2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()))
        with f_col3: sp = st.number_input("الميزانية القصوى", value=0, step=500000)
        st.markdown('</div>', unsafe_allow_html=True)

        # فلترة البيانات
        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # عرض 9 كروت
        items_per_page = 9
        total_p = math.ceil(len(f_df) / items_per_page)
        start = st.session_state.page_idx * items_per_page
        batch = f_df.iloc[start : start + items_per_page]

        for i in range(0, len(batch), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(batch):
                    row = batch.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="premium-nano-card">
                                <div><div class="c-dev">{row[0]}</div><div class="c-proj">🏢 {row[2]}</div></div>
                                <div><div class="c-price">{row[4]}</div><div class="c-meta">📍 {row[3]} | 💳 {row[10]}</div></div>
                            </div>
                        """, unsafe_allow_html=True)
                        if st.button("عرض التفاصيل", key=f"btn_{start+i+j}"):
                            st.session_state.selected_dev = row[0]
                            st.session_state.view = 'details'; st.rerun()

        # أزرار الصفحات
        st.markdown("<br>", unsafe_allow_html=True)
        p1, p2, p3 = st.columns([1,1,1])
        with p1: 
            if st.session_state.page_idx > 0 and st.button("⬅️ السابق"):
                st.session_state.page_idx -= 1; st.rerun()
        with p2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.page_idx+1} من {total_p}</p>", unsafe_allow_html=True)
        with p3:
            if st.session_state.page_idx < total_p - 1 and st.button("التالي ➡️"):
                st.session_state.page_idx += 1; st.rerun()

    # --- ج. صفحة أدوات البروكر (الحاسبة الرقمية) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-section hero-tools">', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية", key="back_from_tools"):
            st.session_state.view = 'main'; st.rerun()
        st.markdown('<h1 style="text-align:center; margin:0; color:black;">🛠️ حاسبة الأقساط والمقدم</h1>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<h3 style='text-align:right; color:#000;'>🧮 أدخل أرقام الوحدة مباشرة:</h3>", unsafe_allow_html=True)
        calc_in, calc_out = st.columns([1, 1.2])
        
        with calc_in:
            u_p = st.number_input("سعر الوحدة الإجمالي (جنيه)", value=2500000, step=100000)
            d_pct = st.number_input("نسبة المقدم المطلوب (%)", value=10, min_value=0, max_value=100)
            years = st.number_input("عدد سنوات التقسيط", value=8, min_value=1, max_value=20)
            
            # الحسابات
            dp_v = u_p * (d_pct / 100)
            rem = u_p - dp_v
            mo_v = rem / (years * 12) if years > 0 else 0

        with calc_out:
            st.markdown(f"""
            <div class="calc-box">
                <div class="result-card" style="background:#fff7ed; border-color:#f59e0b;">
                    <span class="label-big">💳 قيمة المقدم (كاش):</span>
                    <span class="value-huge" style="color:#c2410c;">{dp_v:,.0f} ج.م</span>
                </div>
                <div class="result-card" style="background:#f0fdf4; border-color:#22c55e;">
                    <span class="label-big">📅 القسط الشهري:</span>
                    <span class="value-huge" style="color:#15803d;">{mo_v:,.0f} ج.م</span>
                </div>
                <div class="result-card" style="background:#f0f9ff; border-color:#0ea5e9;">
                    <span class="label-big">🗓️ القسط الربع سنوي:</span>
                    <span class="value-huge" style="color:#0369a1;">{mo_v*3:,.0f} ج.م</span>
                </div>
                <div style="text-align:center; font-weight:900; color:#000; font-size:1.2rem; border-top:2px dashed #ccc; padding-top:10px;">
                    إجمالي سعر الوحدة: {u_p:,.0f} ج.م
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- د. صفحة التفاصيل (الزتونة) ---
    elif st.session_state.view == 'details':
        if st.button("🔙 عودة للشركات", key="back_to_list"):
            st.session_state.view = 'companies'; st.rerun()
        dev_n = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev_n]
        st.markdown(f"<h1 style='background:#001a33; color:white; padding:20px; border-radius:15px; text-align:center;'>🏢 {dev_n}</h1>", unsafe_allow_html=True)
        
        for _, r in projs.iterrows():
            with st.expander(f"📌 {r[2]} - {r[4]}", expanded=True):
                st.info(f"📍 الموقع: {r[3]} | 💳 المقدم: {r[10]} | 📅 التقسيط: {r[9]} سنوات")
                st.error(f"💡 الزتونة الفنية:\n\n{r[11]}")
