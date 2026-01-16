import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل المتطور (تعديل الألوان والخطوط)
st.set_page_config(page_title="BrokerEdge | منصة البروكر الذكية", layout="wide")

st.markdown("""
    <style>
    /* إخفاء عناصر ستريمليت الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 0rem; padding-bottom: 0rem;}
    
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
        background-color: #fcfcfc;
    }

    /* شريط الأخبار المتحرك */
    .ticker-wrapper {
        background: #ed1c24;
        color: white;
        padding: 8px 0;
        overflow: hidden;
        white-space: nowrap;
        font-weight: bold;
    }
    .ticker-text {
        display: inline-block;
        padding-right: 100%;
        animation: ticker 30s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* تصميم كارت المشروع */
    .nawy-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #eee;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. شريط الأخبار ---
st.markdown("""
    <div class="ticker-wrapper">
        <div class="ticker-text">
            🔥 عرض جديد: استلام فوري بمقدم 10% في القاهرة الجديدة -- 📢 تحديث أسعار مشاريع الشيخ زايد متوفر الآن -- ⚠️ تنبيه لجميع البروكـرز: متبقي وحدتين فقط في مشروع Oia Residence
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. الهيدر ---
st.markdown("""
    <div style="background: white; padding: 15px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee;">
        <div style="font-size: 24px; font-weight: bold; color: #00416b;">Broker<span style="color: #ed1c24;">Edge</span></div>
        <div style="font-size: 14px; color: #666;">لوحة تحكم البروكر المحترف</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (الحاسبة وإدارة البيانات) ---
with st.sidebar:
    st.markdown("### 🧮 الحاسبة السريعة")
    unit_p = st.number_input("سعر الوحدة", value=5000000)
    down_p = st.slider("المقدم (%)", 0, 50, 10)
    years = st.slider("السنوات", 1, 10, 8)
    
    dp_val = unit_p * (down_p/100)
    monthly = (unit_p - dp_val) / (years * 12)
    
    st.markdown(f"""
        <div style="background:#f0f4f8; padding:10px; border-radius:8px; text-align:center; border:1px solid #d1d9e0;">
            <p style="margin:0; font-size:12px;">المقدم: <b>{dp_val:,.0f}</b></p>
            <p style="margin:0; font-size:12px;">القسط: <b style="color:#ed1c24;">{monthly:,.0f}</b></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ الإدارة")
    admin_key = st.text_input("باسورد الأدمن", type="password")
    if admin_key == "123":
        file = st.file_uploader("ارفع ملف الإكسيل", type=['xlsx'])
        if file:
            st.session_state['data'] = pd.read_excel(file, engine='openpyxl')
            st.success("تم التحديث!")

# --- 5. محرك البحث والنتائج ---
st.markdown("<br>", unsafe_allow_html=True)
q = st.text_input("", placeholder="ابحث عن مشروع أو مطور هنا...", key="main_search")

if 'data' in st.session_state and st.session_state['data'] is not None:
    df = st.session_state['data']
    
    # فلترة البحث
    if q:
        df = df[df.astype(str).apply(lambda x: x.str.contains(q, case=False)).any(axis=1)]
    
    st.markdown(f"<p style='padding-right:50px;'>نتائج البحث: {len(df)}</p>", unsafe_allow_html=True)
    
    # عرض الكروت في شبكة
    cols = st.columns(3)
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            # جلب البيانات مع وضع قيم افتراضية
            name = row.get('المشروع', 'مشروع جديد')
            loc = row.get('المنطقة', 'مصر')
            price = row.get('السعر', 'اتصل بنا')
            dev = row.get('المطور', 'مطور عقاري')
            
            # زر واتساب
            msg = f"تفاصيل مشروع {name} في {loc}. السعر: {price}"
            
            st.markdown(f"""
                <div class="nawy-card">
                    <img src="https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400" style="width:100%; height:150px; object-fit:cover;">
                    <div style="padding: 15px;">
                        <span style="color: #ed1c24; font-size: 11px; font-weight: bold;">{loc}</span>
                        <h4 style="margin: 5px 0; color: #00416b;">{name}</h4>
                        <p style="color: #777; font-size: 13px;">{dev}</p>
                        <hr style="border:0; border-top:1px solid #eee;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <b style="color:#333;">{price}</b>
                            <a href="https://wa.me/?text={msg}" target="_blank" style="text-decoration:none;">
                                <button style="background:#25D366; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer; font-size:12px;">واتساب</button>
                            </a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # واجهة افتراضية قبل رفع الداتا
    st.markdown("""
        <div style="text-align:center; padding:100px; color:#888;">
            <h2>مرحباً بك في BrokerEdge</h2>
            <p>يرجى رفع ملف الإكسيل من القائمة الجانبية للبدء (الباسورد: 123)</p>
        </div>
    """, unsafe_allow_html=True)
