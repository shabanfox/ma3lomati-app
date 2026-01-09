# --- إدارة التنقل بين الصفحات ---

# 1. الصفحة الرئيسية
if st.session_state.page == 'main':
    st.markdown("<h1 style='text-align: center; color: #003366;'>🏛️ موسوعة المطورين العقاريين</h1>", unsafe_allow_html=True)
    
    if df is not None:
        search = st.text_input("🔍 ابحث عن مطور، منطقة، أو ميزة فنية...")
        
        # تصفية البيانات بناءً على البحث
        filtered = df.copy()
        if search:
            filtered = filtered[
                filtered['Developer'].str.contains(search, case=False, na=False) |
                filtered['Detailed_Info'].str.contains(search, case=False, na=False)
            ]

        # عرض الشركات في كروت
        for i, row in filtered.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="main-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color:#003366; font-size:1.3rem; font-weight:900;">{row['Developer']}</span><br>
                            <span class="info-badge">📍 {row['Area']}</span>
                            <span class="info-badge">💰 {row['Price']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # زر التفاصيل بنفس تنسيق ألوان الصفحة
                if st.button(f"تفاصيل {row['Developer']}", key=f"btn_{i}"):
                    st.session_state.selected_item = row.to_dict()
                    st.session_state.page = 'details'
                    st.rerun()

# 2. صفحة التفاصيل (بعد إصلاح الخطأ وتوحيد الألوان)
elif st.session_state.page == 'details':
    item = st.session_state.selected_item
    
    # زر العودة
    if st.button("🔙 العودة للموسوعة"): 
        st.session_state.page = 'main'
        st.rerun()
    
    # الهيدر الموحد
    st.markdown(f"""
        <div style="background-color: #003366; padding: 20px; border-radius: 12px; margin-bottom: 25px; text-align: center;">
            <h1 style="color: white; margin: 0;">{item.get('Developer')}</h1>
            <p style="color: #cbd5e1; margin-top: 10px;">{item.get('Projects')}</p>
        </div>
    """, unsafe_allow_html=True)
    
    # كروت البيانات الأربعة (نفس ستايل الرئيسية)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f"<div class='main-card' style='text-align:center;'><b>المقدم</b><br><span style='color:#003366;'>{item.get('Down_Payment')}</span></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='main-card' style='text-align:center;'><b>القسط</b><br><span style='color:#003366;'>{item.get('Installments')} سنين</span></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='main-card' style='text-align:center;'><b>السعر</b><br><span style='color:#003366;'>{item.get('Price')}</span></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='main-card' style='text-align:center;'><b>الاستلام</b><br><span style='color:#003366;'>{item.get('Delivery')}</span></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # المعلومات التفصيلية
    col_r, col_l = st.columns([2, 1])
    with col_r:
        st.markdown("### 💡 المعلومات التفصيلية")
        st.markdown(f"""
            <div style="background-color: #f1f5f9; padding: 20px; border-radius: 10px; border-right: 5px solid #003366; color: #1e293b;">
                {item.get('Detailed_Info', 'لا توجد معلومات إضافية')}
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 📝 وصف المطور")
        st.write(item.get('Description'))

    with col_l:
        st.markdown("### 🏢 بيانات المطور")
        st.markdown(f"""
            <div style="background-color: white; padding: 15px; border-radius: 10px; border: 1px solid #e2e8f0;">
                <p><b>👤 المالك:</b> {item.get('Owner')}</p>
                <p><b>📍 المنطقة:</b> {item.get('Area')}</p>
                <p><b>🏗️ النوع:</b> {item.get('Type')}</p>
            </div>
        """, unsafe_allow_html=True)
