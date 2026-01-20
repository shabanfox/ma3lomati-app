# 4. التنسيق الجمالي المطور - ألوان 2026 الاحترافية
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700;900&display=swap');
    
    /* الخلفية العامة */
    .block-container {{ padding-top: 0rem !important; }}
    header, [data-testid="stHeader"] {{ visibility: hidden; display: none; }}
    [data-testid="stAppViewContainer"] {{ 
        background-color: #050505; 
        direction: rtl !important; 
        text-align: right !important; 
        font-family: 'Cairo', sans-serif; 
    }}
    
    /* شريط الأخبار العلوي */
    .ticker-wrap {{ 
        width: 100%; 
        background: #111; 
        padding: 8px 0; 
        overflow: hidden; 
        white-space: nowrap; 
        border-bottom: 2px solid #f59e0b; 
        margin-bottom: 20px; 
    }}
    .ticker {{ 
        display: inline-block; 
        animation: ticker 120s linear infinite; 
        color: #f59e0b; 
        font-size: 14px; 
        font-weight: bold;
    }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}

    /* تنسيق الأزرار والكروت */
    div.stButton > button {{ 
        border-radius: 12px !important; 
        font-family: 'Cairo', sans-serif !important; 
        transition: 0.4s all ease !important; 
    }}
    
    /* كروت المشاريع والمطورين الفخمة */
    div.stButton > button[key*="card_"], div.stButton > button[key*="ready_"] {{
        background-color: #1a1a1a !important; 
        color: #ffffff !important;
        min-height: 140px !important; 
        text-align: right !important;
        font-weight: 700 !important; 
        font-size: 16px !important;
        border: 1px solid #333 !important; 
        border-right: 5px solid #f59e0b !important;
        margin-bottom: 15px !important;
        display: block !important; 
        width: 100% !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3) !important;
    }}
    
    div.stButton > button[key*="card_"]:hover, div.stButton > button[key*="ready_"]:hover {{ 
        background-color: #222 !important;
        transform: translateY(-5px) !important; 
        border-color: #f59e0b !important;
        box-shadow: 0 10px 20px rgba(245,158,11,0.15) !important; 
    }}
    
    /* الصناديق الذكية */
    .smart-box {{ 
        background: #111; 
        border: 1px solid #222; 
        padding: 30px; 
        border-radius: 20px; 
        border-right: 6px solid #f59e0b; 
        color: #eeeeee;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }}
    
    .side-card {{ 
        background: #161616; 
        padding: 18px; 
        border-radius: 15px; 
        border-right: 3px solid #10b981; 
        margin-bottom: 12px;
        color: #ffffff;
    }}
    
    .tool-card {{ 
        background: #121212; 
        padding: 25px; 
        border-radius: 20px; 
        border: 1px solid #222;
        border-top: 5px solid #f59e0b; 
        text-align: center; 
        height: 100%; 
        color: #ffffff;
    }}

    /* ألوان العناوين والمدخلات */
    h1, h2, h3, h4 {{ color: #f59e0b !important; font-weight: 900 !important; }}
    .stSelectbox label, .stTextInput label, .stNumberInput label {{ 
        color: #f59e0b !important; 
        font-weight: bold !important; 
        font-size: 15px !important;
    }}
    
    /* تعديل الـ Tabs لتبدو احترافية */
    .stTabs [data-baseweb="tab-list"] {{ gap: 10px; }}
    .stTabs [data-baseweb="tab"] {{
        background-color: #1a1a1a;
        border-radius: 10px 10px 0 0;
        padding: 10px 20px;
        color: #aaa;
    }}
    .stTabs [aria-selected="true"] {{
        background-color: #f59e0b !important;
        color: #000 !important;
        font-weight: bold;
    }}
    </style>
""", unsafe_allow_html=True)
