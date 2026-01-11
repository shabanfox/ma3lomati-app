import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة والهوية البصرية (الملكية)
st.set_page_config(page_title="منصة معلوماتى العقارية - محرك البحث المطور", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;900&display=swap');
    #MainMenu, footer, header, [data-testid="stHeader"] {visibility: hidden; display: none;}
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #0b0e14; color: white;
    }
    .project-card {
        background: #161b22; border-radius: 15px; padding: 25px; margin-bottom: 20px;
        border: 1px solid #30363d; border-right: 6px solid #f59e0b;
        transition: 0.4s;
    }
    .project-card:hover { border-right-width: 12px; background: #1c2128; }
    .price-tag { background: #f59e0b; color: #000; padding: 3px 12px; border-radius: 5px; font-weight: 900; float: left; }
    .info-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin-top: 15px; }
    .label { color: #8b949e; font-size: 13px; }
    .value { color: #f59e0b; font-weight: 600; font-size: 15px; }
    .desc-box { background: #0d1117; padding: 10px; border-radius: 8px; margin-top: 10px; border-left: 3px solid #f59e0b; font-size: 14px; color: #c9d1d9; }
    </style>
""", unsafe_allow_html=True)

# 2. جلب البيانات (تلقائياً من الرابط الخاص بك)
@st.cache_data(ttl=300)
def load_data():
    csv_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv"
    try:
        df = pd.read_csv(csv_url)
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# 3. واجهة البحث المتطورة
st.title("🏗️ المحرك العقاري الاستشاري")
st.write("استكشف 300+ مشروع ببيانات التقسيط والتفاصيل الدقيقة")

# فلاتر علوية ذكية
c1, c2, c3, c4 = st.columns(4)
with c1:
    search = st.text_input("🔍 اسم المشروع أو المطور")
with c2:
    area_list = df['Area'].unique().tolist() if 'Area' in df.columns else []
    selected_area = st.multiselect("📍 المنطقة", options=area_list)
with c3:
    type_list = df['Type'].unique().tolist() if 'Type' in df.columns else []
    selected_type = st.multiselect("🏠 نوع الوحدة", options=type_list)
with c4:
    # فلتر السعر (Min_Val)
    max_price = int(df['Min_Val'].max()) if 'Min_Val' in df.columns else 100000
    price_filter = st.slider("💰 ميزانية المتر تبدأ من", 0, max_price, 0)

# تطبيق الفلاتر
filtered_df = df
if search:
    filtered_df = filtered_df[filtered_df.apply(lambda row: search.lower() in str(row).lower(), axis=1)]
if selected_area:
    filtered_df = filtered_df[filtered_df['Area'].isin(selected_area)]
if selected_type:
    filtered_df = filtered_df[filtered_df['Type'].isin(selected_type)]
if price_filter > 0:
    filtered_df = filtered_df[filtered_df['Min_Val'] >= price_filter]

# 4. عرض البيانات (40 مشروع في الصفحة)
items_per_page = 40
if 'page' not in st.session_state: st.session_state.page = 0
start_idx = st.session_state.page * items_per_page
current_data = filtered_df.iloc[start_idx : start_idx + items_per_page]

for _, row in current_data.iterrows():
    # استخراج القيم مع وضع قيم افتراضية في حال عدم الوجود
    p_name = row.get('Project Name', row.get('OwnerProjects', 'مشروع غير مسمى'))
    dev = row.get('Developer', 'غير محدد')
    price = row.get('Min_Val', row.get('Start Price (sqm)', 'اتصل بنا'))
    delivery = row.get('Delivery', 'غير محدد')
    down_payment = row.get('Down_Payment', '0%')
    installments = row.get('Installments', '-')
    advantage = row.get('Competitive Advantage', 'موقع استراتيجي')
    description = row.get('Description', row.get('Detailed_Info', 'لا يوجد وصف متاح حالياً لهذا المشروع.'))

    st.markdown(f"""
    <div class="project-card">
        <div class="price-tag">{price} ج.م / متر</div>
        <div style="font-size: 24px; font-weight: 900; color: #f59e0b;">{p_name}</div>
        <div style="color: #8b949e; font-size: 16px;">بواسطة: <b>{dev}</b></div>
        
        <div class="info-grid">
            <div><span class="label">📍 المنطقة:</span><br><span class="value">{row.get('Area', '-')}</span></div>
            <div><span class="label">📅 التسليم:</span><br><span class="value">{delivery}</span></div>
            <div><span class="label">🏠 النوع:</span><br><span class="value">{row.get('Type', row.get('Unit Type', '-'))}</span></div>
            <div><span class="label">💳 مقدم:</span><br><span class="value">{down_payment}</span></div>
            <div><span class="label">⏳ تقسيط:</span><br><span class="value">{installments}</span></div>
            <div><span class="label">📐 المساحة:</span><br><span class="value">{row.get('Size (Acres)', '-')} فدان</span></div>
        </div>
        
        <div class="desc-box">
            <b>📝 نبذة عن المشروع:</b><br>{description[:250]}...
        </div>
        
        <div style="margin-top: 15px; font-size: 13px; color: #f59e0b;">
            ⭐ <b>الميزة التنافسية:</b> {advantage}
        </div>
    </div>
    """, unsafe_allow_html=True)

# أزرار التنقل
# (نفس نظام التنقل السابق بالسابق والتالي...)
