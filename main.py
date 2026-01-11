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

    .custom-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 25px; margin-bottom: 20px;
        transition: 0.3s all; color: white;
    }
    
    /* ستايل أزرار التالي والسابق */
    .stButton button {
        background-color: #1a1a1a !important; color: #f59e0b !important;
        border: 1px solid #f59e0b !important; border-radius: 10px !important;
        font-weight: bold !important; width: 100% !important;
    }
    .stButton button:hover { background-color: #f59e0b !important; color: black !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_master_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_master_data()

# 4. القائمة العلوية
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-size": "18px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- 1. شاشة أدوات البروكر ---
if selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ عُدة البروكر المحترف</h2>", unsafe_allow_html=True)
    col_calc, col_roi, col_msg = st.columns(3)
    
    with col_calc:
        st.markdown("<div class='custom-card'><h3>💰 حاسبة القسط الذكية</h3>", unsafe_allow_html=True)
        total_price = st.number_input("إجمالي سعر الوحدة (ج.م)", min_value=0, value=1000000, step=100000)
        down_payment_pct = st.number_input("نسبة المقدم (%)", min_value=0, max_value=100, value=10, step=5)
        calculated_down_payment = (down_payment_pct / 100) * total_price
        remaining_amount = total_price - calculated_down_payment
        st.markdown(f"<p style='color:#888;'>المقدم: {calculated_down_payment:,.0f} | المتبقي: {remaining_amount:,.0f}</p>", unsafe_allow_html=True)
        installment_years = st.number_input("سنوات التقسيط", min_value=1, max_value=20, value=7, step=1)
        if total_price > 0:
            st.markdown(f"<div style='border:2px solid #f59e0b; text-align:center; padding:10px; border-radius:10px;'><span style='color:#f59e0b; font-size:24px; font-weight:900;'>{remaining_amount/(installment_years*12):,.0f} ج.م/شهر</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_roi:
        st.markdown("<div class='custom-card'><h3>📈 حاسبة العائد ROI</h3>", unsafe_allow_html=True)
        t_inv = st.number_input("قيمة الاستثمار", min_value=0, value=2000000, step=100000)
        rent = st.number_input("إيجار شهري متوقع", min_value=0, value=15000, step=1000)
        if t_inv > 0:
            st.markdown(f"<div style='border:2px solid #00ffcc; text-align:center; padding:10px; border-radius:10px;'><span style='color:#00ffcc; font-size:24px; font-weight:900;'>{(rent*12/t_inv)*100:.2f} % سنوياً</span></div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_msg:
        st.markdown("<div class='custom-card'><h3>📱 عرض سريع</h3>", unsafe_allow_html=True)
        c_name = st.text_input("اسم العميل")
        p_list = df['Projects'].dropna().unique() if not df.empty else ["لا توجد بيانات"]
        s_proj = st.selectbox("اختر المشروع", p_list)
        if st.button("تجهيز الرسالة"):
            st.text_area("النص الجاهز:", value=f"تحية طيبة {c_name}.. أرشح لك مشروع {s_proj}", height=100)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: s_p = st.text_input("🔍 بحث عام...")
    with c2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()) if 'Area' in df.columns else ["الكل"])
    with c3: t_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["الكل"])
    
    dff = df.copy()
    if s_p: dff = dff[dff.apply(lambda r: s_p.lower() in str(r).lower(), axis=1)]
    for _, row in dff.head(20).iterrows(): # عرض أول 20 فقط للتجربة
        st.markdown(f"<div class='custom-card'><h3 style='color:#f59e0b;'>{row.get('Projects','-')}</h3><p>المطور: {row.get('Developer','-')}</p></div>", unsafe_allow_html=True)

# --- 3. شاشة المطورين (مع خاصية التصفح 8 في كل صفحة) ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    # تحضير البيانات
    if not df.empty and 'Developer' in df.columns:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer']).reset_index(drop=True)
        
        # محرك البحث داخل المطورين
        search_d = st.text_input("🔍 ابحث عن اسم مطور محدد...")
        if search_d:
            devs = devs[devs['Developer'].str.contains(search_d, case=False, na=False)]

        # --- منطق التقسيم (Pagination) ---
        items_per_page = 8
        total_pages = math.ceil(len(devs) / items_per_page)
        
        if 'current_page' not in st.session_state:
            st.session_state.current_page = 1

        # تحديد نطاق المطورين للعرض
        start_idx = (st.session_state.current_page - 1) * items_per_page
        end_idx = start_idx + items_per_page
        current_devs = devs.iloc[start_idx:end_idx]

        # عرض الكروت
        for _, row in current_devs.iterrows():
            st.markdown(f"""
                <div class="custom-card" style="border-right-color:white;">
                    <h3 style="color:#f59e0b; margin:0;">🏢 {row['Developer']}</h3>
                    <p style="margin-top:5px;"><b>المالك:</b> {row['Owner']}</p>
                    <p style='color:#bbb; font-size:14px;'>{row['Detailed_Info'] if pd.notna(row['Detailed_Info']) else 'لا توجد تفاصيل.'}</p>
                </div>
            """, unsafe_allow_html=True)

        # أزرار التنقل (التالي والسابق)
        st.write("---")
        c_prev, c_page, c_next = st.columns([1, 2, 1])
        
        with c_prev:
            if st.session_state.current_page > 1:
                if st.button("⬅️ السابق"):
                    st.session_state.current_page -= 1
                    st.rerun()

        with c_page:
            st.markdown(f"<p style='text-align:center; color:#888;'>صفحة {st.session_state.current_page} من {total_pages}</p>", unsafe_allow_html=True)

        with c_next:
            if st.session_state.current_page < total_pages:
                if st.button("التالي ➡️"):
                    st.session_state.current_page += 1
                    st.rerun()
    else:
        st.error("لم يتم العثور على بيانات.")
