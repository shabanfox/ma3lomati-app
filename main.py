import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .project-card {
        background: white; border-radius: 12px; padding: 20px;
        border-right: 8px solid #003366; margin-bottom: 15px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات وتحويل الرابط
@st.cache_data
def load_data():
    # الرابط الخاص بك (تم التأكد من تحويله لـ CSV)
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        # مسح المسافات من أسماء الأعمدة
        df.columns = [c.strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"خطأ في الاتصال بالشيت: {e}")
        return None

df = load_data()

if df is not None:
    # لتجنب KeyError، سنقوم بتعريف المتغيرات بناءً على ترتيب الأعمدة في الشيت بتاعك
    # الترتيب في شيت حضرتك: 0:Developer, 1:Owner, 2:Project, 3:Area, 4:Price, 5:Min_Val, 6:Description... إلخ
    cols = df.columns.tolist()

    # إدارة التنقل
    if 'page' not in st.session_state: st.session_state.page = 'main'

    # --- الصفحة الرئيسية ---
    if st.session_state.page == 'main':
        st.markdown("<h1 style='text-align:center; color:#003366;'>منصة معلوماتى العقارية</h1>", unsafe_allow_html=True)
        
        # فلاتر البحث
        c1, c2, c3 = st.columns(3)
        with c1:
            s_area = st.selectbox("📍 المنطقة", ["الكل"] + sorted(df.iloc[:, 3].dropna().unique().tolist()))
        with c2:
            s_dev = st.text_input("🏢 اسم المطور")
        with c3:
            s_type = st.selectbox("🏠 النوع", ["الكل"] + sorted(df.iloc[:, 7].dropna().unique().tolist()))

        # تطبيق الفلترة
        f_df = df.copy()
        if s_area != "الكل": f_df = f_df[f_df.iloc[:, 3] == s_area]
        if s_type != "الكل": f_df = f_df[f_df.iloc[:, 7] == s_type]
        if s_dev: f_df = f_df[f_df.iloc[:, 0].str.contains(s_dev, na=False, case=False)]

        # عرض النتائج
        grid = st.columns(2)
        for idx, (i, row) in enumerate(f_df.iterrows()):
            with grid[idx % 2]:
                # هنا بنستخدم رقم العمود بدل اسمه عشان نتفادى الـ KeyError
                p_name = row[2]  # عمود Project
                d_name = row[0]  # عمود Developer
                price = row[4]   # عمود Price
                area = row[3]    # عمود Area
                
                st.markdown(f"""
                    <div class="project-card">
                        <h3 style="margin:0; color:#003366;">{p_name}</h3>
                        <p style="color:#64748b; margin-bottom:10px;">المطور: {d_name}</p>
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:#16a34a; font-weight:bold;">{price}</span>
                            <span>📍 {area}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"التفاصيل والزتونة لـ {p_name}", key=f"btn_{i}", use_container_width=True):
                    st.session_state.selected_item = row.to_list() # حفظ كقائمة
                    st.session_state.page = 'details'
                    st.rerun()

    # --- صفحة التفاصيل ---
    elif st.session_state.page == 'details':
        item = st.session_state.selected_item
        if st.button("🔙 عودة"):
            st.session_state.page = 'main'
            st.rerun()

        # عرض البيانات بناءً على ترتيبها في القائمة
        st.markdown(f"""
            <div style="background:white; padding:25px; border-radius:15px; border-right:10px solid #003366;">
                <h1 style="color:#003366;">{item[2]}</h1> <h3>المطور: {item[0]} | المالك: {item[1]}</h3>
            </div>
        """, unsafe_allow_html=True)

        t1, t2 = st.tabs(["💡 الزتونة والمعلومات", "🏗️ مشاريع المطور"])
        with t1:
            st.info(f"**الزتونة الفنية:** {item[11]}") # Detailed_Info
            st.success(f"**السعر:** {item[4]} | **المقدم:** {item[10]} | **التقسيط:** {item[9]} سنوات")
            st.write(f"**الوصف:** {item[6]}")
            st.warning(f"**الاستلام:** {item[8]}")
            
        with t2:
            st.subheader(f"مشاريع أخرى لـ {item[0]}")
            others = df[df.iloc[:, 0] == item[0]]
            for _, p in others.iterrows():
                st.write(f"- {p[2]} ({p[3]})")
