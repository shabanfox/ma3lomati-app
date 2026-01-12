import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق الجمالي (CSS) - النسخة المتقدمة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 1rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; }
    
    /* تصميم الهيدر */
    .main-header { background: linear-gradient(90deg, #111 0%, #000 100%); padding: 15px; border-radius: 15px; border-right: 10px solid #f59e0b; text-align: center; margin-bottom: 20px; }
    .header-title { font-weight: 900; font-size: 28px !important; color: #f59e0b; margin: 0; }

    /* شبكة الكروت (Grid) */
    .pro-card { 
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b; 
        border-radius: 12px; padding: 15px; margin-bottom: 10px; text-align: center; 
        min-height: 220px; transition: 0.3s;
    }
    .pro-card:hover { border-color: #f59e0b; transform: scale(1.02); }
    .card-title { color: #f59e0b; font-size: 18px !important; font-weight: 800; }
    
    /* استايل الأدوات المطور */
    .tool-box { background: #0d0d0d; border: 1px dashed #f59e0b; border-radius: 15px; padding: 20px; margin-bottom: 20px; }
    .tool-result { background: #1a150b; color: #f59e0b; font-size: 24px; font-weight: 900; text-align: center; padding: 15px; border-radius: 10px; margin-top: 10px; }

    /* الفلاتر */
    div[data-baseweb="select"], input { background-color: #111 !important; color: white !important; border-radius: 8px !important; }
    .stButton button { background: #1a1a1a !important; color: #f59e0b !important; border: 1px solid #333 !important; font-weight: bold; border-radius: 8px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data.fillna("غير متوفر").astype(str)
    except: return pd.DataFrame()

df = load_data()

# 4. القائمة العلوية
st.markdown('<div class="main-header"><h1 class="header-title">🏢 مـنـصـة مـعـلـومـاتـي PRO</h1></div>', unsafe_allow_html=True)

selected = option_menu(None, ["🏗️ المشاريع", "🏢 المطورين", "🛠️ الأدوات"], 
    icons=["building", "people", "gear"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "2px solid #f59e0b"}})

# إدارة الصفحات
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# --- 🏗️ قسم المشاريع (الشبكة 9 بنسبة 70%) ---
if selected == "🏗️ المشاريع":
    col_main, col_side = st.columns([0.7, 0.3])
    
    with col_side:
        st.markdown("### 🔍 الفلاتر")
        search_q = st.text_input("بحث بالاسم...")
        area_choice = st.selectbox("المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()) if 'Area' in df.columns else ["الكل"])
        st.info("💡 استخدم البحث السريع للوصول للمشروع مباشرة")

    with col_main:
        f_df = df.copy()
        if search_q: f_df = f_df[f_df.apply(lambda r: search_q.lower() in r.astype(str).str.lower().values, axis=1)]
        if area_choice != "الكل": f_df = f_df[f_df['Area'] == area_choice]

        items = 9  # شبكة 9
        total_p = max(1, math.ceil(len(f_df) / items))
        curr = f_df.iloc[st.session_state.p_page * items : (st.session_state.p_page + 1) * items]

        for i in range(0, len(curr), 3):
            grid = st.columns(3)
            for j in range(3):
                if i+j < len(curr):
                    row = curr.iloc[i+j]
                    with grid[j]:
                        st.markdown(f"""
                            <div class="pro-card">
                                <div class="card-title">{row.get('Project Name', 'مشروع')}</div>
                                <div style="color:#777; font-size:12px; margin-bottom:10px;">{row.get('Developer', 'مطور')}</div>
                                <div style="text-align:right; font-size:13px; color:#ccc;">
                                    <p>📍 {row.get('Area', '-')}</p>
                                    <p>🏠 {row.get('شقق/فيلات', '-')}</p>
                                    <p>📏 {row.get('Size (Acres)', '-')} فدان</p>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
        
        # أزرار التنقل
        n1, n2, n3 = st.columns([1, 1, 1])
        if n3.button("التالي ⬅️") and st.session_state.p_page < total_p-1: st.session_state.p_page += 1; st.rerun()
        n2.markdown(f"<center>{st.session_state.p_page+1} / {total_p}</center>", unsafe_allow_html=True)
        if n1.button("➡️ السابق") and st.session_state.p_page > 0: st.session_state.p_page -= 1; st.rerun()

# --- 🏢 قسم المطورين (شبكة 9) ---
elif selected == "🏢 المطورين":
    devs = df[['Developer', 'Owner']].drop_duplicates().reset_index(drop=True)
    st.markdown("### 🏢 دليل المطورين المعتمدين")
    
    items = 9
    total_d = max(1, math.ceil(len(devs) / items))
    curr_d = devs.iloc[st.session_state.d_page * items : (st.session_state.d_page + 1) * items]

    for i in range(0, len(curr_d), 3):
        grid = st.columns(3)
        for j in range(3):
            if i+j < len(curr_d):
                row = curr_d.iloc[i+j]
                with grid[j]:
                    st.markdown(f"""
                        <div class="pro-card" style="min-height:140px;">
                            <div class="card-title">{row['Developer']}</div>
                            <div style="color:#888;">👤 المالك: {row['Owner']}</div>
                        </div>
                    """, unsafe_allow_html=True)

# --- 🛠️ قسم الأدوات (تصميم مطور بالكامل) ---
elif selected == "🛠️ الأدوات":
    st.markdown("### 🛠️ لوحة الأدوات والحسابات الذكية")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("<div class='tool-box'>", unsafe_allow_html=True)
        st.subheader("💰 حاسبة الأقساط")
        price = st.number_input("سعر الوحدة الإجمالي", value=1000000, step=100000)
        down_p = st.number_input("المقدم (Amount)", value=100000)
        years = st.slider("سنوات التقسيط", 1, 15, 7)
        monthly = (price - down_p) / (years * 12)
        st.markdown(f"<div class='tool-result'>{monthly:,.0f} ج.م / شهر</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("<div class='tool-box'>", unsafe_allow_html=True)
        st.subheader("📐 محول المساحات")
        val = st.number_input("المساحة بالفدان", value=1.0)
        res = val * 4200
        st.markdown(f"<div class='tool-result'>{res:,.0f} متر مربع</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='tool-box'>", unsafe_allow_html=True)
    st.subheader("📝 ملاحظات العميل السريعة")
    st.text_area("سجل تفاصيل المكالمة هنا...", height=150)
    st.markdown("</div>", unsafe_allow_html=True)
