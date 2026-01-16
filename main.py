import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة وستايل "ناوي" الأصلي
st.set_page_config(page_title="BrokerEdge | القمة", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        background-color: #f4f7f6;
    }
    
    /* إخفاء زوائد ستريمليت */
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container {padding: 0rem;}

    /* الهيدر الاحترافي */
    .main-header {
        background: #00416b;
        color: white;
        padding: 20px 60px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* كارت ناوي المطور */
    .property-card {
        background: white;
        border-radius: 20px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #eef0f2;
        margin-bottom: 30px;
        transition: 0.4s;
    }
    .property-card:hover {
        transform: translateY(-10px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.12);
    }
    .price-tag {
        color: #00416b;
        font-size: 20px;
        font-weight: 700;
    }
    .wa-button {
        background-color: #25D366;
        color: white;
        padding: 8px 20px;
        border-radius: 12px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        transition: 0.3s;
    }
    .wa-button:hover { background-color: #128C7E; }
    </style>
    """, unsafe_allow_html=True)

# --- الهيدر ---
st.markdown("""
    <div class="main-header">
        <div style="font-size: 28px; font-weight: 700;">Broker<span style="color: #ed1c24;">Edge</span></div>
        <div style="font-size: 14px; opacity: 0.8;">المنصة الأولى للوكلاء العقاريين</div>
    </div>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية المظلمة (Dark Sidebar) ---
with st.sidebar:
    st.markdown("### 🛠️ لوحة التحكم")
    pw = st.text_input("باسورد الأدمن", type="password")
    if pw == "123":
        f = st.file_uploader("تحديث قاعدة البيانات (Excel)", type=['xlsx'])
        if f:
            st.session_state['data'] = pd.read_excel(f, engine='openpyxl')
            st.success("✅ تم التحديث بنجاح")
    
    st.markdown("---")
    st.markdown("### 💰 حاسبة القروض")
    p = st.number_input("سعر الوحدة", value=10000000)
    y = st.slider("سنوات السداد", 1, 15, 8)
    st.info(f"قسطك التقريبي: { (p/ (y*12)):,.0f} ج.م")

# --- محرك البحث ---
st.markdown("<div style='padding: 40px 60px;'>", unsafe_allow_html=True)
search = st.text_input("", placeholder="🔍 ابحث عن مشروعك المفضل (مثلاً: بادية، سوديك، التجمع)...")

if 'data' in st.session_state:
    df = st.session_state['data']
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    # شبكة الكروت
    cols = st.columns(3)
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            name = row.get('المشروع', 'مشروع عقاري')
            loc = row.get('المنطقة', 'القاهرة')
            price = row.get('السعر', 'طلب السعر')
            dev = row.get('المطور', 'شركة عقارية')
            
            st.markdown(f"""
                <div class="property-card">
                    <img src="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=500" style="width:100%; height:220px; object-fit:cover;">
                    <div style="padding: 20px;">
                        <div style="color: #ed1c24; font-weight: 700; font-size: 12px; margin-bottom: 5px;">{loc.upper()}</div>
                        <h3 style="margin: 0; color: #1e293b; font-size: 22px;">{name}</h3>
                        <p style="color: #64748b; margin: 10px 0;">بواسطة: {dev}</p>
                        <hr style="border: 0; border-top: 1px solid #f1f5f9; margin: 20px 0;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div class="price-tag">{price}</div>
                            <a href="https://wa.me/?text=تفاصيل {name}" class="wa-button">واتساب</a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("<h2 style='text-align:center; color:#cbd5e1; margin-top:100px;'>يرجى رفع ملف البيانات للبدء 🏗️</h2>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
