import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="BrokerEdge Pro", layout="wide")

# إدارة الحالة
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# 2. التنسيق الجمالي (CSS) - ألوان صارخة وواضحة جداً
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; direction: rtl; text-align: right; background-color: #F8FAFC; }
    
    /* الهيدر */
    .main-header {
        background: #0F172A; color: #F59E0B; padding: 25px; text-align: center;
        border-bottom: 5px solid #F59E0B; border-radius: 0 0 20px 20px; margin-bottom: 20px;
    }

    /* الكروت الشبكية */
    .grid-card {
        background: white; border-radius: 15px; border: 2px solid #CBD5E1;
        padding: 20px; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        min-height: 200px;
    }
    .card-title { color: #1E3A8A; font-size: 22px; font-weight: 900; }
    .card-price { color: #EF4444; font-size: 18px; font-weight: bold; }
    
    /* أزرار التنقل */
    .stButton>button {
        background-color: #F59E0B !important; color: #0F172A !important;
        font-weight: 900 !important; border-radius: 10px !important; height: 50px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب البيانات (مع معالجة الأخطاء)
def load_data():
    # الرابط الذي أرسلته مع تحويله لصيغة البرمجة (CSV)
    raw_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(raw_url).fillna("غير متوفر")
        return df
    except:
        # بيانات احتياطية في حال فشل الرابط لتجربة الكود
        data = {
            'Project Name': ['مشروع تجريبي 1', 'مشروع تجريبي 2', 'مشروع تجريبي 3'],
            'Area': ['التجمع الخامس', 'الشيخ زايد', 'العاصمة الإدارية'],
            'Developer': ['مطور 1', 'مطور 2', 'مطور 3'],
            'Price': ['5,000,000', '4,200,000', '7,500,000']
        }
        return pd.DataFrame(data)

df = load_data()

# 4. الهيدر
st.markdown('<div class="main-header"><h1>BrokerEdge PRO 2026</h1></div>', unsafe_allow_html=True)

# 5. المنيو الرئيسي
menu = option_menu(None, ["المشاريع", "المطورين", "الأدوات", "خروج"], 
    icons=["building", "person-badge", "tools", "door-open"], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "white", "border": "2px solid #CBD5E1"},
        "nav-link-selected": {"background-color": "#0F172A", "color": "#F59E0B"}
    }
)

# ----------------- قائمة الخروج -----------------
if menu == "خروج":
    st.info("تم تسجيل الخروج بنجاح. أغلق المتصفح للخصوصية.")
    st.stop()

# ----------------- قائمة الأدوات -----------------
elif menu == "الأدوات":
    st.markdown("<div style='background:white; padding:30px; border-radius:15px; border:2px solid #CBD5E1;'>", unsafe_allow_html=True)
    st.header("🧮 حاسبة الأقساط")
    price = st.number_input("سعر الوحدة", value=5000000)
    years = st.slider("سنوات التقسيط", 1, 15, 8)
    monthly = price / (years * 12)
    st.metric("القسط الشهري التقريبي", f"{monthly:,.0f} ج.م")
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- قائمة المشاريع والمطورين -----------------
else:
    # محرك البحث
    q = st.text_input("", placeholder="🔍 ابحث هنا عن أي شيء...")
    
    dff = df.copy()
    if q:
        dff = dff[dff.apply(lambda r: r.astype(str).str.contains(q, case=False).any(), axis=1)]

    # نظام الترتيب (6 في الصفحة)
    limit = 6
    total_pages = max(1, (len(dff) // limit) + (1 if len(dff) % limit > 0 else 0))
    start_idx = st.session_state.page_num * limit
    current_items = dff.iloc[start_idx : start_idx + limit]

    # العرض الشبكي (2 في كل صف)
    cols = st.columns(2)
    for i, (idx, row) in enumerate(current_items.iterrows()):
        with cols[i % 2]:
            st.markdown(f"""
                <div class="grid-card">
                    <div class="card-title">{row.iloc[0]}</div>
                    <div style="color:#64748B;">📍 {row.iloc[1] if len(row)>1 else ""}</div>
                    <div style="margin-top:10px;">🏢 المطور: <b>{row.iloc[2] if len(row)>2 else ""}</b></div>
                    <hr>
                    <div class="card-price">السعر: {row.iloc[3] if len(row)>3 else "اتصل بنا"}</div>
                </div>
            """, unsafe_allow_html=True)
            with st.expander("كل البيانات"):
                st.write(row)

    # أزرار التنقل
    st.write("---")
    c1, c2, c3 = st.columns([1, 2, 1])
    with c1:
        if st.session_state.page_num > 0:
            if st.button("⬅️ السابق"):
                st.session_state.page_num -= 1
                st.rerun()
    with c2:
        st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page_num + 1} من {total_pages}</p>", unsafe_allow_html=True)
    with c3:
        if (start_idx + limit) < len(dff):
            if st.button("التالي ➡️"):
                st.session_state.page_num += 1
                st.rerun()
