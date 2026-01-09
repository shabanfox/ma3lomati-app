import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. تصميم CSS (الفخامة والوضوح)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #ffffff; 
    }

    /* العنوان الرئيسي */
    .header-box { 
        background: #000; color: #f59e0b; padding: 20px; border-radius: 20px; 
        text-align: center; margin-bottom: 30px; border-bottom: 8px solid #f59e0b;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    /* أزرار الصفحة الرئيسية - فخامة سوداء */
    .stButton > button {
        width: 100% !important; height: 110px !important;
        background-color: #000 !important; color: #fff !important;
        border: 2px solid #f59e0b !important; border-radius: 20px !important;
        font-size: 1.6rem !important; font-weight: 900 !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.2) !important;
        transition: 0.3s all ease;
    }
    .stButton > button:hover { transform: translateY(-5px); border-color: #fff !important; }

    /* كروت المشاريع المجهرية (Micro-Cards) */
    .micro-card {
        background: #ffffff; border: 3px solid #000; padding: 12px; 
        border-radius: 15px; margin-bottom: 10px; box-shadow: 6px 6px 0px #000;
        height: 150px; display: flex; flex-direction: column; justify-content: space-between;
        transition: 0.2s;
    }
    .micro-card:hover { transform: scale(1.02); box-shadow: 10px 10px 0px #f59e0b; border-color: #f59e0b; }
    .m-title { font-size: 1.1rem; font-weight: 900; color: #000; line-height: 1.1; }
    .m-dev { color: #f59e0b; font-weight: 700; font-size: 0.85rem; }
    .m-tag { 
        font-weight: 900; font-size: 0.85rem; background: #000; color: #fff;
        padding: 4px; text-align: center; border-radius: 6px;
    }

    /* لوحة الإضافة الجانبية */
    .side-panel { background: #fdfdfd; border: 3px solid #000; padding: 15px; border-radius: 15px; }

    /* الحاسبة الاحترافية */
    .calc-card { background: #000; color: #fff; padding: 25px; border-radius: 25px; border: 4px solid #f59e0b; text-align: center; }
    .val-huge { font-size: 2.8rem; font-weight: 900; color: #f59e0b !important; }
    </style>
""", unsafe_allow_html=True)

# 3. جلب البيانات
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url); df.columns = [c.strip() for c in df.columns]
        return df
    except: return pd.DataFrame(columns=['المشروع','نوعه','المطور','الموقع','السداد'])

if 'data' not in st.session_state: st.session_state.data = load_data()
if 'view' not in st.session_state: st.session_state.view = 'main'

# --- المحتوى ---
if st.session_state.view == 'main':
    st.markdown('<div class="header-box"><h1>🏠 منصة معلوماتى</h1></div>', unsafe_allow_html=True)
    st.markdown("<div style='height:50px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2, gap="large")
    with c1:
        if st.button("🏢 دليل المشاريع"): st.session_state.view = 'comp'; st.rerun()
    with c2:
        if st.button("🛠️ أدوات البروكر"): st.session_state.view = 'tools'; st.rerun()

elif st.session_state.view == 'comp':
    st.markdown('<div class="header-box"><h2>🔍 المشاريع والإدارة الذكية</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()

    # توزيع الصفحة: 75% مشاريع ، 25% إضافة
    col_grid, col_form = st.columns([0.75, 0.25], gap="medium")

    with col_grid:
        q = st.text_input("🔍 ابحث عن أي تفاصيل...", placeholder="المطور، الموقع، أو المشروع")
        df_f = st.session_state.data
        if q: df_f = df_f[df_f.apply(lambda r: q.lower() in r.astype(str).str.lower().values, axis=1)]
        
        # شبكة المشاريع
        for i in range(0, len(df_f.head(21)), 3):
            cols = st.columns(3)
            for j in range(3):
                if i + j < len(df_f):
                    row = df_f.iloc[i + j]
                    with cols[j]:
                        st.markdown(f"""
                        <div class="micro-card">
                            <div>
                                <div class="m-title">{row[0]}</div>
                                <div class="m-dev">🏢 {row[2]}</div>
                                <div style="font-size:0.7rem; color:#666; margin-top:3px;">📍 {row[3]}</div>
                            </div>
                            <div class="m-tag">{row[4]}</div>
                        </div>
                        """, unsafe_allow_html=True)

    with col_form:
        st.markdown('<div class="side-panel">', unsafe_allow_html=True)
        st.markdown("### ➕ إضافة سريعة")
        with st.form("add_p", clear_on_submit=True):
            n = st.text_input("اسم المشروع")
            d = st.text_input("المطور")
            l = st.text_input("الموقع")
            p = st.text_input("نظام السداد")
            if st.form_submit_button("إضافة للمجموعة"):
                if n:
                    new_r = pd.DataFrame([[n, "", d, l, p]], columns=st.session_state.data.columns)
                    st.session_state.data = pd.concat([new_r, st.session_state.data], ignore_index=True)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

elif st.session_state.view == 'tools':
    st.markdown('<div class="header-box"><h2>🛠️ حاسبات الاستثمار العقاري</h2></div>', unsafe_allow_html=True)
    if st.button("🔙 عودة للرئيسية"): st.session_state.view = 'main'; st.rerun()
    
    tab1, tab2 = st.tabs(["💰 حساب القسط", "📈 عائد ROI"])
    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1: price = st.number_input("السعر الإجمالي", value=2000000)
        with c2: down = st.number_input("المقدم (%)", value=10)
        with c3: years = st.number_input("السنوات", value=8)
        dv = price * (down/100); mv = (price - dv) / (years * 12) if years > 0 else 0
        st.markdown(f'<div class="calc-card"><span class="val-huge">{dv:,.0f} ج.م</span><br>المقدم المطلوب<hr><span class="val-huge" style="color:#22c55e !important;">{mv:,.0f} ج.م</span><br>القسط الشهري</div>', unsafe_allow_html=True)
