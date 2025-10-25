import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Otsuka Bank Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'language' not in st.session_state:
        st.session_state.language = 'JP'
    if 'theme' not in st.session_state:
        st.session_state.theme = 'light'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # 사용자 데이터
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            "name": "山田 太郎",
            "assets": {
                "total": 15480230,
                "deposits": 12045000,
                "loans": 2560000,
                "investments": 875230,
                "savings": 3500000,
                "credit_card": 125000
            },
            "account": "098-96586-6521",
            "emp_num": "12345678",
            "department": "IT事業部",
            "join_date": "2020年4月"
        }
    
    # 급여명세서 데이터
    if 'payslip_data' not in st.session_state:
        st.session_state.payslip_data = {
            "income_items": [
                {"name": "基本給", "amount": 340000},
                {"name": "役職手当", "amount": 50000},
                {"name": "時間外手当", "amount": 25000},
                {"name": "交通費", "amount": 15000}
            ],
            "deduction_items": [
                {"name": "所得税", "amount": 26320},
                {"name": "住民税", "amount": 6520},
                {"name": "健康保険", "amount": 8910},
                {"name": "厚生年金", "amount": 29960},
                {"name": "雇用保険", "amount": 4550},
                {"name": "その他控除", "amount": 70000}
            ]
        }
    
    # 적금 데이터
    if 'savings_data' not in st.session_state:
        st.session_state.savings_data = {
            "name": "山田 太郎",
            "emp_num": "12345678",
            "account": "098-96586-6521",
            "start_date": date(2025, 2, 25),
            "unit_price": 1100,
            "original_units": 4,
            "current_units": 4,
            "years": 3,
            "interest": 10.03,
            "adjustments": []
        }

# 다국어 지원
LANGUAGES = {
    'JP': {
        'title': '大塚銀行 従業員ポータル',
        'subtitle': 'Otsuka Bank Employee Portal',
        'login_id': 'ログインID',
        'password': 'パスワード',
        'login': 'ログイン',
        'login_error': 'ログインIDまたはパスワードが正しくありません',
        'home': '🏠 ホーム',
        'loan': '💰 積立管理',
        'payroll': '📄 給与明細',
        'welcome': 'ようこそ、{}様',
        'last_login': '最終ログイン',
        'account_number': '口座番号',
        'asset_overview': '資産概要',
        'total_assets': '総資産',
        'deposits': '普通預金',
        'loans': 'ローン残高',
        'investments': '投資資産',
        'savings': '積立預金',
        'credit_card': 'クレジット',
        'recent_transactions': '最近の取引',
        'financial_overview': '財務概要',
        'quick_actions': 'クイックアクション',
        'transfer': '振込',
        'payment': '支払い',
        'exchange': '為替',
        'date': '日付',
        'description': '取引内容',
        'amount': '金額',
        'counterparty': '取引先',
        'status': '状態',
        'income_breakdown': '支給内訳',
        'deduction_breakdown': '控除内訳',
        'basic_salary': '基本給',
        'create_payslip': '明細作成',
        'payslip_title': '給与明細書',
        'total_income': '総支給額',
        'total_deduction': '総控除額',
        'net_pay': '差引支給額',
        'savings_management': '積立貯蓄管理システム',
        'savings_subtitle': 'Otsuka Shokai Savings Management System',
        'customer_name': '顧客名',
        'employee_number': '社員番号',
        'account_number': '口座番号',
        'start_date': '積立開始日',
        'unit_price': '1口座金額 (¥)',
        'units': '申込口座数',
        'years': '満期期間 (年)',
        'interest_rate': '年利率 (%)',
        'register': '💾 登録',
        'basic_info': '基本情報',
        'maturity_date': '満期日',
        'savings_overview': '積立概要',
        'monthly_payment': '月々積立額',
        'total_months': '総積立回数',
        'total_savings': '総積立額',
        'estimated_interest': '予想利息',
        'payment_schedule': '入金スケジュール',
        'payment_date': '入金日',
        'payment_amount': '入金額',
        'cumulative_balance': '累計残高',
        'interest': '利息',
        'notes': '備考',
        'logout': 'ログアウト',
        'theme_light': 'ライトモード',
        'theme_dark': 'ダークモード',
        'view_details': '詳細を見る',
        'monthly_trend': '月次推移',
        'asset_allocation': '資産配分'
    },
    'KR': {
        'title': '오츠카 은행 직원 포털',
        'subtitle': 'Otsuka Bank Employee Portal',
        'login_id': '로그인 ID',
        'password': '비밀번호',
        'login': '로그인',
        'login_error': '로그인 ID 또는 비밀번호가 올바르지 않습니다',
        'home': '🏠 홈',
        'loan': '💰 적금 관리',
        'payroll': '📄 급여 명세서',
        'welcome': '{}님, 환영합니다',
        'last_login': '최종 로그인',
        'account_number': '계좌번호',
        'asset_overview': '자산 현황',
        'total_assets': '총 자산',
        'deposits': '보통예금',
        'loans': '대출 잔액',
        'investments': '투자 자산',
        'savings': '적금',
        'credit_card': '신용카드',
        'recent_transactions': '최근 거래 내역',
        'financial_overview': '재무 개요',
        'quick_actions': '빠른 실행',
        'transfer': '송금',
        'payment': '결제',
        'exchange': '환전',
        'date': '날짜',
        'description': '거래 내용',
        'amount': '금액',
        'counterparty': '거래처',
        'status': '상태',
        'income_breakdown': '지급 내역',
        'deduction_breakdown': '공제 내역',
        'basic_salary': '기본급',
        'create_payslip': '명세서 생성',
        'payslip_title': '급여 명세서',
        'total_income': '총 지급액',
        'total_deduction': '총 공제액',
        'net_pay': '차인 지급액',
        'savings_management': '적금 관리 시스템',
        'savings_subtitle': 'Otsuka Shokai Savings Management System',
        'customer_name': '고객명',
        'employee_number': '사원번호',
        'account_number': '계좌번호',
        'start_date': '적금 시작일',
        'unit_price': '1구좌 금액 (¥)',
        'units': '신청 구좌수',
        'years': '만기 기간 (년)',
        'interest_rate': '연이율 (%)',
        'register': '💾 등록',
        'basic_info': '기본 정보',
        'maturity_date': '만기일',
        'savings_overview': '적금 개요',
        'monthly_payment': '월 납입액',
        'total_months': '총 납입 횟수',
        'total_savings': '총 적금액',
        'estimated_interest': '예상 이자',
        'payment_schedule': '납입 일정',
        'payment_date': '납입일',
        'payment_amount': '납입액',
        'cumulative_balance': '누적 잔액',
        'interest': '이자',
        'notes': '비고',
        'logout': '로그아웃',
        'theme_light': '라이트 모드',
        'theme_dark': '다크 모드',
        'view_details': '상세 보기',
        'monthly_trend': '월별 추이',
        'asset_allocation': '자산 배분'
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language][key]

# CSS 스타일링
def load_css():
    css = """
    <style>
    /* 기본 스타일 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Noto Sans JP', 'Malgun Gothic', 'Segoe UI', sans-serif;
    }
    
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        min-height: calc(100vh - 40px);
    }
    
    .dark-mode .main-container {
        background: rgba(18, 18, 18, 0.95);
        color: white;
    }
    
    /* 헤더 스타일 */
    .bank-header {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: white;
        padding: 2rem 3rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .bank-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 1px, transparent 1px);
        background-size: 20px 20px;
        animation: float 20s infinite linear;
    }
    
    @keyframes float {
        0% { transform: translate(0, 0) rotate(0deg); }
        100% { transform: translate(-100px, -100px) rotate(360deg); }
    }
    
    .bank-title {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0,0,0,0.3);
    }
    
    .bank-subtitle {
        font-size: 1.2rem !important;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* 컨트롤 버튼 */
    .header-controls {
        position: absolute;
        top: 1.5rem;
        right: 2rem;
        display: flex;
        gap: 0.8rem;
        z-index: 100;
    }
    
    .control-btn {
        background: rgba(255,255,255,0.2) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        border-radius: 25px !important;
        padding: 0.5rem 1.2rem !important;
        font-weight: 500 !important;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease !important;
    }
    
    .control-btn:hover {
        background: rgba(255,255,255,0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    /* 네비게이션 */
    .nav-container {
        background: white;
        border-radius: 15px;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        display: flex;
        gap: 0;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .dark-mode .nav-container {
        background: #2d3748;
        border: 1px solid #4a5568;
    }
    
    .nav-item {
        padding: 1rem 2rem;
        border-radius: 10px;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #666;
        text-decoration: none;
        margin: 0 0.5rem;
    }
    
    .dark-mode .nav-item {
        color: #cbd5e0;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .nav-item:hover:not(.active) {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
    }
    
    /* 카드 스타일 */
    .asset-card {
        background: linear-gradient(135deg, #fff, #f8f9fa);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 25px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .dark-mode .asset-card {
        background: linear-gradient(135deg, #2d3748, #4a5568);
        border: 1px solid #4a5568;
    }
    
    .asset-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    .asset-value {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2c3e50, #3498db);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
    }
    
    .dark-mode .asset-value {
        background: linear-gradient(135deg, #fff, #cbd5e0);
        -webkit-background-clip: text;
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
        transition: all 0.3s ease;
    }
    
    .dark-mode .metric-card {
        background: #2d3748;
        border-left: 4px solid #764ba2;
    }
    
    .metric-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* 입력 필드 */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
        font-size: 1rem !important;
        background: white !important;
        transition: all 0.3s ease !important;
    }
    
    .dark-mode .stTextInput>div>div>input,
    .dark-mode .stNumberInput>div>div>input,
    .dark-mode .stDateInput>div>div>input,
    .dark-mode .stSelectbox>div>div>select {
        background: #2d3748 !important;
        border-color: #4a5568 !important;
        color: white !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stDateInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* 데이터프레임 */
    .dataframe {
        border-radius: 10px !important;
        overflow: hidden !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
    }
    
    /* 급여명세서 */
    .paystub-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    .dark-mode .paystub-container {
        background: #2d3748;
        border: 1px solid #4a5568;
    }
    
    /* 유틸리티 */
    .text-gradient {
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    .glass-effect {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Malgun+Gothic:wght@300;400;500;600;700&display=swap');
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
    
    # 다크모드 클래스 추가
    if st.session_state.theme == 'dark':
        st.markdown('<div class="dark-mode">', unsafe_allow_html=True)

def render_language_switcher():
    current_lang = st.session_state.language
    if current_lang == 'JP':
        if st.button("🇰🇷 한국어", key="lang_switch", help="Switch to Korean"):
            st.session_state.language = 'KR'
            st.rerun()
    else:
        if st.button("🇯🇵 日本語", key="lang_switch", help"Switch to Japanese"):
            st.session_state.language = 'JP'
            st.rerun()
    return ""

def render_theme_switcher():
    current_theme = st.session_state.theme
    if current_theme == 'light':
        if st.button("🌙", key="theme_switch", help=get_text('theme_dark')):
            st.session_state.theme = 'dark'
            st.rerun()
    else:
        if st.button("☀️", key="theme_switch", help=get_text('theme_light')):
            st.session_state.theme = 'light'
            st.rerun()
    return ""

def render_logout():
    if st.button(get_text('logout'), key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()
    return ""

def render_nav():
    nav_items = [
        ('home', get_text('home')),
        ('loan', get_text('loan')), 
        ('payroll', get_text('payroll'))
    ]
    
    cols = st.columns(len(nav_items))
    for idx, (page, label) in enumerate(nav_items):
        with cols[idx]:
            if st.button(label, use_container_width=True, 
                        type="primary" if st.session_state.current_page == page else "secondary"):
                st.session_state.current_page = page
                st.rerun()

# 대시보드 - 자산 현황
def render_dashboard():
    st.markdown(f"### {get_text('asset_overview')}")
    
    assets = st.session_state.user_data['assets']
    
    # 자산 카드
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="asset-card">
            <div style="color:#666; font-size:0.9rem;">{get_text('total_assets')}</div>
            <div class="asset-value">¥{assets['total']:,}</div>
            <div style="color:#27ae60; font-weight:600;">↗️ +2.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="asset-card">
            <div style="color:#666; font-size:0.9rem;">{get_text('deposits')}</div>
            <div class="asset-value">¥{assets['deposits']:,}</div>
            <div style="color:#666;">普通預金・定期預金</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="asset-card">
            <div style="color:#666; font-size:0.9rem;">{get_text('investments')}</div>
            <div class="asset-value">¥{assets['investments']:,}</div>
            <div style="color:#27ae60; font-weight:600;">↗️ +5.1%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="asset-card">
            <div style="color:#666; font-size:0.9rem;">{get_text('savings')}</div>
            <div class="asset-value">¥{assets['savings']:,}</div>
            <div style="color:#666;">積立預金</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 그래프와 트랜드
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### {get_text('monthly_trend')}")
        # 자산 추이 그래프
        months = ['1月', '2月', '3月', '4月', '5月', '6月']
        values = [14200000, 14500000, 14800000, 15000000, 15200000, 15480230]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=values,
            mode='lines+markers',
            line=dict(color='#667eea', width=4),
            marker=dict(size=8, color='#764ba2'),
            fill='tozeroy',
            fillcolor='rgba(102, 126, 234, 0.1)'
        ))
        
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#2c3e50'),
            margin=dict(l=0, r=0, t=30, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown(f"### {get_text('asset_allocation')}")
        # 자산 배분 파이 차트
        labels = [get_text('deposits'), get_text('investments'), get_text('savings'), get_text('loans')]
        values = [assets['deposits'], assets['investments'], assets['savings'], assets['loans']]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=.3,
            marker_colors=['#667eea', '#764ba2', '#f093fb', '#4ecdc4']
        )])
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=30, b=0),
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # 최근 거래
    st.markdown(f"### {get_text('recent_transactions')}")
    recent_transactions = [
        ["2025/02/15", "給与振込", "¥340,000", "大塚銀行", "✅ 完了"],
        ["2025/02/10", "家賃支払い", "¥120,000", "SMBCアパート", "✅ 完了"],
        ["2025/02/05", "投資信託購入", "¥50,000", "大塚証券", "✅ 完了"],
        ["2025/02/01", "公共料金", "¥24,500", "東京電力", "✅ 完了"],
        ["2025/01/28", "カード決済", "¥18,700", "Amazon Japan", "✅ 完了"],
    ]
    
    df_columns = [get_text('date'), get_text('description'), get_text('amount'), get_text('counterparty'), get_text('status')]
    st.dataframe(
        pd.DataFrame(recent_transactions, columns=df_columns),
        use_container_width=True,
        height=250
    )

# 로그인 페이지
def login():
    st.markdown(f"""
    <div class="bank-header">
        <div class="header-controls">
            {render_language_switcher()}
            {render_theme_switcher()}
        </div>
        <h1 class="bank-title">{get_text('title')}</h1>
        <p class="bank-subtitle">{get_text('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("### ログイン")
            with st.form("login_form"):
                user_id = st.text_input(get_text('login_id'), placeholder="otsuka")
                password = st.text_input(get_text('password'), type="password", placeholder="bank1234")
                
                if st.form_submit_button(get_text('login'), use_container_width=True):
                    if user_id == "otsuka" and password == "bank1234":
                        st.session_state.logged_in = True
                        st.session_state.current_page = 'home'
                        st.rerun()
                    else:
                        st.error(get_text('login_error'))

# 메인 앱
def main():
    initialize_session_state()
    load_css()
    
    # 메인 컨테이너 시작
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        login()
    else:
        # 헤더
        st.markdown(f"""
        <div class="bank-header">
            <div class="header-controls">
                {render_language_switcher()}
                {render_theme_switcher()}
                {render_logout()}
            </div>
            <h1 class="bank-title">{get_text('title')}</h1>
            <p class="bank-subtitle">{get_text('subtitle')}</p>
            <div style="margin-top: 1rem;">
                <h3 style="margin:0; font-weight:300;">{get_text('welcome').format(st.session_state.user_data['name'])}</h3>
                <p style="margin:0; opacity:0.8;">{st.session_state.user_data['department']} | {get_text('account_number')}: {st.session_state.user_data['account']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 네비게이션
        render_nav()
        
        # 페이지 내용
        if st.session_state.current_page == 'home':
            render_dashboard()
        elif st.session_state.current_page == 'loan':
            # 간단한 적금 관리 페이지 (기존 코드와 유사)
            st.info("積立管理ページは現在開発中です。")
        elif st.session_state.current_page == 'payroll':
            # 간단한 급여명세서 페이지 (기존 코드와 유사)
            st.info("給与明細ページは現在開発中です。")
    
    # 메인 컨테이너 종료
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 다크모드 클래스 종료
    if st.session_state.theme == 'dark':
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()