import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل المتطور (Nawy Pro Theme)
st.set_page_config(page_title="BrokerEdge | منصة البروكر الذكية", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    /* إخفاء عناصر ستريمليت الافتراضية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 0rem; padding-bottom: 0rem;}
    
    /* تعريف الخطوط والخلفيات */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: rtl;
        text-align: right;
    }

    /* شريط الأخبار المتحرك (Ticker) */
    .ticker-wrapper {
        background: #ed1c24;
        color: white;
        padding: 8px 0;
        overflow: hidden;
        white-space: nowrap;
        font-size: 14px;
        font-weight: bold;
        border-bottom: 2px solid #c1121f;
    }
    .ticker-text {
        display: inline-block;
        padding-right: 100%;
        animation: ticker 25s linear infinite;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    /* تصميم كارت المشروع */
    .nawy-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #f0f0f0;
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }
    .nawy-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. شريط الأخبار العاجلة ---
st.markdown("""
    <div class="ticker-wrapper">
        <div class="ticker-text">
            🔥 عرض حصري: مقدم 5% لمشروع Mountain View iCity لفترة محدودة -- 📢 إعمار مصر تعلن عن فتح باب الحجز في المرحلة الجديدة لـ Marassi -- 📉 انخفاض سعر الفائدة يؤدي لزيادة الطلب على العقارات التجارية -- ⚠️ تنبيه: تحديث قائمة الأسعار غداً لجميع مشاريع شركة سوديك
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 3. الهيدر (Navigation) ---
st.markdown("""
    <div style="background: white; padding: 15px 50px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #eee;">
        <div style="font-size: 26px; font-weight: bold; color: #00416b;">Broker<span style="color: #ed1c24;">Edge</span></div>
        <div style="display: flex; gap: 25px; color: #444; font-weight: 600; font-size: 15px;">
            <span style="cursor:pointer;">المشاريع</span>
            <span style="cursor:pointer;">المطورين</span>
            <span style="cursor:pointer;">عروض اليوم</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- 4. القائمة الجانبية (الحاسبة والأدوات) ---
with st.sidebar:
    st.markdown("### 🧮 حاسبة القروض العقارية")
    st.write("احسب القسط لعميلك في ثواني:")
    s_price = st.number_input("سعر الوحدة (ج.م)", value=5000000, step=50000)
    s_down = st.slider("المقدم (%)", 0, 50, 10)
    s_years = st.slider("مدة التقسيط (سنوات)", 1, 15, 8)
    
    calc_down = s_price * (s_down/100)
    calc_installment = (s_price - calc_down) / (s_years * 12)
    
    st.markdown(f"""
        <div style="background: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center;">
            <p style="margin:0; color:#64748b; font-size:13px;">المقدم المطلوب</p>
            <h3 style="margin:5px 0; color:#00416b;">{calc_down:,.0f} ج.م</h3>
            <hr style="margin:10px 0; border:0; border-top:1px solid #e2e8f0;">
            <p style="margin:0; color:#64748b; font-size:13px;">القسط الشهري</p>
            <h3 style="margin:5px 0; color:#ed1c24;">{calc_installment:,.0f} ج.م</h3>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📥 تحديث البيانات")
    admin_pw = st.text_input("كلمة مرور الإدارة", type="password")
    if admin_pw == "123":
        up_file = st.file_uploader("ارفع ملف الإكسيل المحدث", type=['xlsx'])
        if up_file:
            st.session_state['master_data'] = pd.read_excel(up_file, engine='openpyxl')
            st.success("تم تحديث قاعدة البيانات!")

# --- 5. الـ Hero Section ---
st.markdown("""
    <div style="background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?ixlib=rb-4.0.3&auto=format&fit=crop&w=1500&q=80'); 
         background-size: cover; background-position: center; height: 300px; display: flex; flex-direction: column; justify-content: center; align-items: center; color: white;">
        <h1 style="font-size: 38px; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">الزتونة.. محرك البحث العقاري الأذكى</h1>
        <p style="font-size: 18px; opacity: 0.9;">بيانات دقيقة، قرارات أسرع، مبيعات أكثر</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. عرض المشاريع والبحث ---
st.markdown("<div style='padding: 30px 50px;'>", unsafe_allow_html=True)
col_q, col_reg = st.columns([3, 1])

with col_q:
    search_query = st.text_input("", placeholder="ابحث باسم المشروع أو المطور (مثال: بالم هيلز التجمع)...")
with col_reg:
    reg_choice = st.selectbox("", ["كل المناطق", "التجمع الخامس", "الشيخ زايد", "العاصمة الإدارية", "الساحل الشمالي"])

# منطق عرض الداتا
if 'master_data' in st.session_state and st.session_state['master_data'] is not None:
    df = st.session_state['master_data']
    
    # تصفية البحث
    if search_query:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]
    
    st.markdown(f"<h5>نتائج البحث: {len(df)} مشروع</h5>", unsafe_allow_html=True)
    
    # شبكة الكروت (3 أعمدة)
    rows = st.columns(3)
    for i, (idx, row) in enumerate(df.iterrows()):
        with rows[i % 3]:
            name = row.get('المشروع', 'مشروع غير مسمى')
            dev = row.get('المطور', 'مطور عقاري')
            loc = row.get('المنطقة', 'مصر')
            price = row.get('السعر', 'اتصل للتفاصيل')
            payment = row.get('نظام السداد', 'أنظمة متنوعة')
            
            # نص الواتساب التلقائي
            wa_msg = f"أهلاً بك، تفاصيل مشروع {name}: \n📍 المنطقة: {loc} \n🏗️ المطور: {dev} \n💰 السعر: {price} \n💳 نظام السداد: {payment} \n\n للمزيد من التفاصيل تواصل معي."
            
            st.markdown(f"""
                <div class="nawy-card">
                    <img src="https://images.unsplash.com/photo-1582407947304-fd86f028f716?w=400&q=80" style="width:100%; height:160px; object-fit:cover;">
                    <div style="padding: 15px;">
                        <span style="color: #ed1c24; font-size: 11px; font-weight: bold;">{loc}</span>
                        <h4 style="margin: 5px 0; color: #00416b; font-size: 18px;">{name}</h4>
                        <p style="color: #777; font-size: 13px; margin-bottom: 12px;">المطور: {dev}</p>
                        <div style="background: #f9fafb; padding: 8px; border-radius: 8px; font-size: 12px; color: #444; margin-bottom: 15px;">
                            ⏱️ {payment}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid #f0f0f0; padding-top: 10px;">
                            <span style="font-weight: 700; color: #333;">{price}</span>
                            <a href="https://wa.me/?text={wa_msg}" target="_blank" style="text-decoration:none;">
                                <button style="background:#25D366; color:white; border:none; padding:6px 12px; border-radius:6px; font-size:12px; font-weight:bold; cursor:pointer;">📲 مشاركة</button>
                            </a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.warning("👋 أهلاً بك! يرجى رفع ملف الإكسيل من القائمة الجانبية (الباسورد: 123) لعرض المشاريع.")

st.markdown("</div>", unsafe_allow_html=True)
