import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود CSS لإخفاء العلامات وتنسيق الألوان والخطوط بوضوح فائق
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stHeader"] {display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f5; 
    }

    /* كروت المشاريع - يمين */
    .mini-card {
        background: white; border-radius: 15px; padding: 20px;
        border-right: 10px solid #002d5a; margin-bottom: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        min-height: 200px; display: flex; flex-direction: column; justify-content: space-between;
    }
    
    .title-text { color: #000000; font-size: 1.3rem; font-weight: 900; margin: 0; line-height: 1.2; }
    .dev-text { color: #1e293b; font-size: 1.1rem; font-weight: 700; margin-top: 5px; }
    .price-text { color: #059669; font-weight: 900; font-size: 1.4rem; margin: 10px 0; }
    
    /* قائمة أقوى 10 مشاريع - يسار */
    .top-project-card {
        background: #ffffff; border-radius: 12px; padding: 15px;
        border-right: 6px solid #d97706; margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .top-title { color: #000000; font-size: 1.1rem; font-weight: 900; }

    /* الأزرار */
    .stButton>button { 
        background-color: #002d5a !important; color: white !important;
        width: 100%; font-family: 'Cairo' !important; font-weight: 900 !important;
        font-size: 1.1rem !important; border-radius: 10px; height: 50px; border: none;
    }

    /* الفلاتر */
    .stSelectbox, .stTextInput, .stNumberInput { font-weight: 700 !important; }
    </style>
""", unsafe_allow_html=True)

# دالة لتنظيف الأرقام من النصوص (مثل "مليون" أو "جنية")
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
        # إضافة أعمدة رقمية مخفية للفلترة
        df['price_num'] = df.iloc[:, 4].apply(extract_number)
        df['downpay_num'] = df.iloc[:, 10].apply(extract_number)
        return df
    except: return None

df = load_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'current_page' not in st.session_state: st.session_state.current_page = 0

    with st.sidebar:
        st.markdown("<h2 style='text-align:center; font-weight:900;'>🏆 كبار المطورين</h2>", unsafe_allow_html=True)
        top_list = ["Mountain View", "Palm Hills", "SODIC", "Emaar Misr", "Ora Dev", "Nile Dev", "Hassan Allam", "TMG"]
        for i, name in enumerate(top_list, 1):
            st.markdown(f"""<div style='background:#002d5a; color:white; padding:12px; border-radius:10px; margin-bottom:10px; text-align:center; font-weight:900; font-size:1.1rem; border-left: 6px solid #fbbf24;'>{name}</div>""", unsafe_allow_html=True)

    if st.session_state.page == 'main':
        st.markdown("<h1 style='color:#002d5a; text-align:center; font-weight:900; font-size:2.8rem;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # صف الفلاتر الأول
        c1, c2, c3 = st.columns([2, 1, 1])
        with c1: search_q = st.text_input("🔍 ابحث عن اسم المشروع أو المطور")
        with c2: s_area = st.selectbox("📍 اختار المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with c3: s_type = st.selectbox("🏠 نوع الوحدة", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        
        # صف الفلاتر الثاني (السعر والمقدم)
        c4, c5 = st.columns(2)
        with c4: max_price = st.number_input("💰 الحد الأقصى للسعر (بالأرقام فقط)", value=0, step=500000)
        with c5: max_down = st.number_input("💵 الحد الأقصى للمقدم (بالأرقام فقط)", value=0, step=100000)

        # فلترة البيانات
        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if max_price > 0: f_df = f_df[f_df['price_num'] <= max_price]
        if max_down > 0: f_df = f_df[f_df['downpay_num'] <= max_down]
        if search_q: f_df = f_df[f_df.iloc[:, 0].str.contains(search_q, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_q, na=False, case=False)]

        st.markdown("---")

        # توزيع الشاشة
        main_col, left_panel = st.columns([2.8, 1.2])

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
                                        <p style="font-size:1.1rem; font-weight:700; color:#475569;">📍 {row[3]}</p>
                                    </div>
                                    <div>
                                        <p class="price-text">{row[4]}</p>
                                        <div style="font-size:1.1rem; color:#ffffff; background:#002d5a; padding:10px; border-radius:10px; text-align:center; font-weight:900;">
                                            مقدم {row[10]} | {row[9]} سنوات
                                        </div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"تفاصيل {row[2][:12]}", key=f"btn_{row[2]}_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()
            
            # أزرار التنقل
            st.write(f"<p style='text-align:center; font-weight:900; font-size:1.3rem;'>صفحة {st.session_state.current_page+1} من {total_pages}</p>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1: 
                if st.session_state.current_page > 0 and st.button("⬅️ السابق"): st.session_state.current_page -= 1; st.rerun()
            with b2: 
                if st.session_state.current_page < total_pages - 1 and st.button("التالي ➡️"): st.session_state.current_page += 1; st.rerun()

        with left_panel:
            st.markdown("<h3 style='text-align:center; color:#ffffff; background:#d97706; padding:15px; border-radius:15px; font-weight:900;'>🔥 أقوى 10 فرص</h3>", unsafe_allow_html=True)
            top_10 = df.head(10)
            for idx, row in top_10.iterrows():
                st.markdown(f"""
                    <div class="top-project-card">
                        <span style="color:#d97706; font-weight:900; font-size:1.2rem;">#{idx+1}</span>
                        <span class="top-title">{row[2]}</span><br>
                        <b style="color:#059669; font-size:1.1rem;">{row[4]}</b> | <small style="font-weight:700;">{row[3]}</small>
                    </div>
                """, unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h1 style='color:#002d5a; font-weight:900;'>{item[2]}</h1>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية:\n\n**{item[11]}**")
        st.success(f"**المطور:** {item[0]} | **السعر:** {item[4]} | **المقدم:** {item[10]} | **التقسيط:** {item[9]} سنوات")
