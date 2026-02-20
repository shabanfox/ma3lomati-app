import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. إدارة الحالة (Persistence) ---
if 'auth' not in st.session_state:
    if "u_session" in st.query_params:
        st.session_state.auth = True
        st.session_state.current_user = st.query_params["u_session"]
    else:
        st.session_state.auth = False

if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0

# --- 3. الروابط والصور ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 4. وظائف النظام ---
def logout():
    st.session_state.auth = False
    st.query_params.clear()
    st.rerun()

@st.cache_data(ttl=60)
def load_data():
    try:
        # روابط الشيتات الخاصة بك
        U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
        U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]:
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

def render_grid(dataframe, prefix):
    if st.session_state.view == f"details_{prefix}":
        if st.button("⬅ عودة للقائمة", key=f"back_{prefix}", use_container_width=True):
            st.session_state.view = "grid"; st.rerun()
        
        item = dataframe.iloc[st.session_state.current_index]
        st.markdown(f"<div class='detail-card'><h3>🔍 تفاصيل: {item[0]}</h3></div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        cols = dataframe.columns
        for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
            with [c1, c2, c3][i]:
                h = '<div class="detail-card">'
                for k in cs: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                st.markdown(h+'</div>', unsafe_allow_html=True)
    else:
        search = st.text_input(f"🔍 بحث سريع في القائمة...", key=f"search_{prefix}")
        filt = dataframe[dataframe.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else dataframe
        
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.75, 0.25])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    card_html = f"🏠 {r[0]}\n🏗️ {r.get('Developer','---')}\n📍 {r.get('Location','---')}"
                    if st.button(card_html, key=f"card_{prefix}_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, f"details_{prefix}"; st.rerun()
            
            # التنقل بين الصفحات
            p1, p_info, p2 = st.columns([1, 2, 1])
            with p1: 
                if st.session_state.page_num > 0:
                    if st.button("السابق", key=f"prev_{prefix}"): st.session_state.page_num -= 1; st.rerun()
            with p_info: st.markdown(f"<p style='text-align:center; color:#f59e0b;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي", key=f"next_{prefix}"): st.session_state.page_num += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b; font-weight:bold; border-bottom:1px solid #333;'>📌 أهم المقترحات</p>", unsafe_allow_html=True)
            for s_idx, s_row in dataframe.head(8).iterrows():
                if st.button(f"⭐ {str(s_row[0])[:20]}", key=f"side_{prefix}_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, f"details_{prefix}"; st.rerun()

# --- 5. التصميم CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.92), rgba(0,0,0,0.92)), url('{BG_IMG}');
        background-size: cover; direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{ background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}'); background-size: cover; border-bottom: 3px solid #f59e0b; padding: 40px; text-align: center; border-radius: 0 0 50px 50px; margin-bottom: 20px; }}
    .detail-card {{ background: rgba(30, 30, 30, 0.8); padding: 20px; border-radius: 15px; border: 1px solid #444; margin-bottom: 10px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; margin-bottom: 0px; font-size: 14px; }}
    .val-white {{ color: white; font-size: 16px; border-bottom: 1px solid #333; padding-bottom: 5px; }}
    div.stButton > button {{ border-radius: 10px !important; }}
    div.stButton > button[key*="card_"] {{ background: #fff !important; color: #000 !important; border-right: 8px solid #f59e0b !important; min-height: 120px !important; font-weight: bold !important; font-size: 16px !important; }}
    .stTabs [aria-selected="true"] {{ background-color: #f59e0b !important; color: black !important; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. نظام الدخول المبسط ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN", use_container_width=True):
            if p == "2026": # كلمة سر بسيطة للتجربة
                st.session_state.auth, st.session_state.current_user = True, u
                st.rerun()
    st.stop()

# --- 7. التحميل الرئيسي ---
df_p, df_d, df_l = load_data()

st.markdown(f'<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً بك: {st.session_state.current_user} | رفيقك العقاري الذكي</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "search", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

# ريست للفلاتر عند تغيير القائمة
if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 8. الأقسام ---

if menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ الحاسبة العقارية</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='detail-card'><h3>💰 القسط</h3>", unsafe_allow_html=True)
        pr = st.number_input("السعر الإجمالي", value=1000000)
        dp = st.number_input("المقدم %", value=10)
        yr = st.number_input("السنين", value=7)
        res = (pr - (pr * dp/100)) / (yr * 12) if yr > 0 else 0
        st.write(f"الشهر: {res:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='detail-card'><h3>📊 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", value=1000000)
        pct = st.number_input("نسبة العمولة %", value=2.5)
        st.write(f"العمولة: {(deal * pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col3:
        st.markdown("<div class='detail-card'><h3>📈 العائد ROI</h3>", unsafe_allow_html=True)
        inv = st.number_input("المبلغ المدفوع", value=500000)
        rent = st.number_input("الإيجار السنوي المتوقع", value=60000)
        st.write(f"العائد: {(rent/inv*100):.1f}% سنوياً")
        st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    t1, t2, t3 = st.tabs(["🏗️ قاعدة البيانات", "🚀 لونشات جديدة", "⚖️ نظام المقارنة"])
    with t1: render_grid(df_p, "proj")
    with t2: render_grid(df_l, "launch")
    with t3:
        st.markdown("<h3 style='color:#f59e0b;'>⚖️ قارن واختار الأفضل لعميلك</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: p1_choice = st.selectbox("المشروع الأول", df_p.iloc[:,0].tolist(), key="p1")
        with c2: p2_choice = st.selectbox("المشروع الثاني", df_p.iloc[:,0].tolist(), key="p2")
        
        if p1_choice and p2_choice:
            d1 = df_p[df_p.iloc[:,0] == p1_choice].iloc[0]
            d2 = df_p[df_p.iloc[:,0] == p2_choice].iloc[0]
            for col in df_p.columns:
                col_a, col_b, col_c = st.columns([2, 1, 2])
                col_a.info(f"{d1[col]}")
                col_b.markdown(f"<p style='text-align:center; color:#f59e0b;'>{col}</p>", unsafe_allow_html=True)
                col_c.success(f"{d2[col]}")

elif menu == "المطورين":
    render_grid(df_d, "dev")

elif menu == "المساعد الذكي":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🤖 محلل البيانات AI</h2>", unsafe_allow_html=True)
    query = st.text_input("عن ماذا تبحث اليوم؟ (مثال: مشاريع الشيخ زايد، شركة إعمار...)")
    if query:
        # بحث شامل في كل الجداول
        res_p = df_p[df_p.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
        if not res_p.empty:
            st.write(f"🔍 وجدنا {len(res_p)} مشروع مطابق:")
            st.dataframe(res_p, use_container_width=True)
        else:
            st.error("لم أجد نتائج مطابقة، حاول تبسيط كلمات البحث.")
    
    st.markdown("---")
    st.info("💡 نصيحة: استخدم نظام المقارنة لتوضيح الفروق السعرية لعميلك بشكل محترف.")

if st.button("🚪 تسجيل خروج"): logout()
st.markdown(f"<p style='text-align:center; color:#666; padding:20px;'>MA3LOMATI PRO © 2026 | User: {st.session_state.current_user}</p>", unsafe_allow_html=True)
