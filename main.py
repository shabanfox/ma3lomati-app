import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة والستايل
st.set_page_config(page_title="BrokerEdge Pro 2026", layout="wide", initial_sidebar_state="collapsed")

# إدارة الحالة (Pagination & Auth)
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'auth' not in st.session_state: st.session_state.auth = True

# 2. التنسيق الجمالي (CSS) - ألوان واضحة وخطوط عريضة
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; background-color: #F1F5F9; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }

    /* الهيدر */
    .main-header {
        background: #1E293B; color: #F59E0B; padding: 30px; text-align: center;
        border-radius: 0 0 30px 30px; border-bottom: 5px solid #F59E0B; margin-bottom: 20px;
    }

    /* الكروت الشبكية */
    .grid-card {
        background: white; border-radius: 15px; border: 2px solid #E2E8F0;
        padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: 0.3s; min-height: 220px;
    }
    .grid-card:hover { border-color: #3B82F6; transform: translateY(-5px); }
    .card-title { color: #1E3A8A; font-size: 20px; font-weight: 900; margin-bottom: 5px; }
    .card-loc { color: #EF4444; font-weight: bold; font-size: 14px; }
    .card-detail { color: #64748B; font-size: 13px; margin: 5px 0; }
    
    /* أزرار التنقل */
    .stButton>button {
        background-color: #3B82F6 !important; color: white !important;
        border-radius: 10px !important; font-weight: bold !important; width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات من Google Sheets
@st.cache_data(ttl=60)
def load_sheet_data(url):
    try:
        # تحويل رابط pubhtml إلى رابط تحميل CSV مباشر
        csv_url = url.replace('/pubhtml', '/export?format=csv')
        df = pd.read_csv(csv_url).fillna("غير متوفر").astype(str)
        return df
    except:
        return pd.DataFrame()

# روابط الشيتات الخاصة بك
sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pubhtml"

df_data = load_sheet_data(sheet_url)

# 4. بناء الواجهة الرئيسية
st.markdown("""
    <div class="main-header">
        <h1 style="margin:0; font-size:35px;">BrokerEdge PRO</h1>
        <p style="color:white; margin:0; opacity:0.8;">المنصة المتكاملة لإدارة المشاريع والمطورين</p>
    </div>
""", unsafe_allow_html=True)

# قائمة الاختيارات العلويّة
menu = option_menu(None, ["المشاريع", "المطورين", "الأدوات", "خروج"], 
    icons=["building", "person-badge", "tools", "door-open"], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "white", "padding": "10px", "border-radius": "15px", "border": "1px solid #E2E8F0"},
        "nav-link-selected": {"background-color": "#1E293B", "color": "#F59E0B"}
    }
)

if menu == "خروج":
    st.session_state.auth = False
    st.warning("تم تسجيل الخروج. يرجى إعادة تحميل الصفحة.")
    st.stop()

# 5. محرك البحث والترقيم (Pagination)
search_q = st.text_input("", placeholder="🔍 ابحث في كامل البيانات (اسم المشروع، المطور، المنطقة)...", label_visibility="collapsed")

# تصفية البيانات بناءً على البحث
dff = df_data.copy()
if search_q:
    dff = dff[dff.apply(lambda r: r.astype(str).str.contains(search_q, case=False).any(), axis=1)]
    st.session_state.page_num = 0

# إعداد الترقيم (6 عناصر في الصفحة)
limit = 6
total_pages = (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0)
start_idx = st.session_state.page_num * limit
end_idx = start_idx + limit
current_items = dff.iloc[start_idx:end_idx]

# 6. عرض المحتوى بناءً على القائمة
if menu in ["المشاريع", "المطورين"]:
    st.markdown(f"<h3>قائمة {menu} ({len(dff)} عنصر)</h3>", unsafe_allow_html=True)
    
    # توزيع العناصر في شبكة (Grid)
    cols = st.columns(2) # عمودين في كل صف
    for i, (idx, row) in enumerate(current_items.iterrows()):
        with cols[i % 2]:
            # تخصيص عرض الكارت بناءً على المنيو (مشروع أو مطور)
            title = row.get('Project Name') if 'Project Name' in row else row.iloc[0]
            subtitle = row.get('Area') if 'Area' in row else "معلومات إضافية"
            extra = row.get('Developer') if 'Developer' in row else "التصنيف"

            st.markdown(f"""
                <div class="grid-card">
                    <div class="card-title">{title}</div>
                    <div class="card-loc">📍 {subtitle}</div>
                    <div class="card-detail">🏢 المطور: <b>{extra}</b></div>
                    <div style="background:#F8FAFC; padding:10px; border-radius:10px; font-size:12px; margin-top:10px; border:1px solid #F1F5F9;">
                        {row.iloc[3] if len(row)>3 else ""}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("شاهد التفاصيل الكاملة للزتونة"):
                st.table(row) # عرض كل بيانات السطر عند الضغط

    # أزرار التالي والسابق
    st.write("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.session_state.page_num > 0:
            if st.button("⬅️ السابق"):
                st.session_state.page_num -= 1
                st.rerun()
    with c2:
        st.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.page_num + 1} من {total_pages}</p>", unsafe_allow_html=True)
    with c3:
        if end_idx < len(dff):
            if st.button("التالي ➡️"):
                st.session_state.page_num += 1
                st.rerun()

elif menu == "الأدوات":
    st.markdown("<div style='background:white; padding:40px; border-radius:20px; box-shadow:0 4px 6px rgba(0,0,0,0.05);'>", unsafe_allow_html=True)
    st.title("🧮 حاسبة البروكر الذكية")
    
    col_a, col_b = st.columns(2)
    with col_a:
        price = st.number_input("سعر الوحدة الإجمالي", value=5000000, step=100000)
        down_payment_pct = st.slider("المقدم (%)", 0, 50, 10)
    with col_b:
        years = st.slider("عدد سنوات التقسيط", 1, 15, 8)
        
    dp_amount = price * (down_payment_pct / 100)
    remaining = price - dp_amount
    monthly = remaining / (years * 12)
    
    st.markdown("---")
    res_1, res_2 = st.columns(2)
    res_1.metric("قيمة المقدم (ج.م)", f"{dp_amount:,.0f}")
    res_2.metric("القسط الشهري (ج.م)", f"{monthly:,.0f}")
    
    st.markdown("</div>", unsafe_allow_html=True)
