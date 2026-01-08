import streamlit as st
import pandas as pd
import requests
from io import StringIO

# 1. إعدادات الصفحة وإخفاء هوية ستريمليت/جيت هب
st.set_page_config(page_title="منصة معلوماتي العقارية", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* إخفاء الهيدر وأيقونة جيت هب والقوائم */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: rtl !important; text-align: right;
        font-family: 'Cairo', sans-serif; background-color: #f0f2f6; color: #1e272e;
    }

    /* هيدر سينمائي متحرك */
    .hero-container {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #c49a6c, #0f172a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        padding: 100px 20px; text-align: center;
        border-bottom: 4px solid #c49a6c; border-radius: 0 0 80px 80px;
        margin-bottom: 50px; box-shadow: 0 20px 40px rgba(0,0,0,0.2);
    }
    @keyframes gradientBG {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }

    /* كارت المطور (Profile) */
    .dev-main-card {
        background: white; border-radius: 25px; padding: 40px;
        margin-bottom: 40px; border-right: 15px solid #c49a6c;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }

    /* شبكة المشاريع (Nawy Style Grid) */
    .project-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
        gap: 25px; margin-top: 20px;
    }
    .project-card {
        background: white; border-radius: 20px; padding: 25px;
        border: 1px solid #eef0f2; transition: all 0.4s ease;
        position: relative; overflow: hidden;
    }
    .project-card:hover {
        transform: translateY(-10px); border-color: #c49a6c;
        box-shadow: 0 20px 40px rgba(196, 154, 108, 0.15);
    }
    .price-tag {
        background: #c49a6c; color: white; padding: 6px 15px;
        border-radius: 10px; font-weight: 900; position: absolute; left: 20px; top: 20px;
    }

    /* تنسيق أدوات البحث */
    .search-box { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 25px rgba(0,0,0,0.05); margin-top: -80px; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات من الرابط (بصيغة CSV لضمان القراءة)
RAW_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQ8MmnRw6KGRVIKIfp_-o8KyvhJKVhHLIZKpFngWHeN0WTsjupFMILryY7EKv6m0vPCD0jwcBND-pvk/pub?output=csv"

@st.cache_data(ttl=5)
def load_data():
    try:
        res = requests.get(RAW_URL)
        res.encoding = 'utf-8'
        df = pd.read_csv(StringIO(res.text))
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("-").astype(str)
    except:
        return pd.DataFrame()

df = load_data()

# الهيدر السينمائي
st.markdown("""
    <div class="hero-container">
        <h1 style="font-size: 4.5em; font-weight: 900; color: #ffffff; margin:0; letter-spacing:-2px;">مـعـلـومـاتـي</h1>
        <p style="font-size: 1.5em; color: #c49a6c; font-weight: 400; opacity: 0.9;">الموسوعة العقارية الشاملة للبروكار المحترف</p>
    </div>
""", unsafe_allow_html=True)

if not df.empty:
    # منطقة البحث (Search Section)
    st.markdown('<div class="search-box">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        # قراءة أول عمود للمطور
        dev_col = df.columns[0]
        s_dev = st.selectbox("🏗️ ابحث عن الشركة", ["عرض جميع الشركات"] + sorted(df[dev_col].unique().tolist()))
    with c2:
        # قراءة العمود الخامس للمنطقة (تعديل الـ index حسب شيتك)
        reg_index = 4 if len(df.columns) > 4 else 0
        reg_col = df.columns[reg_index]
        s_reg = st.selectbox("📍 فلتر بالمنطقة", ["كل المناطق"] + sorted(df[reg_col].unique().tolist()))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("<br><br>", unsafe_allow_html=True)

    if s_dev != "عرض جميع الشركات":
        # عرض بروفايل الشركة (بناءً على أول سطر للمطور)
        dev_rows = df[df[dev_col] == s_dev]
        main = dev_rows.iloc[0]
        
        st.markdown(f"""
            <div class="dev-main-card">
                <h2 style="color:#c49a6c; font-size: 3em; margin-bottom:10px;">{s_dev}</h2>
                <div style="font-size:1.3em; margin-bottom:20px;">👤 <b>المالك / الأونر:</b> {main.get(df.columns[1], '-')}</div>
                <hr style="opacity:0.1; margin:25px 0;">
                <h4 style="color:#c49a6c; font-size:1.5em; margin-bottom:15px;">📜 نبذة عن الشركة وسابقة الأعمال:</h4>
                <p style="line-height:2; font-size:1.15em; color:#444; text-align:justify;">{main.get(df.columns[2], '-')}</p>
            </div>
            <h3 style="text-align:center; font-weight:900; color:#0f172a; margin:40px 0;">🏗️ مشاريع {s_dev}</h3>
        """, unsafe_allow_html=True)

        # شبكة المشاريع
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in dev_rows.iterrows():
            # التأكد إن السطر فيه مشروع (عشان ميعرضش سطر السيرة الذاتية الفاضي)
            if r[df.columns[3]] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-tag">{r.get(df.columns[5], '-')}</div>
                        <h3 style="margin-top:40px; color:#1e293b;">{r[df.columns[3]]}</h3>
                        <p style="color:#666; margin:10px 0;">📍 {r[reg_col]}</p>
                        <div style="background:#fcf8f3; padding:12px; border-radius:12px; font-size:0.9em; border: 1px solid #f1e6d8;">
                            <b>💳 نظام السداد:</b><br>{r.get(df.columns[6], '-')}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # عرض البحث العام (كل المشاريع)
        f_df = df.copy()
        if s_reg != "كل المناطق": f_df = f_df[f_df[reg_col] == s_reg]
        
        st.markdown('<div class="project-grid">', unsafe_allow_html=True)
        for _, r in f_df.iterrows():
            if r[df.columns[3]] != "-":
                st.markdown(f"""
                    <div class="project-card">
                        <div class="price-tag">{r.get(df.columns[5], '-')}</div>
                        <h3 style="margin-top:40px;">{r[df.columns[3]]}</h3>
                        <p style="color:#c49a6c; font-weight:700;">🏢 {r[dev_col]}</p>
                        <p style="color:#666; font-size:0.9em;">📍 {r[reg_col]}</p>
                    </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.error("⚠️ جاري مزامنة البيانات من جوجل شيت... تأكد من نشر الشيت بصيغة CSV.")
