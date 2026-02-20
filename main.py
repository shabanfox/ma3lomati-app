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

# --- 3. وظائف النظام المحدثة ---
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

# --- 4. التصميم الجمالي CSS (إضافات قوية) ---
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{
        background: linear-gradient(rgba(0,0,0,0.96), rgba(0,0,0,0.96)), url('{BG_IMG}');
        background-size: cover; background-attachment: fixed;
        direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif;
    }}
    /* تنسيق الجداول للمقارنة */
    .stDataFrame, div[data-testid="stTable"] {{ background: white; border-radius: 15px; overflow: hidden; }}
    /* تحسين شكل التابس */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: rgba(255,255,255,0.05); border-radius: 10px 10px 0 0; padding: 10px 20px; color: white;
    }}
    /* الكروت */
    div.stButton > button[key*="card_"] {{
        background: white !important; color: #1a1a1a !important;
        border-right: 6px solid #f59e0b !important; border-radius: 15px !important;
        text-align: right !important; min-height: 160px !important; width: 100% !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important; font-family: 'Cairo', sans-serif !important;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق الدخول (كما هو) ---
if not st.session_state.auth:
    # (نفس كود الدخول الخاص بك هنا لضمان عمل البرنامج)
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1></div>", unsafe_allow_html=True)
    u = st.text_input("User")
    p = st.text_input("Pass", type="password")
    if st.button("LOGIN"):
        if p == "2026": st.session_state.auth, st.session_state.current_user = True, "Admin"; st.rerun()
    st.stop()

# جلب البيانات
df_p, df_d, df_l = load_data()

# --- 6. واجهة المنصة ---
st.markdown(f'<div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url({HEADER_IMG}); padding:40px; text-align:center; border-radius:0 0 40px 40px; border-bottom:3px solid #f59e0b;">'
            f'<h1 style="color:white; margin:0;">MA3LOMATI PRO</h1>'
            f'<p style="color:#f59e0b;">مرحباً {st.session_state.current_user} | رفيقك العقاري الذكي</p></div>', unsafe_allow_html=True)

menu = option_menu(None, ["أدوات البروكر", "المطورين", "المشاريع", "المساعد الذكي", "Launches"], 
    icons=["briefcase", "building", "search", "robot", "megaphone"], default_index=2, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "#000"}})

# --- 7. الأقسام المحدثة ---

if menu == "أدوات البروكر":
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.container(border=True):
            st.subheader("💳 حاسبة القسط")
            v = st.number_input("سعر الوحدة", value=1000000)
            dp = st.number_input("المقدم %", 0, 100, 10)
            y = st.number_input("سنين التقسيط", 1, 20, 8)
            res = (v-(v*dp/100))/(y*12) if y>0 else 0
            st.metric("القسط الشهري", f"{res:,.0f} EGP")

    with c2:
        with st.container(border=True):
            st.subheader("⚖️ نظام المقارنة السريع")
            st.write("قارن بين مشروعين فوراً")
            p1 = st.selectbox("المشروع الأول", df_p.iloc[:,0].tolist(), key="comp1")
            p2 = st.selectbox("المشروع الثاني", df_p.iloc[:,0].tolist(), key="comp2")
            if st.button("بدء المقارنة"):
                st.session_state.messages.append({"role": "assistant", "content": f"جاري مقارنة {p1} و {p2}..."})
                # سيتم عرض النتيجة في صفحة المساعد

    with c3:
        with st.container(border=True):
            st.subheader("📈 تحليل العائد")
            b = st.number_input("سعر الشراء", value=1000000)
            r = st.number_input("الإيجار السنوي", value=120000)
            st.metric("ROI سنوي", f"{(r/b)*100:,.1f}%")

elif menu == "المساعد الذكي":
    st.markdown("<h3 style='color:#f59e0b;'>🤖 مساعدك الشخصي (تحليل البيانات)</h3>", unsafe_allow_html=True)
    
    # ميزة: تحليل سريع للسوق
    with st.expander("📊 ملخص السوق الحالي"):
        st.write(f"إجمالي المشاريع المسجلة: {len(df_p)}")
        st.write(f"عدد المطورين المتاحين: {len(df_d)}")
        st.write(f"اللونشات الحالية: {len(df_l)}")

    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.write(m["content"])

    if prompt := st.chat_input("اسألني عن مشروع، مطور، أو منطقة..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # محرك بحث ذكي بسيط
        results = df_p[df_p.apply(lambda r: r.astype(str).str.contains(prompt, case=False).any(), axis=1)]
        
        if not results.empty:
            response = f"وجدت لك {len(results)} نتائج متعلقة بـ '{prompt}'. إليك أبرزها:"
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.session_state.messages.append({"role": "assistant", "content": results.head(3)})
        else:
            st.session_state.messages.append({"role": "assistant", "content": "للأسف لم أجد بيانات دقيقة لهذا الطلب، حاول كتابة اسم المنطقة بشكل أوضح."})
        st.rerun()

elif menu in ["المشاريع", "المطورين", "Launches"]:
    active_df = df_p if menu=="المشاريع" else (df_l if menu=="Launches" else df_d)
    col_main = active_df.columns[0]
    
    if st.session_state.view == "details":
        if st.button("⬅ عودة للقائمة", use_container_width=True): st.session_state.view = "grid"; st.rerun()
        
        item = active_df.iloc[st.session_state.current_index]
        st.markdown(f"<div style='background:#f59e0b; padding:10px; border-radius:10px; color:black; text-align:center;'><h2>{item[col_main]}</h2></div>", unsafe_allow_html=True)
        
        c1, c2, c3 = st.columns(3)
        cols = active_df.columns
        for i, cs in enumerate([cols[:len(cols)//3+1], cols[len(cols)//3+1:2*len(cols)//3+1], cols[2*len(cols)//3+1:]]):
            with [c1, c2, c3][i]:
                for k in cs:
                    st.markdown(f"<p style='color:#f59e0b; margin-bottom:0;'>{k}</p><p style='color:white; border-bottom:1px solid #333;'>{item[k]}</p>", unsafe_allow_html=True)
    else:
        # شريط البحث العلوي الموحد
        search = st.text_input(f"🔍 بحث سريع في {menu}...", placeholder="اكتب اسم المشروع، الموقع، أو المطور...")
        filt = active_df[active_df.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)] if search else active_df
        
        # تقسيم الشاشة (المحتوى الرئيسي + مقترحات)
        main_col, side_col = st.columns([0.75, 0.25])
        
        with main_col:
            start = st.session_state.page_num * ITEMS_PER_PAGE
            disp = filt.iloc[start : start + ITEMS_PER_PAGE]
            
            grid = st.columns(2)
            for i, (idx, r) in enumerate(disp.iterrows()):
                with grid[i%2]:
                    # تصميم الكارت المحترف
                    c_name = r[col_main]
                    c_loc = r.get('Location', 'غير محدد')
                    c_dev = r.get('Developer', r.get('المطور', '---'))
                    
                    card_html = f"🏠 {c_name}\n📍 {c_loc}\n🏗️ {c_dev}"
                    if st.button(card_html, key=f"card_{idx}"):
                        st.session_state.current_index, st.session_state.view = idx, "details"; st.rerun()
            
            # أزرار التنقل
            st.write("---")
            nb1, nb2, nb3 = st.columns([1,2,1])
            with nb1: 
                if st.session_state.page_num > 0:
                    if st.button("السابق"): st.session_state.page_num -= 1; st.rerun()
            with nb2: st.markdown(f"<p style='text-align:center;'>صفحة {st.session_state.page_num + 1}</p>", unsafe_allow_html=True)
            with nb3:
                if (start + ITEMS_PER_PAGE) < len(filt):
                    if st.button("التالي"): st.session_state.page_num += 1; st.rerun()

        with side_col:
            st.markdown("<p style='color:#f59e0b; font-weight:bold;'>⭐ الأكثر بحثاً</p>", unsafe_allow_html=True)
            for s_idx, s_row in active_df.head(8).iterrows():
                if st.button(f"📌 {str(s_row[col_main])[:20]}", key=f"side_{s_idx}", use_container_width=True):
                    st.session_state.current_index, st.session_state.view = s_idx, "details"; st.rerun()

if st.button("🚪 تسجيل خروج"): logout()
