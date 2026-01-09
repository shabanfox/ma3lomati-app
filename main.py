import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS محسن (كروت جانبية بنصف الحجم)
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

    /* كروت المشاريع الرئيسية - يمين */
    .mini-card {
        background: #ffffff; border-radius: 12px; padding: 15px;
        border-right: 8px solid #001a33; margin-bottom: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        min-height: 180px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .title-text { color: #000000 !important; font-size: 1.2rem; font-weight: 900; margin: 0; }
    .price-text { color: #065f46 !important; font-weight: 900; font-size: 1.3rem; }
    
    /* كروت الـ 10 فرص - ميكرو (نصف الحجم) */
    .micro-opportunity-card {
        background: #ffffff; border-radius: 6px; padding: 4px 8px;
        border-right: 4px solid #d97706; margin-bottom: 5px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        display: flex; flex-direction: column;
    }
    .micro-title { color: #000000 !important; font-size: 0.8rem; font-weight: 900; line-height: 1.1; }
    .micro-price { color: #065f46 !important; font-size: 0.75rem; font-weight: 700; }

    /* أزرار عريضة وواضحة */
    .stButton>button { 
        background-color: #001a33 !important; color: #ffffff !important;
        width: 100%; font-family: 'Cairo' !important; font-weight: 900 !important;
        border-radius: 6px; height: 40px; font-size: 0.9rem;
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

    if st.session_state.page == 'main':
        st.markdown("<h2 style='color:#001a33; text-align:center; font-weight:900; font-size:2rem; padding-top:10px;'>🏠 منصة معلوماتى العقارية</h2>", unsafe_allow_html=True)
        
        # الفلاتر
        c1, c2, c3, c4 = st.columns(4)
        with c1: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c2: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        with c3: max_price = st.number_input("💰 أقصى سعر", value=0)
        with c4: max_down = st.number_input("💵 أقصى مقدم", value=0)

        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if max_price > 0: f_df = f_df[f_df['price_num'] <= max_price]
        if max_down > 0: f_df = f_df[f_df['downpay_num'] <= max_down]

        st.markdown("---")

        # التوزيع (3.3 لليمين و 0.7 لليسار لضمان نحافة قائمة الـ 10 فرص)
        main_col, left_panel = st.columns([3.3, 0.7])

        with main_col:
            items_per_page = 9
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
                                        <p style="font-weight:700; color:#475569; font-size:0.9rem;">{row[0]}</p>
                                        <p style="font-size:0.85rem; font-weight:700;">📍 {row[3]}</p>
                                    </div>
                                    <div>
                                        <p class="price-text">{row[4]}</p>
                                        <div style="font-size:0.85rem; color:#ffffff; background:#001a33; padding:5px; border-radius:5px; text-align:center; font-weight:900;">
                                            مقدم {row[10]} | {row[9]}س
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"تفاصيل {row[2][:8]}", key=f"main_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

        with left_panel:
            st.markdown("<h5 style='text-align:center; color:#ffffff; background:#d97706; padding:5px; border-radius:8px; font-weight:900; font-size:0.9rem;'>🔥 أقوى 10 فرص</h5>", unsafe_allow_html=True)
            # عرض 10 مشاريع بحجم Micro
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""
                    <div class="micro-opportunity-card">
                        <div class="micro-title"><span style="color:#d97706;">#{idx+1}</span> {row[2]}</div>
                        <div class="micro-price">{row[4]}</div>
                    </div>
                """, unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"## {item[2]}")
        st.error(f"**الزتونة:** {item[11]}")
