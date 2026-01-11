import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu # ستحتاج لتثبيت المكتبة: pip install streamlit-option-menu

# 1. إعدادات النظام القصوى
st.set_page_config(page_title="Ma3lomati PRO Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (Black & Gold Premium)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الحاوية الرئيسية */
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }

    /* ستايل كروت المشاريع - تحويلها لبطاقات فنية */
    .project-card {
        background: linear-gradient(145deg, #111, #050505);
        border: 1px solid #222; border-right: 4px solid #f59e0b;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        transition: 0.4s all;
    }
    .project-card:hover { border-color: #f59e0b; transform: scale(1.01); box-shadow: 0 10px 20px rgba(245, 158, 11, 0.1); }

    /* تفاصيل السعر والتقسيط */
    .stat-box {
        background: #1a1a1a; padding: 10px; border-radius: 8px;
        text-align: center; border: 1px solid #333;
    }
    .stat-label { color: #888; font-size: 12px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; font-size: 14px; }

    /* أزرار التنقل */
    .nav-btn {
        background: #f59e0b !important; color: #000 !important;
        font-weight: 900 !important; border-radius: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محرك البيانات الشامل
@st.cache_data(ttl=300)
def get_master_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    df = pd.read_csv(url)
    df.columns = [str(c).strip() for c in df.columns]
    return df

df = get_master_data()

# 4. القائمة العلوية الاحترافية (Navigation Bar)
selected = option_menu(
    menu_title=None, 
    options=["المطورين والمشاريع", "أدوات البروكر", "الإعدادات"], 
    icons=["building", "tools", "gear"], 
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#000", "border-bottom": "2px solid #f59e0b"},
        "icon": {"color": "#f59e0b", "font-size": "20px"}, 
        "nav-link": {"font-size": "18px", "text-align": "center", "margin":"0px", "color":"white"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# --- شاشة المطورين والمشاريع ---
if selected == "المطورين والمشاريع":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>📊 قاعدة بيانات السوق العقاري</h2>", unsafe_allow_html=True)
    
    # منطقة الفلاتر الذكية (في سطر واحد لتقليل الفوضى)
    f1, f2, f3, f4 = st.columns([2, 1, 1, 1])
    with f1: search = st.text_input("🔍 ابحث عن (مشروع، مطور، أو استشاري)")
    with f2: area = st.selectbox("📍 المنطقة", ["الكل"] + list(df['Area'].unique()))
    with f3: u_type = st.selectbox("🏠 النوع", ["الكل"] + list(df['Type'].unique()))
    with f4: sort_by = st.selectbox("⚖️ ترتيب حسب", ["الأحدث", "السعر: من الأقل", "السعر: من الأعلى"])

    # تطبيق الفلترة
    dff = df.copy()
    if search: dff = dff[dff.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if area != "الكل": dff = dff[dff['Area'] == area]
    if u_type != "الكل": dff = dff[dff['Type'] == u_type]

    st.write("---")

    # عرض البيانات بنظام الـ Grid المتطور
    for i in range(0, len(dff), 2): # عرض مشروعين في كل صف لشكل أكثر فخامة
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(dff):
                row = dff.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="project-card">
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <h3 style="color:#f59e0b; margin:0;">{row.get('Project Name', 'N/A')}</h3>
                                <span style="background:#f59e0b; color:black; padding:2px 10px; border-radius:5px; font-weight:900;">{row.get('Min_Val', '0')} ج.م</span>
                            </div>
                            <p style="color:#888; margin-top:5px;">بواسطة: <b>{row.get('Developer', 'N/A')}</b> | المالك: {row.get('DeveloperOwner', '-')}</p>
                            
                            <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top:15px;">
                                <div class="stat-box"><span class="stat-label">📍 المنطقة</span><span class="stat-value">{row.get('Area', '-')}</span></div>
                                <div class="stat-box"><span class="stat-label">💵 المقدم</span><span class="stat-value">{row.get('Down_Payment', '-')}</span></div>
                                <div class="stat-box"><span class="stat-label">⏳ التقسيط</span><span class="stat-value">{row.get('Installments', '-')}</span></div>
                            </div>
                            
                            <div style="margin-top:15px; font-size:14px; color:#ccc; border-top:1px solid #222; padding-top:10px;">
                                <b>💡 الميزة:</b> {row.get('Competitive Advantage', '-')}<br>
                                <b>👷 الاستشاري:</b> {row.get('Consultant', '-')}
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    if st.button("👁️ عرض التفاصيل والوصف الكامل", key=f"det_{i+j}"):
                        st.info(f"📄 **وصف المشروع:** {row.get('Detailed_Info', row.get('Description', 'لا يوجد وصف'))}")

# --- شاشة أدوات البروكر ---
elif selected == "أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ عُدة البروكر المحترف</h2>", unsafe_allow_html=True)
    
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("<div class='project-card'><h3>💰 حاسبة القسط السريع</h3>", unsafe_allow_html=True)
        price = st.number_input("إجمالي السعر", min_value=0)
        down = st.number_input("المقدم (قيمة وليس نسبة)", min_value=0)
        years = st.slider("سنوات التقسيط", 1, 15, 7)
        if price > 0:
            monthly = (price - down) / (years * 12)
            st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>{monthly:,.0f} ج.م / شهر</h2>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_r:
        st.markdown("<div class='project-card'><h3>📝 صانع عرض السعر (Draft)</h3>", unsafe_allow_html=True)
        st.text_input("اسم العميل")
        st.selectbox("اختر المشروع المُرشح", df['Project Name'].unique())
        st.button("تجهيز نص الواتساب 📱")
        st.markdown("</div>", unsafe_allow_html=True)
