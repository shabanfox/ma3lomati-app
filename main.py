import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* الخلفية العامة */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f0f2f5; 
    }

    /* خانة البحث - جعلها بارزة جداً */
    .stTextInput input {
        border: 3px solid #001a33 !important;
        border-radius: 10px !important;
        font-size: 1.2rem !important;
        font-weight: 900 !important;
        color: #000000 !important;
        background-color: #ffffff !important;
    }

    /* الكروت الرئيسية - يمين */
    .main-card {
        background: #ffffff; border-radius: 15px; padding: 20px;
        border-right: 12px solid #001a33; margin-bottom: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.15);
        min-height: 220px;
    }
    .main-title { color: #000000 !important; font-size: 1.5rem; font-weight: 900; margin-bottom: 10px; }
    .main-price { color: #059669 !important; font-size: 1.6rem; font-weight: 900; }
    .main-details { color: #1e293b !important; font-size: 1.1rem; font-weight: 700; }

    /* كروت الفرص - يسار (ميكرو) */
    .micro-card {
        background: #ffffff; border-radius: 8px; padding: 8px;
        border-right: 5px solid #d97706; margin-bottom: 6px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .micro-title { color: #000000 !important; font-size: 0.9rem; font-weight: 900; line-height: 1.2; }
    .micro-price { color: #059669 !important; font-size: 0.8rem; font-weight: 700; }

    /* الأزرار */
    .stButton>button { 
        background-color: #001a33 !important; color: #ffffff !important;
        width: 100%; font-family: 'Cairo' !important; font-weight: 900 !important;
        height: 50px; font-size: 1.1rem !important; border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# دالة استخراج الأرقام
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
    
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#001a33; font-weight:900;'>🏠 منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # --- قسم البحث المطور ---
        st.markdown("### 🔍 ابحث عن مشروعك المفضل:")
        search_term = st.text_input("", placeholder="اكتب اسم المشروع أو المطور هنا...", label_visibility="collapsed")
        
        # صف الفلاتر
        col1, col2, col3, col4 = st.columns(4)
        with col1: s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].unique().tolist()))
        with col2: s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].unique().tolist()))
        with col3: m_price = st.number_input("💰 أقصى سعر", value=0, step=1000000)
        with col4: m_down = st.number_input("💵 أقصى مقدم", value=0, step=500000)

        # الفلترة
        f_df = df.copy()
        if search_term:
            f_df = f_df[f_df.iloc[:, 0].str.contains(search_term, na=False, case=False) | f_df.iloc[:, 2].str.contains(search_term, na=False, case=False)]
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if m_price > 0: f_df = f_df[f_df['price_val'] <= m_price]
        if m_down > 0: f_df = f_df[f_df['down_val'] <= m_down]

        st.markdown("<hr style='border: 2px solid #001a33;'>", unsafe_allow_html=True)

        # تقسيم الصفحة
        main_col, side_col = st.columns([3.2, 0.8])

        with main_col:
            # عرض الكروت الرئيسية (3 في كل صف)
            for i in range(0, len(f_df[:12]), 3): # نعرض أول 12 نتيجة لسرعة التحميل
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(f_df):
                        row = f_df.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="main-card">
                                    <div class="main-title">{row[2]}</div>
                                    <div class="main-details">🏢 {row[0]}</div>
                                    <div class="main-details">📍 {row[3]}</div>
                                    <div class="main-price">{row[4]}</div>
                                    <div style="background:#001a33; color:white; padding:5px; border-radius:5px; text-align:center; font-weight:900; margin-top:10px;">
                                        مقدم {row[10]} | {row[9]}س
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button(f"التفاصيل: {row[2][:10]}", key=f"btn_{i+j}"):
                                st.session_state.selected_item = row.to_list()
                                st.session_state.page = 'details'
                                st.rerun()

        with side_col:
            st.markdown("<h4 style='text-align:center; color:#ffffff; background:#d97706; padding:8px; border-radius:10px; font-weight:900;'>🔥 أقوى 10 فرص</h4>", unsafe_allow_html=True)
            for idx, row in df.head(10).iterrows():
                st.markdown(f"""
                    <div class="micro-card">
                        <div class="micro-title">#{idx+1} {row[2]}</div>
                        <div class="micro-price">{row[4]}</div>
                    </div>
                """, unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("⬅️ عودة"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h1 style='color:#001a33; font-weight:900;'>{item[2]}</h1>", unsafe_allow_html=True)
        st.error(f"### 💡 الزتونة الفنية:\n\n**{item[11]}**")
