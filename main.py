import streamlit as st
import pandas as pd
import urllib.parse

# 1. إعدادات الصفحة
st.set_page_config(page_title="منصة معلوماتى العقارية", layout="wide")

# 2. كود التصميم (CSS) - الشكل الرمادي الاحترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* إخفاء الزوائد */
    [data-testid="stHeader"], footer, .stDeployButton, #MainMenu {display: none !important;}
    
    /* خلفية الموقع رمادي فاتح جداً */
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; 
        font-family: 'Cairo', sans-serif; 
        background-color: #f8fafc; 
    }

    .block-container { 
        max-width: 1100px; 
        margin: auto; 
        padding: 1rem 2% !important; 
    }

    /* الهيدر */
    .header-nav { 
        text-align: right; 
        padding: 15px 0; 
        margin-bottom: 5px;
    }

    /* صندوق أدوات البروكر */
    .broker-tool-box { 
        background: linear-gradient(135deg, #003366, #1a4a7a); 
        color: white; 
        padding: 20px; 
        border-radius: 15px; 
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    /* الكروت: خلفية رمادية مميزة */
    .project-card-container { 
        background-color: #edf2f7; 
        border-radius: 12px; 
        margin-bottom: 6px !important; 
        overflow: hidden;
        display: flex;
        align-items: center;
        border: 1px solid #e2e8f0;
        transition: 0.3s;
    }
    .project-card-container:hover { border-color: #003366; }

    /* زرار التفاصيل */
    div.stButton > button {
        background-color: #003366 !important;
        color: white !important;
        border-radius: 6px !important;
        padding: 4px 15px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        border: none !important;
    }
    div.stButton > button:hover { background-color: #D4AF37 !important; }

    /* كروت الإحصائيات */
    .metric-card {
        background: white; padding: 10px; border-radius: 10px; text-align: center;
        border: 1px solid #e2e8f0; box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    </style>
""", unsafe_allow_html=True)

# 3. وظيفة جلب وتنظيف البيانات
@st.cache_data(ttl=60)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [str(c).strip() for c in df.columns]
        # تنظيف الأرقام للعمليات الحسابية
        df['Price_Num'] = pd.to_numeric(df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce').fillna(0)
        df['DP_Pct'] = pd.to_numeric(df['Down_Payment'], errors='coerce').fillna(10)
        df['Years'] = pd.to_numeric(df['Installments'], errors='coerce').fillna(7)
        return df
    except:
        return None

df = load_data()

# إدارة الصفحات
if 'page' not in st.session_state: st.session_state.page = 'main'

# --- الصفحة الرئيسية ---
if st.session_state.page == 'main':
    # الهيدر
    st.markdown('<div class="header-nav"><div style="color:#003366; font-weight:900; font-size:1.8rem;">منصة معلوماتى <span style="color:#D4AF37;">العقارية</span></div></div>', unsafe_allow_html=True)

    if df is not None:
        # ركن المستشار العقاري
        st.markdown('<div class="broker-tool-box"><h3>🎯 محرك المطابقة المالية</h3><p>فلترة المطورين بناءً على ميزانية وقدرة العميل الشرائية</p></div>', unsafe_allow_html=True)
        
        with st.expander("🛠️ لوحة التحكم في ميزانية العميل", expanded=True):
            c1, c2, c3, c4 = st.columns(4)
            with c1: b_total = st.number_input("الميزانية الكلية (ج.م)", value=6000000, step=100000)
            with c2: b_down = st.number_input("المقدم المتاح (ج.م)", value=600000, step=50000)
            with c3: b_month = st.number_input("القسط الشهري (ج.م)", value=40000, step=5000)
            with c4: s_area = st.selectbox("المنطقة", ["الكل"] + sorted(df['Area'].unique().tolist()))

        # منطق المطابقة الذكية
        def match_logic(row):
            price = row['Price_Num']
            if price == 0: return False
            req_dp = price * (row['DP_Pct'] / 100)
            req_mo = (price - req_dp) / (row['Years'] * 12)
            
            # فلترة بالمال وبالموقع
            match_fin = price <= b_total and req_dp <= b_down and req_mo <= b_month
            match_loc = True if s_area == "الكل" else row['Area'] == s_area
            return match_fin and match_loc

        matches = df[df.apply(match_logic, axis=1)]

        # عرض النتائج
        st.markdown(f"**تم إيجاد {len(matches)} عرض يتناسب مع ميزانية عميلك**")

        for _, row in matches.iterrows():
            st.markdown('<div class="project-card-container">', unsafe_allow_html=True)
            col_info, col_img = st.columns([4, 1])
            
            with col_info:
                txt_c, btn_c = st.columns([3, 1])
                with txt_c:
                    dp_val = int(row['Price_Num'] * (row['DP_Pct']/100))
                    mo_val = int((row['Price_Num'] - dp_val) / (row['Years'] * 12))
                    st.markdown(f"""
                        <div style="text-align: right; padding: 15px;">
                            <div style="color: #003366; font-weight: 900; font-size: 1.3rem;">{row.get('Developer')}</div>
                            <div style="color: #D4AF37; font-weight: 700;">المقدم: {dp_val:,} ج.م | القسط: {mo_val:,} ج.م</div>
                            <div style="color: #4a5568; font-size: 0.85rem;">📍 {row.get('Area')} | النوع: {row.get('Type', '-')} | نظام: {int(row['DP_Pct'])}% على {int(row['Years'])} سنين</div>
                        </div>
                    """, unsafe_allow_html=True)
                with btn_c:
                    st.write("")
                    st.write("")
                    if st.button("التفاصيل", key=f"btn_{row.get('Developer')}"):
                        st.session_state.selected_item = row.to_dict()
                        st.session_state.page = 'details'
                        st.rerun()

            with col_img:
                img_url = row.get('Image_URL', 'https://via.placeholder.com/400')
                st.markdown(f'<div style="height: 110px; background-image: url(\'{img_url}\'); background-size: cover; background-position: center; border-right: 1px solid #e2e8f0;"></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# --- صفحة التفاصيل ---
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    st.markdown('<div style="background:white; padding:30px; border-radius:15px; margin-top:10px; border: 1px solid #e2e8f0;">', unsafe_allow_html=True)
    if st.button("⬅️ عودة لمحرك البحث"):
        st.session_state.page = 'main'
        st.rerun()
    
    st.markdown(f"<h1 style='color:#003366;'>{item.get('Developer')}</h1>", unsafe_allow_html=True)
    
    # حسابات سريعة للمشاركة
    price = item['Price_Num']
    dp = price * (item['DP_Pct'] / 100)
    mo = (price - dp) / (item['Years'] * 12)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("كاش المقدم", f"{int(dp):,} ج.م")
    c2.metric("القسط الشهري", f"{int(mo):,} ج.م")
    c3.metric("مدة السداد", f"{int(item['Years'])} سنوات")

    st.markdown("---")
    st.subheader("📝 نبذة عن المطور ومشاريعة")
    st.write(item.get('Description', 'لا يوجد وصف متاح.'))
    st.info(f"📍 أهم المشاريع: {item.get('Projects')}")
    
    # زر مشاركة واتساب للبروكر
    wa_text = f"*تفاصيل عرض عقاري من منصة معلوماتى*\n\nالمطور: {item.get('Developer')}\nالمنطقة: {item.get('Area')}\nالمقدم: {int(dp):,} ج.م\nالقسط: {int(mo):,} ج.م شهرياً\nلمدة: {int(item['Years'])} سنوات"
    wa_url = f"https://wa.me/?text={urllib.parse.quote(wa_text)}"
    st.markdown(f'<a href="{wa_url}" target="_blank" style="text-decoration:none;"><div style="background-color:#25D366; color:white; padding:12px; border-radius:10px; text-align:center; font-weight:bold;">📲 مشاركة العرض مع العميل عبر واتساب</div></a>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
