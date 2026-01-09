import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - تركيز على المربعات النظيفة بدون أيقونات
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* مربع الفلتر المطور */
    .filter-card {
        background: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 30px;
    }

    /* الكارت المربع للشركة */
    .grid-card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        height: 140px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 1px solid #e2e8f0;
        border-bottom: 4px solid #003366;
        transition: all 0.2s ease;
    }
    .grid-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.08);
    }

    /* تنسيق الأزرار تحت الكارت */
    div.stButton > button {
        background-color: white !important;
        color: #003366 !important;
        border: 1px solid #003366 !important;
        border-radius: 6px !important;
        font-family: 'Cairo', sans-serif !important;
        font-weight: bold !important;
        height: 35px;
        font-size: 0.9rem !important;
    }
    div.stButton > button:hover {
        background-color: #003366 !important;
        color: white !important;
    }

    .title-text {
        color: #003366;
        font-weight: 900;
        font-size: 2rem;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'compare_list' not in st.session_state: st.session_state.compare_list = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div class="title-text">منصة معلوماتى العقارية</div>', unsafe_allow_html=True)

    if df is not None:
        # مربع الفلتر النظيف
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            search_query = st.text_input("ابحث عن مطور أو ميزة فنية (مثلاً: تشطيب كامل، تقسيط 10 سنين)", placeholder="اكتب للبحث...")
        with c2:
            areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
            s_area = st.selectbox("تصفية بالمنطقة", areas)
        st.markdown('</div>', unsafe_allow_html=True)

        # منطق الفلترة
        f_df = df.copy()
        if s_area != "الكل":
            f_df = f_df[f_df['Area'] == s_area]
        if search_query:
            f_df = f_df[
                f_df['Developer'].astype(str).str.contains(search_query, case=False, na=False) |
                f_df['Detailed_Info'].astype(str).str.contains(search_query, case=False, na=False)
            ]

        # عرض الشبكة
        grid_cols = st.columns(3)
        for idx, (i, row) in enumerate(f_df.reset_index().iterrows()):
            with grid_cols[idx % 3]:
                st.markdown(f"""
                    <div class="grid-card">
                        <div style="color:#003366; font-weight:900; font-size:1.1rem; margin-bottom:5px;">{row.get('Developer')}</div>
                        <div style="color:#64748b; font-size:0.85rem;">{row.get('Area')}</div>
                        <div style="color:#D4AF37; font-weight:bold; font-size:0.9rem; margin-top:8px;">{row.get('Price')}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # أزرار الأكشن
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("التفاصيل", key=f"d_{idx}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()
                with b2:
                    name = str(row['Developer'])
                    is_in = name in st.session_state.compare_list
                    if st.button("مقارنة" if not is_in else "إزالة", key=f"c_{idx}"):
                        if not is_in: st.session_state.compare_list.append(name)
                        else: st.session_state.compare_list.remove(name)
                        st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)

# --- صفحة التفاصيل (نفس الاستايل المربع النظيف) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("عودة"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"""
        <div style="background-color: #003366; padding: 30px; border-radius: 12px; color: white; text-align: center; margin-bottom: 20px;">
            <h2 style="margin:0;">{item.get('Developer')}</h2>
            <p style="opacity: 0.8; margin-top:10px;">{item.get('Area')}</p>
        </div>
        <div class="filter-card" style="border-right: 8px solid #003366;">
            <h3 style="color:#003366; margin-bottom:15px;">الزتونة الفنية</h3>
            <p style="font-size:1.1rem; line-height:1.7; color:#1e293b;">{item.get('Detailed_Info', 'لا توجد بيانات.')}</p>
            <hr style="border:0; border-top: 1px solid #eee; margin:20px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <p><b>المالك:</b> {item.get('Owner', '-')}</p>
                <p><b>السعر:</b> {item.get('Price', '-')}</p>
                <p><b>التقسيط:</b> {item.get('Installments', '-')}</p>
                <p><b>الاستلام:</b> {item.get('Delivery', '-')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
