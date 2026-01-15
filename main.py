import streamlit as st
import streamlit.components.v1 as components

# إعدادات الصفحة
st.set_page_config(page_title="EstatePro | منصة العقارات الذكية", layout="wide", initial_sidebar_state="collapsed")

# كود CSS و HTML الخاص بخانة المطورين (الجزء الـ 30%)
def developers_ranking_component():
    html_code = """
    <script src="https://cdn.tailwindcss.com"></script>
    <div dir="rtl" class="font-sans p-2">
        <div class="bg-white rounded-2xl shadow-md border border-slate-100 overflow-hidden">
            <div class="bg-slate-900 p-4 flex justify-between items-center">
                <h3 class="text-white font-bold text-sm flex items-center gap-2">
                    🏆 أقوى 10 مطورين 2026
                </h3>
                <span class="flex h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
            </div>
            
            <div class="divide-y divide-slate-50">
                <div class="flex items-center justify-between p-3 hover:bg-blue-50 transition-all cursor-pointer">
                    <div class="flex items-center gap-3">
                        <span class="w-6 h-6 bg-amber-100 text-amber-700 flex items-center justify-center rounded text-xs font-bold">1</span>
                        <div>
                            <h4 class="font-bold text-slate-800 text-xs">مجموعة طلعت مصطفى</h4>
                            <p class="text-[10px] text-slate-500">140B EGP مبيعات</p>
                        </div>
                    </div>
                    <span class="text-[10px] text-green-600 font-bold">+25%</span>
                </div>

                <div class="flex items-center justify-between p-3 hover:bg-blue-50 transition-all cursor-pointer">
                    <div class="flex items-center gap-3">
                        <span class="w-6 h-6 bg-slate-100 text-slate-700 flex items-center justify-center rounded text-xs font-bold">2</span>
                        <div>
                            <h4 class="font-bold text-slate-800 text-xs">بالم هيلز</h4>
                            <p class="text-[10px] text-slate-500">95B EGP مبيعات</p>
                        </div>
                    </div>
                    <span class="text-[10px] text-green-600 font-bold">+18%</span>
                </div>

                <div class="flex items-center justify-between p-3 hover:bg-blue-50 transition-all cursor-pointer">
                    <div class="flex items-center gap-3">
                        <span class="w-6 h-6 bg-orange-100 text-orange-700 flex items-center justify-center rounded text-xs font-bold">3</span>
                        <div>
                            <h4 class="font-bold text-slate-800 text-xs">أورا ديفلوبرز</h4>
                            <p class="text-[10px] text-slate-500">88B EGP مبيعات</p>
                        </div>
                    </div>
                    <span class="text-[10px] text-green-600 font-bold">+30%</span>
                </div>
                
                <div class="p-3 text-center">
                    <button style="font-size: 11px;" class="text-blue-600 font-bold hover:underline">عرض القائمة الكاملة</button>
                </div>
            </div>
        </div>
    </div>
    """
    components.html(html_code, height=600, scrolling=True)

# --- واجهة المستخدم الرئيسية في Streamlit ---

# 1. Header
st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0px; border-bottom: 1px solid #eee; margin-bottom: 20px;">
        <h1 style="color: #0f172a; font-size: 24px; font-weight: 900;">ESTATE<span style="color: #2563eb;">PRO</span></h1>
        <div style="background: #f1f5f9; padding: 5px 15px; border-radius: 20px; font-size: 12px; color: #64748b;">تحديث السوق: يناير 2026</div>
    </div>
""", unsafe_allow_html=True)

# 2. تقسيم الصفحة (70% للمحتوى و 30% للمطورين)
col_main, col_sidebar = st.columns([0.7, 0.3])

with col_main:
    # الجزء الـ 70%
    st.markdown("### 📊 نظرة عامة على السوق")
    
    # بطاقات إحصائية سريعة
    c1, c2, c3 = st.columns(3)
    c1.metric("حجم الاستثمارات", "2.4B EGP", "+12%")
    c2.metric("المشاريع النشطة", "1,240", "5%+")
    c3.metric("متوسط سعر المتر", "45k EGP", "+8%")
    
    st.divider()
    
    # محاكاة للخريطة أو المحتوى الرئيسي
    st.markdown("""
        <div style="height: 400px; background: #e2e8f0; border-radius: 20px; display: flex; align-items: center; justify-content: center; border: 2px dashed #cbd5e1;">
            <p style="color: #64748b; font-weight: bold;">[ خريطة المشاريع التفاعلية تعمل هنا ]</p>
        </div>
    """, unsafe_allow_html=True)

with col_sidebar:
    # الجزء الـ 30% - استدعاء مكون المطورين
    developers_ranking_component()

# Footer
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 12px; margin-top: 50px;'>حقوق النشر © 2026 | منصة المعلومات العقارية الذكية</p>", unsafe_allow_html=True)
