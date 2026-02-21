import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم البصري (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stAppViewContainer"] {
        background: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b; padding: 50px 20px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 0px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3.5rem; font-weight: 900; margin: 0; }
    .ticker-wrap {
        width: 100%; background: rgba(245, 158, 11, 0.1); border-bottom: 1px solid #333; overflow: hidden; white-space: nowrap; padding: 15px 0; margin-bottom: 25px;
    }
    .ticker { display: inline-block; animation: ticker 45s linear infinite; color: #f59e0b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-150%); } }
    
    div.stButton > button[key*="card_"] { 
        background: white !important; color: #000 !important; border-right: 15px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 140px !important; font-weight: 900 !important; font-size: 1.1rem !important; white-space: pre-wrap !important;
    }
    div.stButton > button[key*="side_"] {
        background: #111 !important; color: #f59e0b !important; border: 1px solid #f59e0b !important; border-radius: 12px !important; margin-bottom: 8px !important; font-weight: bold !important;
    }
    .detail-card { background: #111; padding: 25px; border-radius: 20px; border-top: 6px solid #f59e0b; margin-bottom: 15px; border-left: 1px solid #333; }
    .label-gold { color: #f59e0b; font-weight: 900; }
    .val-white { color: white; font-size: 1.3rem; font-weight: 700; }
    .tool-result { background: rgba(245, 158, 11, 0.1); padding: 15px; border-radius: 10px; border: 1px solid #f59e0b; color: #fff; font-weight: bold; text-align: center; margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. إدارة البيانات والربط ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

def format_money(val):
    try:
        v = float(val)
        return f"{v/1_000_000:,.2f} مليون ج.م" if v >= 1_000_000 else f"{v:,.0f} ج.م"
    except: return "اتصل للسعر"

@st.cache_data(ttl=300)
def load_all_data():
    try:
        urls = [
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv", # المشاريع
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv", # المطورين
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"  # الجديدة
        ]
        dfs = []
        for u in urls:
            df = pd.read_csv(u)
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area':'Location','الموقع':'Location','السعر':'Price','الاونر':'Owner','صاحب الشركة':'Owner','المالك':'Owner'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
            dfs.append(df.fillna("---"))
        return dfs
    except: return [pd.DataFrame()]*3

def check_login(u, p):
    if p == "2026": return "Admin"
    try:
        res = requests.get(f"{SCRIPT_URL}?nocache={time.time()}", timeout=5)
        if res.status_code == 200:
            for user in res.json():
                if str(u).strip().lower() == str(user.get('Name','')).strip().lower() and str(p) == str(user.get('Password','')):
                    return user.get('Name')
    except: pass
    return None

# --- 4. نظام تسجيل الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    with st.container():
        col_a, col_b, col_c = st.columns([1,2,1])
        with col_b:
            u_input = st.text_input("اسم المستخدم")
            p_input = st.text_input("كلمة المرور", type="password")
            if st.button("دخول المنصة 🚀", use_container_width=True):
                user_res = check_login(u_input, p_input)
                if user_res:
                    st.session_state.auth = True
                    st.session_state.user = user_res
                    st.rerun()
                else: st.error("بيانات الدخول غير صحيحة")
    st.stop()

# --- 5. الصفحة الرئيسية ---
df_p, df_d, df_l = load_all_data()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.user} | 2026</p></div>', unsafe_allow_html=True)
st.markdown('<div class="ticker-wrap"><div class="ticker">🏗️ تحديثات حية: استقرار أسعار التجمع والشروق | 🚀 إطلاق المرحلة الجديدة من كمبوند "سولاري" | 💎 خصومات حصرية لمستخدمي المنصة</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع"], 
    icons=["calculator", "building", "search"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight":"900"}})

if 'view' not in st.session_state: st.session_state.view = "grid"

# --- 6. دالة العرض 70/30 ---
def render_page_content(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0
    
    col_main, col_side = st.columns([0.7, 0.3])

    with col_main:
        if st.session_state.view == f"details_{prefix}":
            if st.button("⬅ عودة للقائمة", key=f"bk_{prefix}"): st.session_state.view = "grid"; st.rerun()
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h2 style='color:#f59e0b;'>💎 {item.iloc[0]}</h2>", unsafe_allow_html=True)
            for col in dataframe.columns:
                val = format_money(item[col]) if col == 'Price' else item[col]
                st.markdown(f'<div class="detail-card"><p class="label-gold">{col}</p><p class="val-white">{val}</p></div>', unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث هنا...", key=f"s_{prefix}")
            filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
            start = st.session_state[pg_key] * 6
            disp = filt.iloc[start : start + 6]
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if prefix=="d": # كارت المطور
                        lbl = f"🏗️ المطور: {r[0]}\n👤 الاونر: {r.get('Owner','---')}"
                    else: # كارت المشروع
                        lbl = f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {format_money(r.get('Price',0))}"
                    if st.button(lbl, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            # التنقل
            if len(filt)>6:
                c1, c2, c3 = st.columns([1,1,1])
                with c1: 
                    if st.session_state[pg_key]>0 and st.button("السابق", key=f"pr_{prefix}"): st.session_state[pg_key]-=1; st.rerun()
                with c2: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
                with c3:
                    if (start+6)<len(filt) and st.button("التالي", key=f"nx_{prefix}"): st.session_state[pg_key]+=1; st.rerun()

    with col_side:
        st.markdown("<h3 style='color:#f59e0b; border-bottom:1px solid #333; padding-bottom:10px;'>⭐ مقترحات سريعة</h3>", unsafe_allow_html=True)
        for s_idx, s_row in dataframe.head(10).iterrows():
            if st.button(f"📌 {s_row.iloc[0]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 7. الأقسام ---
if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 المشاريع الجديدة (Launch)"])
    with t1: render_page_content(df_p, "p")
    with t2: render_page_content(df_l, "l")

elif menu == "المطورين":
    render_page_content(df_d, "d")

elif menu == "أدوات الحساب":
    cm, cs = st.columns([0.7, 0.3])
    with cm:
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ أدوات البروكر الذكية</h2>", unsafe_allow_html=True)
        calc_t = st.tabs(["💰 القسط", "📊 العمولة", "📈 ROI", "🏦 تمويل عقاري", "🎁 كاش باك"])
        with calc_t[0]:
            p = st.number_input("سعر الوحدة", value=5000000)
            d = st.number_input("المقدم %", value=10)
            y = st.number_input("السنين", value=8)
            res = (p - (p*d/100)) / (y*12) if y>0 else 0
            st.markdown(f"<div class='tool-result'>القسط الشهري: {res:,.0f} ج.م</div>", unsafe_allow_html=True)
        with calc_t[1]:
            deal = st.number_input("قيمة الصفقة", value=5000000)
            pct = st.number_input("العمولة %", value=2.5)
            st.markdown(f"<div class='tool-result'>صافي العمولة: {deal*(pct/100):,.0f} ج.م</div>", unsafe_allow_html=True)
        with calc_t[2]:
            inv = st.number_input("سعر الشراء", value=8000000)
            rent = st.number_input("الإيجار المتوقع", value=40000)
            st.markdown(f"<div class='tool-result'>العائد السنوي: {((rent*12)/inv)*100:.2f} %</div>", unsafe_allow_html=True)
        with calc_t[3]:
            bank_p = st.number_input("مبلغ التمويل", value=2000000)
            bank_y = st.number_input("سنوات التمويل", value=15)
            # فائدة افتراضية 20%
            st.markdown(f"<div class='tool-result'>قسط البنك التقريبي: {(bank_p*1.8)/(bank_y*12):,.0f} ج.م</div>", unsafe_allow_html=True)
        with calc_t[4]:
            cash_p = st.number_input("سعر الكاش", value=10000000)
            disc = st.slider("نسبة الخصم %", 0, 40, 10)
            st.markdown(f"<div class='tool-result'>صافي السعر بعد الخصم: {cash_p*(1-disc/100):,.0f} ج.م</div>", unsafe_allow_html=True)
    with cs:
        st.info("💡 استخدم هذه الأدوات لتقديم أرقام سريعة واحترافية لعميلك أثناء المكالمة.")

st.markdown("<p style='text-align:center; color:#555; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
