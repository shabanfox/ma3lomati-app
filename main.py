import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS)
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
    .card-img { width: 280px; background-size: cover; background-position: center; border-left: 1px solid #eee; }
    .card-body { padding: 20px; flex: 1; display: flex; flex-direction: column; justify-content: center; }
    .btn-view { background: #003366; color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 700; cursor: pointer; }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات مع معالجة ذكية للأعمدة
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        # قراءة البيانات
        df = pd.read_csv(csv_url)
        # تنظيف أسامي الأعمدة (إزالة المسافات وتوحيد الحالة)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"عطل في الاتصال: {e}")
        return None

df = load_data()

# 4. الواجهة الرئيسية
st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)
st.markdown('<div class="hero-bg"><h1>عقاراتك العالمية.. برؤية مصرية</h1><p>دليل المطورين والمشاريع المحدث لحظياً</p></div>', unsafe_allow_html=True)

if df is not None:
    # 5. الفلاتر (تستخدم .get عشان تمنع الـ KeyError)
    st.markdown('<div class="filter-box">', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        search_dev = st.text_input("🔍 اسم المطور")
    
    with c2:
        area_col = 'Area' if 'Area' in df.columns else df.columns[1] if len(df.columns) > 1 else None
        areas = ["كل المناطق"]
        if area_col:
            areas += sorted(list(df[area_col].dropna().unique()))
        search_area = st.selectbox("📍 المنطقة", areas)
        
    with c3:
        search_price = st.selectbox("💰 الفئة السعرية", ["الكل", "أقل من 5 مليون", "5 - 10 مليون", "أكثر من 10 مليون"])
    st.markdown('</div>', unsafe_allow_html=True)

    # 6. الفلترة الآمنة
    f_df = df.copy()
    dev_col = 'Developer' if 'Developer' in df.columns else df.columns[0]
    
    if search_dev:
        f_df = f_df[f_df[dev_col].astype(str).str.contains(search_dev, case=False, na=False)]
    if search_area != "كل المناطق" and area_col:
        f_df = f_df[f_df[area_col] == search_area]

    # 7. عرض الكروت (استخدام row.get يحل مشكلة KeyError نهائياً)
    st.markdown(f'<div style="padding: 0 10%; margin-bottom:10px;"><p style="color:#64748b;">نتائج البحث: ({len(f_df)})</p></div>', unsafe_allow_html=True)
    
    for _, row in f_df.iterrows():
        # سحب الصورة بأمان
        img_url = row.get('Image_URL', row.get('image_url', ""))
        if pd.isna(img_url) or str(img_url).strip() == "":
            img_url = "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400"
            
        st.markdown(f'''
            <div class="project-card">
                <div class="card-img" style="background-image: url('{img_url}')"></div>
                <div class="card-body">
                    <div style="color:#003366; font-weight:900; font-size:1.4rem;">يبدأ من {row.get('Price', 'غير محدد')} ج.م</div>
                    <div style="font-weight:700; font-size:1.3rem; color:#1e293b;">{row.get('Developer', row.get(df.columns[0], 'مطور'))}</div>
                    <div style="color:#D4AF37; font-weight:700;">المالك: {row.get('Owner', 'غير متوفر')}</div>
                    <div style="color:#1e293b; margin-top:5px; font-size:0.95rem;"><b>أهم المشاريع:</b> {row.get('Projects', 'جاري التحديث')}</div>
                    <div style="color:#64748b; font-size:0.85rem;">📍 {row.get('Area', 'موقع غير محدد')}</div>
                </div>
                <div style="display:flex; align-items:center; padding-left:30px;">
                    <button class="btn-view">التفاصيل</button>
                </div>
            </div>
        ''', unsafe_allow_html=True)
else:
    st.error("لم يتم العثور على بيانات. تأكد من 'نشر' الشيت بصيغة CSV")
