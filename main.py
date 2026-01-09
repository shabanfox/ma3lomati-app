import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS بتباين عالي وكروت جانبية صغيرة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f1f5f9; 
    }

    /* كروت المشاريع الرئيسية */
    .mini-card {
        background: #ffffff; border-radius: 15px; padding: 20px;
        border-right: 10px solid #001a33; margin-bottom: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        min-height: 200px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .title-text { color: #000000 !important; font-size: 1.3rem; font-weight: 900; margin: 0; }
    .price-text { color: #065f46 !important; font-weight: 900; font-size: 1.5rem; }
    
    /* كروت أقوى 5 فرص - تصميم أصغر وأكثر رشاقة */
    .top-5-card {
        background: #ffffff; border-radius: 10px; padding: 8px 12px;
        border-right: 5px solid #d97706; margin-bottom: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.08);
    }
    .top-5-title { color: #000000 !important; font-size: 0.95rem; font-weight: 900; }
    .top-5-price { color: #065f46 !important; font-size: 0.85rem; font-weight: 700; }

    .stButton>button { 
        background-color: #001a33 !important; color: #ffffff !important;
        width: 100%; font-family: 'Cairo' !important; font-weight: 900 !important;
        border-radius: 8px; height: 45px;
    }
    </style>
""", unsafe_allow_html=True)

def extract_number(text):
    if pd.isna(text): return 0
    nums = re.findall(r'\d+', str(text).replace(',', ''))
    return int(nums[0]) if nums else 0

# 3. جلب البيانات
@st.cache_data
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [c.strip() for c in df.columns]
        df['price_num'] = df.iloc[:, 4].apply(extract_number)
        df['downpay_num'] = df.iloc[:, 10].apply(extract_number)
        return df
    except: return None

df = load_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    # القائمة الجانبية (Sidebar)
    with st.sidebar:
        st.markdown("<h2 style='text-align:center; font-weight:900;'>🏆 المطورين</h2>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev"]
        for name in top_list:
            st.markdown(f"""<div style='background:#001a33; color:#ffffff; padding:10px; border-radius:8px; margin-bottom:8px; text-align:center; font-weight:700;'>{name}</div>""", unsafe_allow_html=True)

    if st.session_state.page == 'main':
        st.markdown("<h1 style='color:#001a33; text-align:center; font-weight:900; font-size:2.5rem;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # الفلاتر العلوية
        search_q = st.text_input("🔍 ابحث بالاسم")
        c1, c2, c3, c4 = st.columns(4)
        with c1: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c2: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        with c3: max_price = st.number_input("💰 أقصى سعر", value=0)
        with c4: max_down = st.number_input("💵 أقصى مقدم", value=0)

        # منطق الفلترة
        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if max_price > 0: f_df = f_df[f_df['price_num'] <= max_price]
        if max_down > 0: f_df = f_df[f_df['downpay_num'] <= max_down]
        if search_q: f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

        st.markdown("---")

        # توزيع الشاشة: يمين (المشاريع) | يسار (أقوى 5)
        main_col, left_panel = st.columns([3.2, 0.8])

        with main_col:
            items_per_page = 9
            total_pages = math.ceil(len(f_df) / items_per_page)
            current_items = f_df.iloc[st.session_state.current_page * items_per_page : (st.session_state.current_page + 1) * items_per_page]

            for i in range(0, len(current_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(current_items):
                        row = current_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="mini-card">
                                    <div>
                                        <p class="title-text">{row[2]}</p>
                                        <p style="font-weight:700; color:#475569;">{row[0]}</p>
                                        <p style="font-size:0.9rem; font-weight:700;">📍 {row[3]}</p>
                                    </div>
                                    <div>
                                        <p class="price-text">{row[4]}</p>
                                        <div style="font-size:0.9rem; color:#ffffff; background:#001a33; padding:8px; border-radius:8px; text-align:center; font-weight:900;">
                                            مقدم {row[10]} | {row[9]} سنوات
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"تفاصيل {row[2][:8]}", key=f"btn_{row[2]}_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()
            
            # أزرار التنقل
            st.write(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1: 
                if st.session_state.current_page > 0 and st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with b2: 
                if st.session_state.current_page < total_pages - 1 and st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

        with left_panel:
            st.markdown("<h4 style='text-align:center; color:#ffffff; background:#d97706; padding:10px; border-radius:10px; font-weight:900;'>🔥 أقوى 5 فرص</h4>", unsafe_allow_html=True)
            # عرض أول 5 مشاريع فقط
            for idx, row in df.head(5).iterrows():
                st.markdown(f"""
                    <div class="top-5-card">
                        <span style="color:#d97706; font-weight:900;">#{idx+1}</span>
                        <div class="top-5-title">{row[2]}</div>
                        <div class="top-5-price">{row[4]}</div>
                    </div>
                """, unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h1 style='color:#001a33; font-weight:900;'>{item[2]}</h1>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية:\n\n**{item[11]}**")
