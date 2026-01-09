import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - الحفاظ على الهوية البصرية الرمادية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f1f5f9; 
    }

    .filter-box { 
        background: white; padding: 15px; border-radius: 12px; 
        margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }

    .project-card-container { 
        background-color: #edf2f7; border-radius: 10px; 
        margin-bottom: 8px !important; display: flex;
        align-items: center; border: 1px solid #e2e8f0; overflow: hidden;
    }

    .comp-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 2px solid #e2e8f0; text-align: center; height: 100%;
    }
    
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 6px !important; padding: 4px 10px !important;
        font-size: 0.8rem !important; width: 100%;
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
if 'compare_list' not in st.session_state: st.session_state.compare_list = []
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div style="text-align:right;"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # شريط المقارنة
        if st.session_state.compare_list:
            c_top = st.columns([4, 1])
            with c_top[0]: st.info(f"📋 القائمة: {', '.join(st.session_state.compare_list)}")
            with c_top[1]:
                if st.button("📊 قارن الآن"): st.session_state.page = 'compare'; st.rerun()

        # الفلاتر (تم إعادتها بالكامل)
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        f1, f2, f3 = st.columns(3)
        with f1: s_dev = st.text_input("🔍 البحث بالمطور")
        with f2: 
            areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
            s_area = st.selectbox("📍 المنطقة", areas)
        with f3: s_price = st.selectbox("💰 السعر", ["الكل", "أقل من 5 مليون", "10 مليون+"])
        st.markdown('</div>', unsafe_allow_html=True)

        # منطق الفلترة
        f_df = df.copy()
        if s_dev: f_df = f_df[f_df['Developer'].astype(str).str.contains(s_dev, case=False, na=False)]
        if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]

        # عرض الكروت
        for i, row in f_df.iterrows():
            st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
            col_info, col_img = st.columns([4, 1])
            with col_info:
                txt_c, btn_det, btn_comp = st.columns([2.5, 0.7, 0.8])
                with txt_c:
                    st.markdown(f"""
                        <div style="text-align: right; padding: 15px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.2rem;">{row.get('Developer')}</div>
                            <div style="color: #64748b; font-size: 0.85rem;">📍 {row.get('Area')} | {row.get('Price')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_det:
                    st.write("")
                    if st.button("التفاصيل", key=f"d_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()
                with btn_comp:
                    st.write("")
                    name = str(row['Developer'])
                    is_in = name in st.session_state.compare_list
                    if st.button("➕ مقارنة" if not is_in else "❌ إزالة", key=f"c_{i}"):
                        if not is_in: st.session_state.compare_list.append(name)
                        else: st.session_state.compare_list.remove(name)
                        st.rerun()
            with col_img:
                img = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height: 100px; background-image: url(\'{img}\'); background-size: cover; background-position: center;"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:30px; border-radius:15px; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
    st.markdown(f"<h2>{item.get('Developer')}</h2>", unsafe_allow_html=True)
    st.write(item.get('Description', 'لا يوجد وصف.'))
    st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة المقارنة ---
elif st.session_state.page == 'compare':
    st.markdown("<h2 style='text-align:center;'>📊 المقارنة</h2>", unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
    comp_df = df[df['Developer'].isin(st.session_state.compare_list)]
    cols = st.columns(len(comp_df) if len(comp_df) > 0 else 1)
    for idx, (i, row) in enumerate(comp_df.iterrows()):
        with cols[idx]:
            st.markdown(f"""
                <div class="comp-card">
                    <div style="color:#003366; font-weight:900;">{row.get('Developer')}</div>
                    <hr>
                    <p><small>السعر:</small><br>{row.get('Price')}</p>
                    <p><small>المنطقة:</small><br>{row.get('Area')}</p>
                </div>
            """, unsafe_allow_html=True)
