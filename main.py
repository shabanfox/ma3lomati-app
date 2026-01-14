import streamlit as st
import pandas as pd
import math
import feedparser
import urllib.parse
from datetime import datetime
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="Ma3lomati PRO 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0

# 3. جلب الأخبار
@st.cache_data(ttl=1800)
def get_real_news():
    try:
        rss_url = "https://www.youm7.com/rss/SectionRss?SectionID=297"
        feed = feedparser.parse(rss_url)
        return "  •  ".join([item.title for item in feed.entries[:10]])
    except: return "سوق العقارات المصري: متابعة مستمرة لعام 2026."

news_text = get_real_news()

# 4. التنسيق الجمالي (CSS) - التركيز على الشبكة Grid
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    body, [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    .block-container {{ padding-top: 0rem !important; }}
    header {{ visibility: hidden; }}
    
    .luxury-header {{
        background: rgba(15, 15, 15, 0.9); border-bottom: 2px solid #f59e0b;
        padding: 15px 40px; display: flex; justify-content: space-between; align-items: center;
        border-radius: 0 0 25px 25px; margin-bottom: 10px;
    }}
    .logo-text {{ color: #f59e0b; font-weight: 900; font-size: 24px; }}
    
    /* شريط الأخبار */
    .ticker-wrap {{ width: 100%; background: #111; padding: 8px 0; overflow: hidden; white-space: nowrap; border-bottom: 1px solid #222; }}
    .ticker {{ display: inline-block; animation: ticker 150s linear infinite; color: #ccc; font-size: 13px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    /* الكروت الشبكية */
    .grid-card {{
        background: #111; border: 1px solid #222; border-right: 5px solid #f59e0b;
        border-radius: 12px; padding: 15px; height: 200px; margin-bottom: 20px;
        display: flex; flex-direction: column; justify-content: space-between;
    }}
    .ready-sidebar {{
        background: #0f0f0f; border: 1px solid #222; border-radius: 15px; padding: 15px;
        height: 85vh; overflow-y: auto; border-top: 4px solid #10b981;
    }}
    .ready-item {{
        background: #161616; border-right: 4px solid #10b981; padding: 12px; border-radius: 8px; margin-bottom: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب البيانات (تحويل الروابط لـ CSV لتعمل الداتا)
@st.cache_data(ttl=60)
def load_data():
    # تم تعديل الروابط لتكون قابلة للقراءة بصيغة CSV
    sheet_id = "1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1"
    u_p = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
    u_d = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=1626090535" # تأكد من الـ GID الصحيح من الشيت
    
    try:
        p = pd.read_csv(u_p).fillna("").astype(str)
        d = pd.read_csv(u_d).fillna("").astype(str)
        p.columns = [c.strip() for c in p.columns]
        d.columns = [c.strip() for c in d.columns]
        return p, d
    except:
        # لو الرابط فيه مشكلة، نستخدم رابط الـ pub المباشر
        u_alt = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
        p = pd.read_csv(u_alt).fillna("").astype(str)
        return p, pd.DataFrame()

df_p, df_d = load_data()

# 6. نظام الدخول
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; color:#f59e0b; padding-top:100px;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
    if st.text_input("Passcode", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# الهيدر
now = datetime.now().strftime("%H:%M")
st.markdown(f'<div class="luxury-header"><div class="logo-text">MA3LOMATI PRO</div><div style="color:#f59e0b;">⌚ {now}</div></div>', unsafe_allow_html=True)
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)

menu = option_menu(None, ["الأدوات", "المشاريع", "المطورين"], icons=["tools", "building", "person-vcard"], orientation="horizontal")

# التقسيم 70% و 30%
col_main, col_side = st.columns([0.7, 0.3])

# --- الجانب الأيمن: استلام فوري (30%) ---
with col_side:
    st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري فقط</h4>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    # فلترة الاستلام الفوري
    ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
    for _, row in ready_df.iterrows():
        st.markdown(f"""
            <div class="ready-item">
                <b style="color:#f59e0b;">{row.get('Project Name', 'مشروع')}</b><br>
                <small>📍 {row.get('Area', 'غير محدد')}</small>
            </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الأيسر: الشكل الشبكي (70%) ---
with col_main:
    if menu == "المشاريع":
        search = st.text_input("🔍 بحث سـريع...")
        filtered = df_p.copy()
        if search: filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        limit = 6
        page_data = filtered.iloc[st.session_state.p_idx*limit : (st.session_state.p_idx+1)*limit]
        
        # العرض الشبكي الصارم (Grid)
        for i in range(0, len(page_data), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_data):
                    r = page_data.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card">
                                <div>
                                    <h3 style="color:#f59e0b; margin:0; font-size:18px;">{r.get('Project Name', 'اسم المشروع')}</h3>
                                    <p style="color:#ccc; font-size:13px; margin-top:10px;">📍 {r.get('Area', 'المنطقة')}</p>
                                    <p style="color:#aaa; font-size:12px;">🏢 المطور: {r.get('Developer', 'غير مسجل')}</p>
                                </div>
                                <div style="font-size:11px; color:#f59e0b; border-top:1px solid #333; padding-top:5px;">
                                    📏 المساحة: {r.get('Project Area', 'N/A')}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("تفاصيل إضافية"):
                            st.write(f"✨ المميزات: {r.get('Project Features', 'اتصل بنا')}")

        st.markdown("---")
        c1, c2 = st.columns(2)
        if c1.button("التالي ⬅️"): st.session_state.p_idx += 1; st.rerun()
        if c2.button("➡️ السابق"): st.session_state.p_idx = max(0, st.session_state.p_idx-1); st.rerun()

    elif menu == "المطورين":
        # عرض المطورين بشكل شبكي أيضاً
        for i in range(0, len(df_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(df_d):
                    r = df_d.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"""
                            <div class="grid-card" style="height:150px;">
                                <h4 style="color:#f59e0b;">{r.get('Developer', 'شركة تطوير')}</h4>
                                <p style="font-size:12px;">👤 المالك: {r.get('Owner', 'غير معروف')}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        with st.expander("سابقة الأعمال"):
                            st.write(r.get('Detailed_Info', 'لا توجد بيانات حالياً'))

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ الأدوات والبحث الذكي</h2>")
        radar = st.text_input("🕵️ رادار البحث (خارج الشيت)...")
        if radar:
            st.link_button(f"البحث عن {radar} في جوجل", f"https://www.google.com/search?q={urllib.parse.quote(radar + ' عقارات مصر')}")
        
        t = st.tabs(["🧮 القسط", "📈 ROI", "📐 مساحات"])
        with t[0]:
            p = st.number_input("السعر", 1000000); d = st.number_input("المقدم", 0); y = st.slider("السنين", 1, 15, 8)
            st.metric("القسط الشهري", f"{(p-d)/(y*12):,.0f} ج.م")
        with t[1]:
            rent = st.number_input("الإيجار", 10000)
            st.metric("العائد السنوي", f"{(rent*12/p)*100:.2f}%")
        with t[2]:
            m = st.number_input("المتر المربع", 100.0)
            st.write(f"القدم المربع: {m*10.76:,.2f}")

if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()
