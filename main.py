import streamlit as st
import pandas as pd
import math
from streamlit_option_menu import option_menu 

# 1. إعدادات الصفحة وتصميم الواجهة والخطوط
st.set_page_config(page_title="منصة البروكر الذكية", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        direction: RTL;
        text-align: right;
    }

    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    [data-testid="stAppViewContainer"] {
        background-color: #050505;
    }

    /* تصميم كروت الشبكة */
    .grid-card {
        background: rgba(20, 20, 20, 0.9);
        border: 1px solid #333;
        border-top: 4px solid #f59e0b;
        border-radius: 15px;
        padding: 20px;
        margin-bottom: 20px;
        height: 380px;
        transition: 0.3s;
        color: white;
        display: flex;
        flex-direction: column;
    }
    .grid-card:hover {
        transform: translateY(-5px);
        border-color: #f59e0b;
        box-shadow: 0 10px 20px rgba(245, 158, 11, 0.1);
    }
    
    .card-title { color: #f59e0b; font-size: 20px; font-weight: 900; margin-bottom: 5px; }
    .card-subtitle { color: #ccc; font-size: 14px; margin-bottom: 15px; border-bottom: 1px solid #222; padding-bottom: 8px; }
    
    .stat-line { display: flex; justify-content: space-between; margin-bottom: 8px; font-size: 14px; }
    .stat-label { color: #888; }
    .stat-value { color: #fff; font-weight: 600; }

    .badge {
        background: #f59e0b;
        color: black;
        padding: 2px 10px;
        border-radius: 5px;
        font-weight: 700;
        font-size: 13px;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* تحسين شكل الأزرار */
    .stButton button {
        width: 100%;
        background-color: #111 !important;
        color: #f59e0b !important;
        border: 1px solid #f59e0b !important;
        border-radius: 8px !important;
        font-weight: 700 !important;
    }
    .stButton button:hover {
        background-color: #f59e0b !important;
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. وظيفة جلب وتنظيف البيانات
@st.cache_data(ttl=60)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        # تنظيف أسماء الأعمدة من أي مسافات مخفية
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except Exception as e:
        st.error(f"حدث خطأ في الاتصال بالشيت: {e}")
        return pd.DataFrame()

df = load_data()

# 3. القائمة الرئيسية
selected = option_menu(
    menu_title=None,
    options=["أدوات العمل", "قائمة المشاريع", "سجل المطورين"],
    icons=["tools", "building", "person-vcard"],
    default_index=2,
    orientation="horizontal",
    styles={
        "container": {"background-color": "#000", "padding": "5px"},
        "nav-link": {"font-size": "16px", "color": "#888", "font-weight": "600"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black"},
    }
)

# --- صفحة سجل المطورين (المعدلة لتجنب الـ KeyError) ---
if selected == "سجل المطورين":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🏢 سجل كبار المطورين العقاريين</h2>", unsafe_allow_html=True)
    
    if not df.empty:
        # فحص وجود الأعمدة المطلوبة
        req = ['Developer', 'Owner', 'Detailed_Info']
        available_cols = list(df.columns)
        
        if all(col in available_cols for col in req):
            # استخراج المطورين بدون تكرار
            devs = df[req].drop_duplicates(subset=['Developer']).reset_index(drop=True)
            
            search = st.text_input("🔍 ابحث عن اسم المطور...")
            if search:
                devs = devs[devs['Developer'].str.contains(search, case=False, na=False)]
            
            # نظام الصفحات
            items_per_page = 9
            total_pages = max(1, math.ceil(len(devs) / items_per_page))
            if 'p_dev' not in st.session_state: st.session_state.p_dev = 1
            
            start_idx = (st.session_state.p_dev - 1) * items_per_page
            curr_devs = devs.iloc[start_idx : start_idx + items_per_page]
            
            # عرض الشبكة (3 كروت في الصف)
            for i in range(0, len(curr_devs), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(curr_devs):
                        row = curr_devs.iloc[i + j]
                        with cols[j]:
                            st.markdown(f"""
                                <div class="grid-card">
                                    <div class="card-title">🏢 {row['Developer']}</div>
                                    <div class="card-subtitle">👤 المالك: {row['Owner']}</div>
                                    <div style="font-size:14px; color:#aaa; line-height:1.6; flex-grow:1; overflow:hidden;">
                                        <b>نبذة الشركة:</b><br>
                                        {str(row['Detailed_Info'])[:150]}...
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            with st.expander("📄 سابقة الأعمال الكاملة"):
                                st.write(row['Detailed_Info'])
            
            # أزرار التنقل
            st.write("---")
            c1, c2, c3 = st.columns([1, 2, 1])
            with c1:
                if st.session_state.p_dev > 1:
                    if st.button("⬅️ السابق"): st.session_state.p_dev -= 1; st.rerun()
            with c2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.p_dev} من {total_pages}</p>", unsafe_allow_html=True)
            with c3:
                if st.session_state.p_dev < total_pages:
                    if st.button("التالي ➡️"): st.session_state.p_dev += 1; st.rerun()
        else:
            st.warning("⚠️ لم يتم العثور على الأعمدة المطلوبة في الشيت.")
            st.info(f"الأعمدة الحالية هي: {available_cols}")
            st.write("يرجى التأكد من تسمية الأعمدة في جوجل شيت بـ: Developer, Owner, Detailed_Info")

# --- (يمكنك هنا إضافة كود صفحة المشاريع وأدوات العمل بنفس النمط) ---
