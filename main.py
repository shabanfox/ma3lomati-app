import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="BrokerEdge PRO", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة (Pagination)
if 'p_page' not in st.session_state: st.session_state.p_page = 0
if 'd_page' not in st.session_state: st.session_state.d_page = 0

# 2. التنسيق الجمالي (CSS) - الألوان واضحة وزر الخروج فوق عاليسار
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; background-color: #F8FAFC; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }

    /* الهيدر العلوي */
    .top-bar {
        background: #0F172A; padding: 15px 40px; display: flex; 
        justify-content: space-between; align-items: center; color: white;
        border-bottom: 4px solid #F59E0B;
    }
    .logo { font-size: 24px; font-weight: 900; color: #F59E0B; }
    
    /* الكروت الشبكية */
    .grid-card {
        background: white; border-radius: 12px; border: 2px solid #E2E8F0;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        min-height: 200px; transition: 0.3s;
    }
    .grid-card:hover { border-color: #3B82F6; transform: translateY(-5px); }
    .card-title { color: #1E3A8A; font-size: 20px; font-weight: 800; margin-bottom: 8px; }
    
    /* زر الخروج المخصص */
    .logout-btn {
        background: #EF4444; color: white; padding: 5px 20px; 
        border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 14px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات (تحويل روابط pubhtml إلى csv برمجياً)
def fetch_data(url):
    try:
        csv_url = url.replace('/pubhtml', '/export?format=csv')
        return pd.read_csv(csv_url).fillna("غير متوفر")
    except:
        return pd.DataFrame()

# روابط الشيتات الخاصة بك
url_projects = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pubhtml"
url_developers = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pubhtml"

# 4. بناء الهيدر مع زر الخروج فوق عاليسار
st.markdown(f"""
    <div class="top-bar">
        <div class="logo">BrokerEdge PRO</div>
        <a href="/" target="_self" class="logout-btn">🚪 خروج</a>
    </div>
""", unsafe_allow_html=True)

# 5. القائمة الرئيسية
menu = option_menu(None, ["المشاريع", "المطورين", "الأدوات"], 
    icons=["building", "person-vcard", "tools"], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "white", "margin": "10px 0", "border": "1px solid #E2E8F0"},
        "nav-link-selected": {"background-color": "#0F172A", "color": "#F59E0B"}
    }
)

# 6. معالجة الصفحات والعرض
def display_grid(df, state_key):
    q = st.text_input("🔍 بحث سريع...", placeholder="اكتب للبحث في النتائج...")
    if q:
        df = df[df.astype(str).apply(lambda x: x.str.contains(q, case=False)).any(axis=1)]
        st.session_state[state_key] = 0

    limit = 6
    total_pages = max(1, (len(df) // limit) + (1 if len(df) % limit > 0 else 0))
    start = st.session_state[state_key] * limit
    items = df.iloc[start : start + limit]

    # الشبكة
    cols = st.columns(2)
    for i, (idx, row) in enumerate(items.iterrows()):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="grid-card">
                    <div class="card-title">{row.iloc[0]}</div>
                    <div style="color: #64748B; font-weight: bold;">📍 {row.iloc[1] if len(row)>1 else ""}</div>
                    <div style="margin: 10px 0; font-size: 14px;">🏢 المطور: {row.iloc[2] if len(row)>2 else ""}</div>
                    <hr style="border:0; border-top:1px solid #eee;">
                    <div style="color: #EF4444; font-weight: 900;">{row.iloc[3] if len(row)>3 else ""}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("التفاصيل"):
                st.write(row)

    # أزرار التنقل
    st.write("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.session_state[state_key] > 0:
            if st.button("⬅️ السابق", key=f"prev_{state_key}"):
                st.session_state[state_key] -= 1
                st.rerun()
    with c2:
        st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state[state_key] + 1} من {total_pages}</p>", unsafe_allow_html=True)
    with c3:
        if (start + limit) < len(df):
            if st.button("التالي ➡️", key=f"next_{state_key}"):
                st.session_state[state_key] += 1
                st.rerun()

# التشغيل الفعلي للقوائم
if menu == "المشاريع":
    df_p = fetch_data(url_projects)
    if not df_p.empty: display_grid(df_p, 'p_page')
    else: st.error("فشل تحميل بيانات المشاريع. تأكد من إعدادات مشاركة الشيت.")

elif menu == "المطورين":
    df_d = fetch_data(url_developers)
    if not df_d.empty: display_grid(df_d, 'd_page')
    else: st.error("فشل تحميل بيانات المطورين.")

elif menu == "الأدوات":
    st.markdown("<div style='background:white; padding:40px; border-radius:15px; border:2px solid #E2E8F0;'>", unsafe_allow_html=True)
    st.header("🧮 حاسبة القسط الشهري")
    p = st.number_input("سعر الوحدة", value=5000000)
    y = st.slider("السنوات", 1, 15, 8)
    st.metric("القسط الشهري", f"{p/(y*12):,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)
