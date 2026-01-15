import streamlit as st
import streamlit.components.v1 as components

# --- 1. إعدادات الصفحة الأساسية ---
st.set_page_config(
    page_title="EstatePro AI | 2026",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ستايل مخصص (CSS) لتحسين المظهر ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; text-align: right; direction: rtl; }
    .main { background-color: #f8fafc; }
    .stMetric { background: white; padding: 15px; border-radius: 15px; border: 1px solid #e2e8f0; }
</style>
""", unsafe_allow_html=True)

# --- 3. مكون "أقوى 10 مطورين" (الجزء الـ 30%) ---
def developers_sidebar_html():
    devs = [
        {"n": "مجموعة طلعت مصطفى", "s": "145B", "g": "+25%", "c": "bg-amber-500"},
        {"n": "بالم هيلز", "s": "98B", "g": "+18%", "c": "bg-slate-400"},
        {"n": "أورا ديفلوبرز", "s": "85B", "g": "+30%", "c": "bg-orange-400"},
        {"n": "ماونتن فيو", "s": "70B", "g": "+12%", "c": "bg-blue-400"},
        {"n": "إعمار مصر", "s": "62B", "g": "+8%", "c": "bg-blue-400"},
        {"n": "سوديك", "s": "58B", "g": "+15%", "c": "bg-blue-400"},
        {"n": "مدينة مصر", "s": "44B", "g": "+20%", "c": "bg-blue-400"},
        {"n": "سيتي إيدج", "s": "40B", "g": "+5%", "c": "bg-blue-400"},
        {"n": "لافيستا", "s": "35B", "g": "+4%", "c": "bg-blue-400"},
        {"n": "هايد بارك", "s": "30B", "g": "+7%", "c": "bg-blue-400"},
    ]
    
    html_items = "".join([f"""
        <div class="flex items-center justify-between p-3 border-b border-slate-50 hover:bg-slate-50 cursor-pointer transition-all">
            <div class="flex items-center gap-3">
                <span class="w-6 h-6 {d['c']} text-white flex items-center justify-center rounded text-[10px] font-bold">{i+1}</span>
                <div>
                    <div class="font-bold text-slate-800 text-[12px]">{d['n']}</div>
                    <div class="text-[10px] text-slate-400">{d['s']} EGP المبيعات</div>
                </div>
            </div>
            <div class="text-[10px] text-green-600 font-bold">{d['g']}</div>
        </div>
    """ for i, d in enumerate(devs)])

    return f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <div dir="rtl" class="font-sans">
        <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
            <div class="bg-slate-900 p-4 text-white font-bold text-sm flex justify-between items-center">
                <span>🏆 ترتيب المطورين (تحديث حي)</span>
                <span class="text-[10px] opacity-70">2026</span>
            </div>
            {html_items}
            <div class="p-3 bg-slate-50 text-center"><a href="#" class="text-blue-600 text-xs font-bold">تحميل التقرير الكامل PDF</a></div>
        </div>
    </div>
    """

# --- 4. القائمة الجانبية للتنقل (Navigation) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/602/602182.png", width=80)
    st.title("لوحة التحكم")
    page = st.radio("انتقل إلى:", ["🏠 الرئيسية", "🏗️ المشاريع العقارية", "📈 تحليل السوق", "📞 الدعم الفني"])
    st.divider()
    st.info("تم الربط بنجاح مع قاعدة بيانات السوق العقاري المصري.")

# --- 5. منطق الصفحات والمحتوى الرئيسي (70%) ---
col_main, col_side = st.columns([0.7, 0.35], gap="medium")

with col_main:
    if page == "🏠 الرئيسية":
        st.markdown("# مرحباً بك في **EstatePro** 👋")
        st.markdown("### ملخص أداء السوق اليوم")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("المبيعات الكلية", "4.2B EGP", "12%+")
        m2.metric("أكثر المناطق طلباً", "التجمع الخامس", "🔥")
        m3.metric("مشاريع جديدة اليوم", "14 مشروع", "3%+")
        
        st.markdown("---")
        st.markdown("#### 📍 خريطة المشاريع التفاعلية")
        # مكان الخريطة
        st.image("https://raw.githubusercontent.com/andreascecil/image-storage/main/map-placeholder.png", use_container_width=True)

    elif page == "🏗️ المشاريع العقارية":
        st.markdown("# 🏗️ المشاريع العقارية النشطة")
        search = st.text_input("ابحث عن مشروع معين...")
        
        # كروت المشاريع
        projects = [
            {"name": "كمبوند نور", "dev": "طلعت مصطفى", "loc": "حدائق العاصمة", "price": "4.5M - 12M"},
            {"name": "بادية", "dev": "بالم هيلز", "loc": "أكتوبر الجديدة", "price": "3.8M - 15M"},
            {"name": "زد ايست", "dev": "أورا ديفلوبرز", "loc": "التجمع الخامس", "price": "5.2M - 20M"}
        ]
        
        for p in projects:
            with st.expander(f"{p['name']} - {p['dev']}"):
                col_a, col_b = st.columns(2)
                col_a.write(f"**الموقع:** {p['loc']}")
                col_b.write(f"**نطاق السعر:** {p['price']}")
                st.button(f"عرض تفاصيل {p['name']}", key=p['name'])

    elif page == "📈 تحليل السوق":
        st.markdown("# 📈 تحليلات الذكاء الاصطناعي")
        st.line_chart({"أسعار أكتوبر": [10, 12, 15, 18, 22], "أسعار التجمع": [15, 18, 25, 30, 38]})
        st.write("يتوقع نظامنا استمرار صعود أسعار المتر في منطقة شرق القاهرة بنسبة 15% خلال الربع القادم.")

# --- 6. الجزء الـ 30% (ثابت في كل الصفحات) ---
with col_side:
    components.html(developers_sidebar_html(), height=850, scrolling=False)

# --- 7. Footer ---
st.markdown("---")
st.caption("EstatePro 2026 - جميع البيانات محدثة كل 24 ساعة من مصادرها الرسمية.")
