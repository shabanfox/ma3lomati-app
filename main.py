import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="مساعد البروكر الذكي", layout="wide")

# 2. التنسيق (CSS) - الحفاظ على شكل الكروت الرمادية والاسم يمين
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .header-nav { text-align: right; padding: 10px 0; margin-bottom: 5px; }
    .broker-tool-box { 
        background: linear-gradient(135deg, #003366, #00509d); 
        color: white; padding: 25px; border-radius: 15px; margin-bottom: 20px; 
    }
    .project-card-container { 
        background-color: #edf2f7; border-radius: 12px; margin-bottom: 8px; 
        display: flex; align-items: center; border: 1px solid #e2e8f0; 
    }
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 6px !important; padding: 4px 12px !important;
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
        # تنظيف عمود السعر لتحويله لرقم
        df['Price_Numeric'] = df['Price'].replace('[\,ج.م]', '', regex=True).astype(float)
        return df
    except: return None

df = load_data()

# --- واجهة البروكر ---
if 'page' not in st.session_state: st.session_state.page = 'main'

if st.session_state.page == 'main':
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    # ركن المستشار العقاري (The Matchmaker)
    st.markdown('<div class="broker-tool-box"><h3>🎯 محرك المطابقة المالية (للمستشار العقاري)</h3><p>أدخل ميزانية العميل وسأقوم بترشيح أفضل المطورين المتاحين</p></div>', unsafe_allow_html=True)
    
    with st.expander("🛠️ افتح أدوات تحليل الميزانية", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            budget_total = st.number_input("إجمالي الميزانية (ج.م)", min_value=0, value=5000000, step=100000)
        with c2:
            down_payment_ready = st.number_input("المقدم المتاح حالياً", min_value=0, value=500000, step=50000)
        with c3:
            monthly_installment = st.number_input("القسط الشهري المستهدف", min_value=0, value=30000, step=5000)

    if df is not None:
        # منطق الفلترة الذكي (Smart Match)
        # 1. المطورين اللي سعرهم في حدود الميزانية
        # 2. المطورين اللي نظام المقدم بتاعهم يتناسب مع المتاح
        f_df = df[df['Price_Numeric'] <= budget_total].copy()
        
        # حساب القسط المتوقع لكل مطور (افتراضياً)
        # القسط الشهري = (إجمالي السعر - المقدم) / (سنوات القسط * 12)
        def check_feasibility(row):
            price = row['Price_Numeric']
            dp_pct = float(row.get('Down_Payment', 10)) / 100
            years = float(row.get('Installments', 7))
            
            calc_dp = price * dp_pct
            calc_monthly = (price - calc_dp) / (years * 12)
            
            return calc_dp <= down_payment_ready and calc_monthly <= monthly_installment

        # تطبيق المطابقة
        f_df['Is_Match'] = f_df.apply(check_feasibility, axis=1)
        matches = f_df[f_df['Is_Match'] == True]

        st.success(f"تم إيجاد {len(matches)} مطورين يتناسبون مع قدرة العميل المالية")

        # عرض الكروت (نفس التنسيق الرمادي المفضل)
        for _, row in matches.iterrows():
            st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
            col_content, col_img = st.columns([4, 1])
            with col_content:
                txt_c, btn_c = st.columns([3, 1])
                with txt_c:
                    st.markdown(f"""
                        <div style="text-align: right; padding: 15px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer')}</div>
                            <div style="color: #D4AF37; font-weight: 700;">المقدم المطلوب: {int(row['Price_Numeric'] * (float(row.get('Down_Payment', 10))/100)):,} ج.م</div>
                            <div style="color: #4a5568; font-size: 0.85rem;">📍 {row.get('Area')} | القسط المتوقع: {int((row['Price_Numeric'] - (row['Price_Numeric']*(float(row.get('Down_Payment',10))/100))) / (float(row.get('Installments',7))*12)):,} ج/شهر</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("")
                    st.write("")
                    if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()
            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height: 110px; border-radius: 0 10px 10px 0; background-image: url(\'{img_url}\'); background-size: cover; background-position: center;"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# صفحة التفاصيل (يتم عرض تحليل مالي أعمق هنا)
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:30px; border-radius:15px; margin-top:10px; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة للتحليل المالية"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"<h2 style='color:#003366;'>التحليل الاستثماري لـ {item.get('Developer')}</h2>", unsafe_allow_html=True)
    
    # حاسبة استثمارية بسيطة في صفحة التفاصيل
    price = item['Price_Numeric']
    dp = price * (float(item.get('Down_Payment', 10)) / 100)
    inst = (price - dp) / (float(item.get('Installments', 7)) * 12)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("المقدم النقدي", f"{int(dp):,} ج.م")
    c2.metric("القسط الشهري", f"{int(inst):,} ج.م")
    c3.metric("مدة القسط", f"{item.get('Installments')} سنوات")
    
    st.markdown("---")
    st.write(f"**نبذة عن المطور:** {item.get('Description')}")
