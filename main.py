import streamlit as st
import pandas as pd
import requests
import feedparser
import urllib.parse
from datetime import datetime
import pytz
import time
from streamlit_option_menu import option_menu

# 1. إعدادات الصفحة
st.set_page_config(page_title="MA3LOMATI PRO | 2026", layout="wide", initial_sidebar_state="collapsed")

# 2. روابط البيانات (تأكد من إضافة رابط شيت اللونشات الجديد هنا)
SCRIPT_URL = "https://script.google.com/macros/s/AKfycbz2bZa-5WpgxRyhwe5506qnu9WTB6oUwlCVAeqy4EwN3wLFA5OZ3_LfoYXCwW8eq6M2qw/exec"
U_LAUNCHES = "رابط_شيت_اللونشات_الجديد_CSV" # ضع رابط شيت اللونشات هنا

# إدارة الحالة
if 'auth' not in st.session_state: st.session_state.auth = False
if 'current_user' not in st.session_state: st.session_state.current_user = None
if 'selected_item' not in st.session_state: st.session_state.selected_item = None

egypt_tz = pytz.timezone('Africa/Cairo')
egypt_now = datetime.now(egypt_tz)

# 3. التنسيق الجمالي المتكيف مع الموبايل (ألوان فاقعة وواضحة)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الأساسيات */
    [data-testid="stAppViewContainer"] {{ background-color: #000000; direction: rtl !important; text-align: right !important; font-family: 'Cairo', sans-serif; }}
    
    /* شريط الأخبار بلون أصفر فاقع */
    .ticker-wrap {{ background: #FFFF00; padding: 12px 0; border-radius: 0 0 15px 15px; margin-bottom: 20px; }}
    .ticker {{ color: #000 !important; font-weight: bold; font-size: 16px; animation: ticker 30s linear infinite; display: inline-block; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* كروت الموبايل الواضحة */
    div.stButton > button {{
        background-color: #1a1a1a !important; color: #FFFFFF !important;
        border: 2px solid #FFFF00 !important; border-radius: 15px !important;
        font-weight: 900 !important; font-size: 18px !important;
        padding: 20px !important; transition: 0.2s; width: 100% !important;
    }}
    div.stButton > button:active {{ background-color: #FFFF00 !important; color: #000 !important; }}

    /* كروت اللونشات المميزة */
    .launch-card {{
        background: linear-gradient(145deg, #111, #222);
        border-right: 12px solid #FF0000; /* أحمر للتنبيه */
        padding: 20px; border-radius: 15px; margin-bottom: 15px;
        border-top: 1px solid #444;
    }}
    
    .smart-box {{ background: #111; border: 2px solid #FFFF00; padding: 20px; border-radius: 20px; color: white; }}
    .tool-card {{ background: #1a1a1a; padding: 15px; border-radius: 15px; border: 1px solid #FFFF00; text-align: center; margin-bottom: 10px; }}
    
    /* تحسين القائمة للموبايل */
    .nav-link {{ font-size: 16px !important; padding: 10px !important; }}
    </style>
""", unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=60)
def load_all_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        # داتا تجريبية للونشات لو الرابط مش موجود
        l = pd.DataFrame({
            'Project': ['أورا زايد الجديدة', 'نايل بيزنس سيتي'],
            'Dev': ['Ora Dev', 'Nile'],
            'EOI': ['100,000', '50,000'],
            'Status': ['جمع EOIs', 'Coming Soon']
        })
        return p, d, l
    except: return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df_p, df_d, df_l = load_all_data()

# --- شريط الأخبار العلوي ---
st.markdown('<div class="ticker-wrap"><div class="ticker">🚀 عاجل: فتح باب الحجز في مشروع أورا الجديد بالشيخ زايد .. 🔥 أسعار المتر تبدأ من 45 ألف في العاصمة الإدارية .. 🏦 تمويل عقاري حتى 15 سنة متاح الآن ..</div></div>', unsafe_allow_html=True)

# 5. المنيو الرئيسي (تم إضافة اللونشات)
menu = option_menu(None, ["اللونشات 🚀", "المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["rocket", "robot", "search", "building", "calculator"], 
    default_index=0, orientation="horizontal",
    styles={
        "container": {"background-color": "#111", "padding": "0"},
        "nav-link": {"color": "white", "font-size": "14px"},
        "nav-link-selected": {"background-color": "#FFFF00", "color": "black", "font-weight": "bold"}
    })

# --- منطق الصفحات ---

if menu == "اللونشات 🚀":
    st.markdown("<h1 style='color:#FF0000; text-align:center;'>🚀 رادار اللونشات العاجلة</h1>", unsafe_allow_html=True)
    for i, row in df_l.iterrows():
        st.markdown(f"""
        <div class="launch-card">
            <h2 style="color:#FFFF00; margin:0;">{row['Project']}</h2>
            <p style="margin:5px 0;">🏗️ المطور: {row['Dev']}</p>
            <div style="background:#000; padding:10px; border-radius:10px; border:1px dashed #FF0000; display:inline-block; width:100%;">
                <p style="margin:0; font-weight:bold; color:#00FF00;">💰 مبلغ الحجز: {row['EOI']} ج.م</p>
                <p style="margin:0; font-size:14px; color:#aaa;">الحالة: {row['Status']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        msg = f"الحق يا فندم! لونش جديد لـ {row['Project']} بـ EOI {row['EOI']}. تحب أحجزلك؟"
        st.markdown(f"[📲 إرسال التنبيه لعميلك على الواتساب](https://wa.me/?text={urllib.parse.quote(msg)})")

elif menu == "المساعد الذكي":
    st.title("🤖 المساعد الذكي")
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    # (كود المساعد الذكي القديم كما هو لكن داخل smart-box)
    st.write("أدخل بيانات عميلك هنا لاستخراج الترشيحات...")
    st.markdown("</div>", unsafe_allow_html=True)

elif menu == "المشاريع":
    st.title("🏢 دليل المشاريع")
    # (كود المشاريع القديم كما هو مع تحسين الأزرار)
    st.write("استخدم الفلاتر للوصول لمشروعك:")
    # ... نفس كود العرض القديم ...

elif menu == "المطورين":
    st.title("🏗️ المطورين")
    # ... نفس كود المطورين القديم ...

elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة الأدوات (6 أدوات)")
    cols = st.columns(2) # 2 columns better for mobile
    tools = ["حاسبة القسط", "حاسبة ROI", "العمولة", "المساحة", "الضريبة", "التمويل"]
    for i, tool in enumerate(tools):
        with cols[i % 2]:
            st.markdown(f"<div class='tool-card'><h3>{tool}</h3></div>", unsafe_allow_html=True)
            # هنا تضع الـ inputs الخاصة بكل أداة كما في كودك السابق
                else:
                    user_verified = login_user(u_input, p_input)
                    if user_verified:
                        st.session_state.auth = True
                        st.session_state.current_user = user_verified
                        st.rerun()
                    else:
                        st.error("بيانات الدخول غير صحيحة")

    with tab_signup:
        _, c2, _ = st.columns([1,1.5,1])
        with c2:
            reg_name = st.text_input("الأسم بالكامل")
            reg_pass = st.text_input("كلمة السر المرجوة", type="password")
            reg_email = st.text_input("الجيميل")
            reg_wa = st.text_input("رقم الواتساب")
            reg_co = st.text_input("الشركة")
            if st.button("تأكيد الاشتراك ✅"):
                if reg_name and reg_pass and reg_email:
                    if signup_user(reg_name, reg_pass, reg_email, reg_wa, reg_co):
                        st.success("تم تسجيلك بنجاح! اذهب الآن لتبويب تسجيل الدخول.")
                    else: st.error("حدث خطأ في الاتصال بالسيرفر")
                else: st.warning("يرجى ملء الاسم وكلمة السر والإيميل")
    st.stop()

# 6. جلب البيانات
@st.cache_data(ttl=60)
def load_data():
    u_p = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    u_d = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRbRdikcTfH9AzB57igcbyJ2IBT2h5xkGZzSNbd240DO44lKXJlWhxgeLUCYVtpRG4QMxVr7DGPzhRP/pub?output=csv"
    try:
        p = pd.read_csv(u_p).fillna("---")
        d = pd.read_csv(u_d).fillna("---")
        p.columns = p.columns.str.strip()
        d.columns = d.columns.str.strip()
        p.rename(columns={'Area': 'Location', 'الموقع': 'Location', 'Project Name': 'ProjectName'}, inplace=True)
        return p, d
    except: return pd.DataFrame(), pd.DataFrame()

df_p, df_d = load_data()

# 7. الهيدر البصري المطور
st.markdown(f"""
    <div style="background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1600&q=80'); 
                height: 200px; background-size: cover; background-position: center; border-radius: 0 0 30px 30px; 
                display: flex; flex-direction: column; align-items: center; justify-content: center; border-bottom: 4px solid #f59e0b;">
        <h1 style="color: white; margin: 0; font-size: 45px; text-shadow: 2px 2px 10px rgba(0,0,0,0.5);">MA3LOMATI PRO</h1>
        <p style="color: #f59e0b; font-weight: bold; font-size: 18px;">أهلاً بك يا {st.session_state.current_user} في النسخة الاحترافية</p>
    </div>
""", unsafe_allow_html=True)

# 8. شريط المعلومات العلوي
c_top1, c_top2 = st.columns([0.7, 0.3])
with c_top1:
    st.markdown(f'<div class="ticker-wrap"><div class="ticker">🔥 {news_text}</div></div>', unsafe_allow_html=True)
with c_top2:
    st.markdown(f"""<div style='text-align: left; padding: 5px; color: #aaa; font-size: 14px;'>
                📅 {egypt_now.strftime('%Y-%m-%d')} | 🕒 {egypt_now.strftime('%I:%M %p')} 
                <span style='cursor:pointer; color:#f59e0b; margin-right:15px;' onclick='window.location.reload()'>🔄</span></div>""", unsafe_allow_html=True)
    if st.button("🚪 خروج", key="logout"): st.session_state.auth = False; st.rerun()

# 9. المنيو الرئيسي
menu = option_menu(None, ["المساعد الذكي", "المشاريع", "المطورين", "أدوات البروكر"], 
    icons=["robot", "search", "building", "briefcase"], default_index=0, orientation="horizontal",
    styles={"nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "bold"}})

# 10. تفاصيل المشروع (صفحة منبثقة)
if st.session_state.selected_item is not None:
    if st.button("⬅️ عودة للقائمة"): st.session_state.selected_item = None; st.rerun()
    item = st.session_state.selected_item
    st.markdown(f"""<div class='smart-box'>
        <h2>{item.get('ProjectName', item.get('Developer'))}</h2>
        <p>📍 الموقع: {item.get('Location', '---')}</p>
        <p>🏗️ المطور: {item.get('Developer', '---')}</p>
        <p>💰 تفاصيل السعر: {item.get('Starting Price (EGP)', 'تواصل للاستفسار')}</p>
        <hr><p>{item.get('Payment Plan', 'خطط سداد متنوعة متاحة عند التواصل')}</p>
    </div>""", unsafe_allow_html=True)

# --- 11. المساعد الذكي ---
elif menu == "المساعد الذكي":
    st.markdown("<div class='smart-box'>", unsafe_allow_html=True)
    st.title("🤖 مساعد الربط العقاري الذكي")
    col_f1, col_f2, col_f3 = st.columns(3)
    locs = sorted(df_p['Location'].unique().tolist()) if 'Location' in df_p.columns else ["الكل"]
    sel_loc = col_f1.selectbox("📍 المنطقة المستهدفة", ["الكل"] + locs)
    sel_type = col_f2.selectbox("🏠 نوع الوحدة", ["الكل", "شقق", "فيلات", "تجاري", "إداري", "طبي"])
    sel_budget = col_f3.number_input("💰 المقدم المتاح (EGP)", 0, step=50000)
    
    client_wa = st.text_input("رقم واتساب العميل (بدون أصفار لإرسال المقترح فوراً)")
    
    if st.button("🎯 استخراج أفضل الترشيحات"):
        res = df_p.copy()
        if sel_loc != "الكل": res = res[res['Location'] == sel_loc]
        if not res.empty:
            st.success(f"تم إيجاد {len(res.head(10))} مشروع مطابق لطلبك:")
            for idx, r in res.head(6).iterrows():
                with st.container(border=True):
                    c_txt, c_btn = st.columns([0.8, 0.2])
                    c_txt.write(f"🏢 **{r['ProjectName']}** | {r['Developer']} | {r['Location']}")
                    msg = f"أرشح لك مشروع {r['ProjectName']} في {r['Location']}. متاح وحدات {sel_type} تناسب طلبك."
                    link = f"https://wa.me/{client_wa}?text={urllib.parse.quote(msg)}"
                    c_btn.markdown(f"[📲 إرسال للعميل]({link})")
        else: st.warning("لا توجد نتائج مطابقة تماماً، جرب تغيير الفلاتر.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 12. المشاريع ---
elif menu == "المشاريع":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#10b981; text-align:center;'>🔑 استلام فوري / جاهز</h4>", unsafe_allow_html=True)
        ready = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز|سنة', case=False).any(), axis=1)].head(12)
        for i, r in ready.iterrows():
            if st.button(f"✅ {r['ProjectName']}", key=f"ready_{i}"):
                st.session_state.selected_item = r; st.rerun()

    with m_col:
        f1, f2 = st.columns(2)
        search = f1.text_input("🔍 ابحث باسم المشروع")
        area_f = f2.selectbox("📍 فلتر بالمنطقة", ["الكل"] + sorted(df_p['Location'].unique().tolist()))
        dff = df_p[df_p['ProjectName'].str.contains(search, case=False)] if search else df_p
        if area_f != "الكل": dff = dff[dff['Location'] == area_f]
        
        start = st.session_state.p_idx * 6
        page = dff.iloc[start:start+6]
        for i in range(0, len(page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page):
                    row = page.iloc[i+j]
                    if cols[j].button(f"🏢 {row['ProjectName']}\n📍 {row['Location']}\n🏗️ {row['Developer']}", key=f"card_p_{start+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        
        st.markdown("---")
        p1, _, p2 = st.columns([1,2,1])
        if st.session_state.p_idx > 0 and p1.button("⬅️ السابق"): st.session_state.p_idx -= 1; st.rerun()
        if start + 6 < len(dff) and p2.button("التالي ➡️"): st.session_state.p_idx += 1; st.rerun()

# --- 13. المطورين ---
elif menu == "المطورين":
    m_col, s_col = st.columns([0.7, 0.3])
    with s_col:
        st.markdown("<h4 style='color:#f59e0b; text-align:center;'>🏆 أفضل 10 مطورين</h4>", unsafe_allow_html=True)
        for i, r in df_d.head(10).iterrows():
            st.markdown(f"""<div class='side-card'><b>{i+1}. {r['Developer']}</b><br><small>الفئة: {r.get('Developer Category','A')}</small></div>""", unsafe_allow_html=True)

    with m_col:
        search_d = st.text_input("🔍 ابحث عن مطور")
        dfd_f = df_d[df_d['Developer'].str.contains(search_d, case=False)] if search_d else df_d
        start_d = st.session_state.d_idx * 6
        page_d = dfd_f.iloc[start_d:start_d+6]
        for i in range(0, len(page_d), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(page_d):
                    row = page_d.iloc[i+j]
                    if cols[j].button(f"🏗️ {row['Developer']}\n⭐ الفئة: {row.get('Developer Category','A')}\n💼 المالك: {row.get('Owner','---')}", key=f"card_d_{start_d+i+j}"):
                        st.session_state.selected_item = row; st.rerun()
        
        st.markdown("---")
        d1, _, d2 = st.columns([1,2,1])
        if st.session_state.d_idx > 0 and d1.button("⬅️ السابق ", key="d_prev"): st.session_state.d_idx -= 1; st.rerun()
        if start_d + 6 < len(dfd_f) and d2.button("التالي ➡️ ", key="d_next"): st.session_state.d_idx += 1; st.rerun()

# --- 14. حقيبة البروكر ---
elif menu == "أدوات البروكر":
    st.title("🛠️ حقيبة البروكر الاحترافية")
    r1_c1, r1_c2, r1_c3 = st.columns(3)
    r2_c1, r2_c2, r2_c3 = st.columns(3)
    
    with r1_c1:
        st.markdown("<div class='tool-card'><h3>💳 القسط</h3>", unsafe_allow_html=True)
        v = st.number_input("إجمالي السعر", 1000000, key="t1")
        d = st.number_input("المقدم", 100000, key="t2")
        y = st.slider("السنين", 1, 15, 8, key="t3")
        st.metric("القسط الشهري", f"{(v-d)/(y*12):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r1_c2:
        st.markdown("<div class='tool-card'><h3>💰 العمولة</h3>", unsafe_allow_html=True)
        deal = st.number_input("قيمة الصفقة", 1000000, key="t4")
        pct = st.slider("النسبة %", 0.5, 5.0, 1.5, key="t5")
        st.metric("صافي الربح", f"{deal*(pct/100):,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r1_c3:
        st.markdown("<div class='tool-card'><h3>📈 العائد ROI</h3>", unsafe_allow_html=True)
        buy = st.number_input("سعر الشراء", 1000000, key="t6")
        rent = st.number_input("الإيجار السنوي", 100000, key="t7")
        st.metric("نسبة العائد", f"{(rent/buy)*100:,.1f}%")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r2_c1:
        st.markdown("<div class='tool-card'><h3>📐 المساحة</h3>", unsafe_allow_html=True)
        m2 = st.number_input("المساحة بالمتر", 100.0, key="t8")
        st.write(f"القدم المربع: {m2 * 10.76:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r2_c2:
        st.markdown("<div class='tool-card'><h3>📝 الضريبة</h3>", unsafe_allow_html=True)
        tax_v = st.number_input("قيمة العقار", 1000000, key="t9")
        st.write(f"تصرفات (2.5%): {tax_v*0.025:,.0f}")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with r2_c3:
        st.markdown("<div class='tool-card'><h3>🏦 التمويل</h3>", unsafe_allow_html=True)
        loan = st.number_input("قرض التمويل", 500000, key="t10")
        st.write(f"الفائدة التقديرية (20%): {loan*0.20:,.0f}/سنة")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>MA3LOMATI PRO © 2026 | النسخة الاحترافية</p>", unsafe_allow_html=True)

