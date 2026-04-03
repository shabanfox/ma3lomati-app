import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 4. جلب البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 5. التصميم الجمالي (التركيز على الوضوح والتقسيم) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; font-family: 'Cairo', sans-serif;
    }}
    
    /* شريط الأخبار في مكان ثابت وواضح */
    .news-ticker {{
        background: #f59e0b; color: black; padding: 8px; font-weight: 900;
        text-align: center; border-radius: 10px; margin-bottom: 20px; font-size: 18px;
    }}

    /* الهيدر */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; padding: 30px; text-align: center; 
        border-bottom: 4px solid #f59e0b; border-radius: 0 0 30px 30px; margin-bottom: 25px;
    }}

    /* الكروت البيضاء (كلام واضح جداً) */
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #000 !important;
        border-right: 10px solid #f59e0b !important; padding: 20px !important;
        font-size: 18px !important; font-weight: 900 !important; text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important; width: 100% !important;
        min-height: 120px !important; margin-bottom: 15px !important;
    }}
    
    /* تفاصيل واضحة */
    .detail-box {{
        background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px;
        border-top: 4px solid #f59e0b; color: white; margin-bottom: 10px;
    }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 15px; }}
    .text-large {{ font-size: 20px; font-weight: 700; color: white; }}
    </style>
""", unsafe_allow_html=True)

# --- 6. تسجيل الدخول ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<h1 style='text-align:center; color:white;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة السر", type="password")
        if st.button("دخول", use_container_width=True):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 7. الواجهة الداخلية ---
st.markdown('<div class="news-ticker">🔥 آخر الأخبار: انتعاش في سوق العقارات المصري لعام 2026 | مشاريع العاصمة الإدارية تتصدر المشهد</div>', unsafe_allow_html=True)
st.markdown('<div class="royal-header"><h1 style="color:white; margin:0;">MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

# --- 8. التقسيمة 70 - 30 ---
col_main, col_side = st.columns([0.7, 0.3])

with col_main:
    if menu == "المشاريع" or menu == "المطورين" or menu == "Launches":
        active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
        
        # الفلاتر (واضحة جداً)
        st.markdown("<h3 style='color:#f59e0b;'>🔍 البحث والفلاتر</h3>", unsafe_allow_html=True)
        search = st.text_input("ابحث باسم المشروع أو المنطقة...", key="main_search", placeholder="اكتب هنا...")
        
        filt = active_df.copy()
        if search:
            filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]

        if st.session_state.view == "details":
            if st.button("⬅️ عودة للقائمة"): st.session_state.view = "grid"; st.rerun()
            item = active_df.iloc[st.session_state.current_index]
            for k, v in item.items():
                st.markdown(f'<div class="detail-box"><span class="label-gold">{k}:</span><br><span class="text-large">{v}</span></div>', unsafe_allow_html=True)
        else:
            # عرض الشبكة (Grid)
            grid = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(10).iterrows()):
                with grid[i%2]:
                    btn_label = f"🏢 {r.iloc[0]}\n📍 {r.get('Location', r.get('الموقع', '---'))}"
                    if st.button(btn_label, key=f"card_{idx}"):
                        st.session_state.current_index = idx
                        st.session_state.view = "details"; st.rerun()

    elif menu == "المساعد الذكي":
        st.markdown("<div class='detail-box'><h2>🤖 المساعد الذكي</h2><p>اسألني عن أي مشروع في قاعدة البيانات</p></div>", unsafe_allow_html=True)
        for m in st.session_state.messages:
            with st.chat_message(m["role"]): st.write(m["content"])
        
        if prompt := st.chat_input("كيف أساعدك اليوم؟"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            # بحث بسيط في الداتا
            res = "جاري البحث... لم أجد تفاصيل دقيقة، حاول كتابة الاسم بشكل أوضح."
            for df in [df_p, df_d]:
                m = df[df.apply(lambda r: r.astype(str).str.contains(prompt, case=False).any(), axis=1)]
                if not m.empty:
                    res = f"وجدت لك تفاصيل عن **{m.iloc[0,0]}**: \n" + str(m.iloc[0].to_dict())
                    break
            st.session_state.messages.append({"role": "assistant", "content": res})
            st.rerun()

with col_side:
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>🛠️ أدوات سريعة</h3>", unsafe_allow_html=True)
    with st.container(border=True):
        st.subheader("💳 حاسبة القسط")
        v = st.number_input("السعر", 1000000)
        y = st.number_input("السنين", 8)
        st.success(f"القسط: {v/(y*12):,.0f}")
    
    st.markdown("---")
    st.markdown("<h3 style='color:#f59e0b; text-align:center;'>⭐ مقترحات</h3>", unsafe_allow_html=True)
    for _, r in df_p.head(5).iterrows():
        st.markdown(f"<div style='background:rgba(255,255,255,0.1); padding:10px; border-radius:10px; margin-bottom:5px; border-right:3px solid #f59e0b;'>{r.iloc[0]}</div>", unsafe_allow_html=True)

if st.button("🚪 خروج"):
    st.session_state.auth = False; st.rerun()
