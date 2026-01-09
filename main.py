import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) المطور للفلاتر والكروت
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    .search-section {
        background: linear-gradient(135deg, #003366 0%, #001a33 100%);
        padding: 30px; border-radius: 20px; margin-bottom: 20px;
        color: white; box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        text-align: center;
    }

    /* ستايل أزرار الفلاتر السريعة */
    .stButton > button {
        border-radius: 20px !important;
        font-family: 'Cairo', sans-serif !important;
        transition: all 0.3s ease !important;
    }

    /* الكارت المربع المطور */
    .grid-card {
        background: white; border-radius: 15px; padding: 20px;
        margin-bottom: 10px; border-bottom: 4px solid #D4AF37;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        height: 150px; display: flex; flex-direction: column;
        justify-content: center; transition: all 0.3s ease;
    }
    .grid-card:hover { transform: translateY(-5px); border-bottom-color: #003366; }

    /* تنسيق أزرار الأكشن تحت الكارت */
    .action-btn > div > button {
        background-color: #f1f5f9 !important; color: #003366 !important;
        border: 1px solid #e2e8f0 !important; font-size: 0.85rem !important;
        height: 35px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except: return None

df = load_data()

# إدارة الحالة (State)
if 'page' not in st.session_state: st.session_state.page = 'main'
if 'compare_list' not in st.session_state: st.session_state.compare_list = []
if 'filter_area' not in st.session_state: st.session_state.filter_area = "الكل"

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    st.markdown("""
        <div class="search-section">
            <h1 style="margin:0; font-size: 2.2rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></h1>
            <p style="opacity: 0.8;">نظام البحث والفلاتر الذكي للمستشار العقاري</p>
        </div>
    """, unsafe_allow_html=True)

    if df is not None:
        # 1. أزرار المناطق السريعة (Quick Filters)
        st.write("📍 **مناطق البحث السريع:**")
        quick_areas = ["الكل", "التجمع", "الشيخ زايد", "العاصمة الإدارية", "الساحل الشمالي", "أكتوبر"]
        q_cols = st.columns(len(quick_areas))
        
        for idx, area in enumerate(quick_areas):
            with q_cols[idx]:
                if st.button(area, key=f"q_{area}"):
                    st.session_state.filter_area = area

        # 2. شريط البحث المطور
        st.write("---")
        c1, c2 = st.columns([3, 1])
        with c1:
            search_query = st.text_input("🔍 ابحث باسم المطور أو ميزة فنية (مثلاً: تشطيب، أقساط، لاجون)...", placeholder="اكتب هنا للبحث الذكي...")
        with c2:
            # فلتر المنطقة (يتأثر بالأزرار السريعة)
            all_areas = ["الكل"] + sorted(df['Area'].dropna().unique().tolist())
            current_index = all_areas.index(st.session_state.filter_area) if st.session_state.filter_area in all_areas else 0
            s_area = st.selectbox("📍 تصفية بالمنطقة", all_areas, index=current_index)
            st.session_state.filter_area = s_area

        # منطق الفلترة (Search Engine Logic)
        f_df = df.copy()
        if st.session_state.filter_area != "الكل":
            f_df = f_df[f_df['Area'] == st.session_state.filter_area]
        if search_query:
            f_df = f_df[
                f_df['Developer'].astype(str).str.contains(search_query, case=False, na=False) |
                f_df['Detailed_Info'].astype(str).str.contains(search_query, case=False, na=False)
            ]

        # عرض النتائج (Grid 3x3)
        st.markdown(f"<h5>النتائج المتاحة: {len(f_df)}</h5>", unsafe_allow_html=True)
        
        grid_cols = st.columns(3)
        for idx, (i, row) in enumerate(f_df.reset_index().iterrows()):
            with grid_cols[idx % 3]:
                st.markdown(f"""
                    <div class="grid-card">
                        <div style="color: #003366; font-weight: 900; font-size: 1.1rem;">{row.get('Developer')}</div>
                        <div style="color: #64748b; font-size: 0.8rem; margin-top:5px;">📍 {row.get('Area')}</div>
                        <div style="color: #D4AF37; font-weight: bold; font-size: 0.9rem; margin-top:8px;">💰 {row.get('Price')}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                # أزرار الأكشن بتنسيقaction-btn
                b_col1, b_col2 = st.columns(2)
                with b_col1:
                    if st.button("👁️ تفاصيل", key=f"det_{i}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'; st.rerun()
                with b_col2:
                    name = str(row['Developer'])
                    is_in = name in st.session_state.compare_list
                    if st.button("➕ مقارنة" if not is_in else "❌ إزالة", key=f"comp_{i}"):
                        if not is_in: st.session_state.compare_list.append(name)
                        else: st.session_state.compare_list.remove(name)
                        st.rerun()
                st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    if st.button("🔙 عودة للقائمة"): st.session_state.page = 'main'; st.rerun()
    
    st.markdown(f"""
        <div style="background-color: #003366; padding: 25px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
            <h2 style="margin:0;">{item.get('Developer')}</h2>
            <p style="opacity:0.8;">📍 {item.get('Area')}</p>
        </div>
        <div style="background: white; padding: 20px; border-radius: 15px; border-right: 8px solid #003366; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
            <h3 style="color:#003366;">💡 الزتونة الفنية</h3>
            <p style="font-size:1.1rem; line-height:1.7;">{item.get('Detailed_Info', 'لا توجد بيانات.')}</p>
            <hr>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <p><b>👤 المالك:</b> {item.get('Owner', '-')}</p>
                <p><b>💰 السعر:</b> {item.get('Price', '-')}</p>
                <p><b>⏳ التقسيط:</b> {item.get('Installments', '-')}</p>
                <p><b>🕒 الاستلام:</b> {item.get('Delivery', '-')}</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
