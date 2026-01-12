import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات النظام وتطوير الخطوط والتصميم
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    /* استيراد خط القاهرة بأوزان متعددة */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* تنسيق الحاوية الرئيسية */
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; 
        text-align: right; 
        font-family: 'Cairo', sans-serif;
    }

    /* تحسين العناوين الرئيسية */
    h2, h3 {
        font-family: 'Cairo', sans-serif;
        font-weight: 900 !important;
        letter-spacing: 0.5px;
    }

    /* كروت الشبكة المطورة */
    .grid-card {
        background: rgba(17, 17, 17, 0.8);
        border: 1px solid #282828;
        border-top: 5px solid #f59e0b;
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 20px;
        height: 400px;
        transition: all 0.4s ease-in-out;
        color: white;
        display: flex;
        flex-direction: column;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    .grid-card:hover { 
        border-color: #f59e0b; 
        transform: translateY(-8px); 
        box-shadow: 0 15px 35px rgba(245, 158, 11, 0.15);
        background: #0d0d0d;
    }
    
    /* وضوح الخطوط داخل الكارت */
    .card-title { 
        color: #f59e0b; 
        font-size: 22px; 
        font-weight: 900; 
        margin-bottom: 8px;
        line-height: 1.4;
    }
    .card-subtitle { 
        color: #e0e0e0; 
        font-size: 15px; 
        font-weight: 600;
        margin-bottom: 15px; 
        border-bottom: 1px solid #333; 
        padding-bottom: 10px; 
    }
    
    .stat-line { 
        display: flex; 
        justify-content: space-between; 
        font-size: 15px; 
        margin-bottom: 12px; 
        line-height: 1.6;
    }
    .stat-label { color: #999; font-weight: 400; }
    .stat-value { color: #f59e0b; font-weight: 700; }

    .badge-gold { 
        background: linear-gradient(90deg, #f59e0b, #d97706);
        color: black; 
        padding: 4px 12px; 
        border-radius: 6px; 
        font-weight: 800; 
        font-size: 15px; 
        align-self: flex-start; 
        margin-bottom: 15px; 
        box-shadow: 0 4px 10px rgba(245,158,11,0.3);
    }

    /* تطوير شكل الأزرار */
    .stButton button {
        background: #1a1a1a !important;
        color: #f59e0b !important;
        border: 2px solid #f59e0b !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        height: 45px !important;
        transition: 0.3s !important;
    }
    .stButton button:hover {
        background: #f59e0b !important;
        color: black !important;
    }

    /* تحسين نصوص الـ Expander */
    .stExpander {
        border: none !important;
        background: transparent !important;
    }
    .stExpander summary {
        color: #888 !important;
        font-weight: 600 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات
@st.cache_data(ttl=300)
def load_all_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_all_data()

# 3. القائمة العلوية
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    default_index=1, # جعل المشاريع هي الافتتاحية
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "padding": "10px", "border-bottom": "2px solid #333"},
        "nav-link": {"font-size": "18px", "color":"#888", "font-family": "Cairo", "font-weight": "600"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- محتوى الصفحات (باستخدام التصميم المطور) ---

if selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; margin-bottom:30px;'>🏗️ دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
    
    if not df.empty:
        # فلاتر أنيقة
        f1, f2, f3 = st.columns([2,1,1])
        with f1: s_p = st.text_input("🔍 ابحث عن اسم المشروع أو المطور...")
        with f2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()) if 'Area' in df.columns else ["الكل"])
        with f3: t_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["الكل"])
        
        dff = df.copy()
        if s_p: dff = dff[dff.apply(lambda r: s_p.lower() in str(r).lower(), axis=1)]
        if a_p != "الكل": dff = dff[dff['Area'] == a_p]
        if t_p != "الكل": dff = dff[dff['Type'] == t_p]

        items_per_page = 9
        total_pages = max(1, math.ceil(len(dff)/items_per_page))
        if 'pg_p' not in st.session_state: st.session_state.pg_p = 1
        
        curr_p = dff.iloc[(st.session_state.pg_p-1)*items_per_page : st.session_state.pg_p*items_per_page]

        for i in range(0, len(curr_p), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_p):
                    row = curr_p.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div class="card-title">{row.get('Projects','-')}</div>
                                <div class="card-subtitle">🏢 {row.get('Developer','-')}</div>
                                <div class="badge-gold">يبدأ من: {row.get('Min_Val (Start Price)','0')}</div>
                                <div class="stat-line"><span class="stat-label">📍 الموقع:</span><span class="stat-value">{row.get('Area','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">💰 المقدم:</span><span class="stat-value">{row.get('Down_Payment','-')}</span></div>
                                <div class="stat-line"><span class="stat-label">⏳ التقسيط:</span><span class="stat-value">{row.get('Installments','-')}</span></div>
                                <div style="flex-grow:1"></div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("🔍 عرض كامل مواصفات المشروع"):
                            st.write(row.to_dict())

        # أزرار تنقل فخمة
        st.write("---")
        b1, b2, b3 = st.columns([1,2,1])
        with b1: 
            if st.session_state.pg_p > 1:
                if st.button("⬅️ السابق"): st.session_state.pg_p -= 1; st.rerun()
        with b2: st.markdown(f"<p style='text-align:center; color:#666; font-weight:700;'>صفحة {st.session_state.pg_p} من {total_pages}</p>", unsafe_allow_html=True)
        with b3:
            if st.session_state.pg_p < total_pages:
                if st.button("التالي ➡️"): st.session_state.pg_p += 1; st.rerun()

elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center; margin-bottom:30px;'>🏢 سجل كبار المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    if not df.empty:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        s_d = st.text_input("🔍 ابحث عن المطور...")
        if s_d: devs = devs[devs['Developer'].str.contains(s_d, case=False, na=False)]

        items_per_page = 9
        total_pages = max(1, math.ceil(len(devs)/items_per_page))
        if 'pg_d' not in st.session_state: st.session_state.pg_d = 1
        
        curr_d = devs.iloc[(st.session_state.pg_d-1)*items_per_page : st.session_state.pg_d*items_per_page]

        for i in range(0, len(curr_d), 3):
            cols = st.columns(3)
            for j in range(3):
                if i+j < len(curr_d):
                    row = curr_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div class="card-title">🏢 {row['Developer']}</div>
                                <div class="card-subtitle">👤 المالك: {row['Owner']}</div>
                                <div style="font-size:15px; color:#bbb; line-height:1.8; flex-grow:1; overflow:hidden;">
                                    <b>نبذة الشركة:</b><br>{str(row['Detailed_Info'])[:160]}...
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("📄 سابقة الأعمال والتفاصيل"):
                            st.write(row['Detailed_Info'])

        st.write("---")
        d1, d2, d3 = st.columns([1,2,1])
        with d1:
            if st.session_state.pg_d > 1:
                if st.button("⬅️ السابق ", key="d_prev"): st.session_state.pg_d -= 1; st.rerun()
        with d2: st.markdown(f"<p style='text-align:center; color:#666; font-weight:700;'>صفحة {st.session_state.pg_d} من {total_pages}</p>", unsafe_allow_html=True)
        with d3:
            if st.session_state.pg_d < total_pages:
                if st.button("التالي ➡️ ", key="d_next"): st.session_state.pg_d += 1; st.rerun()

elif selected == "🛠️ أدوات البروكر":
    # (كود الأدوات كما هو مع تحسين الخطوط تلقائياً بفضل الـ CSS العلوي)
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات العمل اليومية</h2>", unsafe_allow_html=True)
    # ... (يمكنك وضع كود الحاسبة هنا) ...
