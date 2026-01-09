import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والستايل الفائق الوضوح
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء شريط Streamlit تماماً ليكون تطبيقاً مستقلاً */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* تنسيق الجسم العام - تباين عالٍ جداً */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* خانة البحث - عريضة، حدود غامقة، ونص أسود واضح */
    .stTextInput input {
        border: 4px solid #000000 !important;
        border-radius: 12px !important;
        font-size: 1.3rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
        padding: 15px !important;
    }

    /* كروت المشاريع - 3 في الصف - حدود غامقة جداً */
    .main-card {
        background: #ffffff; border-radius: 15px; padding: 20px;
        border-right: 15px solid #000000; margin-bottom: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
        min-height: 250px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .main-title { color: #000000 !important; font-size: 1.6rem; font-weight: 900; line-height: 1.2; }
    .main-price { color: #166534 !important; font-size: 1.7rem; font-weight: 900; margin: 10px 0; }
    .main-details { color: #000000 !important; font-size: 1.2rem; font-weight: 800; }

    /* كروت الـ 10 فرص (ميكرو) - متباينة جداً */
    .micro-card {
        background: #ffffff; border-radius: 8px; padding: 10px;
        border-right: 6px solid #b45309; margin-bottom: 8px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.1);
    }
    .micro-title { color: #000000 !important; font-size: 0.9rem; font-weight: 900; }

    /* أزرار التنقل والبحث */
    .stButton>button { 
        background-color: #000000 !important; color: #ffffff !important;
        width: 100%; font-family: 'Cairo' !important; font-weight: 900 !important;
        border-radius: 12px; height: 55px; font-size: 1.2rem !important;
    }
    
    /* تحسين شكل الفلاتر */
    label { color: #000000 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
    </style>
""", unsafe_allow_html=True)

# دالة ذكية لتنظيف الأرقام من النصوص
def extract_num(text):
    if pd.isna(text): return 0
    res = re.findall(r'\d+', str(text).replace(',', ''))
    return int(res[0]) if res else 0

# 2. جلب البيانات
@st.cache_data
def get_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns]
        df['price_val'] = df.iloc[:, 4].apply(extract_num)
        df['down_val'] = df.iloc[:, 10].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#000000; font-weight:900; font-size:3rem;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # --- خانة البحث الرئيسية ---
        search_term = st.text_input("🔍 ابحث عن اسم المشروع أو المطور (اكتب هنا للفلترة الفورية):", placeholder="مثال: SODIC أو التجمع الخامس")
        
        # صف الفلاتر التكميلية
        col1, col2, col3, col4 = st.columns(4)
        with col1: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with col2: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        with col3: m_price = st.number_input("💰 ميزانية السعر (جنية)", value=0, step=1000000)
        with col4: m_down = st.number_input("💵 ميزانية المقدم (جنية)", value=0, step=500000)

        # منطق الفلترة المجمع
        f_df = df.copy()
        if search_term:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if m_price > 0: f_df = f_df[f_df['price_val'] <= m_price]
        if m_down > 0: f_df = f_df[f_df['down_val'] <= m_down]

        st.markdown("<hr style='border: 2px solid #000000;'>", unsafe_allow_html=True)

        # التوزيع (3 أعمدة للمشاريع | عمود للفرص)
        main_col, side_col = st.columns([3.1, 0.9])

        with main_col:
            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            start_idx = st.session_state.current_page * items_per_page
            current_items = f_df.iloc[start_idx : start_idx + items_per_page]

            # عرض 3 كروت في كل صف بدقة
            for i in range(0, len(current_items), 3):
                row_cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with row_cols[j]:
                            st.markdown(f"""
                                <div class="main-card">
                                    <div>
                                        <div class="main-title">{row[2]}</div>
                                        <div class="main-details">🏢 {row[0]}</div>
                                        <div class="main-details">📍 {row[3]}</div>
                                    </div>
                                    <div>
                                        <div class="main-price">{row[4]}</div>
                                        <div style="background:#000000; color:white; padding:8px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem;">
                                            مقدم {row[10]} | {row[9]} سنوات
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"عرض تفاصيل {row[2][:10]}", key=f"main_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

            # أزرار التنقل (السابق والتالي)
            st.markdown("---")
            nav1, nav2, nav3 = st.columns([1, 2, 1])
            with nav1:
                if st.session_state.current_page > 0:
                    if st.button("⬅️ الصفحة السابقة"):
                        st.session_state.current_page -= 1
                        st.rerun()
            with nav2:
                st.markdown(f"<p style='text-align:center; font-weight:900; font-size:1.5rem; color:#000000;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            with nav3:
                if st.session_state.current_page < total_pages - 1:
                    if st.button("الصفحة التالية ➡️"):
                        st.session_state.current_page += 1
                        st.rerun()

        with side_col:
            st.markdown("<h5 style='text-align:center; color:#ffffff; background:#b45309; padding:10px; border-radius:12px; font-weight:900;'>🔥 أقوى 10 فرص</h5>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""
                    <div class="micro-card">
                        <div class="micro-title">#{idx+1} {row[2]}</div>
                        <div style="color:#166534; font-size:0.9rem; font-weight:900;">{row[4]}</div>
                    </div>
                """, unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة للقائمة الرئيسية"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h1 style='color:#000000; font-weight:900; font-size:3rem;'>{item[2]}</h1>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية لهذا المشروع:\n\n**{item[11]}**")
        st.success(f"**المطور:** {item[0]} | **المنطقة:** {item[3]} | **السعر:** {item[4]} | **المقدم:** {item[10]} | **التقسيط:** {item[9]} سنوات")
