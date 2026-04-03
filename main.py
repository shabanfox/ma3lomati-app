import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- 2. الروابط والبيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 4. جلب البيانات (مع تحسين التسميات) ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Developer': 'Dev', 'المطور': 'Dev'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 5. وظائف إضافية ---
def get_news():
    try:
        f = feedparser.parse("https://www.youm7.com/rss/SectionRss?SectionID=297")
        return " | ".join([i.title for i in f.entries[:8]])
    except: return "مرحباً بك في MA3LOMATI PRO - وجهتك العقارية الأولى لعام 2026"

# --- 6. التصميم الجمالي المطور ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الأساسيات */
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.94), rgba(0,0,0,0.94)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    header {{ visibility: hidden; }}
    
    /* شريط الأخبار العلوي */
    .ticker-container {{
        background: #f59e0b; color: black; padding: 10px 0;
        overflow: hidden; white-space: nowrap; font-weight: 900;
        border-radius: 0 0 15px 15px; margin-top: -50px; margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(245,158,11,0.3);
    }}
    .ticker-text {{ display: inline-block; animation: scroll 60s linear infinite; font-size: 16px; }}
    @keyframes scroll {{ 0% {{ transform: translateX(-100%); }} 100% {{ transform: translateX(100%); }} }}

    /* الهيدر الملكي */
    .royal-header {{
        background: linear-gradient(45deg, rgba(0,0,0,0.8), rgba(245,158,11,0.1)), url('{HEADER_IMG}');
        background-size: cover; border-radius: 30px; padding: 40px;
        text-align: center; border-bottom: 4px solid #f59e0b; margin-bottom: 30px;
    }}
    .royal-header h1 {{ color: white; font-size: 55px; font-weight: 900; text-shadow: 3px 3px 10px #000; }}

    /* الكروت */
    .stButton > button {{ border-radius: 15px !important; font-weight: 700 !important; }}
    .project-card {{
        background: white; border-radius: 15px; padding: 15px;
        color: black !important; text-align: right; border-right: 8px solid #f59e0b;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2); transition: 0.3s;
    }}
    .detail-card {{
        background: rgba(15,15,15,0.95); border-radius: 20px; border: 1px solid #333;
        padding: 30px; color: white; border-top: 6px solid #f59e0b;
    }}
    .label-gold {{ color: #f59e0b; font-size: 14px; font-weight: 700; margin-bottom: 2px; }}
    .value-white {{ color: white; font-size: 20px; font-weight: 900; margin-bottom: 15px; border-bottom: 1px solid #222; }}
    
    /* وضوح الخطوط في المدخلات */
    .stTextInput input, .stSelectbox select {{
        font-size: 18px !important; font-weight: bold !important; border: 2px solid #f59e0b !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 7. التحقق من الدخول (مبسط للعرض) ---
if not st.session_state.auth:
    st.title("🔐 MA3LOMATI PRO | الدخول")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("دخول"):
        if p == "2026": st.session_state.auth = True; st.session_state.current_user = "Admin"; st.rerun()
        else: st.error("خطأ")
    st.stop()

# --- 8. الواجهة الرئيسية ---
# شريط الأخبار الجديد
st.markdown(f'<div class="ticker-container"><div class="ticker-text">🔥 {get_news()}</div></div>', unsafe_allow_html=True)

# الهيدر
st.markdown(f"""<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style='color:#f59e0b; font-size:20px; font-weight:900;'>أهلاً بك، {st.session_state.current_user}</p></div>""", unsafe_allow_html=True)

# القائمة
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"}})

# --- 9. محتوى الصفحات ---

if menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ أدوات البروكر الاحترافية</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            v = st.number_input("💰 إجمالي السعر", 1000000, step=100000)
            y = st.slider("📅 عدد السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{v/(y*12):,.0f} ج.م")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h2>🤖 المساعد العقاري الذكي</h2><p>اسألني عن أي مشروع أو منطقة وسأبحث لك في البيانات...</p></div>", unsafe_allow_html=True)
    
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])
        
    if pmt := st.chat_input("مثال: قولي معلومات عن مشروع زد أو منطقة التجمع"):
        st.session_state.messages.append({"role": "user", "content": pmt})
        with st.chat_message("user"): st.write(pmt)
        
        # منطق بحث "ذكي" بسيط
        response = "عذراً، لم أجد تفاصيل دقيقة. حاول كتابة اسم المشروع بشكل صحيح."
        for df in [df_p, df_d]:
            match = df[df.apply(lambda r: r.astype(str).str.contains(pmt, case=False).any(), axis=1)]
            if not match.empty:
                info = match.iloc[0].to_dict()
                response = f"✅ وجدت لك هذه المعلومات: \n\n" + "\n".join([f"**{k}**: {v}" for k, v in info.items()])
                break
        
        st.session_state.messages.append({"role": "assistant", "content": response})
        with st.chat_message("assistant"): st.write(response)

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    
    # قسم الفلاتر والبحث
    c_search, c_filter = st.columns([0.7, 0.3])
    with c_search:
        search = st.text_input("🔍 ابحث باسم المشروع، المطور، أو الموقع...", placeholder="اكتب هنا للبحث الفوري...")
    with c_filter:
        loc_list = ["الكل"] + sorted(active_df['Location'].unique().tolist()) if 'Location' in active_df.columns else ["الكل"]
        selected_loc = st.selectbox("📍 فلتر بالموقع", loc_list)

    # تطبيق الفلتر
    filt = active_df.copy()
    if search:
        filt = filt[filt.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
    if selected_loc != "الكل":
        filt = filt[filt['Location'] == selected_loc]

    # العرض
    if st.session_state.view == "details":
        if st.button("⬅️ عودة للقائمة"): st.session_state.view = "grid"; st.rerun()
        item = active_df.iloc[st.session_state.current_index]
        cols = st.columns(3)
        for i, (k, v) in enumerate(item.items()):
            with cols[i % 3]:
                st.markdown(f"<div class='detail-card'><p class='label-gold'>{k}</p><p class='value-white'>{v}</p></div>", unsafe_allow_html=True)
    else:
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        g1, g2 = st.columns(2)
        for i, (idx, r) in enumerate(disp.iterrows()):
            with [g1, g2][i % 2]:
                name = r.iloc[0]
                loc = r.get('Location', '---')
                dev = r.get('Dev', '---')
                st.markdown(f"""
                <div style="background:white; padding:20px; border-radius:15px; margin-bottom:15px; border-right:10px solid #f59e0b; color:black;">
                    <h3 style="margin:0; color:#000;">🏢 {name}</h3>
                    <p style="margin:5px 0;">📍 <b>الموقع:</b> {loc}</p>
                    <p style="margin:0;">🏗️ <b>المطور:</b> {dev}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button("التفاصيل الكاملة 📄", key=f"btn_{idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()

# التذييل
st.markdown("<br><hr><p style='text-align:center; color:#888;'>MA3LOMATI PRO © 2026 | جودة الوضوح والبيانات هي أولويتنا</p>", unsafe_allow_html=True)
