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
if 'messages' not in st.session_state: st.session_state.messages = []
if 'search_query' not in st.session_state: st.session_state.search_query = ""

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف النظام ---
def logout():
    st.session_state.auth = False
    st.rerun()

# --- 4. التصميم الجمالي CSS (دعم الموبايل + زر خروج علوي) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    .block-container {{ padding-top: 0.5rem !important; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    /* الهيدر الملكي */
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('{HEADER_IMG}');
        background-size: cover; background-position: center; border-bottom: 3px solid #f59e0b;
        padding: 40px 20px; text-align: center; border-radius: 0 0 40px 40px; margin-bottom: 20px;
    }}
    /* الكروت المطورة */
    div.stButton > button[key*="card_"] {{
        background: #ffffff !important; color: #111 !important;
        border-right: 6px solid #f59e0b !important; border-radius: 15px !important;
        padding: 15px !important; text-align: right !important; line-height: 1.6 !important;
        min-height: 160px !important; width: 100% !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important; white-space: pre-line !important;
        font-size: 14px !important; margin-bottom: 10px !important;
    }}
    /* تحسين الموبايل */
    @media (max-width: 768px) {{
        div.stButton > button[key*="card_"] {{ min-height: 130px !important; font-size: 13px !important; }}
        .royal-header h1 {{ font-size: 24px !important; }}
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. صفحة الدخول ---
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:50px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    col_lang, _ = st.columns([0.4, 0.6])
    with col_lang: st.button("🌐 EN / AR", key="login_lang")
    pwd = st.text_input("كلمة السر", type="password", placeholder="أدخل كلمة السر لدخول 2026")
    if st.button("دخول 🚀", use_container_width=True):
        if pwd == "2026": st.session_state.auth = True; st.rerun()
        else: st.error("كلمة السر غير صحيحة")
    st.stop()

# --- 6. جلب البيانات ---
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

# --- 7. واجهة المنصة ---

# زر الخروج فوق الهيدر
c_space, c_exit = st.columns([0.88, 0.12])
with c_exit:
    if st.button("🚪 خروج", key="top_logout", use_container_width=True): logout()

st.markdown('<div class="royal-header"><h1>MA3LOMATI PRO</h1><p style="color:#f59e0b;">دليل العقارات الذكي 2026</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 8. المساعد الذكي (الذي يقرأ بياناتك) ---
if menu == "المساعد الذكي":
    st.markdown("<h3 style='color:#f59e0b;'>🤖 المساعد الذكي (خبير بياناتك)</h3>", unsafe_allow_html=True)
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])
    
    if prompt := st.chat_input("اسألني عن أي مشروع (مثلاً: تفاصيل تاج تاور)..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        
        with st.chat_message("assistant"):
            query = prompt.lower()
            # البحث في داتا المشاريع عن اسم المشروع أو المطور
            res = df_p[df_p.apply(lambda r: r.astype(str).str.contains(query, case=False).any(), axis=1)]
            
            if not res.empty:
                row = res.iloc[0]
                ans = f"✅ **إليك تفاصيل {row.get('ProjectName', 'المشروع')}:**\n\n"
                ans += f"🏗️ **المطور:** {row.get('Developer', '---')}\n"
                ans += f"📍 **المنطقة:** {row.get('Location', '---')}\n"
                ans += f"💰 **السعر:** {row.get('Start Price', '---')}\n"
                ans += f"💳 **السداد:** {row.get('Payment Plan', '---')}\n"
                ans += f"✨ **التشطيب:** {row.get('Finishing', '---')}\n"
                ans += f"📝 **معلومات إضافية:** {row.get('Detailed Info & Specifics', '---')}"
            else:
                ans = "عذراً، لم أجد هذا المشروع في قاعدة بياناتي الحالية. حاول كتابة اسم المشروع بشكل صحيح."
            
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})

# --- 9. عرض المشاريع والمطورين ---
elif menu in ["المشاريع", "المطورين", "Launches"]:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    col_main = active_df.columns[0]
    
    if st.session_state.view == "details":
        if st.button("⬅ عودة للقائمة", use_container_width=True): st.session_state.view = "grid"; st.rerun()
        item = active_df.iloc[st.session_state.current_index]
        
        # ربط المطور (الميزة التي طلبتها)
        if "Developer" in item and menu != "المطورين":
            if st.button(f"🏢 عرض ملف المطور: {item['Developer']}", use_container_width=True):
                st.session_state.search_query = item['Developer']
                st.session_state.last_m = "المطورين" # تغيير التبويب برمجياً
                st.session_state.view = "grid"
                st.rerun()
                
        for c in active_df.columns:
            st.markdown(f"<p style='color:#f59e0b; margin:0;'>{c}</p><p style='color:white; border-bottom:1px solid #333;'>{item[c]}</p>", unsafe_allow_html=True)
    
    else:
        search = st.text_input("🔍 ابحث عن أي شيء...", value=st.session_state.search_query)
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
        
        start = st.session_state.page_num * ITEMS_PER_PAGE
        disp = filt.iloc[start : start + ITEMS_PER_PAGE]
        
        m_col, s_col = st.columns([0.75, 0.25])
        with m_col:
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    # عرض تفاصيل الكارت (اسم، مطور، موقع، سعر)
                    card_txt = f"🏠 {r.iloc[0]}\n🏗️ {r.get('Developer','-')}\n📍 {r.get('Location','-')}\n💰 {r.get('Start Price', r.get('Price','-'))}"
                    if st.button(card_txt, key=f"card_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            # أزرار التنقل (ملتصقة بالكروت)
            st.markdown("<br>", unsafe_allow_html=True)
            n1, n2 = st.columns(2)
            with n1:
                if st.session_state.page_num > 0 and st.button("⬅ السابق", key="nav_prev", use_container_width=True):
                    st.session_state.page_num -= 1; st.rerun()
            with n2:
                if (start + ITEMS_PER_PAGE) < len(filt) and st.button("التالي ➡", key="nav_next", use_container_width=True):
                    st.session_state.page_num += 1; st.rerun()

        with s_col:
            st.markdown("<p style='color:#f59e0b;'>🏆 مقترحات</p>", unsafe_allow_html=True)
            for sid, srow in active_df.head(6).iterrows():
                if st.button(f"📌 {str(srow.iloc[0])[:20]}", key=f"side_{sid}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = sid, "details"; st.rerun()

elif menu == "أدوات البروكر":
    st.subheader("🛠️ الحاسبة العقارية")
    v = st.number_input("إجمالي السعر", value=1000000)
    dp = st.slider("المقدم (%)", 0, 100, 10)
    y = st.number_input("السنين", 1, 20, 8)
    st.metric("القسط الشهري المتوقع", f"{(v-(v*dp/100))/(y*12):,.0f}")

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
