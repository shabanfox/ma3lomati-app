import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة (Session State)
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار العقارية
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."
    except: return "MA3LOMATI PRO: منصتك العقارية الأولى في التجمع الخامس."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 20px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    div.stButton > button {
        background-color: white !important; color: #111 !important;
        border-radius: 12px !important; width: 100% !important;
        text-align: right !important; font-weight: bold !important;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3) !important;
    }
    .stSelectbox label, .stTextInput label { color: #f59e0b !important; font-weight: bold !important; }
    .project-card-custom {
        background: #111; border-right: 5px solid #f59e0b; padding: 20px; border-radius: 15px; color: white; margin-bottom: 15px; border: 1px solid #222;
    }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة تسجيل الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b; font-size:50px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1,1])
    with c2:
        pass_input = st.text_input("كود الدخول المباشر", type="password")
        if pass_input == "2026": 
            st.session_state.auth = True
            st.rerun()
    st.stop()

# 6. جلب وتنظيف البيانات (الرابط الخاص بك)
@st.cache_data(ttl=10)
def load_data():
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        df = df.fillna("---")
        
        # دمج المطورين لو فيه اختلاف بسيط
        if 'Developer' in df.columns:
            df['Developer'] = df['Developer'].astype(str).apply(lambda x: " ".join(x.split()).strip())
        
        # حذف المشاريع المكررة
        if 'Project Name' in df.columns:
            df['Project Name'] = df['Project Name'].astype(str).str.strip()
            df = df.drop_duplicates(subset=['Project Name', 'Developer'], keep='first')
        return df
    except:
        return pd.DataFrame()

df_all = load_data()

# 7. الهيدر
now = datetime.now()
h_col1, h_col2, h_col3 = st.columns([1.5, 2, 1])
with h_col1: st.markdown('<div style="color:#f59e0b; font-weight:900; font-size:28px;">MA3LOMATI PRO</div>', unsafe_allow_html=True)
with h_col2:
    st.markdown(f"<div style='text-align:center; color:white;'>📅 {now.strftime('%Y-%m-%d')} | 🕒 {now.strftime('%I:%M %p')}</div>", unsafe_allow_html=True)
with h_col3:
    if st.button("🚪 خروج"): 
        st.session_state.auth = False
        st.rerun()

st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

# 8. القائمة الرئيسية
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "building-up", "person-badge", "briefcase"], default_index=1, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 9. عرض المحتوى
if df_all.empty:
    st.error("⚠️ الداتا مش موجودة. تأكد من عمل Publish to Web بصيغة CSV للشيت.")
else:
    main_col, side_col = st.columns([0.78, 0.22])

    with side_col:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>⚡ صفقات ريسيل</h4>", unsafe_allow_html=True)
        if 'Sales Type' in df_all.columns:
            resale = df_all[df_all['Sales Type'].str.contains('ريسيل', na=False)].head(5)
            for _, row in resale.iterrows():
                st.markdown(f'<div style="background:#111; border-right:3px solid #10b981; padding:8px; border-radius:10px; margin-bottom:5px; font-size:12px; color:white;">{row["Project Name"]}</div>', unsafe_allow_html=True)

    with main_col:
        if st.session_state.selected_item is not None:
            if st.button("⬅️ عودة"): 
                st.session_state.selected_item = None
                st.rerun()
            item = st.session_state.selected_item
            st.markdown(f"""<div class="project-card-custom"><h2>{item.get('Project Name','---')}</h2><hr>
            <p>🏗️ المطور: {item.get('Developer','---')}</p>
            <p>📍 الموقع: {item.get('Location','---')}</p>
            <p>💰 السعر: {item.get('Starting Price (EGP)','---')}</p>
            <p>💳 السداد: {item.get('Payment Plan','---')}</p></div>""", unsafe_allow_html=True)

        elif menu == "المشاريع":
            f1, f2 = st.columns(2)
            s_name = f1.text_input("🔍 ابحث عن مشروع")
            s_loc = f2.selectbox("📍 المنطقة", ["الكل"] + sorted(df_all['Location'].unique().tolist()) if 'Location' in df_all.columns else ["الكل"])
            
            dff = df_all.copy()
            if s_name: dff = dff[dff['Project Name'].str.contains(s_name, case=False)]
            if s_loc != "الكل": dff = dff[dff['Location'] == s_loc]

            limit = 6
            start = st.session_state.p_idx * limit
            page = dff.iloc[start:start+limit]
            
            for i in range(0, len(page), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i+j < len(page):
                        row = page.iloc[i+j]
                        if cols[j].button(f"🏢 {row['Project Name']}\n🏗️ {row['Developer']}", key=f"p_{start+i+j}"):
                            st.session_state.selected_item = row
                            st.rerun()
            
            st.markdown("---")
            c_prev, _, c_next = st.columns([1,2,1])
            if st.session_state.p_idx > 0:
                if c_prev.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
            if start + limit < len(dff):
                if c_next.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

        elif menu == "المطورين":
            dev_list = sorted(df_all['Developer'].unique().tolist())
            for d in dev_list:
                with st.expander(f"🏢 {d}"):
                    p_list = df_all[df_all['Developer'] == d]['Project Name'].tolist()
                    st.write("المشاريع:", ", ".join(p_list))

        elif menu == "المساعد الذكي":
            st.write("🤖 أدخل بيانات العميل لترشيح المشاريع")
            c1, c2 = st.columns(2)
            c1.text_input("رقم الواتساب")
            if c2.button("توليد رسالة"): st.success("جاهز للإرسال!")

        elif menu == "أدوات البروكر":
            st.subheader("💳 حاسبة الأقساط")
            price = st.number_input("السعر", 1000000)
            down = st.number_input("المقدم", 100000)
            st.write(f"المتبقي: {price-down:,.0f}")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
