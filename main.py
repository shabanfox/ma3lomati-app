import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتي PRO", layout="wide", initial_sidebar_state="collapsed")

# 2. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif;
    }
    .main-header {
        background: linear-gradient(90deg, #111 0%, #000 100%);
        padding: 15px 35px; border-radius: 0 0 15px 15px;
        border: 1px solid #222; border-right: 12px solid #f59e0b;
        text-align: center; margin-bottom: 25px;
    }
    .header-title { font-weight: 900; font-size: 35px !important; color: #f59e0b; margin: 0; }
    .pro-card {
        background: #111; border: 1px solid #222; border-top: 4px solid #f59e0b;
        border-radius: 12px; padding: 20px; margin-bottom: 15px;
        min-height: 220px; text-align: center;
    }
    .card-main-title { color: #f59e0b; font-size: 24px !important; font-weight: 900; }
    .stat-row { display: flex; justify-content: space-between; font-size: 14px; margin-top: 10px; color: #ccc; }
    .stat-val { color: #f59e0b; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# 3. الهيدر
st.markdown('<div class="main-header"><h1 class="header-title">🏢 منصة معلوماتي العقارية</h1></div>', unsafe_allow_html=True)

# 4. جلب البيانات بتنظيف عميق
@st.cache_data(ttl=300)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        data = pd.read_csv(url)
        # تنظيف أسماء الأعمدة من المسافات
        data.columns = [str(c).strip() for c in data.columns]
        # تحويل كل البيانات لنصوص واستبدال الفارغ بـ "غير متوفر"
        data = data.astype(str).replace(['nan', 'None', ''], 'غير متوفر')
        return data
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

df = load_data()

# 5. القائمة
selected = option_menu(
    menu_title=None, options=["🛠️ أدوات البروكر", "🏗️ المشاريع", "🏢 المطورين"], 
    icons=["tools", "building", "person-badge"], orientation="horizontal",
    styles={"container": {"background-color": "#000", "border-bottom": "3px solid #f59e0b"}}
)

# --- 🏗️ شاشة المشاريع ---
if selected == "🏗️ المشاريع":
    if not df.empty:
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏗️ دليل المشاريع</h2>", unsafe_allow_html=True)
            
            # فلاتر ذكية
            f1, f2 = st.columns(2)
            with f1: 
                s_p = st.text_input("🔍 ابحث عن مشروع...")
            with f2:
                # التأكد من وجود عمود Area
                area_col = 'Area' if 'Area' in df.columns else df.columns[0]
                unique_areas = sorted(df[area_col].unique().tolist())
                a_p = st.selectbox("📍 المنطقة", ["الكل"] + unique_areas)
            
            # تطبيق الفلترة
            dff = df.copy()
            proj_col = 'Projects' if 'Projects' in df.columns else df.columns[0]
            if s_p:
                dff = dff[dff[proj_col].str.contains(s_p, case=False, na=False)]
            if a_p != "الكل":
                dff = dff[dff[area_col] == a_p]

            # عرض النتائج في شبكة 3x3 (نسبة الـ 70%)
            if not dff.empty:
                items = 9
                pages = max(1, math.ceil(len(dff)/items))
                page = st.selectbox("رقم الصفحة", range(1, pages + 1)) if pages > 1 else 1
                curr = dff.iloc[(page-1)*items : page*items]

                for i in range(0, len(curr), 3):
                    cols = st.columns(3)
                    for j in range(3):
                        if i+j < len(curr):
                            row = curr.iloc[i+j]
                            with cols[j]:
                                # استخراج القيم بأمان
                                p_name = row.get('Projects', 'مشروع غير مسمى')
                                d_name = row.get('Developer', 'مطور غير محدد')
                                loc = row.get('Area', 'غير محدد')
                                down = row.get('Down_Payment', 'تواصل معنا')
                                
                                st.markdown(f"""
                                    <div class="pro-card">
                                        <div class="card-main-title">{p_name}</div>
                                        <div class="card-sub-title">{d_name}</div>
                                        <div class="stat-row"><span>📍 الموقع:</span><span class="stat-val">{loc}</span></div>
                                        <div class="stat-row"><span>💰 المقدم:</span><span class="stat-val">{down}</span></div>
                                    </div>
                                """, unsafe_allow_html=True)
                                with st.expander("🔍 التفاصيل"):
                                    st.write(row.to_dict())
            else:
                st.warning("لا توجد نتائج تطابق بحثك.")
        
        with c_side:
            st.markdown("<div style='height:500px; border-right:1px solid #222; opacity:0.1; margin-right:30px;'></div>", unsafe_allow_html=True)

# --- 🏢 شاشة المطورين ---
elif selected == "🏢 المطورين":
    if not df.empty:
        dev_col = 'Developer' if 'Developer' in df.columns else df.columns[0]
        devs = df[[dev_col, 'Owner', 'Detailed_Info']].drop_duplicates(subset=[dev_col]).reset_index(drop=True)
        
        c_main, c_side = st.columns([0.7, 0.3])
        with c_main:
            st.markdown("<h2 style='color:#f59e0b;'>🏢 المطورين</h2>", unsafe_allow_html=True)
            s_d = st.text_input("🔍 ابحث عن مطور...")
            if s_d:
                devs = devs[devs[dev_col].str.contains(s_d, case=False, na=False)]
            
            # شبكة 3x3
            curr_devs = devs.iloc[:9] 
            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i+j < len(curr_devs):
                        row = curr_devs.iloc[i+j]
                        with cols[j]:
                            st.markdown(f'<div class="pro-card"><div class="card-main-title">{row[dev_col]}</div><div class="card-sub-title">👤 {row.get("Owner", "غير متوفر")}</div></div>', unsafe_allow_html=True)
                            with st.expander("🔍 التفاصيل"): st.write(row.get('Detailed_Info', 'لا توجد بيانات إضافية'))
        with c_side:
            st.markdown("<div style='height:500px; border-right:1px solid #222; opacity:0.1; margin-right:30px;'></div>", unsafe_allow_html=True)

# --- 🛠️ شاشة الأدوات ---
elif selected == "🛠️ أدوات البروكر":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='pro-card'><h3>💰 حاسبة القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=1000000)
        yr = st.number_input("السنين", value=7)
        st.subheader(f"{pr/(yr*12):,.0f} ج/شهري")
        st.markdown("</div>", unsafe_allow_html=True)
    # باقي الأدوات...
