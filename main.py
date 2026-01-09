import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - التحديث هنا للزرار والكارت
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    .block-container { padding: 0rem !important; }
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .header-nav { background: white; height: 75px; padding: 0 8%; display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; }
    .hero-bg {
        background-image: linear-gradient(rgba(0, 30, 60, 0.4), rgba(0, 30, 60, 0.4)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070');
        background-size: cover; background-position: center; height: 250px; 
        display: flex; flex-direction: column; justify-content: center; align-items: center; color: white;
    }
    .filter-box { background: white; margin: -40px 10% 20px 10%; padding: 25px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); position: relative; z-index: 10; }
    
    /* تنسيق الكارت الجديد */
    .project-card { 
        background: white; border-radius: 16px; border: 1px solid #e2e8f0; 
        display: flex; height: 180px; margin-bottom: 20px; overflow: hidden; 
    }
    .card-img { width: 280px; background-size: cover; background-position: center; }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    
    /* تنسيق زرار التفاصيل الأزرق */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 25px !important;
        font-weight: 700 !important;
        font-family: 'Cairo', sans-serif !important;
        width: 100% !important;
        border: none !important;
        transition: 0.3s !important;
    }
    div.stButton > button:hover {
        background-color: #D4AF37 !important;
        color: white !important;
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

if 'page' not in st.session_state:
    st.session_state.page = 'main'
    st.session_state.selected_item = None

# --- صفحة التفاصيل ---
if st.session_state.page == 'details' and st.session_state.selected_item is not None:
    item = st.session_state.selected_item
    if st.button("⬅️ عودة للقائمة الرئيسية"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:20px; margin: 20px 10%; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border-top: 5px solid #003366;">
            <div style="display:flex; gap:30px; flex-wrap:wrap;">
                <img src="{item.get('Image_URL', 'https://via.placeholder.com/400')}" style="width:400px; border-radius:15px; object-fit:cover;">
                <div style="flex:1; text-align:right;">
                    <h1 style="color:#003366; margin:0;">{item.get('Developer')}</h1>
                    <h3 style="color:#D4AF37;">المالك: {item.get('Owner')}</h3>
                    <hr>
                    <p style="font-size:1.1rem; line-height:1.6; color:#475569;"><b>نبذة عن الشركة:</b><br>{item.get('Description', 'لا يوجد وصف متاح حالياً.')}</p>
                    <p style="font-size:1.1rem; color:#1e293b;"><b>المشاريع الحالية:</b> {item.get('Projects')}</p>
                    <p style="font-size:1.1rem; color:#1e293b;"><b>المنطقة:</b> {item.get('Area')}</p>
                    <h2 style="color:#003366;">الأسعار تبدأ من: {item.get('Price')} ج.م</h2>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- الصفحة الرئيسية ---
else:
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-bg"><h1>دليلك العقاري الموثوق</h1><p>استكشف تفاصيل المطورين ومشاريعهم في مصر</p></div>', unsafe_allow_html=True)

    if df is not None:
        # الفلاتر
        st.markdown('<div class="filter-box">', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: search_dev = st.text_input("🔍 ابحث عن مطور")
        with c2: search_area = st.selectbox("📍 اختر المنطقة", ["كل المناطق"] + sorted(list(df['Area'].dropna().unique())))
        with c3: search_price = st.selectbox("💰 الميزانية", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
        st.markdown('</div>', unsafe_allow_html=True)

        # عرض الكروت مع الزرار على اليمين
        f_df = df.copy()
        if search_dev: f_df = f_df[f_df['Developer'].str.contains(search_dev, case=False, na=False)]
        if search_area != "كل المناطق": f_df = f_df[f_df['Area'] == search_area]

        st.markdown('<div style="padding: 0 10%;">', unsafe_allow_html=True)
        for _, row in f_df.iterrows():
            # تقسيم الصف لـ 3 أعمدة (الزرار على اليمين، البيانات في النص، الصورة على الشمال)
            btn_col, info_col, img_col = st.columns([1, 3, 1.5])
            
            with btn_col:
                st.write("") # مسافات للتوسيط الرأسي
                st.write("")
                st.write("")
                if st.button("عرض التفاصيل", key=f"btn_{row.get('Developer')}"):
                    st.session_state.selected_item = row.to_dict()
                    st.session_state.page = 'details'
                    st.rerun()

            with info_col:
                st.markdown(f"""
                    <div style="padding: 20px; text-align: right;">
                        <div style="color: #003366; font-weight: 900; font-size: 1.4rem;">{row.get('Developer')}</div>
                        <div style="color: #D4AF37; font-weight: 700;">المالك: {row.get('Owner')}</div>
                        <div style="color: #64748b; font-size: 0.9rem; margin-top: 5px;">📍 {row.get('Area')} | يبدأ من {row.get('Price')} ج.م</div>
                    </div>
                """, unsafe_allow_html=True)

            with img_col:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f"""
                    <div style="height: 150px; border-radius: 12px; background-image: url('{img_url}'); background-size: cover; background-position: center; margin-top:10px;"></div>
                """, unsafe_allow_html=True)
            
            st.markdown("<hr style='margin: 10px 0; border: 0.5px solid #eee;'>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
