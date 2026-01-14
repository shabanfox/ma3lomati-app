# --- داخل قسم المطورين في الكود ---
elif menu == "المطورين":
    st.markdown("<h2 style='color:#f59e0b;'>🏢 تصنيف المطورين العقاريين</h2>", unsafe_allow_html=True)
    search_d = st.text_input("🔍 ابحث عن مطور (الاسم أو الفئة)...")
    
    filtered_d = df_d.copy()
    if search_d:
        filtered_d = filtered_d[filtered_d.apply(lambda r: r.astype(str).str.contains(search_d, case=False).any(), axis=1)]

    # العرض الشبكي للمطورين
    for i in range(0, len(filtered_d), 2):
        cols = st.columns(2)
        for j in range(2):
            if i+j < len(filtered_d):
                r = filtered_d.iloc[i+j]
                
                # تحديد لون التصنيف (Tier)
                tier = r.get('Developer Category', 'N/A')
                tier_color = "#f59e0b" if "A" in tier.upper() else "#aaa"
                
                with cols[j]:
                    st.markdown(f"""
                        <div class="grid-card" style="height:220px; border-right: 5px solid {tier_color};">
                            <div>
                                <div style="display:flex; justify-content:space-between; align-items:center;">
                                    <h3 style="color:#f59e0b; margin:0; font-size:18px;">{r.get('Developer', 'شركة تطوير')}</h3>
                                    <span style="background:{tier_color}; color:black; padding:2px 8px; border-radius:5px; font-size:10px; font-weight:bold;">{tier}</span>
                                </div>
                                <p style="color:#ccc; font-size:13px; margin-top:10px;">👤 المالك: {r.get('Owner', 'غير مسجل')}</p>
                                <p style="color:#10b981; font-size:14px; font-weight:bold;">🏗️ عدد المشاريع: {r.get('Number of Projects', '0')}</p>
                            </div>
                            <div style="font-size:11px; color:#aaa; border-top:1px solid #333; padding-top:5px; overflow:hidden;">
                                🏆 الميزة: {r.get('Competitive Advantage', 'N/A')[:50]}...
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                    with st.expander("📖 سابقة الأعمال والتفاصيل"):
                        st.write(f"**نبذة عن الشركة:** {r.get('Detailed_Info', 'لا توجد بيانات')}")
