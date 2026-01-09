import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - الحفاظ على الهوية البصرية الملكية
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
        background-color: white; border-radius: 10px; 
        padding: 15px; margin-bottom: 10px; 
        border-right: 5px solid #003366;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }

    .comp-card {
        background: white; border-radius: 15px; padding: 20px;
        border: 2px solid #e2e8f0; text-align: center; height: 100%;
    }
    
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 6px !important; padding: 4px 10px !important;
        font-size: 0.9rem !important; width: 100%;
        font-family: 'Cairo', sans-serif;
    }

    /* تنسيق خاص لصفحة التفاصيل */
    .details-header {
        background-color: #003366; padding: 25px; border-radius: 12px; 
        margin-bottom: 20px; text-align: center; color: white;
    }
    .details-card {
        background-color: white; padding: 20px; border-radius: 10px;
        border-right: 6px solid #003366; margin-bottom: 15px;
        color: #1e293b;
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
    st.markdown('<div style="text-align:right;"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # شريط المقارنة
        if st.session_state.compare_list:
            c_top = st.columns([4, 1])
            with c_top[0]: st.info(f"📋 القائمة المختارة: {', '.join(st.session_state.compare_list)}")
            with c_top[1]:
                if st.button("📊 قارن الآن"): 
                    st.session_state.page = 'compare'
                    st.rerun()

        # الفلاتر
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
            st.markdown(f"""
                <div class="project-card-container">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 3;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.2rem;">{row.get('Developer')}</div>
                            <div style="color: #64748b; font-size: 0.85rem;">📍 {row.get('Area')} | {row.get('Price')}</div>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            c_btn1, c_btn2 = st.columns([1, 1])
            with c_btn1:
                if st.button("👁️ التفاصيل", key=f"det_{i}"):
                    st.session_state.selected_item = row.to_dict()
                    st.session_state.page = 'details'
                    st.rerun()
            with c_btn2:
                name = str(row['Developer'])
                is_in = name in st.session_state.compare_list
                if st.button("➕ مقارنة" if not is_in else "❌ إزالة", key=f"comp_{i}"):
                    if not is_in: st.session_state.compare_list.append(name)
                    else: st.session_state.compare_list.remove(name)
                    st.rerun()

# --- صفحة التفاصيل (بالألوان الموحدة) ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("⬅️ عودة للقائمة الرئيسية"):
        st.session_state.page = 'main'
        st.rerun()

    st.markdown(f"""
        <div class="details-header">
            <h1 style="margin:0;">{item.get('Developer')}</h1>
            <p style="opacity:0.8;">{item.get('Projects', 'بيانات المطور')}</p>
        </div>
        
        <div class="details-card">
            <h3 style="color:#003366;">💡 الزتونة الفنية</h3>
            <p style="font-size:1.1rem; line-height:1.6;">{item.get('Detailed_Info', 'لا توجد بيانات تفصيلية متوفرة حالياً.')}</p>
        </div>

        <div class="details-card" style="border-right-color: #D4AF37;">
            <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
            <p><b>📍 المنطقة:</b> {item.get('Area', '-')}</p>
            <p><b>💰 السعر:</b> {item.get('Price', '-')}</p>
            <p><b>⏳ التقسيط:</b> {item.get('Installments', '-')}</p>
            <hr>
            <p><b>📝 الوصف:</b> {item.get('Description', '-')}</p>
        </div>
    """, unsafe_allow_html=True)

# --- صفحة المقارنة ---
elif st.session_state.page == 'compare':
    st.markdown("<h2 style='text-align:center;'>📊 جدول المقارنة</h2>", unsafe_allow_html=True)
    if st.button("⬅️ عودة"): 
        st.session_state.page = 'main'
        st.rerun()
    
    comp_df = df[df['Developer'].isin(st.session_state.compare_list)]
    if not comp_df.empty:
        st.table(comp_df[['Developer', 'Area', 'Price', 'Installments']])
    else:
        st.warning("القائمة فارغة")
