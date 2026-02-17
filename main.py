import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة حالة الجلسة (Session State) ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth, st.session_state.current_user = True, st.query_params["u_session"]
    else: st.session_state.auth = False

if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0

# --- 3. الروابط والثوابت ---
URL_PROJECTS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
URL_DEVELOPERS = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"

BG_IMG = "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=2070&auto=format&fit=crop"
GOLD_COLOR = "#D4AF37"
DARK_GLASS = "rgba(15, 15, 15, 0.85)"

# --- 4. وظيفة تحميل وتنسيق البيانات ---
@st.cache_data(ttl=60)
def load_data():
    try:
        p = pd.read_csv(URL_PROJECTS)
        d = pd.read_csv(URL_DEVELOPERS)
        l = pd.read_csv(URL_LAUNCHES)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'السعر': 'Price'}, inplace=True, errors="ignore")
            # ترتيب أبجدي تلقائي بناءً على أول عمود
            df.sort_values(by=df.columns[0], inplace=True)
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 5. التصميم العصري (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    * {{ font-family: 'Cairo', sans-serif; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl; text-align: right;
    }}
    header {{ visibility: hidden; }}
    
    /* هيدر الصفحة */
    .main-header {{
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 30px; border-radius: 0 0 40px 40px;
        border-bottom: 2px solid {GOLD_COLOR};
        text-align: center; margin-bottom: 20px;
    }}
    
    /* الكروت الزجاجية */
    .glass-card {{
        background: {DARK_GLASS};
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 20px; padding: 20px;
        transition: 0.4s; margin-bottom: 15px;
    }}
    .glass-card:hover {{ border: 1px solid {GOLD_COLOR}; transform: translateY(-3px); }}

    /* تخصيص الأزرار */
    div.stButton > button {{
        background: rgba(0,0,0,0.6) !important;
        color: {GOLD_COLOR} !important;
        border: 1px solid {GOLD_COLOR} !important;
        border-radius: 12px !important;
        font-weight: 700 !important;
        width: 100%;
    }}
    div.stButton > button:hover {{
        background: {GOLD_COLOR} !important;
        color: black !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 6. بوابة الدخول ---
if not st.session_state.get('auth', False):
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, col_m, _ = st.columns([1, 1.2, 1])
    with col_m:
        st.markdown(f"<div class='glass-card' style='text-align:center;'><h1 style='color:{GOLD_COLOR}'>MA3LOMATI PRO</h1><p>ادخل كلمة السر للوصول للنظام</p></div>", unsafe_allow_html=True)
        pwd = st.text_input("Password", type="password", placeholder="أدخل كلمة السر")
        if st.button("دخول"):
            if pwd == "2026": # يمكنك استبدالها بدالة login_user الأصلية
                st.session_state.auth, st.session_state.current_user = True, "shaban"
                st.rerun()
            else: st.error("خطأ في البيانات")
    st.stop()

# --- 7. التحميل والعرض الرئيسي ---
df_p, df_d, df_l = load_data()

st.markdown(f"""
    <div class="main-header">
        <h1 style="color:{GOLD_COLOR}; margin:0;">MA3LOMATI PRO</h1>
        <p style="color:#888;">مرحباً بك، {st.session_state.current_user} | الاستبصار العقاري 2026</p>
    </div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "cpu"], 
    default_index=2, orientation="horizontal",
    styles={
        "container": {"background-color": "transparent", "border": f"1px solid {GOLD_COLOR}", "border-radius": "15px"},
        "nav-link-selected": {"background-color": GOLD_COLOR, "color": "black", "font-weight": "900"}
    })

# --- 8. دالة العرض الموحدة (تم حل مشكلة الـ ID المتكرر) ---
def render_modern_grid(df, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}"): 
            st.session_state.view = "grid"; st.rerun()
        
        item = df.iloc[st.session_state.current_index]
        st.markdown(f"<h2 style='color:{GOLD_COLOR};'>{item.iloc[0]}</h2>", unsafe_allow_html=True)
        
        cols = st.columns(3)
        for i, col_name in enumerate(df.columns):
            with cols[i%3]:
                st.markdown(f"""<div class='glass-card'><p style='color:#777; font-size:0.8rem; margin:0;'>{col_name}</p>
                <p style='color:white; font-weight:bold; margin:0;'>{item[col_name]}</p></div>""", unsafe_allow_html=True)
    else:
        # حل مشكلة الـ Duplicate Element ID باستخدام prefix في الـ Key
        f1, f2 = st.columns([3, 1])
        with f1: search = st.text_input("🔍 بحث...", placeholder="اكتب اسم المشروع أو المطور...", key=f"search_input_{prefix}")
        with f2: 
            loc_list = ["الكل"] + sorted(df['Location'].unique().tolist()) if 'Location' in df.columns else ["الكل"]
            sel_loc = st.selectbox("📍 تصفية بالموقع", loc_list, key=f"loc_select_{prefix}")

        filt = df.copy()
        if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        if sel_loc != "الكل": filt = filt[filt['Location'] == sel_loc]

        # العرض في كروت
        grid = st.columns(2)
        for i, (idx, row) in enumerate(filt.iterrows()):
            with grid[i%2]:
                st.markdown(f"""
                    <div class="glass-card">
                        <h4 style="color:{GOLD_COLOR}; margin-bottom:5px;">{row[0]}</h4>
                        <p style="color:#aaa; font-size:0.9rem;">📍 {row.get('Location','---')}</p>
                    </div>
                """, unsafe_allow_html=True)
                if st.button("عرض التفاصيل", key=f"btn_{prefix}_{idx}"):
                    st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"
                    st.rerun()

# --- 9. تبديل الأقسام ---
if menu == "أدوات الحساب":
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"<div class='glass-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر", value=5000000)
        yr = st.number_input("السنين", value=8)
        res = (pr * 0.9) / (yr * 12) if yr > 0 else 0
        st.markdown(f"<h3 style='color:{GOLD_COLOR}'>{res:,.0f} ج.م</h3></div>", unsafe_allow_html=True)
    # يمكن إضافة باقي الحاسبات هنا بنفس النمط

elif menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ المشروعات الحالية", "🚀 انطلاقات جديدة"])
    with t1: render_modern_grid(df_p, "p")
    with t2: render_modern_grid(df_l, "l")

elif menu == "المطورين":
    render_modern_grid(df_d, "d")

elif menu == "المساعد الذكي":
    st.info("نظام AI لتحليل السوق العقاري قيد التجهيز لعام 2026.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
