import streamlit as st

# 1. Page Config
st.set_page_config(page_title="MA3LOMATI PRO", layout="wide")

# 2. Ultra-Modern CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
    
    /* Clean Setup */
    [data-testid="stHeader"], .stDeployButton, #MainMenu, footer {display: none !important;}
    
    html, body, [data-testid="stAppViewContainer"] {
        direction: RTL;
        text-align: right;
        font-family: 'Cairo', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }

    /* Modern Top Bar */
    .top-glass-nav {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        padding: 20px 60px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.3);
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 30px;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
    }

    /* Luxury Info Card (Sidebar-like but inside) */
    .info-glass-card {
        background: white;
        border-radius: 24px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.8);
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        position: sticky;
        top: 20px;
    }

    /* Property Premium Card */
    .prop-card-v3 {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        border: 1px solid transparent;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .prop-card-v3:hover {
        transform: translateY(-10px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.08);
        border-color: #6366f1;
    }

    .price-tag-v3 {
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
        color: white;
        padding: 12px 25px;
        border-radius: 15px;
        font-weight: 900;
        font-size: 1.2rem;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }

    .badge-v3 {
        background: #eef2ff;
        color: #4338ca;
        padding: 5px 15px;
        border-radius: 10px;
        font-size: 0.8rem;
        font-weight: 700;
        margin-bottom: 10px;
        display: inline-block;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background: white !important;
        border-left: 1px solid #e2e8f0;
    }
    
    h1, h2, h3 { color: #1e293b; font-weight: 900; }
    </style>
""", unsafe_allow_html=True)

# 3. Layout Structure
st.markdown("""
    <div class="top-glass-nav">
        <div style="font-size: 1.8rem; font-weight: 900; color: #4338ca;">MA3LOMATI <span style="color: #1e293b;">PRO</span></div>
        <div style="color: #64748b; font-weight: 600;">مرحباً بك، أ/ بروكر المحترف</div>
    </div>
""", unsafe_allow_html=True)

# Main Grid
col_content, col_info = st.columns([2.5, 1], gap="large")

with col_info:
    # Sidebar Info (Developer Profile)
    st.markdown("""
        <div class="info-glass-card">
            <h3 style="margin-bottom: 20px;">🏢 ملف المطور</h3>
            <div style="text-align: center; margin-bottom: 20px;">
                <div style="width: 80px; height: 80px; background: #f3f4f6; border-radius: 20px; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 2rem;">🏗️</div>
            </div>
            <h4 style="text-align: center; color: #4338ca;">PRE Developments</h4>
            <p style="color: #64748b; font-size: 0.95rem; line-height: 1.8; text-align: center;">
                رؤية جديدة للتطوير العقاري في مصر، نركز على الجودة والرفاهية في كل تفصيلة.
            </p>
            <hr style="opacity: 0.1; margin: 20px 0;">
            <div style="display: flex; justify-content: space-around; text-align: center;">
                <div><b style="display: block; color: #4338ca;">12</b><small>مشروع</small></div>
                <div><b style="display: block; color: #4338ca;">15</b><small>سنة خبرة</small></div>
                <div><b style="display: block; color: #4338ca;">+5k</b><small>عميل</small></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with col_content:
    # Search & Tabs Area
    st.markdown("### 🔎 استكشاف المشاريع")
    
    # Custom Project Cards Function
    def draw_card(title, loc, price, tag):
        st.markdown(f"""
            <div class="prop-card-v3">
                <div style="flex: 2;">
                    <span class="badge-v3">{tag}</span>
                    <h3 style="margin: 0 0 10px 0;">{title}</h3>
                    <div style="color: #64748b; display: flex; align-items: center; gap: 5px;">
                        📍 {loc}
                    </div>
                </div>
                <div style="text-align: left;">
                    <div class="price-tag-v3">{price} ج.م</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    draw_card("كمبوند ذا بروكس - The Brooks", "القاهرة الجديدة - التجمع", "6,500,000", "سكني")
    draw_card("ستون ريزيدنس - Stone Residence", "التجمع الخامس", "5,200,000", "استلام فوري")
    draw_card("ايفوري جولي - Ivoire Zayed", "الشيخ زايد الجديدة", "9,800,000", "تحت الإنشاء")

# Sidebar for Search (Native)
with st.sidebar:
    st.markdown("### ⚙️ فلاتر البحث")
    st.selectbox("اختر المطور", ["PRE Developments", "Sodic", "Mountain View"])
    st.multiselect("المنطقة", ["التجمع", "أكتوبر", "زايد", "العاصمة"])
    st.write("---")
    st.button("تحديث البيانات 🔄", use_container_width=True)
