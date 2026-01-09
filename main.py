import streamlit as st
import pandas as pd
import math
import re

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }

    /* الهيدر الكبير والفخم */
    .main-header {
        text-align: center; 
        background: linear-gradient(135deg, #001a33 0%, #1e3a8a 100%);
        color: #ffffff; 
        font-weight: 900; 
        font-size: 2.2rem; 
        padding: 20px;
        border-radius: 15px; 
        margin-bottom: 20px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }

    /* حاوية الفلاتر المطورة */
    .filter-section {
        background: white; 
        padding: 15px; 
        border-radius: 12px; 
        margin-bottom: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }

    /* كروت واضحة جداً بحجم نانو */
    .premium-nano-card {
        background: #ffffff; 
        border: 1px solid #cbd5e1; 
        border-right: 6px solid #001a33; 
        border-radius: 10px; 
        padding: 12px; 
        margin-bottom: 8px; 
        min-height: 120px;
        display: flex; 
        flex-direction: column; 
        justify-content: space-between;
        transition: 0.3s ease-in-out;
    }
    .premium-nano-card:hover { transform: translateY(-3px); box-shadow: 0 8px 15px rgba(0,0,0,0.1); }

    /* تفاصيل النصوص الكبيرة */
    .c-dev { color: #000000 !important; font-size: 1.15rem; font-weight: 900; line-height: 1.2; }
    .c-proj { color: #1d4ed8 !important; font-size: 0.95rem; font-weight: 700; margin-bottom: 4px; }
    .c-price { color: #15803d !important; font-size: 1.2rem; font-weight: 900; margin: 5px 0; }
    .c-meta { color: #475569; font-size: 0.85rem; font-weight: 600; background: #f1f5f9; padding: 2px 8px; border-radius: 5px; }

    /* زر تفاصيل واضح ومرتب */
    div.stButton > button {
        background: #001a33 !important; color: white !important;
        font-size: 0.8rem !important; height: 28px !important;
        border-radius: 6px !important; width: 100%; border: none !important;
        font-weight: 900 !important; margin-top: 8px !important;
    }
    
    /* تنسيق الفلاتر */
    label { font-weight: 900 !important; color: #001a33 !important; font-size: 0.9rem !important; }
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
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        df['p_val'] = df.iloc[:, 4].apply(extract_num)
        return df
    except: return None

df = get_data()

if df is not None:
    if 'page' not in st.session_state: st.session_state.page = 'main'
    if 'curr' not in st.session_state: st.session_state.curr = 0

    if st.session_state.page == 'main':
        st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
        
        # قسم الفلاتر المطور
        st.markdown('<div class="filter-section">', unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns([2, 1, 1])
        with col_f1: sq = st.text_input("🔍 ابحث عن مطور أو مشروع محدد:", placeholder="مثال: طلعت مصطفى، بالم هيلز...")
        with col_f2: sa = st.selectbox("📍 اختر المنطقة:", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()))
        with col_f3: sp = st.number_input("💰 ميزانيتك القصوى (جنيه):", value=0, step=1000000)
        st.markdown('</div>', unsafe_allow_html=True)

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # توزيع الصفحة (يمين للكروت، يسار للإضافات)
        main_area, side_area = st.columns([3.3, 0.7])

        with main_area:
            items = 9 
            total = math.ceil(len(f_df) / items)
            start = st.session_state.curr * items
            curr_items = f_df.iloc[start : start + items]

            for i in range(0, len(curr_items), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(curr_items):
                        row = curr_items.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="premium-nano-card">
                                    <div>
                                        <div class="c-dev">{row[0]}</div>
                                        <div class="c-proj">🏢 {row[2]}</div>
                                    </div>
                                    <div>
                                        <div class="c-price">{row[4]}</div>
                                        <div class="c-meta">📍 {row[3]} | 💳 مقدم {row[10]}</div>
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("التفاصيل الفنية", key=f"b_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # التحكم في الصفحات
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.curr > 0:
                    if st.button("⬅️ السابق"): st.session_state.curr -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:900;'>صفحة {st.session_state.curr+1} من {total}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr < total - 1:
                    if st.button("التالي ➡️"): st.session_state.curr += 1; st.rerun()

        with side_area:
            st.markdown("<div style='border-right:3px solid #1e3a8a; padding:15px; background:white; border-radius:10px;'>", unsafe_allow_html=True)
            st.markdown("<h4 style='color:#1e3a8a; margin:0;'>⭐ ملاحظات</h4>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:0.9rem;'>يوجد حالياً <b>{len(f_df)}</b> مشروع مطابق لبحثك.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        if st.button("🔙 العودة لنتائج البحث"): st.session_state.page = 'main'; st.rerun()
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        st.markdown(f"<h2 style='background:#001a33; color:white; padding:15px; border-radius:10px;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        for _, r in projs.iterrows():
            with st.expander(f"📌 مشروع: {r[2]} | السعر: {r[4]}", expanded=True):
                st.success(f"**📍 الموقع:** {r[3]} | **💳 نظام السداد:** مقدم {r[10]} | تقسيط {r[9]} سنوات")
                st.error(f"**💡 الزتونة الفنية (تحليل المطور):**\n\n{r[11]}")
