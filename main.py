import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والستايل الاحترافي
st.set_page_config(page_title="BrokerEdge Pro", layout="wide")

def local_css():
    st.markdown("""
        <style>
        #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
        @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
        html, body, [class*="css"] { font-family: 'Cairo', sans-serif; direction: rtl; text-align: right; background-color: #f8f9fa; }
        .ticker-wrapper { background: #ed1c24; color: white; padding: 10px 0; overflow: hidden; white-space: nowrap; font-weight: bold; }
        .ticker-text { display: inline-block; padding-right: 100%; animation: ticker 25s linear infinite; }
        @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
        .nawy-card { background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); border: 1px solid #eee; margin-bottom: 25px; transition: 0.3s; }
        .nawy-card:hover { transform: translateY(-5px); border-color: #ed1c24; }
        </style>
    """, unsafe_allow_html=True)

local_css()

# 2. شريط الأخبار
st.markdown('<div class="ticker-wrapper"><div class="ticker-text">🔥 تم تحديث جميع أسعار المشاريع لشهر يناير 2026 -- 📢 عرض خاص: مقدم 5% في العاصمة الإدارية -- ⚠️ تنبيه: زيادة أسعار سوديك الأسبوع القادم</div></div>', unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div style="background:white; padding:15px 50px; border-bottom:1px solid #eee; display:flex; justify-content:space-between; align-items:center;"><div style="font-size:24px; font-weight:bold; color:#00416b;">Broker<span style="color:#ed1c24;">Edge</span></div></div>', unsafe_allow_html=True)

# 4. القائمة الجانبية (الأدوات والإدارة)
with st.sidebar:
    st.markdown("### ⚙️ الإدارة والرفع")
    admin_pw = st.text_input("كلمة السر", type="password")
    if admin_pw == "123":
        uploaded_file = st.file_uploader("ارفع ملف الإكسيل", type=['xlsx'])
        if uploaded_file:
            try:
                # استخدام engine='openpyxl' للقراءة الصحيحة
                df_raw = pd.read_excel(uploaded_file, engine='openpyxl')
                st.session_state['master_df'] = df_raw.dropna(how='all')
                st.success("✅ تم تحديث البيانات!")
            except Exception as e:
                st.error(f"حدث خطأ في قراءة الملف: {e}")

    st.markdown("---")
    st.markdown("### 🧮 حاسبة القسط")
    price = st.number_input("سعر الوحدة", value=5000000)
    down = st.slider("المقدم (%)", 0, 50, 10)
    years = st.slider("السنوات", 1, 10, 8)
    calc_dp = price * (down/100)
    calc_month = (price - calc_dp) / (years * 12)
    st.markdown(f"<div style='background:#f1f5f9; padding:10px; border-radius:8px; border:1px solid #cbd5e1;'><p style='margin:0;'>المقدم: <b>{calc_dp:,.0f}</b></p><p style='margin:0;'>القسط: <b style='color:#ed1c24;'>{calc_month:,.0f}</b></p></div>", unsafe_allow_html=True)

# 5. محرك البحث والواجهة
st.markdown("<div style='padding:20px 50px;'>", unsafe_allow_html=True)
q = st.text_input("", placeholder="🔍 ابحث عن مشروع، مطور، أو منطقة...")

if 'master_df' in st.session_state:
    df = st.session_state['master_df']
    if q:
        df = df[df.astype(str).apply(lambda x: x.str.contains(q, case=False)).any(axis=1)]
    
    st.markdown(f"<h5>إجمالي النتائج: {len(df)}</h5>", unsafe_allow_html=True)
    
    # شبكة الكروت
    cols = st.columns(3)
    for i, (idx, row) in enumerate(df.iterrows()):
        with cols[i % 3]:
            # استخراج البيانات بمرونة (البحث عن الكلمة في اسم العمود)
            def get_val(keywords, default):
                for col in df.columns:
                    if any(k in col.lower() for k in keywords):
                        return row[col]
                return default

            p_name = get_val(['مشروع', 'project', 'name'], 'مشروع جديد')
            p_loc = get_val(['منطقة', 'location', 'area'], 'مصر')
            p_price = get_val(['سعر', 'price'], 'اتصل بنا')
            p_dev = get_val(['مطور', 'developer'], 'مطور عقاري')
            p_pay = get_val(['سداد', 'payment', 'قسط'], 'أنظمة متنوعة')

            wa_msg = f"تفاصيل {p_name} - {p_loc}: السعر {p_price}, سداد {p_pay}."
            
            st.markdown(f"""
                <div class="nawy-card">
                    <img src="https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400" style="width:100%; height:160px; object-fit:cover;">
                    <div style="padding:15px;">
                        <span style="color:#ed1c24; font-size:11px; font-weight:bold;">{p_loc}</span>
                        <h4 style="margin:5px 0; color:#00416b; font-size:17px;">{p_name}</h4>
                        <p style="color:#666; font-size:12px; margin-bottom:10px;">{p_dev}</p>
                        <div style="background:#f8f9fa; padding:8px; border-radius:5px; font-size:12px; margin-bottom:15px; border:1px solid #eee;">⏱️ {p_pay}</div>
                        <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid #f1f1f1; padding-top:10px;">
                            <b style="color:#333; font-size:15px;">{p_price}</b>
                            <a href="https://wa.me/?text={wa_msg}" target="_blank" style="text-decoration:none;">
                                <button style="background:#25D366; color:white; border:none; padding:6px 15px; border-radius:6px; cursor:pointer; font-size:12px; font-weight:bold;">📲 مشاركة</button>
                            </a>
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("<div style='text-align:center; padding:100px; color:#999;'><h3>مرحباً بك في BrokerEdge</h3><p>ارفع ملف الإكسيل من القائمة الجانبية بالباسورد (123) لتبدأ</p></div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
