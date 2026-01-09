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
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f4f7f9; 
    }

    /* الهيدر الرئيسي الفخم */
    .main-header {
        text-align: center; color: #ffffff; background: linear-gradient(90deg, #001a33 0%, #1e3a8a 100%);
        font-weight: 900; font-size: 1.6rem; margin-bottom: 15px; padding: 12px;
        border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }

    /* كروت مطورة جمالياً - حجم نانو */
    .premium-card {
        background: #ffffff; 
        border: 1px solid #e5e7eb; 
        border-right: 5px solid #1e40af; 
        border-radius: 8px; 
        padding: 8px 12px;
        margin-bottom: 6px; 
        min-height: 105px; 
        display: flex; 
        flex-direction: column; 
        justify-content: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
    }
    .premium-card:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-right-color: #16a34a;
    }

    .t-dev { color: #0f172a !important; font-size: 0.95rem; font-weight: 900; line-height: 1.1; }
    .t-proj { color: #2563eb !important; font-size: 0.8rem; font-weight: 700; margin: 2px 0; }
    .t-price { color: #059669 !important; font-size: 1.05rem; font-weight: 900; letter-spacing: -0.5px; }
    .t-info { color: #64748b; font-size: 0.75rem; font-weight: 600; background: #f8fafc; padding: 2px 6px; border-radius: 4px; display: inline-block; margin-top: 4px; }

    /* زر التفاصيل الأنيق */
    div.stButton > button {
        background: #0f172a !important; color: white !important;
        font-size: 0.75rem !important; height: 26px !important;
        border-radius: 5px !important; width: 100%; border: none !important;
        font-weight: 700 !important; margin-top: 6px !important;
        transition: 0.3s;
    }
    div.stButton > button:hover { background: #1e40af !important; }

    /* تحسين شكل المدخلات */
    .stTextInput input, .stSelectbox div { border-radius: 8px !important; border: 1px solid #cbd5e1 !important; }
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
        
        # سطر فلاتر عصري
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1: sq = st.text_input("🔍 بحث ذكي (مطور أو مشروع)", placeholder="اكتب اسم الشركة أو المشروع هنا...", label_visibility="collapsed")
        with f2: sa = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()), label_visibility="collapsed")
        with f3: sp = st.number_input("💰 أقصى ميزانية", value=0, label_visibility="collapsed")

        f_df = df.copy()
        if sq: f_df = f_df[f_df.iloc[:, 0].str.contains(sq, na=False, case=False) | f_df.iloc[:, 2].str.contains(sq, na=False, case=False)]
        if sa != "الكل": f_df = f_df[f_df.iloc[:, 3] == sa]
        if sp > 0: f_df = f_df[f_df['p_val'] <= sp]

        # التقسيم: اليمين للكروت واليسار للإضافات
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
                                <div class="premium-card">
                                    <div class="t-dev">{row[0]}</div>
                                    <div class="t-proj">🏢 {row[2]}</div>
                                    <div class="t-price">{row[4]}</div>
                                    <div class="t-info">📍 {row[3]} | 💳 مقدم {row[10]}</div>
                                </div>
                            """, unsafe_allow_html=True)
                            if st.button("عرض التفاصيل", key=f"b_{start+i+j}"):
                                st.session_state.selected_dev = row[0]
                                st.session_state.page = 'details'
                                st.rerun()

            # التحكم في الصفحات بشكل أنيق
            st.markdown("<div style='margin-top:20px;'></div>", unsafe_allow_html=True)
            n1, n2, n3 = st.columns([1,1,1])
            with n1: 
                if st.session_state.curr > 0:
                    if st.button("⬅️ السابق"): st.session_state.curr -= 1; st.rerun()
            with n2: st.markdown(f"<p style='text-align:center; font-weight:700; color:#1e3a8a;'>صفحة {st.session_state.curr+1} من {total}</p>", unsafe_allow_html=True)
            with n3:
                if st.session_state.curr < total - 1:
                    if st.button("التالي ➡️"): st.session_state.curr += 1; st.rerun()

        with side_area:
            st.markdown("<div style='border:1px solid #e5e7eb; padding:15px; background:white; border-radius:12px; box-shadow: 0 4px 6px rgba(0,0,0,0.02);'>", unsafe_allow_html=True)
            st.markdown("<p style='font-weight:900; font-size:1rem; color:#1e3a8a; border-bottom:2px solid #f1f5f9; padding-bottom:5px;'>⭐ زتونة السوق</p>", unsafe_allow_html=True)
            st.markdown("<p style='font-size:0.8rem; line-height:1.6; color:#475569;'>استخدم الفلاتر في الأعلى للوصول لميزانيتك بدقة. اضغط على التفاصيل لقراءة التحليل الفني للمشروع.</p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif st.session_state.page == 'details':
        dev = st.session_state.selected_dev
        projs = df[df.iloc[:, 0] == dev]
        if st.button("⬅️ عودة للقائمة الرئيسية"): st.session_state.page = 'main'; st.rerun()
        st.markdown(f"<h2 style='color:#0f172a; border-right:8px solid #1e3a8a; padding-right:15px;'>🏢 {dev}</h2>", unsafe_allow_html=True)
        st.divider()
        for _, r in projs.iterrows():
            with st.expander(f"📍 {r[2]} - السعر: {r[4]}", expanded=True):
                st.markdown(f"""
                **الموقع:** {r[3]} | **نظام السداد:** مقدم {r[10]} تقسيط {r[9]} سنوات
                <div style='background:#fff4f4; padding:10px; border-radius:8px; border-right:4px solid #ef4444; margin-top:10px;'>
                <b>💡 الزتونة الفنية:</b><br>{r[11]}
                </div>
                """, unsafe_allow_html=True)
