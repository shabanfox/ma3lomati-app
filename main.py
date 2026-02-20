import streamlit as st
import pandas as pd
import requests

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(page_title="MA3LOMATI 2026", layout="wide")

# --- 2. تهيئة الجلسة (بدون استخدام query_params لضمان الاستقرار) ---
if 'auth' not in st.session_state:
    st.session_state.auth = False
if 'view' not in st.session_state:
    st.session_state.view = "grid"

# --- 3. تحميل البيانات (نسخة مبسطة) ---
@st.cache_data(ttl=60)
def load_data():
    try:
        # روابط البيانات الخاصة بك
        urls = {
            "p": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?output=csv",
            "d": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=732423049&single=true&output=csv",
            "l": "https://docs.google.com/spreadsheets/d/e/2PACX-1vR7AlPjwOSyd2JIH646Ie8lzHKwin6LIB8DciEuzaUb2Wo3sbzVK3w6LSRmvE4t0Oe9B7HTw-8fJCu1/pub?gid=1593482152&single=true&output=csv"
        }
        df_p = pd.read_csv(urls["p"]).fillna("---")
        df_d = pd.read_csv(urls["d"]).fillna("---")
        df_l = pd.read_csv(urls["l"]).fillna("---")
        return df_p, df_d, df_l
    except Exception as e:
        st.error(f"خطأ في الاتصال بالشيت: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# --- 4. تصميم الواجهة (CSS بسيط جداً لتجنب الأخطاء) ---
st.markdown("""
    <style>
    body { direction: rtl; text-align: right; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #f59e0b; color: black; font-weight: bold; }
    [data-testid="stSidebar"] { direction: rtl; }
    .card { background-color: #1e1e1e; border: 1px solid #f59e0b; padding: 15px; border-radius: 15px; color: white; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. منطق تسجيل الدخول ---
if not st.session_state.auth:
    st.title("🔑 تسجيل الدخول | MA3LOMATI")
    pwd = st.text_input("كلمة السر الخاصة بالمنصة", type="password")
    if st.button("دخول"):
        if pwd == "2026":
            st.session_state.auth = True
            st.rerun()
        else:
            st.error("كلمة السر غير صحيحة")
    st.stop()

# --- 6. القائمة الرئيسية (استبدال option_menu بـ sidebar عادي لضمان العمل) ---
df_p, df_d, df_l = load_data()

with st.sidebar:
    st.title("MA3LOMATI PRO")
    menu = st.radio("القائمة الرئيسية", ["المشاريع", "المطورين", "أدوات البروكر", "المساعد الذكي (المقارنة)"])
    if st.button("🚪 خروج"):
        st.session_state.auth = False
        st.rerun()

# --- 7. محتوى الأقسام ---
if menu == "المشاريع":
    st.header("🏗️ قاعدة بيانات المشاريع")
    search = st.text_input("بحث بالاسم أو الموقع...")
    
    # فلترة
    filtered_df = df_p[df_p.apply(lambda row: search.lower() in row.astype(str).str.lower().values, axis=1)] if search else df_p
    
    # عرض البيانات في جدول تفاعلي (أكثر استقراراً من الكروت المخصصة)
    st.dataframe(filtered_df, use_container_width=True)

elif menu == "المطورين":
    st.header("🏢 دليل المطورين العقاريين")
    st.table(df_d.head(20))

elif menu == "أدوات البروكر":
    st.header("🛠️ حاسبة الصفقات")
    c1, c2 = st.columns(2)
    with c1:
        total = st.number_input("السعر الإجمالي", value=1000000)
        years = st.number_input("سنين القسط", value=7)
        if years > 0:
            st.metric("القسط الشهري", f"{(total/years/12):,.0f}")
    with c2:
        commission = st.number_input("نسبة العمولة %", value=2.5)
        st.metric("صافي عمولتك", f"{(total * commission / 100):,.0f}")

elif menu == "المساعد الذكي (المقارنة)":
    st.header("⚖️ نظام مقارنة المشاريع")
    col1, col2 = st.columns(2)
    with col1:
        choice1 = st.selectbox("المشروع الأول", df_p.iloc[:, 0].unique())
    with col2:
        choice2 = st.selectbox("المشروع الثاني", df_p.iloc[:, 0].unique())
    
    if choice1 and choice2:
        st.markdown("### نتيجة المقارنة")
        data1 = df_p[df_p.iloc[:, 0] == choice1].iloc[0]
        data2 = df_p[df_p.iloc[:, 0] == choice2].iloc[0]
        
        comparison_data = []
        for col in df_p.columns:
            comparison_data.append({"الخاصية": col, choice1: data1[col], choice2: data2[col]})
        
        st.table(pd.DataFrame(comparison_data))

st.markdown("---")
st.caption("MA3LOMATI PRO 2026 - جميع الحقوق محفوظة")
