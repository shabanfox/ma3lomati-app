import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu 

# 1. إعدادات النظام القصوى
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (Premium Black & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الحاوية الرئيسية */
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* كروت المشاريع والمطورين */
    .custom-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 25px; margin-bottom: 20px;
        transition: 0.3s all; color: white;
    }
    .custom-card:hover { border-color: #f59e0b; transform: translateY(-5px); }

    /* العناوين والأوسمة */
    .price-tag {
        background: #f59e0b; color: black; padding: 5px 15px;
        border-radius: 8px; font-weight: 900; font-size: 16px;
    }

    /* شبكة البيانات */
    .stat-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 15px 0; }
    .stat-box { background: #1a1a1a; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 12px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; }
    
    /* تحسين شكل المدخلات الرقمية */
    .stNumberInput div[data-baseweb="input"] {
        background-color: #1a1a1a !important; color: white !important; border: 1px solid #333 !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات من Google Sheets
@st.cache_data(ttl=300)
def load_master_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        # تنظيف أسماء الأعمدة من المسافات
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except:
        return pd.DataFrame()

df = load_master_data()

# 4. القائمة العلوية (الترتيب: أدوات -> مشاريع -> مطورين)
selected = option_menu(
    menu_title=None, 
    options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000", "border-bottom": "3px solid #f59e0b"},
        "nav-link": {"font-size": "18px", "color":"white", "font-family": "Cairo"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- 1. شاشة أدوات البروكر (تم تحديثها بالكامل) ---
if selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ عُدة البروكر المحترف</h2>", unsafe_allow_html=True)
    
    col_calc, col_roi, col_msg = st.columns(3)
    
    with col_calc:
        st.markdown("<div class='custom-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        p_val = st.number_input("إجمالي السعر (ج.م)", min_value=0, value=1000000, step=100000)
        d_val = st.number_input("المقدم المدفوع (ج.م)", min_value=0, value=100000, step=50000)
        y_val = st.number_input("عدد سنوات التقسيط", min_value=1, max_value=20, value=7, step=1)
        
        if p_val > 0 and y_val > 0:
            monthly = (p_val - d_val) / (y_val * 12)
            st.markdown(f"""
                <div style='background:#000; padding:15px; border-radius:10px; border:1px solid #f59e0b; text-align:center; margin-top:10px;'>
                    <span style='color:#888; font-size:12px;'>القسط الشهري المتوقع</span><br>
                    <span style='color:#f59e0b; font-size:22px; font-weight:900;'>{monthly:,.0f} ج.م</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_roi:
        st.markdown("<div class='custom-card'><h3>📈 حاسبة العائد ROI</h3>", unsafe_allow_html=True)
        total_inv = st.number_input("قيمة الاستثمار الكلي", min_value=0, value=2000000, step=100000)
        expected_rent = st.number_input("الإيجار الشهري المتوقع", min_value=0, value=15000, step=1000)
        
        if total_inv > 0:
            annual_roi = (expected_rent * 12 / total_inv) * 100
            st.markdown(f"""
                <div style='background:#000; padding:15px; border-radius:10px; border:1px solid #00ffcc; text-align:center; margin-top:10px;'>
                    <span style='color:#888; font-size:12px;'>نسبة العائد السنوي</span><br>
                    <span style='color:#00ffcc; font-size:22px; font-weight:900;'>{annual_roi:.2f} %</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_msg:
        st.markdown("<div class='custom-card'><h3>📱 عرض سريع</h3>", unsafe_allow_html=True)
        client_name = st.text_input("اسم العميل", placeholder="مثال: أ/ محمد")
        proj_list = df['Projects'].dropna().unique() if not df.empty and 'Projects' in df.columns else ["لا توجد بيانات"]
        selected_proj = st.selectbox("المشروع المرشح", proj_list)
        
        if st.button("تجهيز نص العرض الاحترافي"):
            # محاولة سحب تفاصيل المشروع للرسالة
            proj_data = df[df['Projects'] == selected_proj]
            area = proj_data['Area'].values[0] if 'Area' in df.columns else 'غير محدد'
            payment = proj_data['Down_Payment'].values[0] if 'Down_Payment' in df.columns else 'اتصل للتفاصيل'
            
            template = f"""*تحية طيبة {client_name if client_name else ''}*.. \nبناءً على تواصلنا، أرشح لك أحد أفضل الفرص حالياً:\n\n🏢 *مشروع:* {selected_proj}\n📍 *المنطقة:* {area}\n💰 *نظام السداد:* {payment} مقدم.\n\nللمناقشة وتحديد موعد معاينة، يسعدني تواصلك."""
            st.text_area("انسخ النص من هنا:", value=template, height=160)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1: search_p = st.text_input("🔍 ابحث عن مشروع أو ميزة...")
    with col2: area_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()) if 'Area' in df.columns else ["الكل"])
    with col3: type_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["الكل"])

    dff_p = df.copy()
    if search_p: dff_p = dff_p[dff_p.apply(lambda r: search_p.lower() in str(r).lower(), axis=1)]
    if 'Area' in dff_p.columns and area_p != "الكل": dff_p = dff_p[dff_p['Area'] == area_p]
    if 'Type' in dff_p.columns and type_p != "الكل": dff_p = dff_p[dff_p['Type'] == type_p]

    for _, row in dff_p.iterrows():
        st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between;">
                    <h3 style="color:#f59e0b; margin:0;">{row.get('Projects', 'اسم المشروع')}</h3>
                    <span class="price-tag">{row.get('Min_Val (Start Price)', '0')}</span>
                </div>
                <p style="color:#aaa; margin-bottom:0;">المطور: <b>{row.get('Developer', '-')}</b></p>
                <div class="stat-grid">
                    <div class="stat-box"><span class="stat-label">المنطقة</span><span class="stat-value">{row.get('Area', '-')}</span></div>
                    <div class="stat-box"><span class="stat-label">المقدم</span><span class="stat-value">{row.get('Down_Payment', '-')}</span></div>
                    <div class="stat-box"><span class="stat-label">التقسيط</span><span class="stat-value">{row.get('Installments', '-')}</span></div>
                </div>
                <div style="color:#ccc; font-size:14px; border-top:1px solid #222; padding-top:10px;">
                    <b>💡 الميزة:</b> {row.get('Description', '-')}
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 3. شاشة المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    search_d = st.text_input("🔍 ابحث عن اسم المطور أو المالك...")
    
    if not df.empty and 'Developer' in df.columns:
        dev_df = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
        if search_d:
            dev_df = dev_df[dev_df.apply(lambda r: search_d.lower() in str(r).lower(), axis=1)]

        for _, row in dev_df.iterrows():
            st.markdown(f"""
                <div class="custom-card" style="border-right-color: #fff;">
                    <h3 style="color:#f59e0b; margin:0;">🏢 {row.get('Developer', '-')}</h3>
                    <p style="color:#eee; margin-top:10px;">👤 <b>المالك:</b> {row.get('Owner', '-')}</p>
                    <div style="background:#1a1a1a; padding:15px; border-radius:10px; color:#bbb; font-size:14px; line-height:1.6;">
                        <b>📖 سابقة الأعمال والتفاصيل:</b><br>
                        {row.get('Detailed_Info', 'لا توجد تفاصيل إضافية مسجلة')}
                    </div>
                </div>
            """, unsafe_allow_html=True)
