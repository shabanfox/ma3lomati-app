import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم الملكي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    .block-container { padding: 0rem !important; }
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .header-nav { 
        background: white; height: 75px; padding: 0 8%; display: flex; 
        justify-content: space-between; align-items: center; border-bottom: 2px solid #e2e8f0; 
    }
    .hero-bg {
        background-image: linear-gradient(rgba(0, 30, 60, 0.4), rgba(0, 30, 60, 0.4)), 
                        url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070');
        background-size: cover; background-position: center; height: 300px; 
        display: flex; flex-direction: column; justify-content: center; align-items: center; color: white;
    }
    .filter-box { 
        background: white; margin: -50px 10% 30px 10%; padding: 25px; 
        border-radius: 15px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); 
        position: relative; z-index: 10; border: 1px solid #edf2f7;
    }
    .project-card { 
        background: white; border-radius: 16px; border: 1px solid #e2e8f0; 
        display: flex; height: 180px; margin: 15px 10%; overflow: hidden; 
        transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); box-shadow: 0 12px 20px rgba(0,0,0,0.05); }
    .card-img { width: 280px; background-size: cover; background-position: center; border-left: 1px solid #eee; }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    .price-tag { color: #003366; font-weight: 900; font-size: 1.4rem; }
    .dev-name { font-weight: 700; font-size: 1.3rem; color: #1e293b; }
    .btn-view { background: #003366; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات - الرابط المباشر الصحيح
@st.cache_data(ttl=300) 
def load_data_from_gsheets():
    # الرابط المباشر لملف الـ CSV من جوجل شيت
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        # مسح أي مسافات زيادة في أسماء الأعمدة
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        return None

df = load_data_from_gsheets()

# 4. واجهة الموقع
st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-bg"><h1>عقاراتك العالمية.. برؤية مصرية</h1><p>دليل المطورين والمشاريع المحدث لحظياً من جوجل شيت</p></div>', unsafe_allow_html=True)

if df is not None:
    # 5. الفلاتر
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: search_dev = st.text_input("🔍 اسم المطور")
    with c2: 
        areas = ["كل المناطق"] + sorted(list(df['Area'].dropna().unique()))
        search_area = st.selectbox("📍 المنطقة", areas)
    with c3: 
        search_price = st.selectbox("💰 الفئة السعرية", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
    st.markdown('</div>', unsafe_allow_html=True)

    # 6. منطق الفلترة
    f_df = df.copy()
    if search_dev:
        f_df = f_df[f_df['Developer'].str.contains(search_dev, case=False, na=False)]
    if search_area != "كل المناطق":
        f_df = f_df[f_df['Area'] == search_area]
    
    # فلترة السعر
    if search_price == "أقل من 5 مليون":
        f_df = f_df[f_df['Min_Val'] < 5]
    elif search_price == "5 - 10 مليون":
        f_df = f_df[(f_df['Min_Val'] >= 5) & (f_df['Min_Val'] < 10)]
    elif search_price == "أكثر من 10 مليون":
        f_df = f_df[f_df['Min_Val'] >= 10]

    # 7. عرض النتائج
    st.markdown(f'<div style="padding: 0 10%; margin-bottom:10px;"><p style="color:#64748b;">تم العثور على ({len(f_df)}) نتائج</p></div>', unsafe_allow_html=True)
    
    for _, row in f_df.iterrows():
        img = row['Image_URL'] if pd.notnull(row['Image_URL']) else "https://via.placeholder.com/400"
        st.markdown(f'''
            <div class="project-card">
                <div class="card-img" style="background-image: url('{img}')"></div>
                <div class="card-body">
                    <div class="price-tag">يبدأ من {row['Price']} ج.م</div>
                    <div class="dev-name">{row['Developer']}</div>
                    <div style="color:#D4AF37; font-weight:700;">المالك: {row['Owner']}</div>
                    <div style="color:#1e293b; margin-top:5px;"><b>أهم المشاريع:</b> {row['Projects']}</div>
                    <div style="color:#64748b; font-size:0.85rem;">📍 {row['Area']}</div>
                </div>
                <div style="display:flex; align-items:center; padding-left:30px;">
                    <button class="btn-view">التفاصيل</button>
                </div>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.error("مشكلة في الوصول لرابط الشيت. تأكد من عمل Publish to Web بصيغة CSV")
