import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. التصميم البصري (CSS) - النسخة الفاخرة ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@700;900&display=swap');
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    .block-container { padding-top: 0rem !important; }
    [data-testid="stStatusWidget"] {display: none !important;}
    
    [data-testid="stAppViewContainer"] {
        background: #0a0a0a;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }

    /* هيدر ملكي فخم بصورة ناطحات سحاب ليلية */
    .royal-header { 
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1510798831971-661eb04b3739?q=80&w=2070&auto=format&fit=crop'); 
        background-size: cover; background-position: center;
        border-bottom: 4px solid #f59e0b; padding: 60px 20px; text-align: center; border-radius: 0 0 50px 50px; 
        box-shadow: 0 10px 30px rgba(245, 158, 11, 0.2);
    }
    .royal-header h1 { color: #f59e0b; font-size: 3.5rem; font-weight: 900; margin: 0; text-shadow: 2px 2px 10px rgba(0,0,0,0.8); }

    /* شريط الأخبار */
    .ticker-wrap {
        width: 100%; background: #1a1a1a; border-bottom: 1px solid #333;
        overflow: hidden; white-space: nowrap; padding: 15px 0; margin-bottom: 25px;
    }
    .ticker { display: inline-block; animation: ticker 45s linear infinite; color: #f59e0b; font-weight: bold; font-size: 1.1rem; }
    .news-msg { margin: 0 80px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-150%); } }

    /* الكروت الرئيسية (البيضاء) */
    div.stButton > button[key*="card_"] { 
        background: white !important; color: #111 !important; border-right: 15px solid #f59e0b !important; 
        border-radius: 15px !important; text-align: right !important; min-height: 140px !important; 
        font-weight: 900 !important; font-size: 1.2rem !important; white-space: pre-wrap !important; 
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3) !important; transition: 0.3s;
    }
    
    /* كروت الجانب (الذهبية المختصرة) */
    div.stButton > button[key*="side_"] {
        background: rgba(245, 158, 11, 0.1) !important; color: #f59e0b !important; 
        border: 1px solid #f59e0b !important; border-radius: 10px !important; margin-bottom: 5px !important;
        font-weight: bold !important; font-size: 0.9rem !important;
    }

    .detail-card { 
        background: #1e1e1e; padding: 25px; border-radius: 20px; 
        border: 1px solid #333; border-top: 8px solid #f59e0b; margin-bottom: 20px; 
    }
    .label-gold { color: #f59e0b; font-weight: 900; font-size: 1.1rem; margin-bottom: 5px; }
    .val-white { color: white; font-size: 1.3rem; font-weight: 700; }
    
    .filter-box { background: rgba(255, 255, 255, 0.03); padding: 20px; border-radius: 20px; border: 1px solid #222; margin-bottom: 25px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. الوظائف والبيانات ---
def format_price_millions(val):
    try:
        v = float(val)
        if v >= 1_000_000: return f"{v/1_000_000:,.2f} مليون ج.م"
        return f"{v:,.0f} ج.م"
    except: return "اتصل للسعر"

@st.cache_data(ttl=300, show_spinner=False)
def load_data():
    try:
        urls = [
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
            "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        ]
        results = []
        for url in urls:
            df = pd.read_csv(url)
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area':'Location','الموقع':'Location','السعر':'Price','المالك':'Owner','الاونر':'Owner','صاحب الشركة':'Owner'}, inplace=True, errors="ignore")
            if 'Price' in df.columns:
                df['Price'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
                df['Price'] = df['Price'].apply(lambda x: x * 1_000_000 if 0 < x < 1000 else x)
            results.append(df.fillna("---"))
        return results
    except: return [pd.DataFrame()]*3

df_p, df_d, df_l = load_data()

# --- 4. الدخول ---
if 'auth' not in st.session_state: st.session_state.auth = False

if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:80px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    u = st.text_input("اسم المستخدم")
    p = st.text_input("كلمة المرور", type="password")
    if st.button("دخول الملكي 🚀"):
        if p == "2026": st.session_state.auth = True; st.session_state.current_user = u if u else "Admin"; st.rerun()
    st.stop()

# --- 5. الهيكل العلوي ---
st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO | 2026</h1><p style="color:#f59e0b; font-size:1.2rem;">نظام إدارة البيانات العقارية الاحترافي</p></div>', unsafe_allow_html=True)

st.markdown("""
    <div class="ticker-wrap"><div class="ticker">
        <span class="news-msg">🏗️ السوق: استقرار أسعار التجمع الخامس عند 45,000 ج للمتر في المتوسط</span>
        <span class="news-msg">📍 جديد: إطلاق مشروع "سولاري" رأس الحكمة بمقدم 5% فقط</span>
        <span class="news-msg">💹 استثمار: العائد الإيجاري في العاصمة الإدارية يصل لـ 12% سنوياً</span>
    </div></div>
""", unsafe_allow_html=True)

menu = option_menu(None, ["أدوات الحساب", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["calculator", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000", "font-weight": "900"}})

if 'view' not in st.session_state: st.session_state.view = "grid"

# --- 6. دالة العرض (التقسيم 70/30) ---
def render_main_ui(dataframe, prefix):
    pg_key = f"pg_{prefix}"
    if pg_key not in st.session_state: st.session_state[pg_key] = 0

    col_main, col_side = st.columns([0.7, 0.3]) # التقسيمة المطلوبة

    with col_main:
        if st.session_state.view == f"details_{prefix}":
            if st.button("⬅ عودة للقائمة الرئيسية", key=f"back_{prefix}"): 
                st.session_state.view = "grid"; st.rerun()
            item = dataframe.iloc[st.session_state.current_index]
            st.markdown(f"<h2 style='color:#f59e0b;'>💎 {item.iloc[0]}</h2>", unsafe_allow_html=True)
            d_cols = st.columns(2)
            for i, c in enumerate(dataframe.columns):
                with d_cols[i%2]:
                    v = format_price_millions(item[c]) if c == 'Price' else item[c]
                    st.markdown(f'<div class="detail-card"><p class="label-gold">{c}</p><p class="val-white">{v}</p></div>', unsafe_allow_html=True)
        else:
            # الفلاتر والشبكة
            st.markdown('<div class="filter-box">', unsafe_allow_html=True)
            f1, f2 = st.columns([2, 1])
            with f1: search = st.text_input("🔍 ابحث عن أي شيء...", key=f"search_{prefix}")
            with f2:
                locs = ["الكل"] + sorted(list(dataframe['Location'].unique())) if 'Location' in dataframe.columns else ["الكل"]
                sel_loc = st.selectbox("📍 تصفية حسب الموقع", locs, key=f"loc_{prefix}")
            st.markdown('</div>', unsafe_allow_html=True)

            filt = dataframe.copy()
            if search: filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
            if sel_loc != "الكل" and 'Location' in filt.columns: filt = filt[filt['Location'] == sel_loc]

            start = st.session_state[pg_key] * 6
            disp = filt.iloc[start : start + 6]
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    if prefix == "d":
                        lbl = f"🏗️ المطور: {r[0]}\n👤 الاونر: {r.get('Owner', '---')}"
                    else:
                        p_txt = format_price_millions(r['Price']) if 'Price' in r else ""
                        lbl = f"🏢 {r[0]}\n📍 {r.get('Location','---')}\n💰 {p_txt}"
                    
                    if st.button(lbl, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # التنقل
            st.write("")
            p1, px, p2 = st.columns([1, 1, 1])
            with p1: 
                if st.session_state[pg_key] > 0:
                    if st.button("السابق", key=f"prev_{prefix}"): st.session_state[pg_key]-=1; st.rerun()
            with px: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state[pg_key]+1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + 6) < len(filt):
                    if st.button("التالي", key=f"next_{prefix}"): st.session_state[pg_key]+=1; st.rerun()

    with col_side:
        st.markdown("<h3 style='color:#f59e0b; border-bottom:2px solid #333; padding-bottom:10px;'>⭐ مقترحات سريعة</h3>", unsafe_allow_html=True)
        for s_idx, s_row in dataframe.head(10).iterrows():
            if st.button(f"📌 {s_row.iloc[0]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()
        
        st.markdown("<br><div style='background:#111; padding:15px; border-radius:15px; border:1px solid #f59e0b; color:#f59e0b; text-align:center;'><b>إحصائية سريعة:</b><br>إجمالي السجلات: " + str(len(dataframe)) + "</div>", unsafe_allow_html=True)

# --- 7. الأقسام ---
if menu == "المشاريع":
    render_main_ui(df_p, "p")
elif menu == "المطورين":
    render_main_ui(df_d, "d")
elif menu == "أدوات الحساب":
    # الأدوات تظهر في مساحة الـ 70% أيضاً
    c_main, c_side = st.columns([0.7, 0.3])
    with c_main:
        st.markdown("<h2 style='color:#f59e0b; text-align:center;'>🛠️ حاسبات البروكر الذكية</h2>", unsafe_allow_html=True)
        t1, t2, t3 = st.tabs(["💰 القسط", "📊 العمولة", "📈 ROI"])
        with t1:
            pr = st.number_input("سعر الوحدة الكامل", value=10000000)
            dp = st.number_input("المقدم %", value=10)
            yr = st.number_input("السنوات", value=8)
            res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
            st.markdown(f"<div class='detail-card'><p class='label-gold'>القسط الشهري:</p><p class='val-white'>{res:,.0f} ج.م</p></div>", unsafe_allow_html=True)
        with t2:
            deal = st.number_input("قيمة البيعة", value=5000000)
            pct = st.number_input("نسبة عمولتك %", value=2.5)
            st.markdown(f"<div class='detail-card'><p class='label-gold'>عمولتك الصافية:</p><p class='val-white'>{deal*(pct/100):,.0f} ج.م</p></div>", unsafe_allow_html=True)
        with t3:
            buy = st.number_input("سعر الشراء الكلي", value=8000000)
            rent = st.number_input("الإيجار الشهري", value=50000)
            roi = ((rent * 12) / buy) * 100 if buy > 0 else 0
            st.markdown(f"<div class='detail-card'><p class='label-gold'>العائد السنوي (%):</p><p class='val-white'>{roi:.2f} %</p></div>", unsafe_allow_html=True)
    with c_side:
        st.info("استخدم هذه الحاسبات لتقديم عرض سريع لعميلك أثناء المكالمة.")

st.markdown("<br><br><p style='text-align:center; color:#444;'>MA3LOMATI PRO © 2026 - All Rights Reserved</p>", unsafe_allow_html=True)
