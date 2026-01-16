import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل العام
st.set_page_config(page_title="BrokerEdge | منصة البروكر المحترف", layout="wide")

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
        background-color: #ffffff;
    }

    /* شريط الأخبار المتحرك */
    .ticker-wrapper {
        background: #ed1c24;
        color: white;
        padding: 10px 0;
        overflow: hidden;
        white-space: nowrap;
        font-weight: bold;
        z-index: 1000;
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

    /* تصميم كروت المشاريع */
    .nawy-card {
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        margin-bottom: 25px;
        transition: transform 0.2s ease;
    }
    .nawy-card:hover {
        transform: translateY(-5px);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. شريط الأخبار ---
st.markdown("""
    <div class="ticker-wrapper">
        <div class="ticker-text">
            🔥 عرض جديد: مقدم 5% لمشاريع "نيوم" لفترة محدودة -- 📢 تم تحديث أسعار "سوديك" و "إعمار" لشهر يناير 2026 -- ⚠️ متبقي وحدات محدودة في "ماونتن فيو" -- 📍 افتتاح مرحلة جديدة في العاصمة الإدارية قريباً
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. الهيدر ---
st.markdown("""
    <div style="background: white; padding: 15px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee;">
        <div style="font-size: 24px; font-weight: bold; color: #00416b;">Broker<span style="color: #ed1c24;">Edge</span></div>
        <div style="color: #666; font-size: 14px; font-weight: 600;">المساعد الذكي للبروكر</div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (الحاسبة وإدارة البيانات) ---
with st.sidebar:
    st.markdown("### 🧮 حاسبة العميل")
    price_input = st.number_input("سعر الوحدة (ج.م)", value=5000000, step=100000)
    down_pct = st.slider("المقدم (%)", 0, 50, 10)
    years_pct = st.slider("عدد السنوات", 1, 10, 8)
    
    final_dp = price_input * (down_pct / 100)
    final_monthly = (price_input - final_dp) / (years_pct * 12)
    
    st.markdown(f"""
        <div style="background:#f8f9fa; padding:15px; border-radius:10px; border:1px solid #dee2e6; text-align:center;">
            <p style="margin:0; font-size:13px; color:#666;">المقدم</p>
            <h4 style="margin:0; color:#00416b;">{final_dp:,.0f}</h4>
            <hr style="margin:10px 0;">
            <p style="margin:0; font-size:13px; color:#666;">القسط الشهري</p>
            <h4 style="margin:0; color:#ed1c24;">{final_monthly:,.0f}</h4>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### ⚙️ الإدارة")
    admin_pw = st.text_input("كلمة السر", type="password")
    if admin_pw == "123":
        uploaded_file = st.file_uploader("ارفع ملف الإكسيل", type=['xlsx'])
        if uploaded_file:
            st.session_state['data'] = pd.read_excel(uploaded_file, engine='openpyxl')
            st.success("تم تحديث الداتا!")

# --- 5. البحث والنتائج ---
st.markdown("<br>", unsafe_allow_html=True)
query = st.text_input("", placeholder="ابحث باسم المشروع، المطور، أو المنطقة...", key="main_search")

if 'data' in st.session_state and st.session_state['data'] is not None:
    df = st.session_state['data']
    
    # فلترة البحث
    if query:
        df = df[df.astype(str).apply(lambda x: x.str.contains(query, case=False)).any(axis=1)]
    
    st.markdown(f"<p style='padding: 0 50px;'>تم العثور على: {len(df)} مشروع</p>", unsafe_allow_html=True)
    
    # عرض الكروت
    cols = st.columns(3)
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            # استخراج البيانات
            p_name = row.get('المشروع', 'مشروع جديد')
            p_loc = row.get('المنطقة', 'مصر')
            p_price = row.get('السعر', 'اتصل بنا')
            p_dev = row.get('المطور', 'مطور عقاري')
            p_pay = row.get('نظام السداد', 'قسط مرن')
            
            # رسالة الواتساب
            wa_msg = f"تفاصيل {p_name}: {p_loc}. السعر {p_price}. نظام السداد {p_pay}."
            
            st.markdown(f"""
                <div class="nawy-card">
                    <img src="https://images.unsplash.com/photo-1564013799919-ab600027ffc6?w=400&q=80" style="width:100%; height:160px; object-fit:cover;">
                    <div style="padding:15px;">
                        <span style="color:#ed1c24; font-size:11px; font-weight:bold;">{p_loc}</span>
                        <h4 style="margin:5px 0; color:#00416b; font-size:18px;">{p_name}</h4>
                        <p style="color:#777; font-size:13px; margin-bottom:10px;">{p_dev}</p>
                        <div style="background:#f8f9fa; padding:8px; border-radius:5px; font-size:12px; margin-bottom:15px;">
                            ⏱️ {p_pay}
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #eee; padding-top:10px;">
                            <b style="color:#333;">{p_price}</b>
                            <a href="https://wa.me/?text={wa_msg}" target="_blank" style="text-decoration:none;">
                                <button style="background:#25D366; color:white; border:none; padding:6px 12px; border-radius:6px; cursor:pointer; font-size:12px; font-weight:bold;">📲 مشاركة</button>
                            </a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    # واجهة الترحيب
    st.markdown("""
        <div style="text-align:center; padding:100px; color:#bbb;">
            <h2 style="color:#00416b;">BrokerEdge</h2>
            <p>يرجى رفع ملف الإكسيل من القائمة الجانبية للبدء (الباسورد: 123)</p>
        </div>
    """, unsafe_allow_html=True)
