import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - النسخة المستقرة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f1f5f9; 
    }

    .block-container { 
        max-width: 1100px; 
        margin: auto; 
        padding: 1rem 3% !important; 
    }

    .header-nav { 
        text-align: right; 
        padding: 15px 0; 
        margin-bottom: 5px;
    }

    .filter-box { 
        background: white; 
        padding: 15px; 
        border-radius: 12px; 
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .project-card-container { 
        background-color: #edf2f7; 
        border-radius: 10px; 
        margin-bottom: 5px !important; 
        display: flex;
        align-items: center;
        border: 1px solid #e2e8f0;
        overflow: hidden;
    }

    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 4px 15px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات مع معالجة الأخطاء
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        # تنظيف أسماء الأعمدة من أي مسافات مخفية
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"فيه مشكلة في ملف جوجل شيت: {e}")
        return None

df = load_data()

if 'page' not in st.session_state:
    st.session_state.page = 'main'
    st.session_state.selected_item = None

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر (بشكل بسيط عشان ميعلقش)
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        
        with c1:
            search_dev = st.text_input("🔍 اسم المطور")
        
        with c2:
            areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist()) if 'Area' in df.columns else ["الكل"]
            search_area = st.selectbox("📍 المنطقة", areas)
            
        with c3:
            # فلتر السعر أو سنوات القسط حسب المتاح في الشيت
            col_to_filter = 'Installments' if 'Installments' in df.columns else 'Price'
            options = ["الكل"] + sorted(df[col_to_filter].dropna().unique().astype(str).tolist()) if col_to_filter in df.columns else ["الكل"]
            search_opt = st.selectbox(f"⏳ {col_to_filter}", options)
        st.markdown('</div>', unsafe_allow_html=True)

        # منطق الفلترة "المؤمن"
        f_df = df.copy()
        if search_dev:
            f_df = f_df[f_df['Developer'].astype(str).str.contains(search_dev, case=False, na=False)]
        if search_area != "الكل":
            f_df = f_df[f_df['Area'] == search_area]
        if search_opt != "الكل" and col_to_filter in df.columns:
            f_df = f_df[f_df[col_to_filter].astype(str) == search_opt]

        # عرض الكروت
        for i, row in f_df.iterrows():
            st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
            col_content, col_img = st.columns([4, 1])
            
            with col_content:
                txt_c, btn_c = st.columns([3, 1])
                with txt_c:
                    st.markdown(f"""
                        <div style="text-align: right; padding: 15px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer', 'بدون اسم')}</div>
                            <div style="color: #D4AF37; font-weight: 700; font-size: 0.9rem;">المالك: {row.get('Owner', '-')}</div>
                            <div style="color: #64748b; font-size: 0.8rem;">📍 {row.get('Area', '-')} | القسط: {row.get('Installments', '-')} | {row.get('Price', '-')}</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("")
                    st.write("")
                    # استخدام index كجزء من المفتاح لضمان عدم تكرار المفاتيح
                    if st.button("التفاصيل", key=f"btn_{i}_{row.get('Developer')}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height: 100px; background-image: url(\'{img_url}\'); background-size: cover; background-position: center;"></div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
else:
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:30px; border-radius:15px; margin-top:10px; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"<h2 style='color:#003366;'>{item.get('Developer')}</h2>", unsafe_allow_html=True)
    st.write(item.get('Description', 'جاري التحديث...'))
    st.markdown('</div>', unsafe_allow_html=True)
