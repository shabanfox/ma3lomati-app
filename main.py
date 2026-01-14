import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="معلوماتي العقارية - Dashboard", layout="wide", page_icon="🏢")

# إضافة CSS مخصص لتحسين المظهر (RTL لدعم اللغة العربية)
st.markdown("""
    <style>
    .main { text-align: right; direction: rtl; }
    .stMarkdown { text-align: right; }
    .css-10trblm { text-align: right; direction: rtl; }
    </style>
    """, unsafe_allow_html=True)

# 1. قاعدة البيانات (Dictionary تحتوي على الوصف التسويقي)
area_info = {
    "القاهرة الجديدة": {
        "title": "التجمع الخامس.. وجهة السكن الراقي",
        "desc": "تعتبر القلب النابض لشرق القاهرة، حيث تجمع بين الحيوية والخصوصية. تتميز بوجود الجولدن سكوير ومنطقة بيت الوطن الواعدة.",
        "projects_count": 225,
        "highlight": "منطقة بيت الوطن والفيو زون"
    },
    "العاصمة الإدارية": {
        "title": "العاصمة الإدارية.. مدينة المستقبل",
        "desc": "بنية تحتية ذكية، قطار مونوريل، وأكبر حديقة مركزية (النهر الأخضر). الاستثمار هنا هو رهان على المستقبل الرقمي لمصر.",
        "projects_count": 135,
        "highlight": "الحي السكني R7 و R8"
    },
    "الساحل الشمالي": {
        "title": "الساحل الشمالي الجديد.. مالديف المتوسط",
        "desc": "من العلمين إلى رأس الحكمة، الوجهة السياحية الأولى والآن وجهة سكنية تعمل طوال العام بفضل رأس الحكمة وساوث ميد.",
        "projects_count": 85,
        "highlight": "رأس الحكمة وسيدي حنيش"
    },
    "مدينة المستقبل": {
        "title": "مدينة المستقبل.. العيش في قلب الطبيعة",
        "desc": "أول مدينة خضراء متكاملة (Gated Communities) تربط بين التجمع الخامس والعاصمة الإدارية بطريقة انسيابية.",
        "projects_count": 48,
        "highlight": "هاب تاون وبلوم فيلدز"
    },
    "الشيخ زايد": {
        "title": "الشيخ زايد ونيو زايد.. هدوء الغرب",
        "desc": "توسعات الحزام الأخضر ونيو زايد توفر أعلى مستويات الخصوصية للفيلات والمجتمعات العمرانية الراقية.",
        "projects_count": 105,
        "highlight": "سوديك ويست ونيو زايد"
    }
}

# --- واجهة التطبيق ---

st.title("🚀 لوحة تحكم معلوماتي العقارية 2026")
st.subheader("دليلك الشامل للمشاريع السكنية الجديدة في مصر")

st.divider()

# القائمة المنسدلة لاختيار المنطقة
col1, col2 = st.columns([1, 2])

with col1:
    selected_area = st.selectbox("📌 اختر المنطقة لاستعراض التفاصيل:", list(area_info.keys()))
    
    # عرض إحصائيات سريعة
    st.metric(label="إجمالي المشاريع التقريبي", value=area_info[selected_area]["projects_count"])
    st.info(f"📍 أهم المعالم: {area_info[selected_area]['highlight']}")

with col2:
    # عرض الوصف (رقم 5 الذي طلبته)
    st.header(area_info[selected_area]["title"])
    st.write(area_info[selected_area]["desc"])
    
    # إضافة زر تفاعلي
    if st.button(f"تحميل شيت مشاريع {selected_area}"):
        st.success(f"يتم الآن تحضير ملف Excel لمشاريع {selected_area}...")

st.divider()

# 2. عرض الجدول (الشيت الذي جمعناه سابقاً)
st.subheader("📊 جدول المشاريع المقترحة")

# بيانات تجريبية للشيت (يمكنك استبدالها بالشيتات الكاملة التي أرسلتها لك)
data = {
    "اسم المشروع": ["ميفيدا", "سولاري", "باديا", "المقصد", "بلوم فيلدز"],
    "المطور": ["إعمار مصر", "مصر إيطاليا", "بالم هيلز", "سيتي إيدج", "تطوير مصر"],
    "المنطقة": ["القاهرة الجديدة", "الساحل الشمالي", "6 أكتوبر", "العاصمة الإدارية", "مدينة المستقبل"]
}
df = pd.DataFrame(data)

# عرض الجدول مع خاصية الفلترة حسب اختيار المستخدم
filtered_df = df[df["المنطقة"] == selected_area] if selected_area in df["المنطقة"].values else df

st.dataframe(filtered_df, use_container_width=True)

# تذييل الصفحة
st.caption("تم التطوير بواسطة 'معلوماتي العقارية' - 2026")

if not st.session_state.auth:
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.markdown("<div style='height:100px;'></div>", unsafe_allow_html=True)
        st.markdown("<h1 style='text-align:center; color:#f59e0b;'>MA3LOMATI PRO</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align:center; color:#666;'>نظام إدارة المعلومات العقارية المتقدم - 2026</p>", unsafe_allow_html=True)
        pwd = st.text_input("كلمة المرور للدخول", type="password")
        if st.button("دخول آمن"):
            if pwd == "2026":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("خطأ في كلمة المرور")
    st.stop()

# 5. الهيدر والقائمة الرئيسية
st.markdown(f'''
    <div class="luxury-header">
        <div class="logo-text">MA3LOMATI PRO</div>
        <div style="color:#aaa; font-weight:bold;">{datetime.now().strftime("%Y-%m-%d | %H:%M")}</div>
    </div>
''', unsafe_allow_html=True)

menu = option_menu(
    None, 
    ["الأدوات", "المشاريع", "المطورين"], 
    icons=["tools", "building", "person-vcard"], 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#050505"},
        "icon": {"color": "#f59e0b", "font-size": "18px"}, 
        "nav-link": {"font-size": "16px", "text-align": "center", "margin":"0px", "--hover-color": "#222", "color": "white"},
        "nav-link-selected": {"background-color": "#f59e0b", "color": "black", "font-weight": "900"},
    }
)

# 6. تقسيم الشاشة (70% محتوى - 30% استلام فوري)
col_main, col_side = st.columns([0.7, 0.3])

# --- الجانب الأيسر: الاستلام الفوري ---
with col_side:
    st.markdown("<h4 style='color:#10b981; text-align:center; margin-bottom:10px;'>⚡ استلام فوري / جاهز</h4>", unsafe_allow_html=True)
    st.markdown("<div class='ready-sidebar'>", unsafe_allow_html=True)
    if not df_p.empty:
        # فلترة المشاريع التي تحتوي كلمة فوري أو جاهز
        ready_df = df_p[df_p.apply(lambda r: r.astype(str).str.contains('فوري|جاهز', case=False).any(), axis=1)]
        if len(ready_df) > 0:
            for _, row in ready_df.iterrows():
                st.markdown(f"""
                <div style='background:#1a1a1a; padding:12px; border-radius:10px; margin-bottom:10px; border-right:4px solid #10b981;'>
                    <div style='color:#f59e0b; font-weight:bold; font-size:14px;'>{row.get('Project Name', 'غير مسمى')}</div>
                    <div style='color:#ccc; font-size:12px;'>📍 {row.get('Area', 'الموقع غير محدد')}</div>
                    <div style='color:#10b981; font-size:11px; margin-top:5px;'>✓ متاح للمعالجة الفورية</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("لا توجد بيانات حالية")
    st.markdown("</div>", unsafe_allow_html=True)

# --- الجانب الأيمن: المحتوى الرئيسي ---
with col_main:
    if menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ مركز العمليات الذكي</h2>", unsafe_allow_html=True)
        
        # 🕵️ أداة الرادار
        st.markdown("""
            <div class='ai-box'>
                <h3 style='color:#f59e0b;'>🕵️ رادار المشاريع الذكي</h3>
                <p style='color:#ccc;'>ابحث عن أي مشروع خارج قاعدة البيانات وسيتم الربط بمصادر السوق</p>
            </div>
        """, unsafe_allow_html=True)
        
        ext_search = st.text_input("أدخل اسم المشروع أو المطور...")
        if ext_search:
            search_q = urllib.parse.quote(ext_search + " عقارات مصر")
            c1, c2, c3 = st.columns(3)
            with c1: st.link_button("🌍 بحث شامل", f"https://www.google.com/search?q={search_q}")
            with c2: st.link_button("🏢 سابقة الأعمال", f"https://www.google.com/search?q={urllib.parse.quote(ext_search + ' سابقة أعمال')}")
            with c3: st.link_button("📍 الخريطة", f"https://www.google.com/maps/search/{search_q}")

        st.markdown("---")

        # 🧮 الأدوات المالية المتكاملة
        t = st.tabs(["🧮 حاسبة الأقساط", "📈 تحليل الاستثمار", "📐 محول المساحات", "💰 حساب العمولة"])
        
        with t[0]: # الأقساط
            cc1, cc2 = st.columns(2)
            with cc1:
                price = st.number_input("إجمالي سعر الوحدة", min_value=0, value=5000000, step=100000)
                down_payment_pct = st.slider("نسبة المقدم %", 0, 50, 10)
            with cc2:
                years = st.slider("مدة التقسيط (سنوات)", 1, 15, 8)
                maintenance = st.checkbox("إضافة مصاريف الصيانة (8%)")
            
            dp_amount = price * (down_payment_pct / 100)
            rem_amount = price - dp_amount
            monthly = rem_amount / (years * 12)
            quarterly = rem_amount / (years * 4)
            
            st.markdown(f"""
            <div style='background:#111; padding:20px; border-radius:10px; border:1px solid #333;'>
                <h4 style='color:#f59e0b;'>النتائج المالية:</h4>
                <p>💰 مبلغ المقدم: <b>{dp_amount:,.0f} ج.م</b></p>
                <p>📅 القسط الشهري: <b style='color:#10b981; font-size:20px;'>{monthly:,.0f} ج.م</b></p>
                <p>🗓️ القسط الربع سنوي: <b>{quarterly:,.0f} ج.م</b></p>
            </div>
            """, unsafe_allow_html=True)

        with t[1]: # الاستثمار
            st.subheader("تحليل العائد الإيجاري المتوقع")
            rent_val = st.number_input("قيمة الإيجار الشهري المتوقعة", value=20000)
            annual_roi = ((rent_val * 12) / price) * 100
            st.metric("نسبة العائد السنوي (ROI)", f"{annual_roi:.2f}%")
            st.info("العائد الجيد في السوق المصري يتراوح بين 7% إلى 12% للسكني، وأعلى للتجاري.")

        with t[2]: # المساحات
            sqm = st.number_input("المساحة بالمتر المربع", value=100.0)
            col_a, col_b = st.columns(2)
            col_a.metric("بالفدان", f"{sqm / 4200:.4f}")
            col_b.metric("بالقدم المربع", f"{sqm * 10.764:.2f}")

        with t[3]: # العمولة
            comm_pct = st.number_input("نسبة العمولة %", value=1.5, step=0.1)
            tax = st.checkbox("خصم ضرائب (14%)")
            net_comm = price * (comm_pct / 100)
            if tax: net_comm = net_comm * 0.86
            st.success(f"صافي العمولة: {net_comm:,.0f} ج.م")

    elif menu == "المشاريع":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المشاريع العقارية</h2>", unsafe_allow_html=True)
        search_p = st.text_input("🔍 ابحث باسم المشروع أو المنطقة...")
        
        if not df_p.empty:
            filtered_p = df_p[df_p.apply(lambda r: r.astype(str).str.contains(search_p, case=False).any(), axis=1)]
            for _, row in filtered_p.head(20).iterrows():
                with st.container():
                    st.markdown(f"""
                    <div class="grid-card">
                        <div style="display:flex; justify-content:space-between;">
                            <span style="color:#f59e0b; font-size:20px; font-weight:bold;">{row.get('Project Name', 'N/A')}</span>
                            <span style="background:#222; padding:2px 10px; border-radius:15px; font-size:12px;">{row.get('Area', 'N/A')}</span>
                        </div>
                        <div style="margin-top:10px; color:#ddd;">
                            <b>المطور:</b> {row.get('Developer', 'N/A')} | <b>النوع:</b> {row.get('Type', 'N/A')}
                        </div>
                        <div style="margin-top:5px; color:#aaa; font-size:13px;">
                            {row.get('Details', '')[:150]}...
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("لم يتم العثور على بيانات المشاريع.")

    elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏗️ سجل المطورين العقاريين</h2>", unsafe_allow_html=True)
        search_d = st.text_input("🔍 ابحث عن شركة تطوير...")
        
        if not df_d.empty:
            filtered_d = df_d[df_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]
            for _, row in filtered_d.head(15).iterrows():
                st.markdown(f"""
                <div class="grid-card" style="border-right-color: #10b981;">
                    <h3 style="color:#10b981;">{row.get('Developer Name', 'N/A')}</h3>
                    <p><b>سابقة الأعمال:</b> {row.get('History', 'غير مسجلة')}</p>
                    <p style="font-size:13px; color:#888;">{row.get('Notes', '')}</p>
                </div>
                """, unsafe_allow_html=True)

# 7. التذييل
st.markdown("---")
st.markdown("<p style='text-align:center; color:#444;'>Ma3lomati PRO © 2026 | Developed for Real Estate Leaders</p>", unsafe_allow_html=True)

