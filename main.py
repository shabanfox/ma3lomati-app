import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS المتكامل والواضح جداً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }
    
    /* الهيدرات النحيفة لتوفير المساحة */
    .compact-hero { background: #001a33; padding: 12px; border-radius: 10px; color: white; text-align: center; margin-bottom:10px; }
    .hero-tools { background: #f59e0b; color: #000; }
    .hero-roi { background: #15803d; color: white; }

    /* كروت الشركات الـ 9 */
    .nano-card {
        background: white; border: 1px solid #cbd5e1; border-right: 6px solid #001a33;
        border-radius: 8px; padding: 10px; margin-bottom: 5px; min-height: 110px;
    }
    .c-dev { color: #000 !important; font-size: 1.1rem; font-weight: 900; }
    .c-price { color: #15803d !important; font-size: 1.2rem; font-weight: 900; }

    /* صناديق الحسابات */
    .calc-box { background: white; padding: 15px; border-radius: 12px; border: 3px solid #001a33; margin-top: 5px; }
    .res-val { font-size: 1.8rem; font-weight: 900; color: #000; display: block; line-height: 1.2; }
    .res-lbl { font-size: 0.9rem; font-weight: 700; color: #444; }

    /* تحسين المدخلات */
    .stNumberInput label { font-weight: 900 !important; color: #000 !important; }
    div.stButton > button { background: #001a33 !important; color: white !important; font-weight: 900 !important; border-radius: 8px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. وظائف البيانات
def extract_num(text):
    if pd.isna(text): return 0
    res = re.findall(r'\d+', str(text).replace(',', ''))
    return int(res[0]) if res else 0

@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        df['p_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = load_data()

# 4. إدارة الصفحات والتنقل
if 'view' not in st.session_state: st.session_state.view = 'main'
if 'page_idx' not in st.session_state: st.session_state.page_idx = 0

if df is not None:
    # --- أ. الصفحة الرئيسية ---
    if st.session_state.view == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; margin:40px 0; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div style="background:white; padding:20px; border-radius:15px; border-top:10px solid #001a33; text-align:center;"><h2>🏢 قسم الشركات</h2><p>دليل المطورين والمشاريع</p></div>', unsafe_allow_html=True)
            if st.button("دخول قسم الشركات", use_container_width=True):
                st.session_state.view = 'comp'; st.rerun()
        with c2:
            st.markdown('<div style="background:white; padding:20px; border-radius:15px; border-top:10px solid #f59e0b; text-align:center;"><h2>🛠️ أدوات البروكر</h2><p>الحاسبات وأدوات الاستثمار</p></div>', unsafe_allow_html=True)
            if st.button("دخول أدوات البروكر", use_container_width=True):
                st.session_state.view = 'tools'; st.rerun()

    # --- ب. قسم الشركات (الـ 9 كروت + الفلاتر) ---
    elif st.session_state.view == 'comp':
        st.markdown('<div class="compact-hero"><h2>🔍 دليل المطورين والمشاريع</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 العودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
        
        # الفلاتر
        f1, f2, f3 = st.columns([2,1,1])
        with f1: q = st.text_input("بحث بالاسم", placeholder="اكتب هنا...", label_visibility="collapsed")
        with f2: loc = st.selectbox("المنطقة", ["الكل"] + sorted(df.iloc[:,3].dropna().unique().tolist()))
        with f3: pr = st.number_input("أقصى سعر", value=0)

        f_df = df.copy()
        if q: f_df = f_df[f_df.iloc[:,0].str.contains(q,na=False,case=False) | f_df.iloc[:,2].str.contains(q,na=False,case=False)]
        if loc != "الكل": f_df = f_df[f_df.iloc[:,3] == loc]
        if pr > 0: f_df = f_df[f_df['p_val'] <= pr]

        # نظام الـ 9 كروت
        itms = 9
        start = st.session_state.page_idx * itms
        batch = f_df.iloc[start : start + itms]
        
        for i in range(0, len(batch), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(batch):
                    r = batch.iloc[i+j]
                    with cols[j]:
                        st.markdown(f'<div class="nano-card"><div class="c-dev">{r[0]}</div><div style="color:#1d4ed8; font-weight:700;">{r[2]}</div><div class="c-price">{r[4]}</div><div style="font-size:0.8rem; color:#444;">📍 {r[3]}</div></div>', unsafe_allow_html=True)
                        if st.button("التفاصيل الفنية", key=f"det_{i+j}"):
                            st.session_state.selected_dev = r[0]
                            st.session_state.view = 'details'; st.rerun()

    # --- ج. قسم أدوات البروكر (حاسبة الأقساط + حاسبة ROI) ---
    elif st.session_state.view == 'tools':
        st.markdown('<div class="compact-hero hero-tools"><h2>🛠️ أدوات ومساعد البروكر</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

        t1, t2 = st.tabs(["🧮 حاسبة الأقساط", "📈 حاسبة أرباح الاستثمار (ROI)"])

        with t1:
            st.markdown("<h4 style='color:#000;'>أدخل أرقام الوحدة:</h4>", unsafe_allow_html=True)
            in1, in2, in3 = st.columns(3)
            with in1: up = st.number_input("سعر الوحدة", value=2000000, step=100000)
            with in2: dp_p = st.number_input("المقدم %", value=10)
            with yrs_col := in3: yrs = st.number_input("سنين التقسيط", value=8)
            
            val_dp = up * (dp_p/100)
            val_mo = (up - val_dp) / (yrs * 12) if yrs > 0 else 0
            
            st.markdown(f"""
                <div class="calc-box">
                    <div style="display:flex; justify-content:space-around; text-align:center;">
                        <div><span class="res-lbl">💳 كاش المقدم</span><span class="res-val" style="color:#c2410c;">{val_dp:,.0f}</span></div>
                        <div style="width:2px; height:50px; background:#ddd;"></div>
                        <div><span class="res-lbl">📅 قسط شهري</span><span class="res-val" style="color:#15803d;">{val_mo:,.0f}</span></div>
                        <div style="width:2px; height:50px; background:#ddd;"></div>
                        <div><span class="res-lbl">🗓️ ربع سنوي</span><span class="res-val" style="color:#0369a1;">{val_mo*3:,.0f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

        with t2:
            st.markdown('<div class="compact-hero hero-roi" style="margin-top:10px;"><h4>حاسبة العائد الاستثماري ROI</h4></div>', unsafe_allow_html=True)
            r1, r2, r3 = st.columns(3)
            with r1: b_p = st.number_input("سعر الشراء", value=2000000, key="buy")
            with r2: s_p = st.number_input("سعر البيع المتوقع", value=3000000, key="sell")
            with r3: rent = st.number_input("الإيجار المتوقع/شهر", value=15000, key="rent")
            
            prof = s_p - b_p
            roi = (prof/b_p)*100 if b_p>0 else 0
            
            st.markdown(f"""
                <div class="calc-box" style="border-color:#15803d;">
                    <div style="display:flex; justify-content:space-around; text-align:center;">
                        <div><span class="res-lbl">💰 صافي الربح</span><span class="res-val" style="color:#15803d;">{prof:,.0f}</span></div>
                        <div style="width:2px; height:50px; background:#eee;"></div>
                        <div><span class="res-lbl">📈 نسبة العائد</span><span class="res-val" style="color:#166534;">%{roi:.1f}</span></div>
                        <div style="width:2px; height:50px; background:#eee;"></div>
                        <div><span class="res-lbl">🏠 عائد الإيجار</span><span class="res-val" style="color:#1e40af;">%{(rent*12/b_p)*100:.1f}</span></div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

    # --- د. صفحة التفاصيل (الزتونة) ---
    elif st.session_state.view == 'details':
        if st.button("🔙 عودة للشركات"): st.session_state.view = 'comp'; st.rerun()
        dev_n = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev_n]
        st.markdown(f"<div class='compact-hero'><h3>🏢 {dev_n}</h3></div>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📌 {r[2]} - {r[4]}", expanded=True):
                st.write(f"📍 **الموقع:** {r[3]} | 💳 **المقدم:** {r[10]}")
                st.error(f"💡 **الزتونة الفنية:**\n\n{r[11]}")
