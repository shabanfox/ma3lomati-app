import streamlit as st
import pandas as pd
import feedparser
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297" 
        feed = feedparser.parse(rss_url)
        news = [item.title for item in feed.entries[:10]]
        return "  •  ".join(news) if news else "جاري تحديث الأخبار العقارية..."
    except: return "سوق العقارات المصري: متابعة مستمرة لآخر المستجدات."

news_text = get_real_news()

# 4. التنسيق (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container { padding-top: 0rem !important; }
    header, [data-testid="stHeader"] { visibility: hidden; display: none; }
    [data-testid="stAppViewContainer"] { background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }
    
    .luxury-header {
        background: rgba(15, 15, 15, 0.9); backdrop-filter: blur(10px);
        border-bottom: 2px solid #f59e0b; padding: 15px 30px;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 999; border-radius: 0 0 25px 25px; margin-bottom: 15px;
    }
    .logo-text { color: #f59e0b; font-weight: 900; font-size: 24px; }
    
    .ticker-wrap { width: 100%; background: transparent; padding: 5px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; margin-bottom: 10px; }
    .ticker { display: inline-block; animation: ticker 150s linear infinite; color: #aaa; font-size: 13px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    /* ستايل الكروت المحسن */
    div.stButton > button[key*="card_p_"] {
        background-color: white !important;
        color: #111 !important;
        border: 2px solid #eee !important;
        border-radius: 15px !important;
        width: 100% !important;
        min-height: 250px !important;
        padding: 20px !important;
        text-align: right !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
    }
    .detail-box { background: #111; padding: 25px; border-radius: 15px; border-right: 5px solid #f59e0b; color: white; }
    </style>
""", unsafe_allow_html=True)

# 5. شاشة الدخول
if not st.session_state.auth:
    st.markdown("<div style='text-align:center; padding-top:100px;'><h1 style='color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    _, c2, _ = st.columns([1,1.5,1])
    with c2:
        passcode = st.text_input("Passcode", type="password")
        if st.button("دخول"):
            if passcode == "2026": 
                st.session_state.auth = True; st.rerun()
    st.stop()

# 6. جلب البيانات (مع معالجة الأسماء)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("غير متوفر")
        d = pd.read_csv(u_d).fillna("غير متوفر")
        # تنظيف مسافات أسماء الأعمدة لضمان عملها
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# الهيدر
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#aaa; font-size:12px;">📅 {datetime.now().strftime("%Y-%m-%d")}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    default_index=1, orientation="horizontal",
    styles={"container": {"background-color": "#0a0a0a", "padding": "0"}, "nav-link-selected": {"background-color": "#f59e0b", "color": "black"}}
)

main_col, side_col = st.columns([0.75, 0.25])

with side_col:
    st.markdown("<p style='color:#10b981; text-align:center; font-weight:bold;'>🔑 استلام فوري</p>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    if not df_p.empty:
        # البحث في كل الأعمدة عن كلمة فوري
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        for _, r in ready.head(10).iterrows():
            st.markdown(f'<div style="background:#161616; padding:10px; border-radius:8px; margin-bottom:5px; border-right:3px solid #10b981;"><div style="color:#f59e0b; font-size:13px;">{r.get("Project Name", "مشاريع")}</div></div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # مكان زر الخروج الجديد (في السايدبار لكنه ظاهر)
    st.markdown("---")
    if st.button("🚪 تسجيل الخروج", use_container_width=True):
        st.session_state.auth = False; st.rerun()

with main_col:
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
        
        st.markdown(f"""
            <div class="detail-box">
                <h1 style="color:#f59e0b;">{item.get('Project Name', 'تفاصيل المشروع')}</h1>
                <p>📍 المنطقة: {item.get('Area', 'غير محدد')}</p>
                <div style="background:#1a1a1a; padding:15px; border-radius:10px; margin:15px 0; border:1px solid #333;">
                    <b style="color:#f59e0b;">📍 الموقع التفصيلي:</b><br>{item.get('Detailed Location', 'راجع الإدارة')}
                </div>
                <div style="line-height:1.8;">{item.get('Project Features', 'لا توجد بيانات إضافية.')}</div>
            </div>
        """, unsafe_allow_html=True)

    elif menu == "المشاريع":
        # الفلاتر
        c1, c2, c3 = st.columns(3)
        with c1:
            cat_list = ["الكل"] + sorted(df_p['Category'].unique().tolist()) if 'Category' in df_p.columns else ["الكل"]
            s_cat = st.selectbox("🏠 الفئة", cat_list)
        with c2:
            area_list = ["الكل"] + sorted(df_p['Area'].unique().tolist()) if 'Area' in df_p.columns else ["الكل"]
            s_area = st.selectbox("📍 المنطقة", area_list)
        with c3:
            s_name = st.text_input("🔍 اسم المشروع")

        # الفلترة الفعلية
        dff = df_p.copy()
        if s_cat != "الكل": dff = dff[dff['Category'] == s_cat]
        if s_area != "الكل": dff = dff[dff['Area'] == s_area]
        if s_name: dff = dff[dff['Project Name'].str.contains(s_name, case=False)]

        # عرض الكروت
        if dff.empty:
            st.warning("لا توجد مشاريع تطابق هذا البحث. تأكد من أسماء الأعمدة في الشيت.")
        else:
            limit = 6
            curr = dff.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
            
            for i, (_, row) in enumerate(curr.iterrows()):
                if i % 2 == 0: cols = st.columns(2)
                with cols[i % 2]:
                    # تصميم الكارت النصي
                    txt = f"🏢 {row.get('Project Name')}\n📍 {row.get('Area')}\n🏗️ {row.get('Developer')}\n🏠 {row.get('Category', '')}\n\n📍 {str(row.get('Detailed Location'))[:45]}..."
                    if st.button(txt, key=f"card_p_{i}"):
                        st.session_state.selected_item = row; st.rerun()
            
            # التنقل
            st.markdown("---")
            p1, p2 = st.columns(2)
            if st.session_state.p_idx > 0:
                if p1.button("السابق"): st.session_state.p_idx -= 1; st.rerun()
            if (st.session_state.p_idx + 1) * limit < len(dff):
                if p2.button("التالي"): st.session_state.p_idx += 1; st.rerun()

    elif menu == "المطورين":
        st.write("قائمة المطورين...") # طبق نفس منطق المشاريع هنا

    elif menu == "الأدوات":
        st.write("حاسبة الأقساط...")
