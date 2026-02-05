import streamlit as st
import pandas as pd
import requests
import feedparser
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- إدارة الحالة عبر الـ URL ---
params = st.query_params
if 'auth' not in st.session_state:
    if params.get("logged_in") == "true":
        st.session_state.auth = True
        st.session_state.current_user = params.get("user", "User")
    else:
        st.session_state.auth = False

if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 2. الروابط والبيانات ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- وظائف مساعدة ---
def logout():
    st.session_state.auth = False
    st.session_state.current_user = None
    st.query_params.clear()
    st.rerun()

@st.cache_data(ttl=60)
def load_data():
    U_P = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    U_D = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv"
    U_L = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        p, d, l = pd.read_csv(U_P), pd.read_csv(U_D), pd.read_csv(U_L)
        for df in [p, d, l]: 
            df.columns = [c.strip() for c in df.columns]
            df.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True, errors="ignore")
        return p.fillna("---"), d.fillna("---"), l.fillna("---")
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_data()

# --- 3. التصميم الجمالي CSS ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 45px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    .detail-card {{ background: rgba(20, 20, 20, 0.9); padding: 25px; border-radius: 20px; border-top: 5px solid #f59e0b; color: white; border: 1px solid #333; margin-bottom:20px; }}
    .label-gold {{ color: #f59e0b; font-weight: 900; font-size: 16px; margin-top: 10px; }}
    .val-white {{ color: white; font-size: 18px; border-bottom: 1px solid #333; padding-bottom:5px; margin-bottom: 10px; }}
    
    /* أزرار الكروت الرئيسية */
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 140px !important; text-align: right !important;
        font-weight: bold !important; font-size: 15px !important;
        border: none !important; margin-bottom: 10px !important;
        display: block !important; width: 100% !important;
        border-radius: 12px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 8px solid #f59e0b !important; }}
    
    /* أزرار المقترحات الجانبية */
    div.stButton > button[key*="side_"] {{
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #eee !important; border: none !important;
        border-right: 3px solid #f59e0b !important;
        text-align: right !important; font-size: 13px !important;
        margin-bottom: 5px !important; border-radius: 8px !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 4. التحقق من تسجيل الدخول ---
if not st.session_state.auth:
    st.warning("يرجى تسجيل الدخول أولاً")
    st.stop()

# --- 5. الهيدر والأزرار العلوية ---
st.markdown(f"""
    <div class="royal-header">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

c_top1, c_top2 = st.columns([0.85, 0.15])
with c_top2:
    st.button("🌐 EN/AR", key="lang_btn", use_container_width=True)
    if st.button("🚪 خروج", key="exit_btn", use_container_width=True): logout()

# --- 6. القائمة الرئيسية ---
menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

if 'last_menu' not in st.session_state or menu != st.session_state.last_menu:
    st.session_state.view, st.session_state.page_num, st.session_state.last_menu = "grid", 0, menu

# --- 7. محتوى الأقسام ---
if menu == "أدوات البروكر":
    st.markdown("<h2 style='text-align:center; color:#f59e0b;'>🛠️ أدوات البروكر</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("💳 حساب القسط")
            v = st.number_input("إجمالي السعر", value=1000000, step=100000)
            down_pct = st.number_input("نسبة المقدم (%)", min_value=0, max_value=100, value=10)
            y = st.number_input("عدد السنين", min_value=1, max_value=20, value=8)
            down_val = v * (down_pct / 100)
            rem = v - down_val
            st.markdown(f"<p style='color:#f59e0b;'>قيمة المقدم: {down_val:,.0f}</p>", unsafe_allow_html=True)
            st.metric("القسط الشهري", f"{rem/(y*12):,.0f}" if y > 0 else "0")
    with c2:
        with st.container(border=True):
            st.subheader("💰 العمولة")
            deal = st.number_input("قيمة الصفقة", value=1000000, step=100000)
            pct = st.number_input("النسبة (%)", min_value=0.0, max_value=10.0, value=2.5, step=0.1)
            st.metric("صافي الربح", f"{deal*(pct/100):,.0f}")
    with c3:
        with st.container(border=True):
            st.subheader("📈 العائد ROI")
            buy = st.number_input("سعر الشراء", value=1000000, step=100000)
            rent = st.number_input("الإيجار السنوي", value=100000, step=10000)
            st.metric("نسبة العائد", f"{(rent/buy)*100:,.1f}%" if buy > 0 else "0%")

elif menu == "المساعد الذكي":
    st.markdown("<div class='detail-card'><h3>🤖 مساعد معلوماتي الذكي</h3></div>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    if pmt := st.chat_input("اسألني عن أي مشروع أو مطور..."):
        st.session_state.messages.append({"role": "user", "content": pmt})
        st.session_state.messages.append({"role": "assistant", "content": "جاري مراجعة قواعد البيانات..."})
        st.rerun()

else:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    if active_df.empty: st.error("لا توجد بيانات متاحة حالياً")
    else:
        col_main = active_df.columns[0]
        
        # --- صفحة التفاصيل ---
        if st.session_state.view == "details":
            item = active_df.iloc[st.session_state.current_index]
            if st.button("⬅ عودة للقائمة", use_container_width=True):
                st.session_state.view = "grid"; st.rerun()
            
            st.markdown(f"<h2 style='color:#f59e0b; text-align:center;'>{item[col_main]}</h2>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            all_cols = active_df.columns
            n = len(all_cols)
            for i, col_set in enumerate([all_cols[:n//3+1], all_cols[n//3+1:2*n//3+1], all_cols[2*n//3+1:]]):
                with [c1, c2, c3][i]:
                    h = '<div class="detail-card">'
                    for k in col_set: h += f'<p class="label-gold">{k}</p><p class="val-white">{item[k]}</p>'
                    st.markdown(h+'</div>', unsafe_allow_html=True)
        
        # --- صفحة الشبكة (الرئيسية) ---
        else:
            search = st.text_input("🔍 بحث سريع...")
            filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
            
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            main_c, side_c = st.columns([0.75, 0.25])
            
            with main_c:
                grid = st.columns(2)
                for i, (idx, r) in enumerate(disp.iterrows()):
                    with grid[i%2]:
                        name = r[col_main]
                        loc = r.get('Location', '---')
                        dev = r.get('Developer', '---')
                        # زر الكارت الرئيسي
                        if st.button(f"🏢 {name}\n📍 {loc}\n🏗️ {dev}", key=f"card_{idx}"):
                            st.session_state.current_index, st.session_state.view = idx, "details"
                            st.rerun()
            
            with side_c:
                st.markdown("<p style='color:#f59e0b; font-weight:bold; font-size:18px; border-bottom:1px solid #333;'>🏆 مقترحات</p>", unsafe_allow_html=True)
                # عرض أول 8 مقترحات كأزرار تفاعلية
                suggestions = active_df.head(8)
                for s_idx, s_row in suggestions.iterrows():
                    s_name = str(s_row[col_main])[:30]
                    # زر المقترح الجانبي
                    if st.button(f"📌 {s_name}", key=f"side_{s_idx}", use_container_width=True):
                        st.session_state.current_index = s_idx
                        st.session_state.view = "details"
                        st.rerun()

            # --- الترقيم (Pagination) ---
            st.write("---")
            p1, p_info, p2 = st.columns([1, 2, 1])
            with p1:
                if st.session_state.page_num > 0:
                    if st.button("⬅ السابق", use_container_width=True):
                        st.session_state.page_num -= 1; st.rerun()
            with p_info:
                st.markdown(f"<p style='text-align:center; color:#888;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            with p2:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي ➡", use_container_width=True):
                        st.session_state.page_num += 1; st.rerun()

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | جميع الحقوق محفوظة</p>", unsafe_allow_html=True)
