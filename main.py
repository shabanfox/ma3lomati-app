import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="BrokerEdge | ابحث عن منزلك", layout="wide")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 0rem;}
    
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; }
    
    /* تصميم الـ Card الخاص بناوي */
    .nawy-card {
        background: white; 
        border-radius: 12px; 
        overflow: hidden; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.05); 
        border: 1px solid #eee;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. الهيدر ---
st.markdown("""
    <div style="background: white; padding: 15px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f0f0f0;">
        <div style="font-size: 24px; font-weight: bold; color: #00416b;">Broker<span style="color: #ed1c24;">Edge</span></div>
        <div style="display: flex; gap: 20px; color: #333; font-weight: 600;">
            <span>المشاريع</span> | <span>المطورين</span> | <span>الزتونة</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. الـ Hero Section ---
st.markdown("""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1500&q=80'); 
         background-size: cover; height: 350px; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white;">
        <h1 style="font-size: 40px; margin-bottom: 10px;">كل مشاريع مصر في مكان واحد</h1>
        <p style="font-size: 18px; opacity: 0.9;">أداة البروكر الذكية للوصول لأدق البيانات</p>
    </div>
    """, unsafe_allow_html=True)

# --- 4. محرك البحث الذكي ---
st.markdown("<br>", unsafe_allow_html=True)
col_search, col_filter = st.columns([3, 1])

with col_search:
    search_q = st.text_input("", placeholder="ابحث باسم المشروع، المطور، أو المنطقة...")
with col_filter:
    region_filter = st.selectbox("", ["كل المناطق", "التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية"])

# --- 5. منطق الداتا (رفع الملف وعرض الكروت) ---
if 'master_data' not in st.session_state:
    st.session_state['master_data'] = None

# زر مخفي للمدير لرفع الملف
with st.expander("⚙️ لوحة التحكم (لرفع الإكسيل)"):
    pw = st.text_input("كلمة المرور", type="password")
    if pw == "123":
        uploaded_file = st.file_uploader("ارفع ملف الإكسيل المحدث", type=['xlsx'])
        if uploaded_file:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.session_state['master_data'] = df
            st.success("تم تحديث البيانات بنجاح!")

# عرض البيانات
if st.session_state['master_data'] is not None:
    df = st.session_state['master_data']
    
    # فلترة البحث
    if search_q:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)]
    
    st.markdown(f'<h3 style="padding: 20px 0;">تم العثور على {len(df)} مشروع</h3>', unsafe_allow_html=True)
    
    # رسم الكروت (Grid 3 columns)
    cols = st.columns(3)
    for idx, row in df.iterrows():
        with cols[idx % 3]:
            # استخراج البيانات مع قيم افتراضية
            p_name = row.get('المشروع', 'مشروع جديد')
            p_dev = row.get('المطور', 'مطور عقاري')
            p_loc = row.get('المنطقة', 'موقع مميز')
            p_price = row.get('السعر', 'اتصل بنا')
            p_img = "https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=400&q=80" # صورة افتراضية شيك
            
            st.markdown(f"""
                <div style="background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 10px rgba(0,0,0,0.05); border: 1px solid #eee; margin-bottom: 25px;">
                    <img src="{p_img}" style="width: 100%; height: 180px; object-fit: cover;">
                    <div style="padding: 15px;">
                        <div style="font-size: 12px; color: #ed1c24; font-weight: bold; margin-bottom: 5px;">{p_loc}</div>
                        <h4 style="margin: 0; color: #333; font-size: 18px;">{p_name}</h4>
                        <p style="color: #777; font-size: 13px; margin: 5px 0 15px 0;">المطور: {p_dev}</p>
                        <div style="border-top: 1px solid #f5f5f5; padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 16px; font-weight: bold; color: #00416b;">{p_price}</span>
                            <span style="color: #ed1c24; font-size: 12px; font-weight: bold; cursor: pointer;">التفاصيل ←</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
else:
    st.info("👋 مرحباً بك! يرجى رفع ملف الداتا من لوحة التحكم بالأسفل للبدء.")
