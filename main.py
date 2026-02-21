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
    
    /* هيدر المنصة */
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url('https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center; border-bottom: 4px solid #f59e0b; padding: 60px 20px; text-align: center; border-radius: 0 0 50px 50px;
    }
    .royal-header h1 { color: #f59e0b; font-size: 3.5rem; font-weight: 900; margin: 0; }
    
    /* كروت الشبكة (Grid) */
    div.stButton > button[key*="card_"] { 
        background: white !important; color: #000 !important; border-right: 12px solid #f59e0b !important; border-radius: 15px !important; text-align: right !important; min-height: 120px !important; font-weight: 900 !important; font-size: 1.1rem !important; transition: 0.3s !important;
    }
    div.stButton > button[key*="card_"]:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(245, 158, 11, 0.3) !important; }

    /* كروت التفاصيل الكاملة (100%) */
    .full-detail-card {
        background: #111; padding: 30px; border-radius: 20px; border: 1px solid #333; border-right: 8px solid #f59e0b; margin-bottom: 20px; width: 100%;
    }
    .full-detail-card:nth-child(even) { border-right-color: #ffffff; }
    
    .detail-label { color: #f59e0b; font-size: 1rem; font-weight: bold; margin-bottom: 5px; opacity: 0.8; }
    .detail-value { color: white; font-size: 1.6rem; font-weight: 900; }
    
    /* شريط الأخبار */
    .ticker-wrap { width: 100%; background: rgba(245, 158, 11, 0.1); padding: 12px 0; margin-bottom: 25px; border-bottom: 1px solid #333; overflow: hidden; }
    .ticker { display: inline-block; animation: ticker 40s linear infinite; color: #f59e0b; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-150%); } }
    </style>
""", unsafe_allow_html=True)

# --- 3. جلب البيانات (بنفس الروابط) ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"

def format_price(val):
    try:
        v = float(val)
        return f"{v/1_000_000:,.2f} مليون ج.م" if v >= 1_000_000 else f"{v:,.0f} ج.م"
    except: return val

@st.cache_data(ttl=300)
def load_data():
    urls = [
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    ]
    dfs = []
    for u in urls:
        df = pd.read_csv(u).fillna("---")
        df.columns = [c.strip() for c in df.columns]
        df.rename(columns={'Area':'Location','الموقع':'Location','السعر':'Price','الاونر':'Owner','صاحب الشركة':'Owner','المالك':'Owner'}, inplace=True, errors="ignore")
        dfs.append(df)
    return dfs

# --- 4. تسجيل الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<h1 style='color:#f59e0b; text-align:center; padding-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    with st.container():
        _, col, _ = st.columns([1,1.5,1])
        with col:
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.button("دخول 🚀", use_container_width=True):
                if p == "2026": # دخول سريع للأدمن
                    st.session_state.auth, st.session_state.user = True, "Admin"; st.rerun()
                else: st.error("خطأ في البيانات")
    st.stop()

# --- 5. العرض الرئيسي (70/30) ---
df_p, df_d, df_l = load_data()
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً {st.session_state.user}</p></div>', unsafe_allow_html=True)
st.markdown('<div class="ticker-wrap"><div class="ticker">🏗️ عقارات مصر 2026: استقرار في أسعار التجمع والشروق | 🚀 إطلاق مشاريع جديدة بالساحل الشمالي | 💎 خصومات حصرية للمستخدمين</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع"], 
    icons=["calculator", "building", "search"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'view' not in st.session_state: st.session_state.view = "grid"

def render_content(df, prefix):
    col_main, col_side = st.columns([0.7, 0.3])
    
    with col_main:
        if st.session_state.view == f"details_{prefix}":
            if st.button("⬅ عودة للمشاريع", key=f"bk_{prefix}"):
                st.session_state.view = "grid"; st.rerun()
            
            item = df.iloc[st.session_state.current_index]
            st.markdown(f"<h1 style='color:#f59e0b; border-bottom: 2px solid #333; padding-bottom:10px;'>{item.iloc[0]}</h1>", unsafe_allow_html=True)
            
            # عرض التفاصيل بمساحة 100%
            for col in df.columns:
                val = format_price(item[col]) if col == 'Price' else item[col]
                st.markdown(f"""
                    <div class="full-detail-card">
                        <div class="detail-label">{col}</div>
                        <div class="detail-value">{val}</div>
                    </div>
                """, unsafe_allow_html=True)
        else:
            search = st.text_input("🔍 ابحث هنا...", key=f"s_{prefix}")
            filt = df[df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df
            
            # شبكة الكروت (2 في كل صف)
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    lbl = f"🏢 {r[0]}\n📍 {r.get('Location','---')}"
                    if st.button(lbl, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()

    with col_side:
        st.markdown("<h3 style='color:#f59e0b;'>⭐ مقترحات</h3>", unsafe_allow_html=True)
        for s_idx, s_row in df.head(8).iterrows():
            if st.button(f"📌 {s_row.iloc[0]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 6. تشغيل الصفحات ---
if menu == "المشاريع":
    t1, t2 = st.tabs(["🏗️ جميع المشاريع", "🚀 لانش جديد"])
    with t1: render_content(df_p, "p")
    with t2: render_content(df_l, "l")
elif menu == "المطورين":
    render_content(df_d, "d")
elif menu == "أدوات الحساب":
    # (هنا نضع الـ 6 أدوات التي برمجناها سابقاً)
    st.info("قسم الأدوات قيد التشغيل بالـ 6 حاسبات المطورة...")
    t1, t2, t3, t4, t5, t6 = st.tabs(["💰 القسط", "📊 العمولة", "📈 ROI", "🏦 تمويل", "🎁 كاش باك", "🔮 تضخم"])
    # ... (باقي كود الأدوات)
