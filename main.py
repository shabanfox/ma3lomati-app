import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة - الأفضل هو العرض الكامل (Wide Mode)
st.set_page_config(page_title="BrokerEdge Pro", layout="wide", initial_sidebar_state="expanded")

# 1. تخصيص الـ CSS للوصول لأعلى جودة تصميم
st.markdown("""
<style>
    /* الخط والخلفية العامة */
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif;
        text-align: right;
        direction: rtl;
    }

    /* إخفاء الهيدر والفوتر بتوع streamlit */
    header, footer {visibility: hidden;}

    /* تجميل الأزرار الجانبية */
    .stButton>button {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# 2. الهيدر الاحترافي (Hero Section)
header_html = """
<div dir="rtl" style="background: #0f172a; padding: 30px; border-radius: 20px; margin-bottom: 25px; border-right: 8px solid #3b82f6;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h1 style="color: white; margin: 0; font-size: 28px;">BrokerEdge <span style="color: #3b82f6;">Pro</span></h1>
            <p style="color: #94a3b8; margin: 5px 0 0 0;">مرحباً بك في المركز الذكي لإدارة بيانات السوق</p>
        </div>
        <div style="background: rgba(59, 130, 246, 0.1); padding: 10px 20px; border-radius: 12px; border: 1px solid #3b82f6;">
            <span style="color: #3b82f6; font-weight: bold;">حالة السوق اليوم: 📈 نشط جداً</span>
        </div>
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 3. شريط الأدوات السريع (Quick Actions)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.info("**أحدث أسعار المتر**\n\nالتجمع: 48,000 ج.م")
with col2:
    st.success("**أعلى عمولة حالية**\n\nمشروع بادية: 5.5%")
with col3:
    st.warning("**موعد زيادة الأسعار**\n\nإعمار: بعد 3 أيام")
with col4:
    st.error("**وحدات إعادة بيع لقطة**\n\nعدد 4 وحدات متوفرة")

st.markdown("---")

# 4. محرك البحث (The Engine)
st.subheader("🔍 البحث الذكي عن الوحدات والمشاريع")
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    search_term = st.text_input("بحث بالاسم أو الكلمة الدلالية (مثلاً: استلام فوري)...")
with c2:
    region = st.selectbox("المنطقة", ["الكل", "التجمع الخامس", "العاصمة الإدارية", "الشيخ زايد", "المستقبل"])
with c3:
    st.button("بدء البحث المتقدم")

# 5. عرض المشاريع (النسخة الأفضل للكروت)
st.markdown("### 🏢 المشاريع المقترحة للعملاء حالياً")

# بيانات تجريبية (مجهزة للربط مع الإكسيل لاحقاً)
projects = [
    {"name": "Mountain View iCity", "dev": "MV", "type": "شقق وفيلات", "start_price": "8.5M", "plan": "10% / 9 Yrs", "img": "https://images.unsplash.com/photo-1460317442991-0ec209397118?w=500&q=80"},
    {"name": "IL Bosco City", "dev": "Misr Italia", "type": "شقق", "start_price": "6.2M", "plan": "5% / 8 Yrs", "img": "https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=500&q=80"},
    {"name": "The Waterway", "dev": "Waterway", "type": "تجاري وسكني", "start_price": "14.0M", "plan": "Cash / Short term", "img": "https://images.unsplash.com/photo-1554435493-93422e8220c8?w=500&q=80"}
]

cols = st.columns(3)
for i, p in enumerate(projects):
    with cols[i]:
        card = f"""
        <div dir="rtl" style="background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.05); border: 1px solid #f1f5f9; margin-bottom: 20px;">
            <img src="{p['img']}" style="width: 100%; height: 180px; object-fit: cover;">
            <div style="padding: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                    <span style="font-size: 12px; color: #64748b; font-weight: bold;">{p['dev']}</span>
                    <span style="background: #f0fdf4; color: #16a34a; padding: 2px 10px; border-radius: 10px; font-size: 11px;">متوفر داتا الأسعار</span>
                </div>
                <h4 style="margin: 0; color: #0f172a; font-size: 18px; font-weight: bold;">{p['name']}</h4>
                <p style="color: #64748b; font-size: 13px; margin: 8px 0;">نوع الوحدات: {p['type']}</p>
                <div style="background: #f8fafc; border-radius: 10px; padding: 10px; margin: 15px 0;">
                    <div style="display: flex; justify-content: space-between; font-size: 13px;">
                        <span style="color: #64748b;">أقل مقدم</span>
                        <span style="color: #1e3a8a; font-weight: bold;">{p['plan']}</span>
                    </div>
                </div>
                <button style="width: 100%; background: #1e3a8a; color: white; border: none; padding: 10px; border-radius: 10px; cursor: pointer; font-family: 'Cairo';">عرض الزتونة كاملة</button>
            </div>
        </div>
        """
        st.markdown(card, unsafe_allow_html=True)

# 6. الـ Sidebar (أدوات البروكر)
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/609/609036.png", width=80)
    st.title("أدواتي")
    st.button("🔄 تحديث داتا السوق")
    st.button("📊 تقرير مقارنة للعميل")
    st.button("📱 إرسال واتساب مباشر")
    st.markdown("---")
    st.info("إصدار التجريبي v2.0 - 2026")
