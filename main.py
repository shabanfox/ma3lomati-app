import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والستايل الجمالي
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* تنسيق الحاويات والفلاتر */
    .filter-box { background: white; padding: 20px; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 25px; }

    /* الكارت بحجم أصغر ومتناسق */
    .dev-card {
        background: #ffffff; border-radius: 12px; padding: 15px;
        border-right: 8px solid #001a33; margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        min-height: 220px; display: flex; flex-direction: column; justify-content: space-between;
        transition: 0.3s;
    }
    .dev-card:hover { transform: translateY(-5px); box-shadow: 0 8px 16px rgba(0,0,0,0.12); }

    /* ألوان الخطوط ووضوحها */
    .card-dev-name { color: #001a33 !important; font-size: 1.25rem; font-weight: 900; line-height: 1.2; }
    .card-project-name { color: #475569 !important; font-size: 1rem; font-weight: 700; margin-top: 5px; }
    .card-loc { color: #64748b !important; font-size: 0.9rem; font-weight: 600; }
    .card-price { color: #166534 !important; font-size: 1.3rem; font-weight: 900; margin: 8px 0; }
    .card-badge { background: #001a33; color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.85rem; text-align: center; }

    /* الأزرار */
    .stButton>button { 
        background-color: #001a33 !important; color: white !important;
        font-weight: 700 !important; border-radius: 8px; height: 38px; width: 100%; border: none !important;
    }
    .stButton>button:hover { background-color: #16a34a !important; }
    </style>
""", unsafe_allow_html=True)

def extract_num(text):
    if pd.isna(text): return 0
    res = re.findall(r'\d+', str(text).replace(',', ''))
    return int(res[0]) if res else 0

@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        df['price_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # قسم الفلاتر والبحث
        with st.container():
            st.markdown('<div class="filter-box">', unsafe_allow_html=True)
            search_query = st.text_input("🔍 ابحث (اسم المطور أو المشروع):", placeholder="مثال: بالم هيلز أو بادية...")
            
            c1, c2 = st.columns(2)
            with c1:
                area_filter = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()))
            with c2:
                price_limit = st.number_input("💰 أقصى سعر (جنيه)", value=0, step=1000000)
            st.markdown('</div>', unsafe_allow_html=True)

        # تطبيق الفلاتر
        f_df = df.copy()
        if search_query:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_query, na=False, case=False) | 
                        f_df.iloc[:, 2].str.contains(search_query, na=False, case=False)]
        if area_filter != "الكل":
            f_df = f_df[f_df.iloc[:, 3] == area_filter]
        if price_limit > 0:
            f_df = f_df[f_df['price_val'] <= price_limit]

        st.markdown("---")
        
        # تقسيم الشاشة: الجزء الأكبر للكروت والجزء الأصغر للإضافات
        main_col, side_col = st.columns([3.2, 0.8])

        with main_col:
            # إعدادات العرض (3 أعمدة × 4 صفوف = 12 كارت)
            items_per_page = 12
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            for i in range(0, len(current_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="dev-card">
                                    <div>
                                        <div class="card-dev-name">🏢 {row[0]}</div>
                                        <div class="card-project-name">✨ {row[2]}</div>
                                        <div class="card-loc">📍 {row[3]}</div>
                                    </div>
                                    <div>
                                        <div class="card-price">{row[4]}</div>
                                        <div class="card-badge">مقدم {row[10]} | {row[9]}س</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"التفاصيل", key=f"btn_{start_idx + i + j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار التنقل
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1, 2, 1])
            with n1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with n2:
                st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

        with side_col:
            st.markdown("<h5 style='text-align:center; color:white; background:#d97706; padding:10px; border-radius:10px; font-weight:900;'>⭐ إضافات / فرص</h5>", unsafe_allow_html=True)
            st.info("هنا يمكنك إضافة ملاحظات عامة أو تنبيهات للمستخدمين حول السوق العقاري.")
            # عرض سريع لأرخص 5 مشاريع
            st.write("**🔥 أقل مقدم متاح:**")
            low_down = df.sort_values(by='price_val').head(5)
            for _, r in low_down.iterrows():
                st.markdown(f"<small>• {r[2]} ({r[4]})</small>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        dev_name = st.session_state.selected_dev
        dev_projects = df[df.iloc[:, 0] == dev_name]
        
        if st.button("🔙 عودة للقائمة"): st.session_state.page = 'main'; st.rerun()
        
        st.markdown(f"<div style='background:#001a33; color:white; padding:25px; border-radius:15px; margin-bottom:20px;'><h1>🏢 {dev_name}</h1></div>", unsafe_allow_html=True)
        
        st.subheader("🏗️ كافة مشاريع المطور والزتونة الفنية:")
        for _, row in dev_projects.iterrows():
            with st.expander(f"📍 {row[2]} - {row[4]}"):
                st.write(f"**الموقع:** {row[3]} | **النوع:** {row[7]}")
                st.write(f"**نظام السداد:** مقدم {row[10]} | تقسيط {row[9]} سنوات")
                st.error(f"**💡 الزتونة الفنية:** {row[11]}")
