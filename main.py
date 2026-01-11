import streamlit as st
import pandas as pd

# 1. إعدادات المتصفح وتصفير الهوامش
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (The Modern Look)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد المزعجة */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] > section:first-child > div:first-child { padding-top: 0rem !important; }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #f0f2f6; color: #1e1e1e;
    }

    /* هيدر الدخول البيضاوي المنسدل */
    .login-oval {
        background: #000; border-radius: 0 0 400px 400px;
        padding: 50px 20px; text-align: center; border-bottom: 5px solid #f59e0b;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2); margin-bottom: 40px;
    }
    .login-oval h1 { color: #f59e0b; font-weight: 900; font-size: 2.5rem; margin: 0; }

    /* كروت المشاريع (تصميم فندقي) */
    .project-box {
        background: white; border-radius: 15px; padding: 20px;
        border: 1px solid #e0e0e0; margin-bottom: 20px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03); transition: 0.4s;
    }
    .project-box:hover { border-right: 10px solid #f59e0b; transform: scale(1.01); }

    .price-label {
        background: #f59e0b; color: black; padding: 4px 15px;
        border-radius: 50px; font-weight: 900; font-size: 1.1rem; float: left;
    }

    .project-name { color: #000; font-size: 1.4rem; font-weight: 900; margin-bottom: 5px; }
    .dev-name { color: #666; font-size: 0.9rem; font-weight: 700; }

    /* شبكة البيانات الصغير */
    .mini-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 15px 0; }
    .mini-item { background: #f8f9fa; padding: 8px; border-radius: 10px; text-align: center; border: 1px solid #eee; }
    .mini-label { color: #999; font-size: 0.7rem; display: block; }
    .mini-value { color: #333; font-weight: 700; font-size: 0.85rem; }

    /* أزرار الملاحة */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        background-color: #fff; border: 1px solid #ddd; padding: 10px 30px; border-radius: 10px; font-weight: 700;
    }
    .stTabs [aria-selected="true"] { background-color: #f59e0b !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. إدارة الداتا والوصول
if 'auth' not in st.session_state: st.session_state.auth = False

@st.cache_data(ttl=600)
def fetch_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    data = pd.read_csv(url)
    data.columns = [str(c).strip() for c in data.columns]
    return data

# --- شاشة الدخول ---
if not st.session_state.auth:
    st.markdown('<div class="login-oval"><h1>معلوماتى العقارية PRO</h1></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        pwd = st.text_input("كود الدخول الموحد", type="password", placeholder="Password here...")
        if st.button("فتح المنصة الآن", use_container_width=True):
            if pwd == "Ma3lomati_2026":
                st.session_state.auth = True
                st.rerun()
            else: st.error("الكود غير صحيح!")
    st.stop()

# --- محتوى المنصة ---
df = fetch_data()

# الهيدر العلوي الذكي
st.markdown("""
    <div style="background:white; padding:15px; border-radius:15px; box-shadow:0 2px 10px rgba(0,0,0,0.05); margin-bottom:25px; display:flex; justify-content:space-between; align-items:center;">
        <h3 style="margin:0; color:#000;">🏠 لوحة تحكم المنصة</h3>
        <span style="background:#000; color:#f59e0b; padding:5px 15px; border-radius:10px; font-weight:700;">إصدار 2026</span>
    </div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏗️ المشاريع (345+)", "🏢 دليل المطورين", "🛠️ أدوات البروكر"])

# --- 1. صفحة المشاريع ---
with tab1:
    col_s, col_a = st.columns([3, 1])
    with col_s: search = st.text_input("🔍 ابحث في المشاريع والمطورين والميزات التنافسية...", "")
    with col_a: 
        areas = ["كل المناطق"] + sorted(df['Area'].dropna().unique().tolist())
        sel_area = st.selectbox("📍 المنطقة", areas)

    # الفلترة الذكية
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_area != "كل المناطق": dff = dff[dff['Area'] == sel_area]

    st.caption(f"نتائج البحث: {len(dff)} مشروع")

    for _, row in dff.iterrows():
        st.markdown(f"""
        <div class="project-box">
            <div class="price-label">{row.get('Min_Val (Start Price)', '-')}</div>
            <div class="dev-name">{row.get('Developer', '-')}</div>
            <div class="project-name">{row.get('Projects', 'اسم المشروع')}</div>
            
            <div class="mini-grid">
                <div class="mini-item"><span class="mini-label">المنطقة</span><span class="mini-value">{row.get('Area', '-')}</span></div>
                <div class="mini-item"><span class="mini-label">المقدم</span><span class="mini-value">{row.get('Down_Payment', '-')}</span></div>
                <div class="mini-item"><span class="mini-label">التقسيط</span><span class="mini-value">{row.get('Installments', '-')}</span></div>
            </div>
            
            <div style="border-top:1px solid #eee; padding-top:10px; font-size:0.9rem;">
                <b style="color:#f59e0b;">🌟 الميزة التنافسية:</b> {row.get('Description', '-')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        with st.expander("📄 سابقة الأعمال وتفاصيل إضافية"):
            st.write(f"**المالك:** {row.get('Owner', '-')}")
            st.write(f"**الاستشاري الهندسي:** {row.get('Consultant', '-')}")
            st.write(f"**موعد التسليم:** {row.get('Delivery', '-')}")
            st.info(row.get('Detailed_Info', 'لا يوجد وصف مطول حالياً'))

# --- 2. صفحة المطورين ---
with tab2:
    st.header("🏢 دليل كبار المطورين")
    devs = df.drop_duplicates(subset=['Developer'])
    for _, d_row in devs.iterrows():
        with st.expander(f"🏢 {d_row['Developer']}"):
            st.markdown(f"**المالك الرئيسي:** {d_row.get('Owner', '-')}")
            st.markdown(f"**عن المطور:**\n{d_row.get('Detailed_Info', 'لا توجد بيانات إضافية')}")

# --- 3. صفحة الأدوات ---
with tab3:
    st.header("🛠️ حاسبات عقارية")
    t1, t2 = st.columns(2)
    with t1:
        st.subheader("💰 القسط الشهري")
        v = st.number_input("سعر الوحدة", value=1000000)
        d = st.number_input("المقدم", value=100000)
        y = st.slider("السنوات", 1, 15, 7)
        if v > 0: st.metric("القسط الشهري", f"{(v-d)/(y*12):,.0f} ج.م")
    with t2:
        st.subheader("📱 عرض واتساب سريع")
        proj_sel = st.selectbox("اختر مشروعاً", df['Projects'].unique())
        st.button("توليد نص العرض")
