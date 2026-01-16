import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة حالة الصفحة (Pagination)
if 'page_num' not in st.session_state:
    st.session_state.page_num = 0

# 3. ستايل الألوان الواضحة (High Contrast Style)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
        background-color: #F8FAFC !important; /* خلفية فاتحة جداً مريحة للعين */
    }
    
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }

    /* الهيدر الملون بوضوح */
    .header-box {
        background: #0F172A; /* كحلي غامق جداً */
        color: #FFFFFF;
        padding: 40px 20px;
        text-align: center;
        border-bottom: 5px solid #F59E0B; /* برتقالي ذهبي واضح */
        border-radius: 0 0 30px 30px;
        margin-bottom: 20px;
    }

    /* كروت المشاريع بألوان واضحة */
    .project-card {
        background: white;
        border-radius: 15px;
        border: 2px solid #E2E8F0;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: 0.3s;
    }
    .project-card:hover {
        border-color: #3B82F6; /* أزرق واضح عند التمرير */
        box-shadow: 0 10px 15px rgba(0,0,0,0.1);
    }
    
    .status-badge {
        background: #DCFCE7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 12px;
    }

    /* أزرار التنقل */
    .stButton>button {
        width: 100%;
        background-color: #3B82F6 !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 4. وظائف البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        return p
    except: return pd.DataFrame()

df_p = load_data()

# 5. الهيدر
st.markdown("""
    <div class="header-box">
        <h1 style="color: #F59E0B; font-size: 40px; font-weight: 900; margin-bottom: 10px;">Broker<span style="color:white;">Edge</span> PRO</h1>
        <p style="font-size: 18px; color: #CBD5E1;">الدليل العقاري الأسرع والأكثر وضوحاً في مصر</p>
    </div>
""", unsafe_allow_html=True)

# 6. المنيو
menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={
        "container": {"background-color": "white", "padding": "10px", "border-radius": "15px", "border": "1px solid #E2E8F0"},
        "nav-link-selected": {"background-color": "#0F172A", "color": "white"}
    }
)

# 7. محرك البحث
search_q = st.text_input("", placeholder="🔍 اكتب اسم المشروع أو المطور (البحث يعمل تلقائياً)...", label_visibility="collapsed")

if menu == "المشاريع":
    # فلترة البحث
    dff = df_p.copy()
    if search_q:
        dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search_q, case=False).any(), axis=1)]
        st.session_state.page_num = 0 # إعادة الترقيم عند البحث

    # إعدادات الترقيم (6 فقط في الصفحة)
    items_per_page = 6
    total_pages = len(dff) // items_per_page + (1 if len(dff) % items_per_page > 0 else 0)
    
    start_idx = st.session_state.page_num * items_per_page
    end_idx = start_idx + items_per_page
    current_items = dff.iloc[start_idx:end_idx]

    # العرض في شبكة
    main_col, side_col = st.columns([0.75, 0.25])
    
    with main_col:
        st.markdown(f"<h3>عرض المشاريع ({start_idx + 1} - {min(end_idx, len(dff))} من {len(dff)})</h3>", unsafe_allow_html=True)
        
        cols = st.columns(2)
        for i, (idx, row) in enumerate(current_items.iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                    <div class="project-card">
                        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                            <h3 style="color: #1E293B; margin: 0; font-size: 20px;">{row.get('Project Name', 'مشروع جديد')}</h3>
                            <span class="status-badge">متاح</span>
                        </div>
                        <p style="color: #3B82F6; font-weight: bold; margin: 5px 0;">📍 {row.get('Area', 'الموقع')}</p>
                        <p style="color: #64748B; font-size: 14px;">🏢 المطور: <b>{row.get('Developer', 'غير محدد')}</b></p>
                        <div style="background: #F1F5F9; padding: 10px; border-radius: 10px; font-size: 13px; color: #475569; margin-top: 15px;">
                            📏 المساحة: {row.get('Project Area', 'N/A')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        
        # أزرار التنقل (التالي والسابق)
        st.write("---")
        c1, c2, c3 = st.columns([1, 2, 1])
        with c1:
            if st.session_state.page_num > 0:
                if st.button("⬅️ السابق"):
                    st.session_state.page_num -= 1
                    st.rerun()
        with c2:
            st.markdown(f"<p style='text-align:center; font-weight:bold; margin-top:10px;'>صفحة {st.session_state.page_num + 1} من {total_pages}</p>", unsafe_allow_html=True)
        with c3:
            if end_idx < len(dff):
                if st.button("التالي ➡️"):
                    st.session_state.page_num += 1
                    st.rerun()

    with side_col:
        st.markdown("""
            <div style="background: white; padding: 20px; border-radius: 15px; border: 2px solid #10B981;">
                <h4 style="color: #10B981; text-align: center; margin-top: 0;">🔑 استلام فوري</h4>
                <p style="font-size: 12px; color: #64748B; text-align: center;">أحدث الوحدات الجاهزة للسكن</p>
            </div>
        """, unsafe_allow_html=True)
        
        # فلترة الاستلام الفوري (أول 5 مشاريع فقط للجانب)
        ready_df = dff[dff.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(5)
        for _, r in ready_df.iterrows():
            st.markdown(f"""
                <div style="background: #ECFDF5; border-right: 4px solid #10B981; padding: 12px; border-radius: 8px; margin-top: 10px;">
                    <div style="font-size: 14px; font-weight: bold; color: #065F46;">{r.get('Project Name')}</div>
                    <div style="font-size: 11px; color: #059669;">📍 {r.get('Area')}</div>
                </div>
            """, unsafe_allow_html=True)

elif menu == "الأدوات":
    st.markdown("<div style='background: white; padding: 30px; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    st.header("🧮 حاسبة الأقساط الواضحة")
    price = st.number_input("سعر الوحدة الإجمالي (ج.م)", value=5000000, step=100000)
    years = st.slider("عدد سنوات التقسيط", 1, 15, 8)
    
    installment = price / (years * 12)
    st.markdown(f"""
        <div style="background: #EFF6FF; border: 2px solid #3B82F6; padding: 20px; border-radius: 15px; text-align: center; margin-top: 20px;">
            <h2 style="color: #1E40AF; margin: 0;">{installment:,.0f} ج.م</h2>
            <p style="color: #3B82F6; font-weight: bold;">قسطك الشهري</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
