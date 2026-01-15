import React, { useState, useEffect } from 'react';
import { TrendingUp, Award, ChevronRight, RefreshCw, Search, MapPin, Filter, Menu, Bell } from 'lucide-react';

// --- المكون الفرعي: قائمة أقوى 10 مطورين (The 30% Side) ---
const TopDevelopersSidebar = () => {
  const [loading, setLoading] = useState(true);
  const [developers, setDevelopers] = useState([]);

  useEffect(() => {
    // محاكاة جلب البيانات المتجددة
    setTimeout(() => {
      setDevelopers([
        { id: 1, name: "طلعت مصطفى (TMG)", sales: "140B EGP", growth: "+25%" },
        { id: 2, name: "بالم هيلز (Palm Hills)", sales: "95B EGP", growth: "+18%" },
        { id: 3, name: "أورا (Ora Developers)", sales: "88B EGP", growth: "+30%" },
        { id: 4, name: "ماونتن فيو (DMG)", sales: "72B EGP", growth: "+15%" },
        { id: 5, name: "إعمار مصر (Emaar)", sales: "65B EGP", growth: "+10%" },
        { id: 6, name: "سوديك (SODIC)", sales: "60B EGP", growth: "+12%" },
        { id: 7, name: "مدينة مصر", sales: "45B EGP", growth: "+22%" },
        { id: 8, name: "سيتي إيدج", sales: "42B EGP", growth: "+8%" },
        { id: 9, name: "لافيستا (La Vista)", sales: "38B EGP", growth: "+5%" },
        { id: 10, name: "هايد بارك", sales: "35B EGP", growth: "+9%" },
      ]);
      setLoading(false);
    }, 800);
  }, []);

  return (
    <div className="bg-white rounded-2xl shadow-sm border border-slate-200 h-full flex flex-col">
      <div className="p-5 border-b border-slate-100 flex justify-between items-center bg-slate-50 rounded-t-2xl">
        <div>
          <h3 className="font-bold text-slate-800 flex items-center gap-2">
            <Award className="text-amber-500 w-5 h-5" />
            تصنيف المطورين 2026
          </h3>
        </div>
        <RefreshCw className={`w-4 h-4 text-slate-400 ${loading ? 'animate-spin' : ''}`} />
      </div>
      
      <div className="flex-1 overflow-y-auto p-2 custom-scrollbar">
        {loading ? (
          [...Array(8)].map((_, i) => <div key={i} className="h-14 bg-slate-50 animate-pulse m-2 rounded-lg" />)
        ) : (
          developers.map((dev, index) => (
            <div key={dev.id} className="group flex items-center justify-between p-3 hover:bg-slate-50 transition-all cursor-pointer rounded-xl border border-transparent hover:border-slate-100">
              <div className="flex items-center gap-3">
                <span className={`w-6 h-6 flex items-center justify-center rounded-lg text-xs font-bold 
                  ${index < 3 ? 'bg-slate-800 text-white' : 'bg-slate-100 text-slate-500'}`}>
                  {index + 1}
                </span>
                <div>
                  <h4 className="font-bold text-slate-700 text-sm group-hover:text-blue-600 transition-colors">{dev.name}</h4>
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] text-slate-400 font-medium">{dev.sales}</span>
                    <span className="text-[10px] text-green-500 font-bold">{dev.growth}</span>
                  </div>
                </div>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-300 group-hover:text-blue-500 transform group-hover:translate-x-1 transition-all" />
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// --- المكون الرئيسي: المنصة بالكامل ---
export default function RealEstatePlatform() {
  return (
    <div className="min-h-screen bg-[#F8FAFC] font-sans text-right" dir="rtl">
      
      {/* 1. Header / Navigation */}
      <nav className="bg-white border-b border-slate-200 px-6 py-4 sticky top-0 z-50 shadow-sm">
        <div className="max-w-[1600px] mx-auto flex justify-between items-center">
          <div className="flex items-center gap-8">
            <h1 className="text-2xl font-black text-slate-900 tracking-tighter">ESTATE<span className="text-blue-600">PRO</span></h1>
            <div className="hidden md:flex items-center gap-6 text-slate-600 font-medium">
              <a href="#" className="hover:text-blue-600">المشاريع</a>
              <a href="#" className="hover:text-blue-600">الخريطة الذكية</a>
              <a href="#" className="hover:text-blue-600">تحليل السوق</a>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <div className="relative">
              <Search className="w-5 h-5 absolute right-3 top-2.5 text-slate-400" />
              <input type="text" placeholder="بحث عن مطور أو مشروع..." className="bg-slate-100 pr-10 pl-4 py-2 rounded-full text-sm w-64 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all" />
            </div>
            <button className="p-2 bg-slate-100 rounded-full text-slate-600"><Bell size={20}/></button>
            <div className="w-10 h-10 bg-blue-600 rounded-full border-2 border-white shadow-sm flex items-center justify-center text-white font-bold">A</div>
          </div>
        </div>
      </nav>

      {/* 2. Main Content Area */}
      <main className="max-w-[1600px] mx-auto p-6 flex flex-col lg:flex-row gap-6 h-[calc(100vh-85px)]">
        
        {/* الجزء الـ 70% (Content Area) */}
        <div className="lg:w-[70%] flex flex-col gap-6">
          {/* Welcome & Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="bg-blue-600 p-6 rounded-2xl text-white shadow-lg shadow-blue-100">
              <p className="text-blue-100 text-sm">إجمالي مبيعات السوق اليوم</p>
              <h2 className="text-3xl font-bold mt-1">2.4B <span className="text-lg font-normal">EGP</span></h2>
            </div>
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <p className="text-slate-400 text-sm">المشاريع الجديدة (2026)</p>
              <h2 className="text-3xl font-bold text-slate-800 mt-1">128</h2>
            </div>
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
              <p className="text-slate-400 text-sm">مؤشر نمو العقارات</p>
              <h2 className="text-3xl font-bold text-green-500 mt-1">+14.2%</h2>
            </div>
          </div>

          {/* Main Visual/Map Placeholder */}
          <div className="flex-1 bg-white rounded-3xl border border-slate-200 shadow-sm relative overflow-hidden group">
            <div className="absolute inset-0 bg-[url('https://www.google.com/maps/about/images/home/home-map-visual.jpg')] bg-cover opacity-20 group-hover:scale-105 transition-transform duration-700"></div>
            <div className="relative z-10 p-8 flex flex-col h-full">
              <div className="flex justify-between items-start">
                <h2 className="text-2xl font-bold text-slate-800">الخريطة العقارية التفاعلية</h2>
                <button className="bg-white p-2 rounded-lg shadow-sm border border-slate-100 flex items-center gap-2 text-sm font-bold"><Filter size={16}/> تصفية النتائج</button>
              </div>
              <div className="mt-auto flex gap-4">
                 <div className="bg-white/90 backdrop-blur p-4 rounded-xl border border-white shadow-xl max-w-xs">
                    <p className="text-xs text-blue-600 font-bold mb-1 italic">أحدث طرح</p>
                    <h4 className="font-bold text-slate-800">نور سيتي - طلعت مصطفى</h4>
                    <p className="text-xs text-slate-500 mt-1 flex items-center gap-1"><MapPin size={10}/> حدائق العاصمة</p>
                 </div>
              </div>
            </div>
          </div>
        </div>

        {/* الجزء الـ 30% (Developers Ranking) */}
        <div className="lg:w-[30%]">
          <TopDevelopersSidebar />
        </div>

      </main>
    </div>
  );
}
    
    r_limit = 8
    r_start = st.session_state.ready_idx * r_limit
    r_page = ready_df.iloc[r_start : r_start + r_limit]
    
    st.markdown("<div class='ready-sidebar-container'>", unsafe_allow_html=True)
    for _, row in r_page.iterrows():
        st.markdown(f"<div class='ready-card'><div class='ready-title'>{row.get('Project Name')}</div><div class='ready-loc'>📍 {row.get('Area')}</div></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    # أزرار تحكم الاستلام الفوري
    rc1, rc2 = st.columns(2)
    if rc1.button("السابق 🔼", key="r_prev"): st.session_state.ready_idx = max(0, st.session_state.ready_idx - 1); st.rerun()
    if rc2.button("التالي 🔽", key="r_next"): 
        if r_start + r_limit < len(ready_df): st.session_state.ready_idx += 1; st.rerun()

# --- الجانب الرئيسي ---
with main_col:
    if menu == "المشاريع":
        search = st.text_input("🔍 بحث في المشاريع...")
        filtered = df_p.copy()
        if search: filtered = filtered[filtered.apply(lambda r: r.astype(str).str.contains(search, case=False).any(), axis=1)]
        
        p_page = filtered.iloc[st.session_state.p_idx*6 : (st.session_state.p_idx+1)*6]
        for i in range(0, len(p_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(p_page):
                    r = p_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3 style='color:#f59e0b; font-size:18px;'>{r.get('Project Name')}</h3><p style='font-size:13px;'>📍 {r.get('Area')}</p><p style='color:#aaa; font-size:12px;'>🏢 {r.get('Developer')}</p></div>", unsafe_allow_html=True)
                        with st.expander("التفاصيل الكاملة"):
                            st.write(f"🎨 **Master Plan:** {r.get('Master Plan')}")
                            st.write(f"⚙️ **Management:** {r.get('Management')}")
                            st.write(f"✨ **المميزات:** {r.get('Project Features')}")

    elif menu == "المطورين":
        d_page = df_d.iloc[st.session_state.d_idx*6 : (st.session_state.d_idx+1)*6]
        for i in range(0, len(d_page), 2):
            cols = st.columns(2)
            for j in range(2):
                if i+j < len(d_page):
                    r = d_page.iloc[i+j]
                    with cols[j]:
                        st.markdown(f"<div class='grid-card'><h3>{r.get('Developer')}</h3><p>👤 {r.get('Owner')}</p><p style='color:#10b981;'>🏗️ المشاريع: {r.get('Number of Projects')}</p></div>", unsafe_allow_html=True)
                        with st.expander("سابقة الأعمال"): st.write(r.get('Detailed_Info'))

    elif menu == "الأدوات":
        st.markdown("<h2 style='color:#f59e0b;'>🛠️ صندوق أدوات البروكر الذكي</h2>", unsafe_allow_html=True)
        t1, t2, t3, t4, t5 = st.tabs(["🧮 حاسبة الأقساط", "💰 العائد والعمولة", "📐 تحويل المساحات", "🕵️ رادار البحث", "📝 المفكرة"])
        
        with t1:
            c1, c2 = st.columns(2)
            price = c1.number_input("سعر الوحدة", 1000000)
            down = c2.number_input("المقدم", price*0.1)
            years = st.slider("سنوات التقسيط", 1, 15, 8)
            st.metric("القسط الشهري", f"{(price-down)/(years*12):,.0f} ج.م")
            
        with t2:
            c1, c2 = st.columns(2)
            rent = c1.number_input("الإيجار المتوقع", 10000)
            comm_pct = c2.number_input("نسبة العمولة %", 1.5)
            st.info(f"📈 العائد السنوي (ROI): {(rent*12/price)*100:.2f}%")
            st.success(f"💵 عمولة البيع المتوقعة: {price*(comm_pct/100):,.0f} ج.م")

        with t3:
            sqm = st.number_input("المساحة بالمتر المربع", 100.0)
            st.write(f"📏 بالقدم المربع: {sqm*10.76:,.2f} sqft")
            st.write(f"📏 بالفدان: {sqm/4200:.4f} فدان")

        with t4:
            radar = st.text_input("🕵️ ابحث عن أي مشروع أو مطور في جوجل...")
            if radar: st.link_button(f"بحث عن {radar}", f"https://www.google.com/search?q={urllib.parse.quote(radar + ' عقارات مصر')}")

        with t5:
            st.text_area("📝 سجل ملاحظاتك السريعة هنا (لحفظها مؤقتاً أثناء المكالمة):")
            st.button("حفظ الملاحظات")

if st.button("🚪 خروج"): st.session_state.auth = False; st.rerun()

