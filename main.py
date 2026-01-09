import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية | التفاصيل", layout="wide")

# كود التصميم المطور
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }
    .main-title { color: #003366; font-weight: 900; font-size: 2.5rem; margin-bottom: 10px; }
    .detail-card { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-top: 20px; }
    .back-btn { background: #64748b; color: white; border: none; padding: 8px 20px; border-radius: 8px; cursor: pointer; text-decoration: none; }
    .section-head { color: #D4AF37; font-weight: 700; font-size: 1.5rem; border-bottom: 2px solid #D4AF37; display: inline-block; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# وظيفة جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# إدارة التنقل بين الصفحات
if 'selected_dev' not in st.session_state:
    st.session_state.selected_dev = None

# --- الصفحة الرئيسية ---
if st.session_state.selected_dev is None:
    st.markdown('<div style="padding: 20px 8%; background: white; border-bottom: 1px solid #ddd;">'
                '<h1 class="main-title">معلوماتى <span style="color:#D4AF37;">العقارية</span></h1>'
                '<p style="color:#64748b;">دليلك الشامل لأقوى المطورين في مصر</p></div>', unsafe_allow_html=True)
    
    # (هنا بنحط الفلاتر اللي عملناها قبل كدة...)
    # لنختصر الكود، سننتقل فوراً لعرض الكروت
    if df is not None:
        for _, row in df.iterrows():
            col1, col2 = st.columns([4, 1])
            with col1:
                # عرض كارت المطور
                st.markdown(f"""
                <div style="background:white; padding:20px; border-radius:15px; margin-bottom:10px; border-right: 5px solid #003366;">
                    <h3 style="margin:0; color:#003366;">{row.get('Developer', 'مطور')}</h3>
                    <p style="margin:5px 0; color:#64748b;">📍 {row.get('Area', '-')} | 👤 المالك: {row.get('Owner', '-')}</p>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                # زرار عرض التفاصيل
                if st.button(f"عرض التفاصيل", key=row.get('Developer')):
                    st.session_state.selected_dev = row.to_dict()
                    st.rerun()

# --- صفحة التفاصيل ---
else:
    dev = st.session_state.selected_dev
    if st.button("⬅️ رجوع للرئيسية"):
        st.session_state.selected_dev = None
        st.rerun()
    
    st.markdown(f'<div class="detail-card">', unsafe_allow_html=True)
    
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        img = dev.get('Image_URL', "https://via.placeholder.com/400")
        st.image(img, use_container_width=True)
        
    with col_info:
        st.markdown(f"<h1 style='color:#003366;'>{dev.get('Developer')}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:1.2rem; color:#D4AF37;'><b>بإدارة:</b> {dev.get('Owner')}</p>", unsafe_allow_html=True)
        st.markdown('<p class="section-head">نبذة عن المطور</p>', unsafe_allow_html=True)
        st.write(dev.get('Description', 'لا يوجد وصف متاح حالياً لهذا المطور.'))
        
        st.markdown('<p class="section-head">أهم المشاريع</p>', unsafe_allow_html=True)
        projects = str(dev.get('Projects', '')).split('،')
        for p in projects:
            st.markdown(f"✅ {p.strip()}")

    st.markdown('</div>', unsafe_allow_html=True)
