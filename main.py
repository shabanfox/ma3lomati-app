# 7. عرض النتائج
    st.markdown(f'<div style="padding: 0 10%; margin-bottom:10px;"><p style="color:#64748b;">تم العثور على ({len(f_df)}) نتائج</p></div>', unsafe_allow_html=True)
    
    for _, row in f_df.iterrows():
        # حل مشكلة KeyError: بنجرب نجيب الرابط، ولو مش موجود بنحط صورة افتراضية
        try:
            img = row['Image_URL'] if pd.notnull(row['Image_URL']) else "https://via.placeholder.com/400"
        except KeyError:
            img = "https://via.placeholder.com/400" # صورة احتياطية لو العمود مش موجود
            
        st.markdown(f'''
            <div class="project-card">
                <div class="card-img" style="background-image: url('{img}')"></div>
                <div class="card-body">
                    <div class="price-tag">يبدأ من {row.get('Price', 'غير محدد')} ج.م</div>
                    <div class="dev-name">{row.get('Developer', 'مطور غير معروف')}</div>
                    <div style="color:#D4AF37; font-weight:700;">المالك: {row.get('Owner', 'غير مدرج')}</div>
                    <div style="color:#1e293b; margin-top:5px;"><b>أهم المشاريع:</b> {row.get('Projects', 'جاري التحديث')}</div>
                    <div style="color:#64748b; font-size:0.85rem;">📍 {row.get('Area', 'منطقة غير محددة')}</div>
                </div>
                <div style="display:flex; align-items:center; padding-left:30px;">
                    <button class="btn-view">التفاصيل</button>
                </div>
            </div>
        ''', unsafe_allow_html=True)
