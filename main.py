import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. حقن Tailwind CSS وخط Cairo في قلب Streamlit
st.markdown("""
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* تطبيق الخط على كل العناصر */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* إخفاء واجهة ستريمليت الافتراضية */
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; background-color: #f9fafb; }
    
    /* تصميم كارت المشاريع بأسلوب Tailwind */
    .custom-card {
        background: white;
        border-radius: 1rem;
        border-right: 5px solid #2563eb;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);
        padding: 1.5rem;
        transition: 0.3s;
    }
    .custom-card:hover { transform: translateY(-5px); box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); }
    </style>
""", unsafe_allow_html=True)

# 3. وظائف جلب البيانات (الأخبار وجوجل شيت)
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        feed = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "متابعة مستمرة لآخر مستجدات العقارات"
    except: return "سوق العقارات المصري: تحديثات يناير 2026"

@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        return p
    except: return pd.DataFrame()

# 4. بناء الهيدر بأسلوب Tailwind (HTML داخل st.markdown)
st.markdown("""
    <nav style="background: white; box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05); padding: 1rem 2rem; display: flex; justify-content: space-between; align-items: center;">
        <div style="font-size: 1.5rem; font-weight: 800; color: #1e3a8a;">Broker<span style="color: #3b82f6;">Edge</span></div>
        <div style="background: #3b82f6; color: white; padding: 0.5rem 1.5rem; border-radius: 0.5rem; font-weight: bold; cursor: pointer;">دخول البروكر</div>
    </nav>
    <header style="background: #1e3a8a; padding: 4rem 1rem; text-align: center; color: white;">
        <h1 style="font-size: 2.25rem; font-weight: 800; margin-bottom: 1rem;">كل داتا السوق في جيبك</h1>
        <p style="color: #bfdbfe; margin-bottom: 2rem;">ابحث عن المشاريع، قارن المطورين، واحصل على الزتونة فوراً</p>
    </header>
""", unsafe_allow_html=True)

# شريط الأخبار
st.markdown(f"""
    <div style="background: #f1f5f9; padding: 5px 0; overflow: hidden; border-bottom: 1px solid #e2e8f0;">
        <marquee scrollamount="5" direction="right" style="color: #475569; font-size: 14px;">🔥 {get_real_news()}</marquee>
    </div>
""", unsafe_allow_html=True)

# 5. محرك البحث والتبويبات
df_p = load_data()

with st.container():
    st.markdown("<div style='max-width: 900px; margin: -30px auto 30px auto;'>", unsafe_allow_html=True)
    search_q = st.text_input("", placeholder="🔍 ابحث عن اسم المشروع أو المطور...", label_visibility="collapsed")
    st.markdown("</div>", unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={
        "container": {"background-color": "white", "padding": "5px", "border-radius": "10px", "box-shadow": "0 2px 4px rgba(0,0,0,0.05)"},
        "nav-link-selected": {"background-color": "#1e3a8a", "color": "white"}
    }
)

# 6. عرض النتائج بأسلوب الـ Grid الاحترافي
if menu == "المشاريع":
    dff = df_p.copy()
    if search_q:
        dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search_q, case=False).any(), axis=1)]

    # توزيع المشاريع في كروت
    main_col, side_col = st.columns([0.75, 0.25])
    
    with main_col:
        cols = st.columns(2)
        for i, (idx, row) in enumerate(dff.head(10).iterrows()):
            with cols[i % 2]:
                st.markdown(f"""
                    <div class="custom-card">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <h3 style="color: #1e3a8a; font-size: 1.2rem; font-weight: 800; margin:0;">{row.get('Project Name', 'مشروع')}</h3>
                            <span style="background: #dcfce7; color: #166534; font-size: 10px; padding: 2px 8px; border-radius: 10px; font-weight: bold;">محدث</span>
                        </div>
                        <p style="color: #64748b; font-size: 13px; margin: 10px 0;">📍 {row.get('Area', 'الموقع')}</p>
                        <div style="border-top: 1px solid #f1f5f9; padding-top: 10px; display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 14px; font-weight: 700; color: #1e40af;">{row.get('Developer', 'المطور')}</span>
                            <span style="color: #3b82f6; font-size: 12px; cursor: pointer;">التفاصيل ←</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                with st.expander("فتح الزتونة"):
                    st.write(f"✨ **المميزات:** {row.get('Project Features', 'N/A')}")
                    st.info(f"📐 **المساحة:** {row.get('Project Area', 'N/A')}")

    with side_col:
        st.markdown("""
            <div style="background: white; padding: 1rem; border-radius: 1rem; border: 1px solid #e2e8f0;">
                <h4 style="color: #16a34a; font-size: 15px; font-weight: 800; margin-bottom: 1rem;">🔑 استلام فوري</h4>
            </div>
        """, unsafe_allow_html=True)
        # هنا يمكن وضع فلترة الاستلام الفوري بنفس أسلوب الكود الأول
        ready_df = dff[dff.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        for _, r in ready_df.head(5).iterrows():
            st.markdown(f"""
                <div style="background: #f0fdf4; border-right: 3px solid #16a34a; padding: 10px; border-radius: 8px; margin-bottom: 8px;">
                    <div style="font-size: 13px; font-weight: bold; color: #166534;">{r.get('Project Name')}</div>
                    <div style="font-size: 11px; color: #15803d;">📍 {r.get('Area')}</div>
                </div>
            """, unsafe_allow_html=True)

# 7. الأدوات
elif menu == "الأدوات":
    st.markdown("<div style='background: white; padding: 2rem; border-radius: 1rem; box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1);'>", unsafe_allow_html=True)
    st.subheader("🧮 حاسبة الأقساط السريعة")
    c1, c2 = st.columns(2)
    with c1: price = st.number_input("سعر الوحدة", 1000000)
    with c2: years = st.slider("عدد السنوات", 1, 15, 8)
    st.metric("القسط الشهري التقريبي", f"{price/(years*12):,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

