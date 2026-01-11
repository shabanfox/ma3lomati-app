import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (شاشة كاملة)
st.set_page_config(page_title="Broker Intelligence System", layout="wide", initial_sidebar_state="expanded")

# 2. CSS احترافي (أسود فاحم + ذهبي مطفي + أبيض)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الخلفية والخطوط */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #0d1117; color: white;
    }

    /*Sidebar Styling*/
    [data-testid="stSidebar"] { background-color: #000000; border-left: 2px solid #f59e0b; width: 250px !important; }
    
    /* تصميم الأزرار الجانبية */
    .st-emotion-cache-16ids9d { font-weight: 900 !important; color: #f59e0b !important; }

    /* كروت البيانات */
    .info-card {
        background: #161b22; border: 1px solid #30363d; border-right: 5px solid #f59e0b;
        padding: 20px; border-radius: 10px; margin-bottom: 15px;
    }
    
    .price-badge {
        background: #f59e0b; color: #000; padding: 2px 10px; border-radius: 5px;
        font-weight: 900; font-size: 1.1rem; float: left;
    }
    
    /* أزرار الأكشن */
    div.stButton > button {
        width: 100%; background-color: #f59e0b !important; color: black !important;
        font-weight: 900 !important; border-radius: 8px !important; border: none !important;
        height: 50px; transition: 0.3s;
    }
    div.stButton > button:hover { background-color: #ffffff !important; transform: scale(1.02); }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return pd.DataFrame()

df = load_data()

# 4. القائمة الجانبية (Navigation) - بديل الصفحة الرئيسية
with st.sidebar:
    st.markdown("<h1 style='text-align:center; color:#f59e0b;'>Ma3lomati PRO</h1>", unsafe_allow_html=True)
    st.write("---")
    menu = st.radio("القائمة الرئيسية", ["🏢 المطورين والمشاريع", "🛠️ أدوات البروكر الذكية"], index=0)
    st.write("---")
    if st.button("🔒 تسجيل الخروج"):
        st.session_state.auth = False
        st.rerun()

# --- الجزء الأول: المطورين والمشاريع ---
if menu == "🏢 المطورين والمشاريع":
    st.title("دليل المطورين والمشاريع الذكي")
    
    # محرك بحث متقدم باستخدام الأعمدة الجديدة
    with st.expander("🔍 فلاتر البحث المتقدمة", expanded=True):
        c1, c2, c3 = st.columns(3)
        with c1:
            search_query = st.text_input("بحث بالاسم أو المطور")
        with c2:
            area_opt = df['Area'].unique().tolist() if 'Area' in df.columns else []
            selected_area = st.multiselect("المنطقة", area_opt)
        with c3:
            type_opt = df['Type'].unique().tolist() if 'Type' in df.columns else []
            selected_type = st.multiselect("نوع الوحدة", type_opt)

    # تصفية الداتا
    fdata = df
    if search_query:
        fdata = fdata[fdata.apply(lambda r: search_query.lower() in str(r).lower(), axis=1)]
    if selected_area:
        fdata = fdata[fdata['Area'].isin(selected_area)]
    if selected_type:
        fdata = fdata[fdata['Type'].isin(selected_type)]

    # العرض بنظام الـ Grid (3 مشاريع في الصف)
    st.write(f"تم العثور على {len(fdata)} مشروع")
    
    for i in range(0, len(fdata), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(fdata):
                row = fdata.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="info-card">
                            <div class="price-badge">{row.get('Min_Val', row.get('Start Price (sqm)', '0'))}</div>
                            <h3 style="color:#f59e0b; margin-bottom:5px;">{row.get('Project Name', 'مشروع')}</h3>
                            <p style="font-size:0.9rem; color:#8b949e;">{row.get('Developer', 'مطور مجهول')}</p>
                            <hr style="border-color:#30363d">
                            <p>📍 {row.get('Area', '-')}</p>
                            <p>💳 مقدم: {row.get('Down_Payment', '-%')}</p>
                            <p>⏳ قسط: {row.get('Installments', '-')}</p>
                            <p>👷 استشاري: {row.get('Consultant', '-')}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("تفاصيل كاملة", key=f"btn_{i+j}"):
                        st.session_state.selected_p = row.get('Project Name')
                        # هنا يمكن فتح Modal أو صفحة تفصيلية

# --- الجزء الثاني: أدوات البروكر ---
elif menu == "🛠️ أدوات البروكر الذكية":
    st.title("أدوات البروكر المحترف")
    
    tab1, tab2, tab3 = st.tabs(["💰 حاسبة الأقساط", "📈 تحليل الاستثمار ROI", "📄 مولد عروض الأسعار"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            total_p = st.number_input("إجمالي سعر الوحدة", min_value=0, step=100000)
            down_p = st.slider("نسبة المقدم (%)", 0, 50, 10)
        with col2:
            years = st.number_input("مدة التقسيط (سنوات)", 1, 15, 7)
            
        if total_p > 0:
            dp_val = total_p * (down_p / 100)
            monthly = (total_p - dp_val) / (years * 12)
            st.success(f"المقدم المطلوب: {dp_val:,.0f} ج.م")
            st.warning(f"القسط الشهري: {monthly:,.0f} ج.م")

    with tab2:
        st.info("حاسبة العائد الإيجاري المتوقع بناءً على سعر المنطقة")
        # معادلات ROI متطورة

    with tab3:
        st.write("اختر المشروع لإنشاء ملف PDF عرض سعر سريع للعميل (قريباً)")
