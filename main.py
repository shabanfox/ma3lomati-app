import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى", layout="wide")

# 2. تصميم CSS (تثبيت الهوية والشبكة والجانب الأيسر)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    /* جعل القائمة الجانبية تظهر في اليسار */
    [data-testid="stSidebar"] {
        direction: RTL;
        background-color: #f8f9fa;
        border-right: none;
        border-left: 5px solid #000;
    }
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    .hero-header { 
        background: #000000; color: #FFD700; padding: 20px; border-radius: 15px; 
        text-align: center; margin-bottom: 30px; border: 4px solid #FFD700;
    }

    /* الأزرار الرئيسية */
    div.stButton > button {
        width: 100% !important; height: 90px !important;
        background-color: #ffffff !important; color: #000 !important;
        border: 5px solid #000 !important; border-radius: 15px !important;
        font-size: 1.5rem !important; font-weight: 900 !important;
        box-shadow: 7px 7px 0px 0px #000 !important; transition: 0.1s;
    }
    div.stButton > button:active { transform: translate(4px, 4px); box-shadow: 0px 0px 0px 0px !important; }

    /* كروت الشبكة 3x3 */
    .project-card {
        background: #ffffff; border: 3px solid #000000; padding: 15px; 
        border-radius: 15px; margin-bottom: 20px; box-shadow: 6px 6px 0px #000;
        height: 250px; display: flex; flex-direction: column; justify-content: space-between;
    }
    .p-title { font-size: 1.4rem; font-weight: 900; color: #000; }
    .p-dev { color: #2563eb; font-weight: 700; font-size: 1rem; }
    .p-tag { 
        font-weight: 900; font-size: 1.2rem; background: #FFD700; 
        padding: 5px; border: 2px solid #000; text-align: center; border-radius: 8px;
    }

    /* صناديق النتائج */
    .res-card { background: #000; color: #fff; padding: 20px; border-radius: 20px; border: 3px solid #FFD700; text-align: center; }
    .res-v { font-size: 2.2rem; font-weight: 900; color: #FFD700 !important; }

    /* المدخلات */
    label { font-weight: 900 !important; color: #000 !important; }
    input { border: 3px solid #000 !important; font-weight: 900 !important; border-radius: 10px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return None

if 'data' not in st.session_state:
    st.session_state.data = load_data()

if 'view' not in st.session_state: st.session_state.view = 'main'

# --- القائمة الجانبية (إضافة مشاريع) ---
with st.sidebar:
    st.markdown("### ➕ إضافة مشروع جديد")
    with st.form("add_form", clear_on_submit=True):
        new_name = st.text_input("اسم المشروع")
        new_dev = st.text_input("المطور")
        new_loc = st.text_input("الموقع")
        new_price = st.text_input("السعر / طريقة السداد")
        submit = st.form_submit_button("حفظ المشروع")
        if submit:
            new_row = pd.DataFrame([[new_name, "", new_dev, new_loc, new_price]], columns=st.session_state.data.columns)
            st.session_state.data = pd.concat([new_row, st.session_state.data], ignore_index=True)
            st.success("تمت الإضافة بنجاح!")

# --- المحتوى الرئيسي ---
if st.session_state.data is not None:
    if st.session_state.view == 'main':
        st.markdown('<div class="hero-header"><h1>🏠 منصة معلوماتى العقارية</h1></div>', unsafe_allow_html=True)
        _, col_mid, _ = st.columns([0.05, 0.9, 0.05])
        with col_mid:
            c1, c2 = st.columns(2, gap="large")
            with c1:
                if st.button("🏢\nدليل المشاريع"): st.session_state.view = 'comp'; st.rerun()
            with c2:
                if st.button("🛠️\nأدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

    elif st.session_state.view == 'comp':
        st.markdown('<div class="hero-header"><h2>🔍 دليل المشاريع (3×3)</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة"): st.session_state.view = 'main'; st.rerun()
        
        # الفلاتر والبحث
        f1, f2 = st.columns([2, 1])
        with f1: q = st.text_input("🔍 ابحث عن مشروع أو مطور...", placeholder="اكتب هنا...")
        with f2: dev_filter = st.selectbox("🎯 تصفية بالمطور", ["الكل"] + list(st.session_state.data.iloc[:, 2].unique()))
        
        # تطبيق الفلترة
        df_f = st.session_state.data
        if q: df_f = df_f[df_f.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]
        if dev_filter != "الكل": df_f = df_f[df_f.iloc[:, 2] == dev_filter]

        st.markdown("---")
        
        # شبكة 3x3
        for i in range(0, len(df_f.head(18)), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(df_f):
                    row = df_f.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="project-card">
                            <div>
                                <div class="p-title">{row[0]}</div>
                                <div class="p-dev">🏢 {row[2]}</div>
                                <div style="font-size:0.9rem; color:#666; margin-top:5px;">📍 {row[3]}</div>
                            </div>
                            <div class="p-tag">{row[4]}</div>
                        </div>
                        """, unsafe_allow_html=True)

    elif st.session_state.view == 'tools':
        st.markdown('<div class="hero-header"><h2>🛠️ أدوات البروكر</h2></div>', unsafe_allow_html=True)
        if st.button("🔙 عودة"): st.session_state.view = 'main'; st.rerun()
        
        t1, t2 = st.tabs(["💰 الأقساط", "📈 الاستثمار ROI"])
        with t1:
            # حاسبة الأقساط
            c1, c2, c3 = st.columns(3)
            with c1: pr = st.number_input("السعر", value=2000000)
            with c2: dn = st.number_input("المقدم %", value=10)
            with c3: yr = st.number_input("السنين", value=8)
            dv = pr * (dn/100); mv = (pr - dv) / (yr * 12) if yr > 0 else 0
            st.markdown(f'<div class="res-card"><span class="res-v">{dv:,.0f} ج.م</span><br>المقدم<hr><span class="res-v" style="color:#22c55e !important;">{mv:,.0f} ج.م</span><br>القسط</div>', unsafe_allow_html=True)
        
        with t2:
            # حاسبة ROI
            r1, r2, r3 = st.columns(3)
            with r1: bp = st.number_input("شراء", value=2000000)
            with r2: sp = st.number_input("بيع", value=3500000)
            with r3: rt = st.number_input("إيجار", value=15000)
            prof = sp - bp; roi = (prof/bp)*100 if bp > 0 else 0
            st.markdown(f'<div class="res-card"><span class="res-v">{prof:,.0f} ج.م</span><br>الربح<hr><span class="res-v" style="color:#FFD700 !important;">%{roi:.1f}</span><br>العائد</div>', unsafe_allow_html=True)
