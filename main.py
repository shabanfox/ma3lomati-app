import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS الملكي (أزرار متساوية الأبعاد 100%)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .main-header {
        background: #000; color: #f59e0b; padding: 15px; text-align: center;
        border-bottom: 6px solid #f59e0b; font-weight: 900; font-size: 2rem; margin-bottom: 30px;
    }

    /* تثبيت أحجام الأزرار الرئيسية في الهوم */
    .home-btn button {
        height: 200px !important; width: 100% !important;
        font-size: 2rem !important; border-radius: 0px !important;
        border: 6px solid #000 !important; box-shadow: 12px 12px 0px #f59e0b !important;
        font-weight: 900 !important;
    }

    /* السحر هنا: توحيد مقاس أزرار الشبكة 3x3 */
    div.stButton > button {
        width: 100% !important; 
        height: 100px !important; /* طول ثابت لكل الأزرار */
        background-color: #ffffff !important; 
        color: #000 !important;
        border: 4px solid #000 !important; 
        border-radius: 0px !important;
        box-shadow: 5px 5px 0px #000 !important; 
        transition: 0.1s;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        overflow: hidden !important; /* منع النص من تغيير حجم الزر */
        text-overflow: ellipsis !important;
    }
    
    div.stButton > button:hover { 
        background-color: #f59e0b !important; 
        transform: translate(2px, 2px); 
        box-shadow: 2px 2px 0px #000 !important;
    }

    div.stButton > button p { 
        font-weight: 900 !important; 
        font-size: 0.95rem !important; 
        white-space: normal !important; /* السماح بالنزول لسطر جديد */
        text-align: center !important;
    }

    /* تنسيق الحاسبة */
    .calc-card {
        background: #000; color: #f59e0b; padding: 25px; border: 4px solid #f59e0b;
        text-align: center; font-weight: 900; font-size: 1.8rem;
    }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'view' not in st.session_state: st.session_state.view = 'home'
if 'page' not in st.session_state: st.session_state.page = 0
df = load_data()

# --- محتوى المنصة ---

# أ. الصفحة الرئيسية
if st.session_state.view == 'home':
    st.markdown('<div class="main-header">🏠 منصة معلوماتى العقارية</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:80px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🏢\nدليل الشركات"): st.session_state.view = 'companies'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="home-btn">', unsafe_allow_html=True)
        if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ب. صفحة الشركات (الشبكة المنتظمة)
elif st.session_state.view == 'companies':
    st.markdown('<div class="main-header">🏢 دليل المشاريع العقارية</div>', unsafe_allow_html=True)
    if st.button("🔙 العودة للقائمة الرئيسية"): st.session_state.view = 'home'; st.rerun()

    q = st.text_input("🔍 ابحث عن (مشروع، مطور، موقع)...")
    df_f = df
    if q:
        df_f = df[df.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]

    st.markdown("---")
    
    # 60% يمين للشبكة و 40% يسار فارغ
    col_grid, col_empty = st.columns([0.6, 0.4])

    with col_grid:
        items_per_page = 9
        start_idx = st.session_state.page * items_per_page
        current_data = df_f.iloc[start_idx : start_idx + items_per_page]

        # الشبكة 3x3 متساوية تماماً
        for i in range(0, len(current_data), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(current_data):
                    row = current_data.iloc[i + j]
                    with cols[j]:
                        # عرض اسم المشروع والمطور بشكل موحد
                        btn_label = f"{row.iloc[0]}\n{row.iloc[2]}"
                        if st.button(btn_label, key=f"grid_{start_idx+i+j}"):
                            st.sidebar.markdown(f"### 📍 {row.iloc[0]}")
                            st.sidebar.info(f"**المطور:** {row.iloc[2]}\n\n**الموقع:** {row.iloc[3]}\n\n**السداد:** {row.iloc[4]}")

        # أزرار التنقل (السابق / التالي)
        st.write("")
        nav1, nav2, nav3 = st.columns([1, 1, 1])
        if nav1.button("⬅️ السابق") and st.session_state.page > 0:
            st.session_state.page -= 1; st.rerun()
        nav2.markdown(f"<p style='text-align:center; font-weight:bold;'>صفحة {st.session_state.page + 1}</p>", unsafe_allow_html=True)
        if nav3.button("التالي ➡️") and (start_idx + items_per_page) < len(df_f):
            st.session_state.page += 1; st.rerun()

# ج. صفحة الأدوات
elif st.session_state.view == 'tools':
    st.markdown('<div class="main-header">🛠️ أدوات البروكر المستثمر</div>', unsafe_allow_html=True)
    if st.button("🔙 عودة"): st.session_state.view = 'home'; st.rerun()
    
    t1, t2 = st.tabs(["💰 حاسبة القسط", "📈 العائد ROI"])
    with t1:
        pr = st.number_input("سعر الوحدة", value=2000000)
        yr = st.slider("سنوات التقسيط", 1, 15, 8)
        st.markdown(f'<div class="calc-card">القسط: {pr/(yr*12):,.0f} ج.م</div>', unsafe_allow_html=True)
    with t2:
        buy = st.number_input("تكلفة الشراء", value=1000000)
        rent = st.number_input("الإيجار السنوي", value=100000)
        st.markdown(f'<div class="calc-card">العائد: {(rent/buy)*100:.1f}%</div>', unsafe_allow_html=True)
