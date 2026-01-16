elif menu == "المطورين":
        st.markdown("<h3 style='color:#f59e0b;'>🏗️ دليل المطورين العقاريين</h3>", unsafe_allow_html=True)
        
        # 1. البحث في المطورين
        s_d = st.text_input("🔍 ابحث باسم المطور، المالك، أو المنطقة الرئيسية...")
        
        dff_d = df_d.copy()
        if s_d:
            # البحث في كافة الأعمدة المتاحة للمطور
            dff_d = dff_d[dff_d.apply(lambda r: r.astype(str).str.contains(s_d, case=False).any(), axis=1)]

        # 2. عرض النتائج
        if dff_d.empty:
            st.warning("لم يتم العثور على بيانات لهذا المطور.")
        else:
            # عرض المطورين في نظام كروت (2 في كل صف)
            for i in range(0, len(dff_d), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(dff_d):
                        row = dff_d.iloc[i + j]
                        with cols[j]:
                            # تصميم كارت المطور (بيانات سريعة)
                            dev_label = (
                                f"🏗️ {row.get('Developer', 'غير مسجل')}\n"
                                f"👑 المالك: {row.get('Owner', 'غير مسجل')}\n"
                                f"⭐ الفئة: {row.get('Developer Category', 'C')}\n"
                                f"━━━━━━━━━━━━━━\n"
                                f"🏢 المشاريع: {row.get('Number of Projects', '0')}\n"
                                f"📍 المقر: {row.get('Headquarters Address', 'القاهرة')[:30]}...\n"
                                f"📖 تفاصيل سابقة الأعمال"
                            )
                            if st.button(dev_label, key=f"card_d_{i+j}"):
                                st.session_state.selected_item = row
                                st.rerun()

    # --- تعديل منطق عرض "تفاصيل المطور" في الجزء العلوي من main_col ---
    if st.session_state.selected_item is not None:
        item = st.session_state.selected_item
        # نتحقق إذا كان العنصر المختار "مطور" أم "مشروع" بناءً على اسم الأعمدة
        is_developer = 'Developer' in item and 'Project Name' not in item
        
        if is_developer:
            if st.button("⬅️ عودة لقائمة المطورين"):
                st.session_state.selected_item = None
                st.rerun()
            
            st.markdown(f"""
                <div class="detail-box" style="border-right: 5px solid #f59e0b;">
                    <h1 style="color:#f59e0b; margin-bottom:5px;">{item.get('Developer')}</h1>
                    <p style="font-size:18px; color:#aaa;">⭐ تصنيف المطور: {item.get('Developer Category')}</p>
                    <hr style="opacity:0.1;">
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0;">
                        <div style="background:#1a1a1a; padding:15px; border-radius:10px;">
                            <b style="color:#f59e0b;">👑 المالك / مجلس الإدارة:</b><br>{item.get('Owner')}
                        </div>
                        <div style="background:#1a1a1a; padding:15px; border-radius:10px;">
                            <b style="color:#f59e0b;">🏢 عدد المشاريع:</b><br>{item.get('Number of Projects')} مشروع
                        </div>
                        <div style="background:#1a1a1a; padding:15px; border-radius:10px;">
                            <b style="color:#f59e0b;">📍 منطقة النشاط الرئيسية:</b><br>{item.get('Main Region of Activity')}
                        </div>
                        <div style="background:#1a1a1a; padding:15px; border-radius:10px;">
                            <b style="color:#f59e0b;">📍 العنوان الرئيسي:</b><br>{item.get('Headquarters Address')}
                        </div>
                    </div>

                    <div style="background:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:20px; border-right:3px solid #f59e0b;">
                        <h4 style="color:#f59e0b;">📖 سابقة الأعمال (Previous Projects):</h4>
                        <p style="line-height:1.8;">{item.get('Previous Projects', 'لا توجد بيانات مسجلة.')}</p>
                    </div>

                    <div style="background:#1a1a1a; padding:15px; border-radius:10px; margin-bottom:20px;">
                        <h4 style="color:#f59e0b;">ℹ️ معلومات تفصيلية (Detailed Info):</h4>
                        <p style="line-height:1.8;">{item.get('Detailed_Info', 'لا توجد معلومات إضافية.')}</p>
                    </div>

                    <div style="text-align:center; margin-top:30px;">
                        <a href="{item.get('Company Website / Portfolio', '#')}" target="_blank" 
                           style="background:#f59e0b; color:black; padding:12px 30px; border-radius:25px; text-decoration:none; font-weight:bold;">
                           🌐 زيارة الموقع الإلكتروني / البروفايل
                        </a>
                    </div>
                </div>
            """, unsafe_allow_html=True)
