import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- إدارة الحالة (Session State) ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'search_query' not in st.session_state: st.session_state.search_query = ""
if 'menu_index' not in st.session_state: st.session_state.menu_index = 2

# --- 2. الروابط الأساسية ووظائف النظام ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

def logout():
    st.session_state.auth = False
    st.rerun()

# --- 3. التصميم (CSS) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 2px solid #f59e0b;
        padding: 30px 10px; text-align: center; border-radius: 20px; margin-bottom: 10px;
    }}
    div.stButton > button[key*="card_"] {{
        background: #ffffff !important; color: #111 !important;
        border-right: 6px solid #f59e0b !important; border-radius: 15px !important;
        padding: 15px !important; text-align: right !important;
        min-height: 150px !important; width: 100% !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
        white-space: pre-line !important; font-size: 14px !important;
    }}
    .dev-link {{ color: #f59e0b; font-weight: bold; text-decoration: underline; cursor: pointer; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. الدخول ---
if not st.session_state.auth:
    c_l, c_r = st.columns([0.4, 0.6])
    with c_l:
        st.markdown("<h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة السر لدخول 2026", type="password")
        if st.button("دخول"):
            if pwd == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# --- 5. الهيدر وزر الخروج العلوي ---
c_emp, c_out = st.columns([0.85, 0.15])
with c_out: 
    if st.button("🚪 خروج", key="top_exit"): logout()

st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1></div>', unsafe_allow_html=True)

# --- 6. القائمة (Menu) ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], 
    default_index=st.session_state.menu_index, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# إذا تغير المنيو يدوياً، نصفر البحث
if menu != ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"][st.session_state.menu_index]:
    st.session_state.menu_index = ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"].index(menu)
    st.session_state.search_query = ""
    st.session_state.view = "grid"

# --- 7. جلب البيانات ---
@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName', 'Developer': 'Developer'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 8. المحتوى ---
if menu in ["المشاريع", "المطورين", "Launches"]:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    col_main = active_df.columns[0]

    if st.session_state.view == "details":
        if st.button("⬅ عودة"): st.session_state.view = "grid"; st.rerun()
        item = active_df.iloc[st.session_state.current_index]
        
        # ميزة الربط: إذا كنا في صفحة مشروع، نظهر زر للانتقال للمطور
        if menu != "المطورين" and "Developer" in item:
            if st.button(f"🏢 عرض ملف المطور: {item['Developer']}", use_container_width=True):
                st.session_state.search_query = item['Developer']
                st.session_state.menu_index = 1 # ننتقل لتبويب المطورين
                st.session_state.view = "grid"
                st.rerun()
        
        for c in active_df.columns:
            st.markdown(f"<p style='color:#f59e0b; margin:0;'>{c}</p><p style='color:white; border-bottom:1px solid #333;'>{item[c]}</p>", unsafe_allow_html=True)

    else:
        # مربع البحث (مربوط بالـ Session State)
        st.session_state.search_query = st.text_input("🔍 بحث...", value=st.session_state.search_query)
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(st.session_state.search_query, case=False).any(), axis=1)] if st.session_state.search_query else active_df
        
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_c, s_c = st.columns([0.75, 0.25])
        with m_c:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    # نص الكارت
                    dev_name = r.get('Developer', '---')
                    txt = f"🏠 {r.iloc[0]}\n🏗️ المطور: {dev_name}\n📍 {r.get('Location','-')}\n💰 {r.get('Price','-')}"
                    
                    if st.button(txt, key=f"card_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, "details"
                        st.rerun()
            
            # أزرار التنقل
            st.markdown("<br>", unsafe_allow_html=True)
            b1, b2 = st.columns(2)
            with b1:
                if st.session_state.page_num > 0 and st.button("⬅ السابق", key="nav_p"):
                    st.session_state.page_num -= 1; st.rerun()
            with b2:
                if (start + ITEMS_PER_PAGE) < len(filt) and st.button("التالي ➡", key="nav_n"):
                    st.session_state.page_num += 1; st.rerun()

        with s_c:
            st.markdown("<p style='color:#f59e0b;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for sid, srow in active_df.head(6).iterrows():
                if st.button(f"📌 {str(srow.iloc[0])[:20]}", key=f"side_{sid}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = sid, "details"; st.rerun()

elif menu == "أدوات البروكر":
    st.title("🛠️ أدواتك الاحترافية")
    # (كود الحاسبة هنا)

elif menu == "المساعد الذكي":
    st.title("🤖 المساعد الذكي")
    # (كود الـ AI هنا)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO 2026</p>", unsafe_allow_html=True)
