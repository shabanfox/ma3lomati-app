import streamlit as st
import pandas as pd
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - ستايل الكروت الكبيرة 2*2
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f4f7f9; 
    }

    /* مربع الفلتر */
    .filter-card {
        background: white; padding: 25px; border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0; margin-bottom: 20px;
    }

    /* الكارت المربع الكبير 2*2 */
    .grid-card {
        background: white; border-radius: 15px; padding: 25px;
        height: 180px; display: flex; flex-direction: column;
        justify-content: center; border: 1px solid #e2e8f0;
        border-right: 6px solid #003366; /* تمييز جانبي فخم */
        transition: all 0.3s ease;
    }
    .grid-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        border-right-color: #D4AF37;
    }

    /* تنسيق الأزرار */
    div.stButton > button {
        background-color: white !important; color: #003366 !important;
        border: 2px solid #003366 !important; border-radius: 8px !important;
        font-family: 'Cairo', sans-serif !important; font-weight: bold !important;
        height: 42px; font-size: 1rem !important; width: 100%;
    }
    div.stButton > button:hover { background-color: #003366 !important; color: white !important; }

    .title-text { color: #003366; font-weight: 900; font-size: 2.2rem; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات ومعالجتها
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        # ترتيب أبجدي
        if 'Developer' in df.columns:
            df = df.sort_values(by='Developer', ascending=True)
        return df
    except: return None

df = load_data()

# إدارة الحالة
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'current_page_num' not in st.session_state: st.session_state.current_page_num = 1
if 'compare_list' not in st.session_state: st.session_state.compare_list = []

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown('<div class="title-text">منصة معلوماتى العقارية</div>', unsafe_allow_html=True)

    if df is not None:
        # مربع الفلتر
        st.markdown('<div class="filter-card">', unsafe_allow_html=True)
        c1, c2 = st.columns([2, 1])
        with c1:
            search_query = st.text_input("🔍 ابحث بالعربي أو English (مطور، منطقة، ميزة فنية)...", placeholder="اكتب للبحث...")
        with c2:
            areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
            s_area = st.selectbox("تصفية بالمنطقة", areas)
        st.markdown('</div>', unsafe_allow_html=True)

        # منطق الفلترة
        f_df = df.copy()
        if s_area != "الكل":
            f_df = f_df[f_df['Area'] == s_area]
        if search_query:
            f_df = f_df[
                f_df['Developer'].astype(str).str.contains(search_query, case=False, na=False) |
                f_df.get('Detailed_Info', '').astype(str).str.contains(search_query, case=False, na=False) |
                f_df.get('Area', '').astype(str).str.contains(search_query, case=False, na=False)
            ]

        # --- تقسيم الصفحات (6 كروت في الصفحة لنظام 2*2) ---
        items_per_page = 6 # 3 صفوف × 2 كارت
        total_items = len(f_df)
        total_pages = math.ceil(total_items / items_per_page)
        
        if 'last_search' not in st.session_state or st.session_state.last_search != search_query:
            st.session_state.current_page_num = 1
            st.session_state.last_search = search_query

        start_idx = (st.session_state.current_page_num - 1) * items_per_page
        end_idx = start_idx + items_per_page
        page_items = f_df.iloc[start_idx:end_idx]

        # عرض الشبكة 2*2
        grid_cols = st.columns(2) # عمودين فقط
        for idx, (i, row) in enumerate(page_items.reset_index().iterrows()):
            with grid_cols[idx % 2]:
                st.markdown(f"""
                    <div class="grid-card">
                        <div style="color:#003366; font-weight:900; font-size:1.3rem; margin-bottom:8px;">{row.get('Developer')}</div>
                        <div style="color:#64748b; font-size:1rem;">📍 {row.get('Area', '-')}</div>
                        <div style="color:#D4AF37; font-weight:bold; font-size:1.1rem; margin-top:12px;">💰 {row.get('Price', '-')}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("👁️ عرض التفاصيل", key=f"d_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()
                with b2:
                    name = str(row['Developer'])
                    is_in = name in st.session_state.compare_list
                    if st.button("➕ مقارنة" if not is_in else "❌ إزالة", key=f"c_{i}"):
                        if not is_in: st.session_state.compare_list.append(name)
                        else: st.session_state.compare_list.remove(name)
                        st.rerun()
                st.markdown("<div style='margin-bottom:30px;'></div>", unsafe_allow_html=True)

        # أزرار التنقل
        if total_pages > 1:
            st.write("---")
            col_p = st.columns([1, 1, 1])
            with col_p[1]:
                st.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.current_page_num} من {total_pages}</p>", unsafe_allow_html=True)
                c_prev, c_next = st.columns(2)
                with c_prev:
                    if st.button("السابق") and st.session_state.current_page_num > 1:
                        st.session_state.current_page_num -= 1; st.rerun()
                with c_next:
                    if st.button("التالي") and st.session_state.current_page_num < total_pages:
                        st.session_state.current_page_num += 1; st.rerun()

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للقائمة"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"""
        <div style="background-color: #003366; padding: 40px; border-radius: 15px; color: white; text-align: center; margin-bottom: 25px;">
            <h1 style="margin:0;">{item.get('Developer')}</h1>
            <p style="font-size:1.2rem; opacity: 0.9; margin-top:10px;">📍 {item.get('Area')}</p>
        </div>
        <div class="filter-card" style="border-right: 10px solid #D4AF37;">
            <h3 style="color:#003366; margin-bottom:20px; font-size:1.5rem;">💡 الزتونة الفنية</h3>
            <p style="font-size:1.2rem; line-height:1.8; color:#1e293b; background:#f8fafc; padding:20px; border-radius:10px;">
                {item.get('Detailed_Info', 'لا توجد بيانات تفصيلية.')}
            </p>
            <hr style="border:0; border-top: 1px solid #eee; margin:25px 0;">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 25px; font-size:1.1rem;">
                <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
                <p><b>💰 السعر:</b> {item.get('Price', '-')}</p>
                <p><b>⏳ التقسيط:</b> {item.get('Installments', '-')}</p>
                <p><b>🕒 الاستلام:</b> {item.get('Delivery', '-')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
