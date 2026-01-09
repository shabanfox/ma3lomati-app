import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS المتكامل (تصميم موحد وبدون فواصل)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* كروت البوابة الرئيسية */
    .gate-container {
        display: flex; gap: 20px; justify-content: center; margin-top: 50px;
    }
    .main-gate-card {
        background: white; border-radius: 20px; padding: 30px; text-align: center;
        border: 1px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        transition: 0.3s ease; height: 260px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; width: 100%;
    }
    .main-gate-card:hover { transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
    .card-companies { border-top: 10px solid #001a33; }
    .card-tools { border-top: 10px solid #f59e0b; }
    .gate-icon { font-size: 4rem; margin-bottom: 10px; }
    .gate-title { font-size: 2rem; font-weight: 900; color: #001a33; }

    /* الهيدر الموحد لصفحات المحتوى */
    .hero-section {
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        padding: 30px 20px; border-radius: 0 0 30px 30px;
        margin-bottom: 25px; color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    }
    .hero-tools { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); }

    /* تصميم الكروت الـ 9 (Nano Premium) */
    .premium-nano-card {
        background: #ffffff; border: 1px solid #cbd5e1; border-right: 8px solid #001a33;
        border-radius: 12px; padding: 15px; margin-bottom: 10px; min-height: 130px;
        display: flex; flex-direction: column; justify-content: space-between;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .c-dev { color: #000000 !important; font-size: 1.2rem; font-weight: 900; line-height: 1.2; }
    .c-proj { color: #1d4ed8 !important; font-size: 1rem; font-weight: 700; }
    .c-price { color: #15803d !important; font-size: 1.3rem; font-weight: 900; margin: 5px 0; }
    .c-meta { color: #475569; font-size: 0.9rem; font-weight: 600; background: #f1f5f9; padding: 3px 10px; border-radius: 6px; }

    /* أزرار التفاصيل */
    div.stButton > button {
        background: #001a33 !important; color: white !important;
        font-size: 0.85rem !important; height: 32px !important;
        border-radius: 8px !important; width: 100%; border: none !important;
        font-weight: 900 !important; transition: 0.3s;
    }
    div.stButton > button:hover { background: #1e40af !important; transform: scale(1.02); }

    /* تنسيق الفلاتر داخل الهيدر */
    label { color: white !important; font-weight: 700 !important; font-size: 1rem !important; }
    .stTextInput input, .stSelectbox div, .stNumberInput input { border-radius: 10px !important; }
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
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        df['p_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = get_data()

# 4. إدارة حالة التنقل
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page_idx' not in st.session_state: st.session_state.page_idx = 0

if df is not None:
    
    # --- أ. الصفحة الرئيسية (البوابة) ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; margin:60px 0; font-weight:900; font-size:3rem;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        col_gate1, col_gate2 = st.columns(2)
        with col_gate1:
            st.markdown('<div class="main-gate-card card-companies"><div class="gate-icon">🏢</div><div class="gate-title">الشركات</div><p style="color:#64748b;">دليل المطورين والمشاريع</p></div>', unsafe_allow_html=True)
            if st.button("دخول قسم الشركات", use_container_width=True):
                st.session_state.view = 'companies'; st.rerun()
        with col_gate2:
            st.markdown('<div class="main-gate-card card-tools"><div class="gate-icon">🛠️</div><div class="gate-title">أدوات البروكر</div><p style="color:#64748b;">الحاسبات والأدوات الذكية</p></div>', unsafe_allow_html=True)
            if st.button("دخول أدوات البروكر", use_container_width=True):
                st.session_state.view = 'tools'; st.rerun()

    # --- ب. صفحة الشركات (الفلاتر + الكروت الـ 9) ---
    elif st.session_state.view == 'companies':
        st.markdown('<div class="hero-section">', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"):
            st.session_state.view = 'main'; st.rerun()
        st.markdown('<h2 style="text-align:center; margin-bottom:20px;">🔍 ابحث في قاعدة بيانات العقارات</h2>', unsafe_allow_html=True)
        f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
        with f_col1: sq = st.text_input("ابحث عن مطور أو مشروع", placeholder="مثال: مدينة نصر، بالم هيلز...")
        with f_col2: sa = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()))
        with f_col3: sp = st.number_input("الميزانية القصوى", value=0, step=500000)
        st.markdown('</div>', unsafe_allow_html=True)

        # منطق الفلترة
        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # عرض الكروت بنظام 3 في كل صف (إجمالي 9)
        m_body, s_body = st.columns([3.4, 0.6])
        with m_body:
            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
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
                            if st.button("عرض التفاصيل الفنية", key=f"d_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.view = 'details'; st.rerun()

            # أزرار التنقل بين الصفحات
            st.markdown("<br>", unsafe_allow_html=True)
            pg1, pg2, pg3 = st.columns([1,1,1])
            with pg1: 
                if st.session_state.page_idx > 0 and st.button("⬅️ السابق"):
                    st.session_state.page_idx -= 1; st.rerun()
            with pg2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.page_idx+1} من {total_pages}</p>", unsafe_allow_html=True)
            with pg3:
                if st.session_state.page_idx < total_pages - 1 and st.button("التالي ➡️"):
                    st.session_state.page_idx += 1; st.rerun()

    # --- ج. صفحة أدوات البروكر (الحاسبة الذكية) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-section hero-tools">', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"):
            st.session_state.view = 'main'; st.rerun()
        st.markdown('<h2 style="text-align:center; margin:0;">🛠️ مساعد البروكر الذكي (حاسبة الأقساط)</h2>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        calc_in, calc_out = st.columns([1, 1.2])
        with calc_in:
            st.markdown("### 🧮 أدخل بيانات الوحدة")
            u_p = st.number_input("سعر الوحدة الإجمالي", value=2000000, step=100000)
            d_p_pct = st.slider("نسبة المقدم (%)", 0, 50, 10)
            years = st.slider("سنوات التقسيط", 1, 15, 8)
            
            # حسابات البروكر
            dp_val = u_p * (d_p_pct / 100)
            remain = u_p - dp_val
            monthly = remain / (years * 12)
            quarter = monthly * 3

        with calc_out:
            st.markdown("### 📊 ملخص العرض المالي")
            st.markdown(f"""
                <div style="background:white; padding:25px; border-radius:15px; border:2px solid #f59e0b; box-shadow: 0 10px 20px rgba(0,0,0,0.05);">
                    <p style="font-size:1.2rem;">💰 <b>الإجمالي:</b> {u_p:,.0f} ج.م</p>
                    <hr>
                    <div style="background:#fff7ed; padding:15px; border-radius:10px; margin-bottom:10px;">
                        <span style="font-size:1rem;">💳 قيمة المقدم:</span><br>
                        <span style="font-size:1.8rem; font-weight:900; color:#c2410c;">{dp_val:,.0f} ج.م</span>
                    </div>
                    <div style="background:#f0fdf4; padding:15px; border-radius:10px; margin-bottom:10px;">
                        <span style="font-size:1rem;">📅 القسط الشهري:</span><br>
                        <span style="font-size:1.8rem; font-weight:900; color:#15803d;">{monthly:,.0f} ج.م</span>
                    </div>
                    <div style="background:#f0f9ff; padding:15px; border-radius:10px;">
                        <span style="font-size:1rem;">🗓️ القسط الربع سنوي:</span><br>
                        <span style="font-size:1.8rem; font-weight:900; color:#0369a1;">{quarter:,.0f} ج.م</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            if st.button("📸 جاهز للتصوير والإرسال"):
                st.balloons()

    # --- د. صفحة التفاصيل الفنية (الزتونة) ---
    elif st.session_state.view == 'details':
        if st.button("🔙 عودة لقسم الشركات"):
            st.session_state.view = 'companies'; st.rerun()
        dev_name = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev_name]
        st.markdown(f"<h1 style='background:#001a33; color:white; padding:20px; border-radius:15px; text-align:center;'>🏢 {dev_name}</h1>", unsafe_allow_html=True)
        
        for _, r in projs.iterrows():
            with st.expander(f"📌 مشروع: {r[2]} | السعر: {r[4]}", expanded=True):
                st.markdown(f"""
                <div style="padding:10px; font-size:1.1rem;">
                <b>📍 الموقع:</b> {r[3]} <br>
                <b>💳 نظام السداد:</b> مقدم {r[10]} | تقسيط على {r[9]} سنوات <br><br>
                <div style="background:#fff4f4; padding:15px; border-radius:10px; border-right:5px solid #ef4444;">
                <b style="color:#ef4444;">💡 الزتونة الفنية (رأي الخبير):</b><br>{r[11]}
                </div>
                </div>
                """, unsafe_allow_html=True)
