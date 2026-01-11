import streamlit as st
import pandas as pd

# 1. إعدادات النظام (Fullscreen & Dark Mode Ready)
st.set_page_config(page_title="Ma3lomati PRO Dashboard", layout="wide", initial_sidebar_state="collapsed")

# 2. هندسة التصميم (Black & Gold Master Theme)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء الزوائد الافتراضية لستريمليت */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الحاوية الأساسية */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; 
        background-color: #050505; color: white;
    }

    /* شريط التنقل العلوي */
    .nav-bar {
        background: #000; padding: 15px; border-bottom: 2px solid #f59e0b;
        display: flex; justify-content: center; gap: 30px; position: sticky; top: 0; z-index: 999;
    }

    /* كروت المشاريع */
    .project-card {
        background: linear-gradient(145deg, #111, #080808);
        border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 15px; padding: 20px; margin-bottom: 20px;
        min-height: 420px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .project-card:hover { border-color: #f59e0b; transform: translateY(-5px); box-shadow: 0 10px 30px rgba(245, 158, 11, 0.1); }

    /* صناديق الأرقام (التقسيط والمقدم) */
    .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 15px 0; }
    .stat-item { background: #1a1a1a; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #333; }
    .stat-label { color: #888; font-size: 11px; display: block; }
    .stat-value { color: #f59e0b; font-weight: 700; font-size: 13px; }

    /* الهيدر والأسعار */
    .price-tag { background: #f59e0b; color: #000; padding: 5px 12px; border-radius: 6px; font-weight: 900; font-size: 1.1rem; }
    .dev-name { color: #888; font-size: 14px; font-weight: 600; }
    
    /* الأزرار */
    div.stButton > button {
        background-color: #000 !important; color: #f59e0b !important;
        border: 1px solid #f59e0b !important; border-radius: 8px !important;
        font-weight: 700 !important; width: 100% !important;
    }
    div.stButton > button:hover { background-color: #f59e0b !important; color: #000 !important; }
    </style>
""", unsafe_allow_html=True)

# 3. محرك البيانات (قاعدة البيانات المباشرة)
@st.cache_data(ttl=300)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# 4. الملاحة وإدارة الصفحات
if 'view' not in st.session_state: st.session_state.view = "database"

st.markdown('<div class="nav-bar">', unsafe_allow_html=True)
c_nav1, c_nav2 = st.columns(2)
with c_nav1:
    if st.button("🏢 دليل المشاريع"): st.session_state.view = "database"
with c_nav2:
    if st.button("🛠️ أدوات البروكر"): st.session_state.view = "tools"
st.markdown('</div>', unsafe_allow_html=True)

# --- شاشة قاعدة البيانات ---
if st.session_state.view == "database":
    st.markdown("<h1 style='text-align:center; color:#f59e0b; margin:20px 0;'>📊 محرك البحث العقاري الاستشاري</h1>", unsafe_allow_html=True)
    
    # قسم الفلاتر الذكية
    with st.container():
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search = st.text_input("🔍 ابحث عن (اسم المشروع، المطور، الاستشاري، ميزة تنافسية...)", placeholder="مثال: التجمع الخامس، ماونتن فيو...")
        with f2:
            all_areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
            sel_area = st.selectbox("📍 المنطقة", all_areas)
        with f3:
            all_types = ["الكل"] + sorted(df['Type'].dropna().unique().tolist())
            sel_type = st.selectbox("🏠 النوع", all_types)

    # معالجة الفلترة
    filtered_df = df.copy()
    if search:
        filtered_df = filtered_df[filtered_df.apply(lambda r: search.lower() in str(r).lower(), axis=1)]
    if sel_area != "الكل":
        filtered_df = filtered_df[filtered_df['Area'].str.contains(sel_area, na=False)]
    if sel_type != "الكل":
        filtered_df = filtered_df[filtered_df['Type'].str.contains(sel_type, na=False)]

    st.markdown(f"<p style='text-align:left; color:#888; font-size:14px;'>تم العثور على {len(filtered_df)} نتيجة مطابقة</p>", unsafe_allow_html=True)

    # عرض البيانات بنظام الـ 2 كارت في الصف
    for i in range(0, len(filtered_df), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(filtered_df):
                row = filtered_df.iloc[i + j]
                with cols[j]:
                    st.markdown(f"""
                        <div class="project-card">
                            <div>
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <h2 style="color:#f59e0b; margin:0; font-size:1.6rem;">{row.get('Project Name', 'N/A')}</h2>
                                    <div class="price-tag">{row.get('Min_Val', row.get('Start Price (sqm)', '0'))}</div>
                                </div>
                                <span class="dev-name">بواسطة: {row.get('Developer', '-')}</span>
                                
                                <div class="stat-grid">
                                    <div class="stat-item"><span class="stat-label">📍 المنطقة</span><span class="stat-value">{row.get('Area', '-')}</span></div>
                                    <div class="stat-item"><span class="stat-label">💵 المقدم</span><span class="stat-value">{row.get('Down_Payment', '-')}</span></div>
                                    <div class="stat-item"><span class="stat-label">⏳ التقسيط</span><span class="stat-value">{row.get('Installments', '-')}</span></div>
                                </div>
                                
                                <div style="background:#151515; padding:15px; border-radius:10px; border-right:3px solid #f59e0b;">
                                    <p style="margin:0; font-size:13px;"><span style="color:#f59e0b; font-weight:bold;">🌟 الميزة:</span> {row.get('Competitive Advantage', '-')}</p>
                                    <p style="margin:10px 0 0 0; font-size:13px;"><span style="color:#f59e0b; font-weight:bold;">👷 الاستشاري:</span> {row.get('Consultant', '-')}</p>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    with st.expander(f"👁️ عرض الوصف والتفاصيل: {row.get('Project Name')}"):
                        st.write(f"**المالك الرئيسي:** {row.get('DeveloperOwner', '-')}")
                        st.write(f"**حالة التسليم:** {row.get('Delivery', '-')}")
                        st.write(f"**نوع الوحدة:** {row.get('Unit Type', row.get('Type', '-'))}")
                        st.info(row.get('Detailed_Info', row.get('Description', 'لا يوجد وصف تفصيلي متوفر')))

# --- شاشة أدوات البروكر ---
elif st.session_state.view == "tools":
    st.markdown("<h1 style='text-align:center; color:#f59e0b; margin:20px 0;'>🛠️ أدوات البروكر المحترف</h1>", unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown('<div class="project-card"><h3>💰 حاسبة الأقساط السريعة</h3>', unsafe_allow_html=True)
        total_p = st.number_input("إجمالي سعر الوحدة (ج.م)", min_value=0, step=100000)
        dp_p = st.slider("نسبة المقدم (%)", 0, 50, 10)
        yrs = st.number_input("سنوات التقسيط", 1, 15, 7)
        if total_p > 0:
            dp_v = total_p * (dp_p / 100)
            mnth = (total_p - dp_v) / (yrs * 12)
            st.markdown(f"<div style='background:#000; padding:15px; border-radius:10px; border:1px solid #f59e0b; text-align:center;'><h4>المقدم: {dp_v:,.0f} ج.م</h4><h2 style='color:#f59e0b;'>{mnth:,.0f} ج.م / شهر</h2></div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_t2:
        st.markdown('<div class="project-card"><h3>📱 مولد عرض الواتساب</h3>', unsafe_allow_html=True)
        p_select = st.selectbox("اختر المشروع المُراد مشاركته", df['Project Name'].unique())
        if st.button("تجهيز نص العرض"):
            p_res = df[df['Project Name'] == p_select].iloc[0]
            msg = f"🏢 *عرض مشروع: {p_select}*\n\n📍 المنطقة: {p_res['Area']}\n💰 سعر المتر: {p_res['Min_Val']}\n💳 المقدم: {p_res['Down_Payment']}\n⏳ التقسيط: {p_res['Installments']}\n🌟 ميزة المشروع: {p_res['Competitive Advantage']}\n\n*لمزيد من التفاصيل تواصل معنا!*"
            st.text_area("انسخ النص أدناه:", msg, height=180)
        st.markdown('</div>', unsafe_allow_html=True)
