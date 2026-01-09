import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة (يجب أن تكون أول سطر)
st.set_page_config(page_title="موسوعة المطورين", layout="wide")

# 2. كود التصميم CSS لتوحيد الألوان (نفس الألوان اللي طلبتها)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [data-testid="stAppViewContainer"] { 
        direction: RTL; text-align: right; font-family: 'Cairo', sans-serif; background-color: #f8fafc; 
    }
    .main-card { 
        background-color: white; border-radius: 12px; padding: 20px; 
        margin-bottom: 15px; border-right: 6px solid #003366;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    .info-badge {
        background-color: #f1f5f9; color: #003366; padding: 4px 12px; 
        border-radius: 8px; font-size: 0.85rem; margin-left: 8px; font-weight: bold;
    }
    div.stButton > button {
        background-color: #003366 !important; color: white !important;
        border-radius: 10px !important; font-family: 'Cairo', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

# 3. حل مشكلة الـ NameError (تعريف الحالة الابتدائية)
if 'page' not in st.session_state:
    st.session_state.page = 'main'
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None

# 4. دالة جلب البيانات (تأكد من وضع الرابط الصحيح هنا)
@st.cache_data
def load_data():
    # هنا تضع رابط CSV الخاص بك من جوجل شيت
    csv_url = "ضع_رابط_الشيت_هنا" 
    try:
        # كبيانات تجريبية إذا لم يجد الرابط
        df = pd.read_csv(csv_url)
        return df
    except:
        # بيانات وهمية للتجربة فقط في حال فشل الرابط
        return pd.DataFrame([{"Developer": "Mountain View", "Area": "التجمع", "Price": "8.5M", "Detailed_Info": "معلومات تجريبية"}])

df = load_data()

# --- إدارة الصفحات ---

# الصفحة الرئيسية
if st.session_state.page == 'main':
    st.markdown("<h1 style='text-align: center; color: #003366;'>🏛️ موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)
    
    search = st.text_input("🔍 ابحث عن مطور أو منطقة أو ميزة فنية...", placeholder="مثلاً: ساويرس، التجمع، تشطيب كامل")
    
    filtered = df.copy()
    if search:
        filtered = filtered[
            filtered['Developer'].str.contains(search, case=False, na=False) |
            filtered.get('Detailed_Info', '').str.contains(search, case=False, na=False)
        ]

    for i, row in filtered.iterrows():
        st.markdown(f"""
            <div class="main-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <span style="color:#003366; font-size:1.4rem; font-weight:900;">{row['Developer']}</span><br><br>
                        <span class="info-badge">📍 {row.get('Area', 'غير محدد')}</span>
                        <span class="info-badge">💰 {row.get('Price', 'غير محدد')}</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button(f"عرض التفاصيل الفنية لـ {row['Developer']}", key=f"btn_{i}"):
            st.session_state.selected_item = row.to_dict()
            st.session_state.page = 'details'
            st.rerun()

# صفحة التفاصيل (بالألوان الموحدة)
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    if st.button("🔙 عودة للقائمة الرئيسية"):
        st.session_state.page = 'main'
        st.rerun()
    
    # تصميم الهيدر بنفس الوان الرئيسية
    st.markdown(f"""
        <div style="background-color: #003366; padding: 30px; border-radius: 15px; margin-bottom: 25px; text-align: center; color: white;">
            <h1 style="margin: 0;">{item['Developer']}</h1>
            <p style="font-size: 1.2rem; opacity: 0.8;">{item.get('Projects', 'مشاريع متنوعة')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # كروت البيانات
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown(f"<div class='main-card' style='text-align:center;'><b>📍 المنطقة</b><br><span style='color:#003366;'>{item.get('Area')}</span></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='main-card' style='text-align:center;'><b>💰 السعر</b><br><span style='color:#003366;'>{item.get('Price')}</span></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='main-card' style='text-align:center;'><b>🕒 الاستلام</b><br><span style='color:#003366;'>{item.get('Delivery', 'قريباً')}</span></div>", unsafe_allow_html=True)

    # تفاصيل البروكر (الزتونة)
    st.markdown("### 💡 الزتونة الفنية (للمستشار العقاري)")
    st.markdown(f"""
        <div style="background-color: white; padding: 25px; border-radius: 12px; border-right: 8px solid #003366; box-shadow: 0 2px 10px rgba(0,0,0,0.05); color: #1e293b; font-size: 1.1rem; line-height: 1.8;">
            {item.get('Detailed_Info', 'لا توجد معلومات إضافية متوفرة حالياً لهذا المطور.')}
        </div>
    """, unsafe_allow_html=True)
