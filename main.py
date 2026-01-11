import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu 
import math

# 1. إعدادات النظام
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (Premium Black & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* تصميم الكروت في الشبكة */
    .grid-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222;
        border-top: 4px solid #f59e0b;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        height: 300px;
        transition: 0.3s all;
        color: white;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    .grid-card:hover { 
        border-color: #f59e0b; 
        transform: translateY(-5px); 
        box-shadow: 0 5px 15px rgba(245, 158, 11, 0.2); 
    }
    
    .card-title { color: #f59e0b; font-size: 18px; font-weight: 900; }
    .card-subtitle { color: #888; font-size: 13px; margin-bottom: 10px; }
    .card-body { color: #bbb; font-size: 12px; line-height: 1.5; overflow: hidden; text-overflow: ellipsis; }

    /* أزرار التنقل بين الصفحات */
    .stButton button {
        background-color: #1a1a1a !important; color: #f59e0b !important;
        border: 1px solid #f59e0b !important; border-radius: 8px !important;
        width: 100%;
    }
    
    /* أدوات البروكر */
    .tool-card {
        background: #0a0a0a; border: 1px solid #222; border-right: 5px solid #f59e0b;
        padding: 20px; border-radius: 15px; height: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محرك جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_data()

# 4. القائمة العلوية (من اليسار لليمين: أدوات - مشاريع - مطورين)
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-size": "17px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- القسم الأول: أدوات البروكر ---
if selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ عُدة البروكر المحترف</h2>", unsafe_allow_html=True)
    col_calc, col_roi, col_msg = st.columns(3)
    
    with col_calc:
        st.markdown("<div class='tool-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        price = st.number_input("إجمالي السعر (ج.م)", min_value=0, value=1000000, step=100000)
        down_pct = st.number_input("نسبة المقدم (%)", min_value=0, max_value=100, value=10, step=5)
        down_val = (down_pct/100) * price
        remain = price - down_val
        st.write(f"المقدم: {down_val:,.0f} | المتبقي: {remain:,.0f}")
        years = st.number_input("سنوات التقسيط", min_value=1, max_value=20, value=7)
        if years > 0:
            monthly = remain / (years * 12)
            st.markdown(f"<div style='background:#111; padding:10px; border-radius:10px; border:1px solid #f59e0b; text-align:center;'><h3 style='color:#f59e0b; margin:0;'>{monthly:,.0f} ج.م/شهر</h3></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_roi:
        st.markdown("<div class='tool-card'><h3>📈 حاسبة العائد ROI</h3>", unsafe_allow_html=True)
        inv = st.number_input("قيمة الاستثمار", min_value=0, value=2000000)
        rent = st.number_input("إيجار شهري متوقع", min_value=0, value=15000)
        if inv > 0:
            roi = (rent * 12 / inv) * 100
            st.markdown(f"<div style='background:#111; padding:10px; border-radius:10px; border:1px solid #00ffcc; text-align:center;'><h3 style='color:#00ffcc; margin:0;'>{roi:.2f} % سنوياً</h3></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_msg:
        st.markdown("<div class='tool-card'><h3>📱 رسالة عرض</h3>", unsafe_allow_html=True)
        c_name = st.text_input("اسم العميل")
        p_list = df['Projects'].dropna().unique() if not df.empty else ["لا توجد مشاريع"]
        s_proj = st.selectbox("المشروع", p_list)
        if st.button("تجهيز النص"):
            st.code(f"أهلاً {c_name}.. أرشح لك مشروع {s_proj} بتفاصيل استثمارية مميزة.")
        st.markdown("</div>", unsafe_allow_html=True)

# --- القسم الثاني: المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: search_p = st.text_input("🔍 ابحث عن أي شيء...")
    with c2: area_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()) if 'Area' in df.columns else ["الكل"])
    with c3: type_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["الكل"])
    
    # فلترة وعرض مبسط للمشاريع (يمكنك تطبيق الشبكة هنا أيضاً لاحقاً)
    dff_p = df.copy()
    if search_p: dff_p = dff_p[dff_p.apply(lambda r: search_p.lower() in str(r).lower(), axis=1)]
    for _, row in dff_p.head(10).iterrows():
        st.markdown(f"<div class='tool-card' style='margin-bottom:10px;'><h4>{row.get('Projects','-')}</h4><p>{row.get('Developer','-')} | {row.get('Area','-')}</p></div>", unsafe_allow_html=True)

# --- القسم الثالث: المطورين (شبكة 3×3 و9 في الصفحة) ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    if not df.empty and 'Developer' in df.columns:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        search_d = st.text_input("🔍 ابحث عن مطور...")
        if search_d:
            devs = devs[devs['Developer'].str.contains(search_d, case=False, na=False)]

        # نظام الصفحات (9 مطورين في الصفحة)
        items_per_page = 9
        total_pages = math.ceil(len(devs) / items_per_page)
        
        if 'page' not in st.session_state: st.session_state.page = 1

        start_idx = (st.session_state.page - 1) * items_per_page
        current_devs = devs.iloc[start_idx : start_idx + items_per_page]

        # عرض الشبكة
        for i in range(0, len(current_devs), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_devs):
                    row = current_devs.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div>
                                    <div class="card-title">🏢 {row['Developer']}</div>
                                    <div class="card-subtitle">👤 المالك: {row['Owner']}</div>
                                    <div class="card-body">{str(row['Detailed_Info'])[:150]}...</div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("قراءة المزيد"):
                            st.write(row['Detailed_Info'])

        # أزرar التنقل
        st.write("---")
        p1, p2, p3 = st.columns([1, 2, 1])
        with p1:
            if st.session_state.page > 1:
                if st.button("⬅️ السابق"):
                    st.session_state.page -= 1
                    st.rerun()
        with p2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page} من {total_pages}</p>", unsafe_allow_html=True)
        with p3:
            if st.session_state.page < total_pages:
                if st.button("التالي ➡️"):
                    st.session_state.page += 1
                    st.rerun()
