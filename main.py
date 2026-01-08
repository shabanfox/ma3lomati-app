import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعداد الصفحة (يجب أن يظل أول سطر)
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide", page_icon="🏢")

# 2. روابط البيانات
PROJECTS_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTqvcugfByqHf-Hld_dKW6dEM5OKqhrZpK_gI8mYRbVnxiRs1rXoILP2jT3uDVNc8pVqUKfF-o6X3xx/pub?output=csv"

# 3. التنسيق (CSS) - الجمالية والاحترافية
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء عناصر Streamlit التقنية */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}

    /* نقل شريط التمرير لليسار وتنسيق الصفحة */
    html { direction: ltr !important; }
    body, [data-testid="stAppViewContainer"] {
        direction: rtl !important;
        font-family: 'Cairo', sans-serif;
        background-color: #0d1117;
        color: white;
    }
    
    /* شريط تمرير فخم في اليسار */
    ::-webkit-scrollbar { width: 14px !important; }
    ::-webkit-scrollbar-track { background: #0d1117 !important; }
    ::-webkit-scrollbar-thumb { 
        background: linear-gradient(to bottom, #d4af37, #aa8a2e) !important; 
        border-radius: 20px; 
    }

    /* الهيدر العملاق المتحرك */
    .hero-section {
        position: relative; height: 350px; overflow: hidden;
        border-radius: 30px; margin-bottom: 50px;
        display: flex; align-items: center; justify-content: center;
        border: 1px solid rgba(212, 175, 55, 0.3);
    }
    .hero-bg {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background-image: url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?auto=format&fit=crop&w=1600&q=80');
        background-size: cover; background-position: center;
        animation: kenburns 15s infinite alternate; z-index: 1;
    }
    .hero-overlay {
        position: absolute; top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(45deg, rgba(13,17,23,0.9), rgba(13,17,23,0.4)); z-index: 2;
    }
    .hero-content { position: relative; z-index: 3; text-align: center; }
    .main-title { color: #d4af37; font-size: 4em; font-weight: 900; text-shadow: 0 5px 15px rgba(0,0,0,0.5); margin: 0; }

    @keyframes kenburns { 0% {transform: scale(1) translate(0,0);} 100% {transform: scale(1.1) translate(-2%, -2%);} }

    /* تنسيق كروت المشاريع (Glassmorphism) */
    .project-card {
        background: rgba(28, 33, 40, 0.8);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 30px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .project-card:hover {
        border-color: #d4af37;
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(212, 175, 55, 0.15);
        background: rgba(34, 39, 46, 0.95);
    }
    
    .price-badge {
        background: linear-gradient(135deg, #d4af37, #f1c40f);
        color: #000; padding: 6px 20px; border-radius: 12px;
        font-weight: 900; float: left; box-shadow: 0 4px 10px rgba(212, 175, 55, 0.4);
    }

    /* تحسين شكل الفلاتر */
    .stSelectbox, .stTextInput { margin-bottom: 20px; }
    label { color: #d4af37 !important; font-weight: bold !important; font-size: 1.1em !important; }
    </style>
    
    <div class="hero-section">
        <div class="hero-bg"></div>
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1 class="main-title">منصة معلوماتي</h1>
            <p style="font-size: 1.3em; letter-spacing: 2px;">بوابتك العقارية الذكية لمستقبل الاستثمار</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 4. جلب البيانات
@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(PROJECTS_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("غير مدرج").astype(str)
    except: return pd.DataFrame()

df = load_data()

if not df.empty:
    # 5. منطقة الفلاتر (المنطقة بقت اختيار)
    st.markdown("<h2 style='color:#d4af37; text-align:center;'>🎯 ابدأ البحث الآن</h2>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    
    with c1:
        # جلب كل المناطق من الشيت وحذف التكرار
        regions_list = ["كل المناطق"] + sorted(df['المنطقة'].unique().tolist())
        s_reg = st.selectbox("📍 المنطقة", options=regions_list)
    
    with c2:
        s_pri = st.text_input("💰 السعر المتاح", placeholder="مثال: 5,000,000")
        
    with c3:
        s_typ = st.text_input("🏗️ نوع الوحدة", placeholder="سكني، تجاري..")

    # منطق الفلترة المتقاطع
    f_df = df.copy()
    if s_reg != "كل المناطق":
        f_df = f_df[f_df['المنطقة'] == s_reg]
    if s_pri:
        f_df = f_df[f_df['السعر'].str.contains(s_pri, case=False)]
    if s_typ:
        # ببحث في عمود النوع أو أول عمود لو مش موجود
        col = 'النوع' if 'النوع' in f_df.columns else f_df.columns[0]
        f_df = f_df[f_df[col].str.contains(s_typ, case=False)]

    st.markdown(f"**تم إيجاد {len(f_df)} فرصة عقارية مميزة**")
    st.markdown("<br>", unsafe_allow_html=True)

    # 6. عرض النتائج بكروت "جاذبة"
    for _, row in f_df.iterrows():
        st.markdown(f"""
            <div class="project-card">
                <div class="price-badge">EGP {row.get('السعر', '-')}</div>
                <h2 style="color:#d4af37; margin-bottom:15px; font-weight:900;">{row.get('المشروع', '-')}</h2>
                <div style="font-size:1.1em; margin-bottom:20px;">
                    <span style="opacity:0.7;">🏢 المطور:</span> <b>{row.get('المطور', '-')}</b> | 
                    <span style="opacity:0.7;">📍 الموقع:</span> <b>{row.get('المنطقة', '-')}</b>
                </div>
                <div style="background:rgba(212,175,55,0.07); padding:20px; border-right:5px solid #d4af37; border-radius:10px;">
                    <p style="margin:0; line-height:1.6;">{row.get('سابقة_الأعمال', 'لا توجد تفاصيل إضافية متاحة حالياً.')}</p>
                </div>
                <div style="margin-top:20px; font-size:0.9em; display:flex; gap:30px;">
                    <span><b style="color:#d4af37;">👤 المالك:</b> {row.get('المالك', '-')}</span>
                    <span><b style="color:#d4af37;">💳 السداد:</b> {row.get('السداد', '-')}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("📦 جاري مزامنة قاعدة البيانات من جوجل شيت..")
