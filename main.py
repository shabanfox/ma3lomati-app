import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء القوائم الافتراضية */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #0e1117; color: white;
    }

    .sticky-nav {
        position: fixed; top: 0; right: 0; left: 0; background: #000000;
        z-index: 999; padding: 15px 20px; border-bottom: 2px solid #f59e0b;
        display: flex; justify-content: space-around;
    }

    .project-card {
        background: #1a1c23; border-right: 5px solid #f59e0b; 
        padding: 20px; margin-bottom: 20px; border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3); transition: 0.3s;
    }
    .project-card:hover { transform: translateY(-5px); border-right-width: 10px; }

    .title-tag { color: #f59e0b; font-size: 20px; font-weight: 900; margin-bottom: 10px; display: block; }
    .label-gold { color: #f59e0b; font-weight: 700; font-size: 14px; }
    .val-text { color: #e0e0e0; font-weight: 400; margin-left: 10px; }
    
    .content-spacer { margin-top: 80px; }
    </style>
""", unsafe_allow_html=True)

# 2. وظيفة جلب البيانات من رابط Google Sheets الخاص بك
@st.cache_data(ttl=300)
def load_data_from_gsheets():
    # تحويل رابط الـ HTML إلى رابط CSV للقراءة البرمجية
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        # تنظيف العناوين في حال وجود مسافات زائدة
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ في تحميل البيانات: {e}")
        return pd.DataFrame()

# 3. محرك البحث والفلترة
df = load_data_from_gsheets()

st.markdown('<div class="content-spacer"></div>', unsafe_allow_html=True)

if not df.empty:
    st.title("🏗️ دليل المشاريع العقارية الذكي")
    
    # صف البحث والفلاتر
    c1, c2 = st.columns([2, 1])
    with c1:
        search = st.text_input("🔍 ابحث (اسم المشروع، المطور، الميزة...)", placeholder="مثال: ماونتن فيو أو التجمع")
    with c2:
        # فلتر المناطق بناءً على البيانات الموجودة فعلياً في الشيت
        unique_areas = df['Area'].unique().tolist() if 'Area' in df.columns else []
        area_filter = st.multiselect("📍 تصفية حسب المنطقة", options=unique_areas)

    # تطبيق الفلترة
    filtered_df = df
    if search:
        filtered_df = filtered_df[filtered_df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
    if area_filter:
        filtered_df = filtered_df[filtered_df['Area'].isin(area_filter)]

    # 4. نظام تقسيم الصفحات (40 مشروع)
    items_per_page = 40
    if 'page' not in st.session_state: st.session_state.page = 0
    
    total_results = len(filtered_df)
    total_pages = (total_results - 1) // items_per_page + 1
    start_idx = st.session_state.page * items_per_page
    end_idx = start_idx + items_per_page
    
    current_page_data = filtered_df.iloc[start_idx:end_idx]

    # عرض المشاريع بنظام الـ Cards
    for _, row in current_page_data.iterrows():
        st.markdown(f"""
        <div class="project-card">
            <span class="title-tag">🏢 {row.get('Project Name', 'N/A')}</span>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                <div><span class="label-gold">المطور:</span> <span class="val-text">{row.get('Developer', 'غير محدد')}</span></div>
                <div><span class="label-gold">المنطقة:</span> <span class="val-text">{row.get('Area', 'غير محدد')}</span></div>
                <div><span class="label-gold">السعر (متر):</span> <span class="val-text">{row.get('Start Price (sqm)', 'غير محدد')}</span></div>
                <div><span class="label-gold">التسليم:</span> <span class="val-text">{row.get('Delivery', '-')}</span></div>
                <div><span class="label-gold">نوع الوحدة:</span> <span class="val-text">{row.get('Unit Type', '-')}</span></div>
                <div><span class="label-gold">الاستشاري:</span> <span class="val-text">{row.get('Consultant', '-')}</span></div>
            </div>
            <div style="margin-top:10px; border-top: 1px solid #333; padding-top:10px;">
                <span class="label-gold">💡 الميزة التنافسية:</span> <span class="val-text">{row.get('Competitive Advantage', '-')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # أزرار التنقل بين الصفحات
    st.markdown("---")
    nav_c1, nav_c2, nav_c3 = st.columns([1, 2, 1])
    with nav_c1:
        if st.session_state.page > 0:
            if st.button("⬅️ السابق"): 
                st.session_state.page -= 1
                st.rerun()
    with nav_c2:
        st.write(f"<p style='text-align:center'>صفحة {st.session_state.page + 1} من {total_pages} (إجمالي {total_results} مشروع)</p>", unsafe_allow_html=True)
    with nav_c3:
        if end_idx < total_results:
            if st.button("التالي ➡️"): 
                st.session_state.page += 1
                st.rerun()
else:
    st.info("جاري سحب البيانات من Google Sheets... تأكد من صحة الرابط والأعمدة.")
