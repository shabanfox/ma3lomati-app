import streamlit as st
import pandas as pd
import feedparser
import urllib.parse
from datetime import datetime
import pytz
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة الفخمة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. جلب الوقت بتوقيت مصر (تحديث حي)
egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 3. إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'p_idx' not in st.session_state: st.session_state.p_idx = 0
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

# 4. التنسيق الجمالي المتطور (CSS)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ background-color: #050505; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    .ticker-wrap {{ width: 100%; background: #111; padding: 10px 0; overflow: hidden; white-space: nowrap; border-bottom: 2px solid #f59e0b; margin-bottom: 10px; }}
    .ticker {{ display: inline-block; animation: ticker 120s linear infinite; color: #aaa; font-size: 14px; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    div.stButton > button {{ border-radius: 12px !important; font-family: 'Cairo', sans-serif !important; transition: 0.3s !important; width: 100% !important; }}
    div.stButton > button[key*="card_"] {{
        background-color: white !important; color: #111 !important;
        min-height: 120px !important; text-align: right !important;
        font-weight: bold !important; border: none !important; margin-bottom: 15px !important;
    }}
    div.stButton > button[key*="card_"]:hover {{ transform: translateY(-5px) !important; border-right: 10px solid #f59e0b !important; box-shadow: 0 10px 20px rgba(245,158,11,0.2) !important; }}
    
    .smart-box {{ background: #111; border: 1px solid #333; padding: 30px; border-radius: 20px; border-right: 8px solid #f59e0b; color: white; margin-bottom: 20px; }}
    .tool-card {{ background: #1a1a1a; padding: 20px; border-radius: 15px; border: 1px solid #333; height: 100%; border-top: 4px solid #f59e0b; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ color: #f59e0b !important; font-weight: bold !important; }}
    </style>
""", unsafe_allow_html=True)

# 5. جلب وتنظيف البيانات (حل مشكلة KeyError)
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        
        # توحيد أسماء الأعمدة ديناميكياً
        mapping = {
            'Area': 'Location', 'الموقع': 'Location',
            'Unit Type': 'UnitType', 'النوع': 'UnitType', 'Available Units (Types)': 'UnitType',
            'Project Name': 'ProjectName', 'اسم المشروع': 'ProjectName',
            'Developer': 'Developer', 'المطور': 'Developer'
        }
        p.rename(columns=mapping, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 6. الهيدر البصري
st.markdown("""
    <div style="height: 180px; background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1512917774080-9991f1c4c750?auto=format&fit=crop&w=1500&q=80'); background-size: cover; background-position: center; border-radius: 0 0 30px 30px; display: flex; align-items: center; justify-content: center; flex-direction: column;">
        <h1 style="color: #f59e0b; font-size: 45px; margin: 0;">MA3LOMATI PRO</h1>
        <p style="color: white; font-size: 18px;">المساعد العقاري الاحترافي - مصر 2026</p>
    </div>
""", unsafe_allow_html=True)

# 7. نظام الدخول
if not st.session_state.auth:
    _, c2, _ = st.columns([1,1,1])
    with c2:
        if st.text_input("كود الدخول المباشر", type="password") == "2026": st.session_state.auth = True; st.rerun()
    st.stop()

# 8. شريط المعلومات والأخبار
st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text if "news_text" in locals() else "جاري جلب آخر أخبار السوق العقاري..."}</div></div>', unsafe_allow_html=True)
c_inf1, c_inf2, c_inf3 = st.columns(3)
c_inf1.write(f"🕒 توقيت القاهرة: {egypt_now.strftime('%I:%M %p')}")
c_inf2.write(f"📅 التاريخ: {egypt_now.strftime('%Y-%m-%d')}")
if c_inf3.button("🚪 تسجيل الخروج"): st.session_state.auth = False; st.rerun()

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "حقيبة الأدوات"], 
    icons=["robot", "search", "people", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black"}})

# 10. تفاصيل المشروع المختيار
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"<div class='smart-box'><h2>{item.get('ProjectName', 'التفاصيل')}</h2><p>📍 {item.get('Location', '---')}</p><p>🏗️ {item.get('Developer', '---')}</p><hr><p>{item.get('Payment Plan', 'تواصل للاستفسار عن نظام السداد')}</p></div>", unsafe_allow_html=True)

# --- 11. المساعد الذكي (100% مساحة) ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 المساعد الذكي للربط المالي")
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1: 
        locs = sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else []
        sel_loc = st.selectbox("المنطقة المستهدفة", ["الكل"] + locs)
    with col_f2:
        sel_type = st.selectbox("نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري", "إداري"])
    with col_f3:
        sel_bud = st.number_input("المقدم المتاح (EGP)", 0)
        
    client_wa = st.text_input("رقم واتساب العميل (إرسال المقترح بنقرة واحدة)")
    
    if st.button("🎯 استخراج أفضل الترشيحات"):
        res = df_p.copy()
        if sel_loc != "الكل": res = res[res['Location'] == sel_loc]
        if sel_type != "الكل" and 'UnitType' in res.columns: 
            res = res[res['UnitType'].astype(str).str.contains(sel_type, case=False)]
            
        if res.empty: st.warning("لم يتم العثور على نتائج مطابقة حالياً.")
        else:
            for _, r in res.head(5).iterrows():
                with st.container(border=True):
                    c_txt, c_btn = st.columns([0.8, 0.2])
                    c_txt.write(f"🏢 **{r.get('ProjectName','---')}** | المطور: {r.get('Developer','---')} | السعر يبدأ من: {r.get('Starting Price (EGP)','---')}")
                    wa_msg = f"أرشح لك مشروع {r.get('ProjectName')} في {r.get('Location')}. متاح وحدات {sel_type}. للمزيد تواصل معي."
                    wa_link = f"https://wa.me/{client_wa}?text={urllib.parse.quote(wa_msg)}"
                    c_btn.markdown(f"[📲 واتساب]({wa_link})")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 12. المشاريع (مع الاستلام الفوري) ---
elif menu == "المشاريع":
    col_p, col_ready = st.columns([0.7, 0.3])
    with col_ready:
        st.markdown("<div class='smart-box' style='border-right-color:#10b981;'><h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري</h4>", unsafe_allow_html=True)
        ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)].head(10)
        for _, r in ready_df.iterrows():
            if st.button(f"✅ {r.get('ProjectName','---')}", key=f"r_{r.get('ProjectName')}"):
                st.session_state.selected_item = r; st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_p:
        search_p = st.text_input("🔍 ابحث عن مشروع...")
        filt_p = df_p[df_p['ProjectName'].str.contains(search_p, case=False)] if search_p else df_p
        start = st.session_state.p_idx * 5
        for i, r in filt_p.iloc[start:start+5].iterrows():
            if st.button(f"🏢 {r.get('ProjectName')} | {r.get('Location')} | {r.get('Developer')}", key=f"card_p_{i}"):
                st.session_state.selected_item = r; st.rerun()

# --- 13. المطورين (أفضل 10) ---
elif menu == "المطورين":
    col_d, col_top10 = st.columns([0.7, 0.3])
    with col_top10:
        st.markdown("<div class='smart-box'><h4 style='color:#f59e0b; text-align:center;'>🏆 Top 10 Developers</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(10).iterrows():
            st.write(f"{i+1}. {r.get('Developer','---')}")
        st.markdown("</div>", unsafe_allow_html=True)
    with col_d:
        for i, r in df_d.iterrows():
            if st.button(f"🏗️ {r.get('Developer')} | المالك: {r.get('Owner','---')}", key=f"card_d_{i}"):
                st.session_state.selected_item = r; st.rerun()

# --- 14. حقيبة الأدوات (6 أدوات احترافية) ---
elif menu == "حقيبة الأدوات":
    st.title("🛠️ حقيبة البروكر الاحترافية")
    c1, c2, c3 = st.columns(3)
    c4, c5, c6 = st.columns(3)
    
    with c1:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💳 حاسبة الأقساط")
        price = st.number_input("السعر الإجمالي", 1000000)
        down = st.number_input("المقدم", 100000)
        yrs = st.slider("السنين", 1, 15, 8)
        st.metric("القسط الشهري", f"{(price-down)/(yrs*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("💰 حاسبة العمولة")
        val = st.number_input("قيمة الصفقة", 1000000)
        pct = st.slider("النسبة %", 0.5, 5.0, 1.5)
        st.metric("صافي الربح", f"{val*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📈 العائد ROI")
        buy = st.number_input("سعر الشراء", 1000000, key="roi")
        rent = st.number_input("الإيجار السنوي", 100000)
        st.metric("العائد السنوي", f"{(rent/buy)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
    with c4:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📐 محول المساحة")
        m2 = st.number_input("بالمتر", 100.0)
        st.write(f"القدم المربع: {m2 * 10.76:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c5:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📝 الضريبة والرسوم")
        t_v = st.number_input("قيمة العقار", 1000000, key="tax")
        st.write(f"ضريبة تصرفات (2.5%): {t_v*0.025:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
    with c6:
        st.markdown("<div class='tool-card'>", unsafe_allow_html=True)
        st.subheader("📊 تمويل بنكي")
        loan = st.number_input("القرض", 500000)
        st.write(f"الفائدة التقريبية (20%): {loan*0.20:,.0f} سنوي")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026</p>", unsafe_allow_html=True)
