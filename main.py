import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. ستايل متطور للفلاتر ---
st.markdown("""
    <style>
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { direction: rtl !important; text-align: right !important; }
    
    /* ستايل حاوية الفلاتر */
    .filter-box {
        background: rgba(255, 255, 255, 0.07);
        padding: 20px;
        border-radius: 20px;
        border: 1px solid rgba(245, 158, 11, 0.3);
        margin-bottom: 25px;
    }
    .filter-title {
        color: #f59e0b;
        font-weight: 900;
        margin-bottom: 10px;
        font-size: 1.1rem;
    }
    /* تعديل شكل الـ Slider */
    .stSlider [data-baseweb="slider"] { margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الوظائف التقنية (نفس الكود السابق مع تحسين الكاش) ---
@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        # قراءة البيانات مع ضمان السرعة
        p = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv")
        l = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv")
        d = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv")
        
        for df in [p, l, d]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price', 'سعر': 'Price'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 4. دالة العرض مع الفلاتر المطورة ---
def render_grid_with_filters(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    if st.session_state.view == f"details_{prefix}":
        # (كود التفاصيل كما هو بدون تغيير)
        if st.button("⬅ عودة", key=f"back_{prefix}", use_container_width=True): 
            st.session_state.view = "grid"; st.rerun()
        item = dataframe.iloc[st.session_state.current_index]
        st.write(f"### {item.iloc[0]}")
        # ... باقي كود التفاصيل
    else:
        # --- منطقة الفلاتر الذكية ---
        with st.container():
            st.markdown('<div class="filter-box">', unsafe_allow_html=True)
            
            # السطر الأول: بحث نصي واختيار موقع
            c1, c2 = st.columns([2, 1])
            with c1:
                search = st.text_input("🔍 ابحث (بالاسم، المطور، الوصف...)", key=f"search_{prefix}", placeholder="مثال: التجمع الخامس، بالم هيلز...")
            with c2:
                loc_list = ["الكل"] + sorted([str(x) for x in dataframe['Location'].unique() if str(x) not in ["---", "nan", ""]])
                sel_area = st.selectbox("📍 تصفية بالموقع", loc_list, key=f"loc_{prefix}")

            # السطر الثاني: فلتر السعر (Range Slider)
            if 'Price' in dataframe.columns and dataframe['Price'].max() > 0:
                min_p = float(dataframe['Price'].min())
                max_p = float(dataframe['Price'].max())
                
                st.markdown('<p class="filter-title">💰 ميزانية العميل (جنية مصري)</p>', unsafe_allow_html=True)
                price_range = st.slider(
                    "",
                    min_value=min_p,
                    max_value=max_p,
                    value=(min_p, max_p),
                    format="%d",
                    key=f"price_{prefix}"
                )
            else:
                price_range = (0, 1000000000)

            st.markdown('</div>', unsafe_allow_html=True)

        # --- منطق الفلترة ---
        filt = dataframe.copy()
        if search:
            filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_area != "الكل":
            filt = filt[filt['Location'].astype(str).str.contains(sel_area, case=False, na=False)]
        if 'Price' in filt.columns:
            filt = filt[(filt['Price'] >= price_range[0]) & (filt['Price'] <= price_range[1])]

        # --- العرض (Grid) ---
        # (نفس كود العرض بالكروت والصفحات كما هو لضمان ثبات الشكل)
        items_per_page = 6
        start = st.session_state[pg_key] * items_per_page
        disp = filt.iloc[start : start + items_per_page]
        
        # ... تكملة كود الـ Grid الخاص بك
        grid = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with grid[i%2]:
                p_v = f"{int(r['Price']):,}" if ('Price' in r and r['Price'] > 0) else "اتصل للسعر"
                if st.button(f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_v}", key=f"c_{prefix}_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

# --- الكود الرئيسي ---
df_p, df_d, df_l = load_data()
# ... استدعاء المنيو والتابات
