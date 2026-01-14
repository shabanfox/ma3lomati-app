elif menu == "المطورين":
        st.markdown("<h2 style='color:#f59e0b;'>🏢 دليل المطورين العقاريين</h2>", unsafe_allow_html=True)
        
        # خانة البحث والفلترة
        search_d = st.text_input("🔍 ابحث عن مطور، فئة (Tier)، أو مالك...")
        
        # تأكد من أن df_d تحتوي على البيانات
        if not df_d.empty:
            filtered_d = df_d.copy()
            if search_query:
                filtered_d = filtered_d[filtered_d.apply(lambda r: r.astype(str).str.contains(search_query, case=False).any(), axis=1)]
            
            # العرض الشبكي للمطورين (2 في كل صف)
            for i in range(0, len(filtered_d), 2):
                cols = st.columns(2)
                for j in range(2):
                    if i + j < len(filtered_d):
                        r = filtered_d.iloc[i + j]
                        
                        # استخراج البيانات مع قيم افتراضية
                        dev_name = r.get('Developer', 'شركة تطوير')
                        tier = r.get('Developer Category', 'N/A')
                        num_projs = r.get('Number of Projects', '0')
                        owner = r.get('Owner', 'غير مسجل')
                        advantage = r.get('Competitive Advantage', 'N/A')
                        
                        # تحديد لون الـ Tier (ذهبي للـ Tier A)
                        tier_color = "#f59e0b" if "A" in str(tier).upper() else "#aaa"
                        
                        with cols[j]:
                            st.markdown(f"""
                                <div class="grid-card" style="height:220px; border-right: 5px solid {tier_color};">
                                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                        <h3 style="color:#f59e0b; margin:0; font-size:18px;">{dev_name}</h3>
                                        <span style="background:{tier_color}; color:black; padding:2px 8px; border-radius:5px; font-size:10px; font-weight:bold;">{tier}</span>
                                    </div>
                                    <div style="margin-top:10px;">
                                        <p style="color:#ccc; font-size:13px; margin-bottom:5px;">👤 المالك: {owner}</p>
                                        <p style="color:#10b981; font-size:14px; font-weight:bold;">🏗️ عدد المشاريع: {num_projs}</p>
                                    </div>
                                    <div style="font-size:11px; color:#aaa; border-top:1px solid #333; padding-top:8px; height:40px; overflow:hidden;">
                                        🏆 الميزة: {advantage[:60]}...
                                    </div>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # تفاصيل إضافية عند الضغط
                            with st.expander("📖 سابقة الأعمال والتفاصيل"):
                                st.write(f"**نبذة عن الشركة:** {r.get('Detailed_Info', 'لا توجد بيانات متاحة حالياً.')}")
        else:
            st.warning("⚠️ لا توجد بيانات في شيت المطورين حالياً. تأكد من تسمية الأعمدة بشكل صحيح.")
