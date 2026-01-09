import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS بتباين لوني عالي (High Contrast)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء عناصر Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    /* خلفية الموقع رمادية فاتحة جداً لراحة العين */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #e5e7eb; 
    }

    /* كروت المشاريع - بيضاء ناصعة لتبرز فوق الخلفية الرمادية */
    .mini-card {
        background: #ffffff; border-radius: 15px; padding: 20px;
        border-right: 12px solid #001a33; margin-bottom: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2); /* ظل أقوى لبروز الكارت */
        min-height: 200px; display: flex; flex-direction: column; justify-content: space-between;
    }
    
    /* خطوط سوداء صريحة مغايرة للون الكارت الأبيض */
    .title-text { color: #000000 !important; font-size: 1.4rem; font-weight: 900; margin: 0; }
    .dev-text { color: #111827 !important; font-size: 1.1rem; font-weight: 700; margin-top: 5px; }
    .price-text { color: #065f46 !important; font-weight: 900; font-size: 1.5rem; margin: 10px 0; }
    
    /* كروت الـ Top 10 - لون ذهبي غامق */
    .top-project-card {
        background: #ffffff; border-radius: 12px; padding: 15px;
        border-right: 8px solid #92400e; margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .top-title { color: #000000 !important; font-size: 1.1rem; font-weight: 900; }

    /* الأزرار بلون كحلي غامق وكلام أبيض */
    .stButton>button { 
        background-color: #001a33 !important; color: #ffffff !important;
        width: 100%; font-family: 'Cairo' !important; font-weight: 900 !important;
        font-size: 1.2rem !important; border-radius: 10px; height: 50px;
    }

    /* توضيح الفلاتر */
    label { color: #000000 !important; font-weight: 900 !important; font-size: 1.1rem !important; }
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

    with st.sidebar:
        st.markdown("<h2 style='text-align:center; font-weight:900; color:#000000;'>🏆 كبار المطورين</h2>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev", "Hassan Allam", "TMG"]
        for name in top_list:
            st.markdown(f"""<div style='background:#001a33; color:#ffffff; padding:12px; border-radius:10px; margin-bottom:10px; text-align:center; font-weight:900; border-left: 6px solid #fbbf24;'>{name}</div>""", unsafe_allow_html=True)

    if st.session_state.page == 'main':
        st.markdown("<h1 style='color:#000000; text-align:center; font-weight:900; font-size:3rem;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # الفلاتر
        search_q = st.text_input("🔍 ابحث هنا بالاسم")
        c1, c2, c3, c4 = st.columns(4)
        with c1: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c2: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        with c3: max_price = st.number_input("💰 أقصى سعر", value=0, step=1000000)
        with c4: max_down = st.number_input("💵 أقصى مقدم", value=0, step=500000)

        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if max_price > 0: f_df = f_df[f_df['price_num'] <= max_price]
        if max_down > 0: f_df = f_df[f_df['downpay_num'] <= max_down]
        if search_q: f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

        st.markdown("<hr style='border: 2px solid #000000;'>", unsafe_allow_html=True)

        main_col, left_panel = st.columns([3, 1])

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
                                        <p class="dev-text">{row[0]}</p>
                                        <p style="font-size:1.1rem; font-weight:900; color:#1f2937;">📍 {row[3]}</p>
                                    </div>
                                    <div>
                                        <p class="price-text">{row[4]}</p>
                                        <div style="font-size:1.1rem; color:#ffffff; background:#001a33; padding:10px; border-radius:10px; text-align:center; font-weight:900;">
                                            مقدم {row[10]} | {row[9]} سنوات
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"تفاصيل {row[2][:10]}", key=f"btn_{row[2]}_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()
            
            # التنقل
            st.write(f"<p style='text-align:center; font-weight:900; font-size:1.5rem; color:#000000;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1: 
                if st.session_state.current_page > 0 and st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with b2: 
                if st.session_state.current_page < total_pages - 1 and st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

        with left_panel:
            st.markdown("<h3 style='text-align:center; color:#ffffff; background:#92400e; padding:15px; border-radius:15px; font-weight:900;'>🔥 أقوى 10 فرص</h3>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""
                    <div class="top-project-card">
                        <span style="color:#92400e; font-weight:900; font-size:1.2rem;">#{idx+1}</span>
                        <span class="top-title">{row[2]}</span><br>
                        <b style="color:#065f46; font-size:1.1rem;">{row[4]}</b>
                    </div>
                """, unsafe_allow_html=True)
