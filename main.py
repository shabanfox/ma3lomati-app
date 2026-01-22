import streamlit as st
import pandas as pd

# --- 1. جلب البيانات ---
@st.cache_data(ttl=60)
def load_launch_data():
    # الرابط الخاص بك (تم التأكد من صيغة الـ CSV والـ GID)
    URL_LAUNCHES = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
    try:
        df = pd.read_csv(URL_LAUNCHES).fillna("---")
        df.columns = df.columns.str.strip() # تنظيف العناوين
        return df
    except:
        return pd.DataFrame()

# --- 2. ستايل الكروت (CSS) ---
st.markdown("""
    <style>
    /* جعل الزر يبدو كأنه كارت احترافي */
    div.stButton > button[key^="lnch_"] {
        background-color: #161616 !important;
        color: white !important;
        border: 1px solid #333 !important;
        border-top: 5px solid #f59e0b !important;
        border-radius: 15px !important;
        padding: 20px !important;
        min-height: 180px !important;
        width: 100% !important;
        text-align: right !important;
        display: block !important;
        transition: 0.3s !important;
    }
    div.stButton > button[key^="lnch_"]:hover {
        border-color: #f59e0b !important;
        transform: translateY(-5px) !important;
        background-color: #1a1a1a !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. عرض صفحة اللونشات ---
def show_launches_page():
    st.markdown("<h2 style='text-align:center; color:white;'>🚀 دليل اللونشات 2026</h2>", unsafe_allow_html=True)
    
    df_launch = load_launch_data()
    
    if df_launch.empty:
        st.info("جاري مزامنة البيانات من الشيت... تأكد من نشر الشيت بصيغة CSV")
        return

    # حالة عرض التفاصيل
    if st.session_state.get('selected_launch') is not None:
        item = st.session_state.selected_launch
        if st.button("⬅️ عودة لجميع اللونشات"):
            st.session_state.selected_launch = None
            st.rerun()
        
        # تصميم صفحة التفاصيل
        st.markdown(f"""
            <div style="background:#161616; padding:30px; border-radius:20px; border-right:8px solid #f59e0b;">
                <h1 style="color:#f59e0b;">{item.get('Project', 'مشروع جديد')}</h1>
                <h3>🏢 المطور: {item.get('Developer', '---')}</h3>
                <hr>
                <p style="font-size:20px;">📍 الموقع: {item.get('Location', '---')}</p>
                <p style="font-size:20px;">💰 جدية الحجز (EOI): {item.get('EOI', '---')}</p>
                <p style="font-size:18px; color:#aaa;">📝 ملاحظات: {item.get('Notes', 'لا توجد ملاحظات إضافية')}</p>
            </div>
        """, unsafe_allow_html=True)
        return

    # عرض شبكة الكروت
    cols = st.columns(3)
    for index, row in df_launch.iterrows():
        # استخراج البيانات
        dev = str(row.get('Developer', 'مطور')).strip()
        proj = str(row.get('Project', 'مشروع')).strip()
        loc = str(row.get('Location', '---')).strip()
        
        with cols[index % 3]:
            # الزر هو الكارت نفسه
            # نضع النص داخل الزر بتنسيق بسيط
            button_label = f"🏢 {dev}\n\n{proj}\n\n📍 {loc}"
            
            if st.button(button_label, key=f"lnch_{index}"):
                st.session_state.selected_launch = row
                st.rerun()

# استدعاء الصفحة (توضع داخل شرط menu == "اللونشات")
if 'selected_launch' not in st.session_state:
    st.session_state.selected_launch = None

show_launches_page()
