import streamlit as st
import pandas as pd
import requests
import time
from streamlit_option_menu import option_menu

# --- 1. إعدادات الصفحة ---
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# --- إدارة الحالة ---
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'view' not in st.session_state: st.session_state.view = "grid"
if 'current_index' not in st.session_state: st.session_state.current_index = 0
if 'page_num' not in st.session_state: st.session_state.page_num = 0
if 'messages' not in st.session_state: st.session_state.messages = []

# --- 2. الروابط الأساسية ---
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
HEADER_IMG = "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1200&q=80"
BG_IMG = "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=1920&q=80"
ITEMS_PER_PAGE = 6

# --- 3. وظائف النظام ---
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

def logout():
    st.session_state.auth = False
    st.session_state.current_user = None
    st.rerun()

# --- 4. التصميم CSS المحدث ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.95), rgba(0,0,0,0.95)), url('{BG_IMG}');
        background-size: cover; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    .royal-header {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('{HEADER_IMG}');
        background-size: cover; border-bottom: 3px solid #f59e0b; padding: 40px; text-align: center; border-radius: 0 0 40px 40px;
    }}
    /* تعديل التابس لتكون واضحة */
    .stTabs [data-baseweb="tab-list"] {{ gap: 20px; border-bottom: 1px solid #333; justify-content: center; }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px; background-color: transparent !important; color: #fff !important; font-weight: bold !important;
    }}
    .stTabs [aria-selected="true"] {{ border-bottom: 3px solid #f59e0b !important; color: #f59e0b !important; }}
    
    /* الكروت */
    div.stButton > button[key*="card_"] {{
        background: #fff !important; color: #1a1a1a !important; border-right: 8px solid #f59e0b !important;
        border-radius: 12px !important; text-align: right !important; min-height: 140px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4) !important;
    }}
    .detail-card {{ background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid #333; }}
    .label-gold {{ color: #f59e0b; font-weight: bold; margin-bottom: 0px; }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول (Admin) ---
if not st.session_state.auth:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("SIGN IN", use_container_width=True):
            if p == "2026": st.session_state.auth, st.session_state.current_user = True, u; st.rerun()
    st.stop()

# جلب البيانات
df_p, df_d, df_l = load_data()

# --- 6. واجهة المنصة الرئيسية ---
st.markdown(f'<div class="royal-header"><h1 style="color:white; margin:0;">MA3LOMATI PRO</h1><p style="color:#f59e0b;">مرحباً بك: {st.session_state.current_user}</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي"], 
    icons=["briefcase", "building", "house", "robot"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

if 'last_m' not in st.session_state or menu != st.session_state.last_m:
    st.session_state.view, st.session_state.page_num, st.session_state.last_m = "grid", 0, menu

# --- 7. الأقسام المدمجة ---

if menu == "المشاريع":
    # دمج تبويب "مشاريع جديدة" داخل المشاريع
    t1, t2, t3 = st.tabs(["🏗️ قاعدة بيانات المشاريع", "🚀 مشاريع جديدة (Launches)", "⚖️ نظام المقارنة"])
    
    with t1:
        # كود عرض المشاريع العادية
        search = st.text_input("🔍 ابحث عن مشروع أو منطقة...")
        filt = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else df_p
        
        # عرض بنظام الجريد (مبسط هنا)
        if st.session_state.view == "details_p":
            if st.button("⬅ عودة"): st.session_state.view = "grid"; st.rerun()
            item = df_p.iloc[st.session_state.current_index]
            st.table(item)
        else:
            cols = st.columns(2)
            for i, (idx, r) in enumerate(filt.head(ITEMS_PER_PAGE).iterrows()):
                with cols[i%2]:
                    if st.button(f"🏠 {r[0]}\n📍 {r.get('Location','---')}", key=f"card_p_{idx}", use_container_width=True):
                        st.session_state.current_index, st.session_state.view = idx, "details_p"; st.rerun()

    with t2:
        # كود عرض اللونشات (مشاريع جديدة)
        st.markdown("<h3 style='color:#f59e0b;'>🚀 أحدث الانطلاقات في السوق</h3>", unsafe_allow_html=True)
        for idx, r in df_l.iterrows():
            with st.container(border=True):
                st.write(f"🆕 **{r[0]}**")
                st.write(f"🏗️ المطور: {r.get('Developer','---')}")
                if st.button("عرض التفاصيل كاملة", key=f"card_l_{idx}"):
                    st.info(f"تفاصيل إضافية: {r.to_dict()}")

    with t3:
        # نظام المقارنة الاحترافي
        st.markdown("<h3 style='color:#f59e0b;'>⚖️ قارن بين مشروعين لاتخاذ القرار</h3>", unsafe_allow_html=True)
        c1, c2 = st.columns(2)
        with c1: p1 = st.selectbox("اختر المشروع الأول", df_p.iloc[:,0].tolist(), key="s1")
        with c2: p2 = st.selectbox("اختر المشروع الثاني", df_p.iloc[:,0].tolist(), key="s2")
        
        if p1 and p2:
            d1 = df_p[df_p.iloc[:,0] == p1].iloc[0]
            d2 = df_p[df_p.iloc[:,0] == p2].iloc[0]
            st.markdown("---")
            # مقارنة عمود بعمود
            for col in df_p.columns[:10]: # مقارنة أول 10 خصائص
                col_a, col_b, col_c = st.columns([2,1,2])
                col_a.write(f"✅ {d1[col]}")
                col_b.markdown(f"<p style='text-align:center; color:#f59e0b;'>{col}</p>", unsafe_allow_html=True)
                col_c.write(f"✅ {d2[col]}")

elif menu == "المساعد الذكي":
    st.markdown("<h3 style='color:#f59e0b;'>🤖 مساعد معلوماتي الذكي</h3>", unsafe_allow_html=True)
    st.info("اكتب اسم أي منطقة أو شركة مطورة، وسأقوم بتحليل البيانات لك فوراً.")
    
    if prompt := st.chat_input("مثال: ما هي أرخص مشاريع التجمع؟"):
        with st.chat_message("user"): st.write(prompt)
        # منطق بحث بسيط
        res = df_p[df_p.apply(lambda r: r.astype(str).str.contains(prompt, case=False).any(), axis=1)]
        with st.chat_message("assistant"):
            if not res.empty:
                st.write(f"بناءً على تحديثات 2026، وجدت {len(res)} نتائج مطابقة لطلبك:")
                st.dataframe(res.head(5))
            else:
                st.write("عذراً، لم أجد بيانات مطابقة تماماً. حاول البحث باسم المنطقة (مثال: زايد، التجمع، الساحل).")

elif menu == "أدوات البروكر":
    # (نفس كود الحاسبة الخاص بك)
    st.subheader("🛠️ أدوات النجاح")
    # ... حاسبة الأقساط والعمولات ...

elif menu == "المطورين":
    # (نفس كود المطورين الخاص بك)
    st.dataframe(df_d)

if st.button("🚪 خروج"): logout()
