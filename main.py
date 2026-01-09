import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - نظام الشبكة والألوان الملكية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f1f5f9; 
    }

    /* تصميم الكارت المربع */
    .grid-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 15px;
        border-bottom: 5px solid #003366;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        transition: transform 0.2s;
    }
    .grid-card:hover { transform: translateY(-5px); }

    .filter-box { 
        background: white; padding: 20px; border-radius: 15px; 
        margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }

    /* تنسيق الأزرار تحت الكارت */
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 8px !important; padding: 5px !important;
        font-size: 0.85rem !important; width: 100%;
        font-family: 'Cairo', sans-serif; height: 35px;
    }
    
    .details-header {
        background-color: #003366; padding: 30px; border-radius: 15px; 
        margin-bottom: 20px; text-align: center; color: white;
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
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div style="text-align:right; margin-bottom:20px;"><div style="color:#003366; font-weight:900; font-size:2.2rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # شريط المقارنة
        if st.session_state.compare_list:
            c_top = st.columns([4, 1])
            with c_top[0]: st.info(f"📋 القائمة المختارة: {', '.join(st.session_state.compare_list)}")
            with c_top[1]:
                if st.button("📊 قارن الآن"): 
                    st.session_state.page = 'compare'; st.rerun()

        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        f1, f2 = st.columns([2, 1])
        with f1: s_dev = st.text_input("🔍 ابحث عن مطور...")
        with f2: 
            areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
            s_area = st.selectbox("📍 المنطقة", areas)
        st.markdown('</div>', unsafe_allow_html=True)

        # فلترة البيانات
        f_df = df.copy()
        if s_dev: f_df = f_df[f_df['Developer'].astype(str).str.contains(s_dev, case=False, na=False)]
        if s_area != "الكل": f_df = f_df[f_df['Area'] == s_area]

        # --- عرض الشبكة 3 في الصف ---
        cols = st.columns(3) # 3 كروت في كل صف
        for i, row in f_df.reset_index().iterrows():
            with cols[i % 3]: # توزيع الكروت بالتساوي على الأعمدة
                st.markdown(f"""
                    <div class="grid-card">
                        <div style="color: #003366; font-weight: 900; font-size: 1.2rem; margin-bottom: 10px;">{row.get('Developer')}</div>
                        <div style="color: #64748b; font-size: 0.85rem;">📍 {row.get('Area')}</div>
                        <div style="color: #D4AF37; font-weight: bold; font-size: 0.9rem;">💰 {row.get('Price')}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # أزرار التحكم جنب بعض تحت كل كارت
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("👁️ تفاصيل", key=f"det_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()
                with b2:
                    name = str(row['Developer'])
                    is_in = name in st.session_state.compare_list
                    if st.button("➕ قارن" if not is_in else "❌ إزالة", key=f"comp_{i}"):
                        if not is_in: st.session_state.compare_list.append(name)
                        else: st.session_state.compare_list.remove(name)
                        st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)

# --- صفحة التفاصيل (بالألوان الملكية) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'; st.rerun()

    st.markdown(f"""
        <div class="details-header">
            <h1 style="margin:0;">{item.get('Developer')}</h1>
            <p style="opacity:0.8;">{item.get('Area', 'الموقع')}</p>
        </div>
        <div style="background: white; padding: 25px; border-radius: 15px; border-right: 8px solid #003366; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <h3 style="color:#003366;">💡 الزتونة الفنية</h3>
            <p style="font-size:1.1rem; line-height:1.8;">{item.get('Detailed_Info', 'لا توجد بيانات تفصيلية.')}</p>
            <hr>
            <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
            <p><b>💰 السعر:</b> {item.get('Price', '-')}</p>
            <p><b>⏳ التقسيط:</b> {item.get('Installments', '-')}</p>
            <p><b>📝 وصف:</b> {item.get('Description', '-')}</p>
        </div>
    """, unsafe_allow_html=True)

# --- صفحة المقارنة ---
elif st.session_state.page == 'compare':
    st.markdown("<h2 style='text-align:center; color:#003366;'>📊 مقارنة المطورين</h2>", unsafe_allow_html=True)
    if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
    comp_df = df[df['Developer'].isin(st.session_state.compare_list)]
    if not comp_df.empty:
        st.dataframe(comp_df[['Developer', 'Area', 'Price', 'Installments']], use_container_width=True)
    else:
        st.warning("القائمة فارغة")
