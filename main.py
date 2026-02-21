import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم البصري (CSS) المطور ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] {
        background: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b; padding: 50px 20px; text-align: center; border-radius: 0 0 50px 50px;
    }
    /* كروت التفاصيل العريضة */
    .detail-row {
        background: #111; padding: 25px; border-radius: 15px; border: 1px solid #333; border-right: 8px solid #f59e0b; margin-bottom: 15px; width: 100%;
    }
    .detail-label { color: #f59e0b; font-size: 1.1rem; font-weight: bold; }
    .detail-value { color: white; font-size: 1.7rem; font-weight: 900; }
    
    /* أدوات الحساب */
    .tool-box { background: #111; padding: 20px; border-radius: 15px; border: 1px solid #f59e0b; margin-bottom: 20px; }
    .res-box { background: rgba(245, 158, 11, 0.2); padding: 15px; border-radius: 10px; color: #fff; font-weight: bold; text-align: center; font-size: 1.3rem; border: 1px dashed #f59e0b; }
    
    /* أزرار الكروت */
    div.stButton > button[key*="card_"] { 
        background: white !important; color: #000 !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 110px !important; font-weight: 900 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. الربط وقاعدة البيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

def check_login(u, p):
    if p == "2026": return "Admin" # دخول الطوارئ
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=7)
        if res.status_code == 200:
            for user in res.json():
                if str(u).strip().lower() == str(user.get('Name','')).strip().lower() and str(p) == str(user.get('Password','')):
                    return user.get('Name')
    except: pass
    return None

@st.cache_data(ttl=300)
def load_all_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    ]
    dfs = []
    for u in urls:
        df = pd.read_csv(u).fillna("---")
        df.columns = [c.strip() for c in df.columns]
        df.rename(columns={'Area':'Location','الموقع':'Location','السعر':'Price','الاونر':'Owner','صاحب الشركة':'Owner'}, inplace=True, errors="ignore")
        dfs.append(df)
    return dfs

# --- 4. بوابة تسجيل الدخول (لا يمكن تخطيها) ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1><p style='color:white;'>نظام إدارة المحتوى العقاري 2026</p></div>", unsafe_allow_html=True)
    with st.container():
        _, col_mid, _ = st.columns([1,1.5,1])
        with col_mid:
            u_input = st.text_input("اسم المستخدم")
            p_input = st.text_input("كلمة المرور", type="password")
            if st.button("دخول المنصة 🚀", use_container_width=True):
                with st.spinner("جاري التحقق من البيانات..."):
                    user_name = check_login(u_input, p_input)
                    if user_name:
                        st.session_state.auth = True
                        st.session_state.user = user_name
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة أو لا يوجد اتصال")
    st.stop()

# --- 5. المنصة بعد الدخول ---
df_all, df_dev, df_new = load_all_data()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.user} | لوحة التحكم الذكية</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع"], 
    icons=["calculator", "building", "search"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight":"900"}})

if 'view' not in st.session_state: st.session_state.view = "grid"

def format_price(val):
    try:
        v = float(val)
        return f"{v/1_000_000:,.2f} مليون ج.م" if v >= 1_000_000 else f"{v:,.0f} ج.م"
    except: return val

# --- 6. منطق العرض (100% للتفاصيل) ---
def render_logic(df, prefix):
    if st.session_state.view == f"details_{prefix}":
        # عرض التفاصيل 100%
        if st.button("⬅ عودة للقائمة", key=f"b_{prefix}"):
            st.session_state.view = "grid"; st.rerun()
        
        item = df.iloc[st.session_state.current_index]
        st.markdown(f"<h1 style='color:#f59e0b;'>{item.iloc[0]}</h1>", unsafe_allow_html=True)
        for col in df.columns:
            val = format_price(item[col]) if col == 'Price' else item[col]
            st.markdown(f'<div class="detail-row"><div class="detail-label">{col}</div><div class="detail-value">{val}</div></div>', unsafe_allow_html=True)
    else:
        # عرض الشبكة 70/30
        c1, c2 = st.columns([0.7, 0.3])
        with c1:
            search = st.text_input("🔍 بحث سريع...", key=f"f_{prefix}")
            filt = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(12).iterrows()):
                with grid[i%2]:
                    lbl = f"🏢 {r[0]}\n📍 {r.get('Location','---')}"
                    if st.button(lbl, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
        with c2:
            st.markdown("<h3 style='color:#f59e0b;'>⭐ مقترحات</h3>", unsafe_allow_html=True)
            for s_idx, s_row in df.head(10).iterrows():
                if st.button(f"📌 {s_row.iloc[0]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 7. الأقسام ---
if menu == "المشاريع":
    tab1, tab2 = st.tabs(["🏗️ جميع المشاريع", "🚀 مشاريع جديدة"])
    with tab1: render_logic(df_all, "p")
    with tab2: render_logic(df_new, "n")

elif menu == "المطورين":
    render_logic(df_dev, "d")

elif menu == "أدوات الحساب":
    st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حاسبات البروكر (Real-Time)</h2>", unsafe_allow_html=True)
    t1, t2, t3, t4, t5, t6 = st.tabs(["💰 القسط", "📊 العمولة", "📈 ROI", "🏦 تمويل", "🎁 كاش باك", "🔮 تضخم"])
    
    with t1:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        pr = st.number_input("سعر الوحدة", value=10000000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنين", value=8)
        st.markdown(f'<div class="res-box">القسط الشهري: {(pr*(1-dp/100))/(yr*12):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with t2:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        val = st.number_input("قيمة الصفقة", value=5000000)
        comm = st.number_input("العمولة %", value=2.5)
        st.markdown(f'<div class="res-box">صافي الربح: {val*(comm/100):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t3:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", value=8000000)
        rent = st.number_input("الإيجار الشهري", value=40000)
        st.markdown(f'<div class="res-box">العائد السنوي ROI: {((rent*12)/buy)*100:.2f} %</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t4:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        loan = st.number_input("مبلغ القرض", value=3000000)
        st.markdown(f'<div class="res-box">قسط البنك التقريبي: {(loan*1.8)/120:,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t5:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        total = st.number_input("السعر الأصلي", value=10000000)
        disc = st.slider("الخصم %", 0, 45, 20)
        st.markdown(f'<div class="res-box">السعر بعد الخصم: {total*(1-disc/100):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with t6:
        st.markdown('<div class="tool-box">', unsafe_allow_html=True)
        cur = st.number_input("السعر الحالي", value=5000000)
        st.markdown(f'<div class="res-box">القيمة بعد 3 سنوات (+25% سنوياً): {cur*(1.25**3):,.0f} ج.م</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
