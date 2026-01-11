import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu 

# 1. إعدادات النظام
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (Premium Black & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    .custom-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 25px; margin-bottom: 20px;
        transition: 0.3s all; color: white;
    }
    
    .price-tag {
        background: #f59e0b; color: black; padding: 5px 15px;
        border-radius: 8px; font-weight: 900; font-size: 16px;
    }

    .stat-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 15px 0; }
    .stat-box { background: #1a1a1a; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 12px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; }
    
    /* تحسين المدخلات */
    .stNumberInput label { color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=300)
def load_master_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        data.columns = [str(c).strip() for c in data.columns]
        return data
    except: return pd.DataFrame()

df = load_master_data()

# 4. القائمة العلوية
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

# --- 1. شاشة أدوات البروكر (التعديل الجديد في حاسبة المقدم) ---
if selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ عُدة البروكر المحترف</h2>", unsafe_allow_html=True)
    
    col_calc, col_roi, col_msg = st.columns(3)
    
    with col_calc:
        st.markdown("<div class='custom-card'><h3>💰 حاسبة القسط الذكية</h3>", unsafe_allow_html=True)
        
        # مدخلات السعر والنسبة
        total_price = st.number_input("إجمالي سعر الوحدة (ج.م)", min_value=0, value=1000000, step=100000)
        down_payment_pct = st.number_input("نسبة المقدم (%)", min_value=0, max_value=100, value=10, step=5)
        
        # حسابات تلقائية واضحة للعميل
        calculated_down_payment = (down_payment_pct / 100) * total_price
        remaining_amount = total_price - calculated_down_payment
        
        st.markdown(f"""
            <div style='background:#111; padding:10px; border-radius:8px; margin:10px 0; border:1px dashed #444;'>
                <p style='margin:0; font-size:13px; color:#888;'>قيمة المقدم: <b style='color:white;'>{calculated_down_payment:,.0f} ج.م</b></p>
                <p style='margin:0; font-size:13px; color:#888;'>المبلغ المتبقي: <b style='color:white;'>{remaining_amount:,.0f} ج.م</b></p>
            </div>
        """, unsafe_allow_html=True)
        
        installment_years = st.number_input("سنوات التقسيط", min_value=1, max_value=20, value=7, step=1)
        
        if total_price > 0 and installment_years > 0:
            monthly_inst = remaining_amount / (installment_years * 12)
            st.markdown(f"""
                <div style='background:#000; padding:15px; border-radius:10px; border:2px solid #f59e0b; text-align:center; margin-top:10px;'>
                    <span style='color:#888; font-size:12px;'>القسط الشهري</span><br>
                    <span style='color:#f59e0b; font-size:24px; font-weight:900;'>{monthly_inst:,.0f} ج.م</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_roi:
        st.markdown("<div class='custom-card'><h3>📈 حاسبة العائد ROI</h3>", unsafe_allow_html=True)
        t_inv = st.number_input("قيمة الاستثمار", min_value=0, value=2000000, step=100000)
        rent = st.number_input("إيجار شهري متوقع", min_value=0, value=15000, step=1000)
        
        if t_inv > 0:
            roi_res = (rent * 12 / t_inv) * 100
            st.markdown(f"""
                <div style='background:#000; padding:15px; border-radius:10px; border:2px solid #00ffcc; text-align:center; margin-top:10px;'>
                    <span style='color:#888; font-size:12px;'>العائد السنوي</span><br>
                    <span style='color:#00ffcc; font-size:24px; font-weight:900;'>{roi_res:.2f} %</span>
                </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_msg:
        st.markdown("<div class='custom-card'><h3>📱 عرض سريع</h3>", unsafe_allow_html=True)
        c_name = st.text_input("اسم العميل")
        p_list = df['Projects'].dropna().unique() if not df.empty and 'Projects' in df.columns else ["لا توجد بيانات"]
        s_proj = st.selectbox("اختر المشروع", p_list)
        
        if st.button("تجهيز الرسالة"):
            proj_info = df[df['Projects'] == s_proj]
            area = proj_info['Area'].values[0] if 'Area' in df.columns else 'غير محدد'
            template = f"""*تحية طيبة {c_name if c_name else ''}*.. \nبناءً على تواصلنا، أرشح لك:\n\n🏢 *مشروع:* {s_proj}\n📍 *المنطقة:* {area}\n\nللمناقشة، يسعدني تواصلك."""
            st.text_area("النص الجاهز:", value=template, height=120)
        st.markdown("</div>", unsafe_allow_html=True)

# --- 2. شاشة المشاريع ---
elif selected == "🏗️ المشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1: s_p = st.text_input("🔍 ابحث هنا...")
    with c2: a_p = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df['Area'].dropna().unique().tolist()) if 'Area' in df.columns else ["الكل"])
    with c3: t_p = st.selectbox("🏠 النوع", ["الكل"] + sorted(df['Type'].dropna().unique().tolist()) if 'Type' in df.columns else ["الكل"])

    dff = df.copy()
    if s_p: dff = dff[dff.apply(lambda r: s_p.lower() in str(r).lower(), axis=1)]
    if 'Area' in dff.columns and a_p != "الكل": dff = dff[dff['Area'] == a_p]
    if 'Type' in dff.columns and t_p != "الكل": dff = dff[dff['Type'] == t_p]

    for _, row in dff.iterrows():
        st.markdown(f"""
            <div class="custom-card">
                <div style="display: flex; justify-content: space-between;">
                    <h3 style="color:#f59e0b; margin:0;">{row.get('Projects', 'مشروع')}</h3>
                    <span class="price-tag">{row.get('Min_Val (Start Price)', '0')}</span>
                </div>
                <div class="stat-grid">
                    <div class="stat-box"><span class="stat-label">المطور</span><span class="stat-value">{row.get('Developer', '-')}</span></div>
                    <div class="stat-box"><span class="stat-label">المقدم</span><span class="stat-value">{row.get('Down_Payment', '-')}</span></div>
                    <div class="stat-box"><span class="stat-label">التقسيط</span><span class="stat-value">{row.get('Installments', '-')}</span></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

# --- 3. شاشة المطورين ---
elif selected == "🏢 المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 المطورين العقاريين</h2>", unsafe_allow_html=True)
    s_d = st.text_input("🔍 بحث عن مطور...")
    if not df.empty and 'Developer' in df.columns:
        devs = df[['Developer', 'Owner', 'Detailed_Info']].drop_duplicates(subset=['Developer'])
        if s_d: devs = devs[devs.apply(lambda r: s_d.lower() in str(r).lower(), axis=1)]
        for _, row in devs.iterrows():
            st.markdown(f"""
                <div class="custom-card" style="border-right-color:white;">
                    <h3 style="color:#f59e0b;">🏢 {row['Developer']}</h3>
                    <p><b>المالك:</b> {row['Owner']}</p>
                    <p style='color:#bbb; font-size:14px;'>{row['Detailed_Info']}</p>
                </div>
            """, unsafe_allow_html=True)
