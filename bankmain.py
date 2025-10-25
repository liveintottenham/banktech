import streamlit as st
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import time

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
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'adjustments' not in st.session_state:
        st.session_state.adjustments = []
    if 'last_capture_warning' not in st.session_state:
        st.session_state.last_capture_warning = 0
    
    # 사용자 데이터
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            "name": "山田 太郎",
            "account": "098-96586-6521",
            "emp_num": "12345678",
            "department": "IT事業部"
        }
    
    # 적금 데이터 저장소
    if 'savings_list' not in st.session_state:
        st.session_state.savings_list = []
    
    # 급여 데이터 저장소
    if 'payroll_list' not in st.session_state:
        st.session_state.payroll_list = []

# 다국어 지원
LANGUAGES = {
    'EN': {
        'title': 'Otsuka Bank Employee Portal',
        'subtitle': 'Secure Banking Management System',
        'login_id': 'Login ID',
        'password': 'Password',
        'login': 'Login',
        'login_error': 'Incorrect Login ID or Password',
        'home': '🏠 Home',
        'savings': '💰 Savings',
        'payroll': '📄 Payroll',
        'welcome': 'Welcome, {}',
        'account_number': 'Account Number',
        'asset_overview': 'Asset Overview',
        'total_savings': 'Total Savings',
        'active_plans': 'Active Plans',
        'monthly_payment': 'Monthly Payment',
        'recent_transactions': 'Recent Transactions',
        'quick_access': 'Quick Access',
        'new_savings': 'New Savings Plan',
        'view_savings': 'View Savings',
        'savings_management': 'Savings Management',
        'savings_name': 'Savings Name',
        'monthly_amount': 'Monthly Amount',
        'period': 'Savings Period',
        'start_date': 'Start Date',
        'interest_rate': 'Annual Interest Rate',
        'create_plan': 'Create Plan',
        'savings_details': 'Savings Details',
        'payment_schedule': 'Payment Schedule',
        'logout': 'Logout',
        'customer_name': 'Customer Name',
        'employee_number': 'Employee Number',
        'basic_info': 'Basic Information',
        'savings_calc': 'Savings Calculator',
        'adjust_payment': 'Payment Adjustment',
        'payment_history': 'Payment History',
        'basic_salary': 'Basic Salary',
        'overtime_pay': 'Overtime Pay',
        'bonus': 'Bonus',
        'allowances': 'Allowances',
        'insurance': 'Insurance',
        'tax': 'Tax',
        'other_deductions': 'Other Deductions',
        'net_salary': 'Net Salary',
        'generate_payslip': 'Generate Payslip',
        'payslip_date': 'Payslip Date',
        'income_items': 'Income Items',
        'deduction_items': 'Deduction Items',
        'total_income': 'Total Income',
        'total_deduction': 'Total Deduction',
        'add_adjustment': 'Add Adjustment',
        'adjustment_month': 'Adjustment Month',
        'adjustment_amount': 'Adjustment Amount',
        'remove': 'Remove',
        'no_capture': '⚠️ この画面のスクリーンショット・撮影は禁止されています',
        'security_warning': '🔒 セキュリティ警告: このページは監視されています'
    },
    'JP': {
        'title': '大塚銀行 従業員ポータル',
        'subtitle': 'セキュアバンキング管理システム',
        'login_id': 'ログインID',
        'password': 'パスワード',
        'login': 'ログイン',
        'login_error': 'ログインIDまたはパスワードが正しくありません',
        'home': '🏠 ホーム',
        'savings': '💰 積立',
        'payroll': '📄 給与',
        'welcome': 'ようこそ、{}様',
        'account_number': '口座番号',
        'asset_overview': '資産概要',
        'total_savings': '総積立額',
        'active_plans': '実行中プラン',
        'monthly_payment': '月間支払額',
        'recent_transactions': '最近の取引',
        'quick_access': 'クイックアクセス',
        'new_savings': '新規積立作成',
        'view_savings': '積立一覧',
        'savings_management': '積立貯蓄管理',
        'savings_name': '積立名',
        'monthly_amount': '月間積立額',
        'period': '積立期間',
        'start_date': '開始日',
        'interest_rate': '年利率',
        'create_plan': 'プラン作成',
        'savings_details': '積立詳細',
        'payment_schedule': '入金スケジュール',
        'logout': 'ログアウト',
        'customer_name': '顧客名',
        'employee_number': '社員番号',
        'basic_info': '基本情報',
        'savings_calc': '積立計算',
        'adjust_payment': '入金調整',
        'payment_history': '入金履歴',
        'basic_salary': '基本給',
        'overtime_pay': '残業代',
        'bonus': 'ボーナス',
        'allowances': 'その他手当',
        'insurance': '社会保険料',
        'tax': '税金',
        'other_deductions': 'その他控除',
        'net_salary': '差引支給額',
        'generate_payslip': '明細発行',
        'payslip_date': '給与日',
        'income_items': '支給内訳',
        'deduction_items': '控除内訳',
        'total_income': '総支給額',
        'total_deduction': '総控除額',
        'add_adjustment': '調整追加',
        'adjustment_month': '調整回',
        'adjustment_amount': '調整金額',
        'remove': '削除',
        'no_capture': '⚠️ この画面のスクリーンショット・撮影は禁止されています',
        'security_warning': '🔒 セキュリティ警告: このページは監視されています'
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language].get(key, LANGUAGES['EN'].get(key, key))

# CSS 스타일링 - 모던 머터리얼 디자인
def load_css():
    css = """
    <style>
    /* 기본 스타일 - 세련된 그레이 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 50%, #f8f9fa 100%);
        font-family: 'Noto Sans JP', 'Segoe UI', 'Hiragino Sans', sans-serif;
        color: #2d3748;
    }
    
    /* 메인 콘텐츠 영역 */
    .main-content {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 0px;
        padding: 0px;
        margin: 0px;
    }
    
    /* 헤더 스타일 - 모던한 은행 디자인 */
    .bank-header {
        background: linear-gradient(135deg, #2c5282 0%, #3182ce 100%);
        color: white;
        padding: 2.5rem 0;
        margin: -1rem -1rem 0 -1rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        border-bottom: none;
        position: relative;
        overflow: hidden;
    }
    
    .bank-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" opacity="0.1"><polygon points="0,0 1000,50 1000,100 0,100" fill="white"/></svg>');
        background-size: cover;
    }
    
    .bank-title {
        font-size: 2.8rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
        text-align: center;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        letter-spacing: -0.5px;
        position: relative;
    }
    
    .bank-subtitle {
        font-size: 1.2rem !important;
        opacity: 0.95;
        text-align: center;
        margin-bottom: 0 !important;
        font-weight: 400;
        letter-spacing: 0.3px;
        position: relative;
    }
    
    /* 네비게이션 - 모던한 탭 디자인 */
    .nav-container {
        background: white;
        padding: 0;
        margin: 0 -1rem;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .nav-buttons {
        display: flex;
        justify-content: center;
        gap: 0;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .nav-btn {
        flex: 1;
        max-width: 180px;
        background: transparent;
        border: none;
        color: #64748b;
        padding: 1.5rem 1rem;
        font-weight: 600;
        font-size: 1rem;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-bottom: 3px solid transparent;
        position: relative;
        overflow: hidden;
    }
    
    .nav-btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(59, 130, 246, 0.1), transparent);
        transition: left 0.5s;
    }
    
    .nav-btn:hover::before {
        left: 100%;
    }
    
    .nav-btn:hover {
        background: rgba(59, 130, 246, 0.05);
        color: #1e40af;
        transform: translateY(-1px);
    }
    
    .nav-btn.active {
        background: rgba(59, 130, 246, 0.08);
        color: #1e40af;
        border-bottom: 3px solid #3b82f6;
    }
    
    /* 메트릭 카드 - 모던 머터리얼 디자인 */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        color: #2d3748;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #f1f5f9;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        border-color: #e2e8f0;
    }
    
    /* 버튼 스타일 - 모던 머터리얼 */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
        letter-spacing: 0.3px;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
    }
    
    .stButton>button:hover::before {
        left: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4) !important;
        background: linear-gradient(135deg, #4f87f8 0%, #2d50c5 100%) !important;
    }
    
    /* 보조 버튼 */
    .stButton>button[kind="secondary"] {
        background: linear-gradient(135deg, #64748b 0%, #475569 100%) !important;
        box-shadow: 0 2px 8px rgba(100, 116, 139, 0.2) !important;
    }
    
    .stButton>button[kind="secondary"]:hover {
        background: linear-gradient(135deg, #747b8a 0%, #565e6e 100%) !important;
        box-shadow: 0 4px 12px rgba(100, 116, 139, 0.3) !important;
    }
    
    /* 입력 필드 - 모던한 디자인 */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select {
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.8rem 1.2rem !important;
        font-size: 1rem !important;
        color: #2d3748 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stDateInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        background: white !important;
    }
    
    /* 캡처 방지 배너 - 모던한 디자인 */
    .capture-warning {
        background: linear-gradient(45deg, #dc2626, #b91c1c);
        color: white;
        padding: 1.2rem;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 0 -1rem 2rem -1rem;
        border-bottom: none;
        animation: alertPulse 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
    }
    
    .capture-warning::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shimmer 3s infinite;
    }
    
    .security-alert {
        background: linear-gradient(45deg, #d97706, #b45309);
        color: white;
        padding: 1rem;
        text-align: center;
        font-size: 0.95rem;
        margin: 0 -1rem 1.5rem -1rem;
        border-bottom: none;
        animation: glow 4s ease-in-out infinite;
        box-shadow: 0 2px 8px rgba(217, 119, 6, 0.3);
    }
    
    @keyframes alertPulse {
        0%, 100% { 
            opacity: 1;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.3);
        }
        50% { 
            opacity: 0.95;
            box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4);
        }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes glow {
        0%, 100% { 
            box-shadow: 0 2px 8px rgba(217, 119, 6, 0.3);
        }
        50% { 
            box-shadow: 0 4px 16px rgba(217, 119, 6, 0.5);
        }
    }
    
    /* 이중 언어 표기 - 개선된 디자인 */
    .bilingual {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding: 1.2rem;
        background: white;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .bilingual:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateX(4px);
    }
    
    .bilingual-jp {
        font-weight: 600;
        color: #1e293b;
        font-size: 1rem;
    }
    
    .bilingual-en {
        font-size: 0.85rem;
        color: #64748b;
        font-weight: 500;
    }
    
    /* 카드 컨테이너 */
    .content-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .content-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    /* 테이블 스타일 */
    .dataframe {
        border-radius: 16px !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08) !important;
        background: white !important;
        border: 1px solid #f1f5f9 !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: white;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 60px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 0px;
        gap: 8px;
        padding: 0 2rem;
        font-weight: 600;
        color: #64748b;
        border-bottom: 3px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: transparent !important;
        color: #1e40af !important;
        border-bottom: 3px solid #3b82f6 !important;
    }
    
    /* 언어 스위처 */
    .lang-switcher {
        display: flex;
        gap: 8px;
        justify-content: center;
        margin: 1rem 0;
    }
    
    .lang-btn {
        background: rgba(255,255,255,0.2) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 0.5rem 1.5rem !important;
    }
    
    .lang-btn:hover {
        background: rgba(255,255,255,0.3) !important;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
    
    /* 스크롤바 스타일 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    /* 애니메이션 효과 */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.6s ease-out;
    }
    
    /* 그리드 레이아웃 개선 */
    .stColumn {
        padding: 0.5rem;
    }
    
    /* 프로그레스 바 */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 캡처 방지 경고 표시
def show_security_warnings():
    current_time = time.time()
    
    # 30초마다 캡처 경고 표시
    if current_time - st.session_state.last_capture_warning > 30:
        st.markdown(f'<div class="capture-warning">{get_text("no_capture")}</div>', unsafe_allow_html=True)
        st.session_state.last_capture_warning = current_time
    else:
        st.markdown(f'<div class="capture-warning">{get_text("no_capture")}</div>', unsafe_allow_html=True)
    
    # 항상 보안 경고 표시
    st.markdown(f'<div class="security-alert">{get_text("security_warning")}</div>', unsafe_allow_html=True)

# 적금 계산 함수
def calculate_savings_schedule(monthly_amount, period_years, interest_rate, start_date, adjustments=None):
    total_months = period_years * 12
    monthly_interest_rate = interest_rate / 100 / 12
    today = datetime.now().date()
    
    schedule = []
    current_balance = 0
    
    for month in range(1, total_months + 1):
        payment_date = start_date + relativedelta(months=month-1)
        
        # 조정된 금액 확인
        actual_amount = monthly_amount
        adjustment_note = ""
        if adjustments and month in adjustments:
            actual_amount = adjustments[month]
            adjustment_note = f"調整済: ¥{adjustments[month]:,}"
        
        # 이자 계산 (반올림)
        monthly_interest = round(current_balance * monthly_interest_rate)
        current_balance += actual_amount + monthly_interest
        
        # 상태 결정 (오늘 기준)
        if payment_date < today:
            status = "✅ 入金完了"
        elif payment_date == today:
            status = "⏳ 本日入金"
        else:
            status = "📅 入金予定"
        
        schedule.append({
            '回': month,
            '入金日': payment_date.strftime('%Y/%m/%d'),
            '入金額': f"¥{actual_amount:,}",
            '利息': f"¥{monthly_interest:,}",
            '残高': f"¥{current_balance:,}",
            '状態': status,
            '備考': adjustment_note
        })
    
    total_payment = monthly_amount * total_months
    total_interest = current_balance - total_payment
    
    return {
        'schedule': schedule,
        'total_months': total_months,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'final_balance': current_balance,
        'completion_rate': len([x for x in schedule if '完了' in x['状態']]) / total_months * 100
    }

# 급여 계산 함수
def calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction):
    total_income = basic_salary + overtime_pay
    total_deductions = income_tax + residence_tax + health_insurance + pension + employment_insurance + other_deduction
    net_salary = total_income - total_deductions
    
    return {
        'total_income': total_income,
        'total_deductions': total_deductions,
        'net_salary': net_salary,
        'income_breakdown': {
            'basic_salary': {'jp': '基本給', 'en': 'Basic Salary', 'amount': basic_salary},
            'overtime_pay': {'jp': '残業代', 'en': 'Overtime Pay', 'amount': overtime_pay}
        },
        'deduction_breakdown': {
            'income_tax': {'jp': '所得税', 'en': 'Income Tax', 'amount': income_tax},
            'residence_tax': {'jp': '住民税', 'en': 'Residence Tax', 'amount': residence_tax},
            'health_insurance': {'jp': '健康保険', 'en': 'Health Insurance', 'amount': health_insurance},
            'pension': {'jp': '厚生年金', 'en': 'Pension', 'amount': pension},
            'employment_insurance': {'jp': '雇用保険', 'en': 'Employment Insurance', 'amount': employment_insurance},
            'other_deduction': {'jp': '控除額', 'en': 'Other Deduction', 'amount': other_deduction}
        }
    }

# 네비게이션
def render_nav():
    nav_items = [
        ('home', '🏠 ホーム'),
        ('savings', '💰 積立'), 
        ('payroll', '📄 給与')
    ]
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    st.markdown('<div class="nav-buttons">', unsafe_allow_html=True)
    
    cols = st.columns(len(nav_items))
    for idx, (page, label) in enumerate(nav_items):
        with cols[idx]:
            is_active = st.session_state.current_page == page
            if st.button(
                label, 
                key=f"nav_{page}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# 홈 페이지
def render_home():
    show_security_warnings()
    
    st.markdown(f"## 👋 {get_text('welcome').format(st.session_state.user_data['name'])}")
    
    # 요약 메트릭
    st.markdown("### 📊 資産概要")
    
    # 실제 데이터 계산
    total_savings = 0
    monthly_payment = 0
    active_plans = len(st.session_state.savings_list)
    
    for savings in st.session_state.savings_list:
        calc = savings['calculation']
        total_savings += calc['final_balance']
        monthly_payment += savings['monthly_amount']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 1rem;">総積立額</div>
            <div style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{total_savings:,.0f}</div>
            <div style="font-size: 0.8rem; opacity: 0.6;">前月比 +2.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 1rem;">月間支払額</div>
            <div style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{monthly_payment:,.0f}</div>
            <div style="font-size: 0.8rem; opacity: 0.6;">実行中プラン</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.8; margin-bottom: 1rem;">実行中プラン</div>
            <div style="font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">{active_plans}</div>
            <div style="font-size: 0.8rem; opacity: 0.6;">総プラン数</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 資産成長トレンド")
        months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        values = [14200000, 14500000, 14800000, 15000000, 15200000, 15400000, 15600000, 15800000, 16000000, 16200000, 16400000, 16600000]
        
        chart_data = pd.DataFrame({
            '月': months,
            '資産': values
        })
        st.area_chart(chart_data.set_index('月'), height=300)
    
    with col2:
        st.markdown("### 🎯 積立分布")
        if st.session_state.savings_list:
            labels = [savings['name'] for savings in st.session_state.savings_list]
            values = [savings['monthly_amount'] * savings['period'] * 12 for savings in st.session_state.savings_list]
            chart_data = pd.DataFrame({
                'カテゴリ': labels,
                '金額': values
            })
            st.bar_chart(chart_data.set_index('カテゴリ'), height=300)
        else:
            st.info("積立プランがありません")
    
    # 빠른 접근
    st.markdown("### ⚡ クイックアクセス")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 新規積立作成", use_container_width=True, type="primary"):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col2:
        if st.button("📊 積立一覧表示", use_container_width=True):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col3:
        if st.button("📄 給与明細作成", use_container_width=True):
            st.session_state.current_page = 'payroll'
            st.rerun()

# 적금 관리 페이지
def render_savings():
    show_security_warnings()
    
    st.markdown("## 💰 積立貯蓄管理")
    
    tab1, tab2 = st.tabs(["🆕 新規積立作成", "📋 積立一覧"])
    
    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🆕 新規積立口座開設")
        
        # 기본 정보 입력
        st.markdown("#### 📝 基本情報")
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("顧客名", st.session_state.user_data['name'])
            employee_number = st.text_input("社員番号", st.session_state.user_data['emp_num'])
            account_number = st.text_input("口座番号", st.session_state.user_data['account'])
        
        with col2:
            savings_name = st.text_input("積立名", "定期積立預金")
            monthly_amount = st.number_input("月間積立額 (¥)", min_value=1000, value=3000, step=1000)
            period = st.selectbox("積立期間", [3, 5], index=0, format_func=lambda x: f"{x}年")
            interest_rate = st.number_input("年利率 (%)", min_value=0.1, value=2.5, step=0.1, format="%.1f")
            start_date = st.date_input("開始日", date(2025, 1, 1))
        
        # 조정 입력
        st.markdown("#### ⚙️ 入金調整")
        st.info("特定の回で入金額を調整する場合は設定してください")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            new_month = st.number_input("調整回", min_value=1, max_value=36, value=1, key="new_month")
        with col2:
            new_amount = st.number_input("調整金額 (¥)", min_value=0, value=3000, key="new_amount")
        with col3:
            if st.button("➕ 追加", use_container_width=True):
                st.session_state.adjustments.append({'month': new_month, 'amount': new_amount})
                st.success(f"{new_month}回目を調整しました")
        
        # 현재 조정 목록 표시
        if st.session_state.adjustments:
            st.markdown("**現在の調整内容:**")
            for i, adj in enumerate(st.session_state.adjustments):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📅 {adj['month']}回目: ¥{adj['amount']:,}")
                with col2:
                    st.write(f"⚡ デフォルト: ¥{monthly_amount:,}")
                with col3:
                    if st.button("🗑️ 削除", key=f"remove_{i}"):
                        st.session_state.adjustments.pop(i)
                        st.rerun()
        
        # 최종 생성 버튼
        if st.button("🚀 積立プラン作成", use_container_width=True, type="primary"):
            adjustments_dict = {adj['month']: adj['amount'] for adj in st.session_state.adjustments}
            
            # 적금 계산
            calculation = calculate_savings_schedule(
                monthly_amount, 
                period, 
                interest_rate, 
                start_date, 
                adjustments_dict
            )
            
            # 새로운 적금 플랜 생성
            new_savings = {
                'id': len(st.session_state.savings_list) + 1,
                'name': savings_name,
                'customer_name': customer_name,
                'employee_number': employee_number,
                'account_number': account_number,
                'monthly_amount': monthly_amount,
                'period': period,
                'interest_rate': interest_rate,
                'start_date': start_date.strftime('%Y/%m/%d'),
                'adjustments': adjustments_dict,
                'calculation': calculation,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.savings_list.append(new_savings)
            st.session_state.adjustments = []
            st.success("🎉 積立プランが正常に作成されました！")
            st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        if not st.session_state.savings_list:
            st.info("登録されている積立プランがありません。")
        else:
            for savings in st.session_state.savings_list:
                with st.expander(f"📒 {savings['name']} - {savings['account_number']}", expanded=False):
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    
                    # 기본 정보
                    st.markdown("#### 📋 基本情報")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("**顧客名**")
                        st.write(savings['customer_name'])
                    with col2:
                        st.markdown("**社員番号**")
                        st.write(savings['employee_number'])
                    with col3:
                        st.markdown("**口座番号**")
                        st.write(savings['account_number'])
                    with col4:
                        st.markdown("**開始日**")
                        st.write(savings['start_date'])
                    
                    # 적금 정보
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown("**月間積立額**")
                        st.write(f"¥{savings['monthly_amount']:,.0f}")
                    with col2:
                        st.markdown("**積立期間**")
                        st.write(f"{savings['period']}年")
                    with col3:
                        st.markdown("**年利率**")
                        st.write(f"{savings['interest_rate']}%")
                    with col4:
                        completion = savings['calculation']['completion_rate']
                        st.markdown("**進捗率**")
                        st.write(f"{completion:.1f}%")
                    
                    # 계산 결과
                    calc = savings['calculation']
                    st.markdown("#### 計算結果")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("総支払額", f"¥{calc['total_payment']:,.0f}")
                    with col2:
                        st.metric("総利息", f"¥{calc['total_interest']:,.0f}")
                    with col3:
                        st.metric("最終残高", f"¥{calc['final_balance']:,.0f}")
                    with col4:
                        st.metric("総月数", f"{calc['total_months']}")
                    
                    # 입금 스케줄
                    st.markdown("#### 入金スケジュール")
                    schedule_data = []
                    for item in savings['calculation']['schedule'][:12]:  # 처음 12개만 표시
                        schedule_data.append({
                            '回': item['回'],
                            '日付': item['入金日'],
                            '金額': item['入金額'],
                            '利息': item['利息'],
                            '残高': item['残高'],
                            '状態': item['状態'],
                            '備考': item['備考']
                        })
                    
                    schedule_df = pd.DataFrame(schedule_data)
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
                    
                    # 삭제 버튼
                    if st.button(f"🗑️ 削除", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# 급여 명세서 페이지
def render_payroll():
    show_security_warnings()
    
    st.markdown("## 📄 給与明細管理")
    
    with st.form("payroll_form"):
        st.subheader("給与情報")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 支給内訳")
            basic_salary = st.number_input("基本給", value=300000, step=10000, key="basic_salary")
            overtime_pay = st.number_input("残業代", value=50000, step=5000, key="overtime_pay")
        
        with col2:
            st.markdown("#### 控除内訳")
            income_tax = st.number_input("所得税", value=25000, step=1000, key="income_tax")
            residence_tax = st.number_input("住民税", value=15000, step=1000, key="residence_tax")
            health_insurance = st.number_input("健康保険", value=20000, step=1000, key="health_insurance")
            pension = st.number_input("厚生年金", value=30000, step=1000, key="pension")
            employment_insurance = st.number_input("雇用保険", value=5000, step=1000, key="employment_insurance")
            other_deduction = st.number_input("控除額", value=10000, step=1000, key="other_deduction")
            payslip_date = st.date_input("給与日", datetime.now().date(), key="payslip_date")
        
        if st.form_submit_button("📄 明細発行", use_container_width=True, type="primary"):
            # 급여 계산
            salary_data = calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction)
            
            # 급여 명세서 저장
            new_payslip = {
                'id': len(st.session_state.payroll_list) + 1,
                'date': payslip_date.strftime('%Y/%m/%d'),
                'salary_data': salary_data,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.payroll_list.append(new_payslip)
            
            # 결과 표시
            st.success("🎉 給与明細が作成されました！")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("総支給額", f"¥{salary_data['total_income']:,.0f}")
            with col2:
                st.metric("総控除額", f"¥{salary_data['total_deductions']:,.0f}")
            with col3:
                st.metric("差引支給額", f"¥{salary_data['net_salary']:,.0f}")
            
            # 상세 내역
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### 支給内訳詳細")
                for item_key, item_data in salary_data['income_breakdown'].items():
                    st.markdown(f"**{item_data['jp']}**: ¥{item_data['amount']:,.0f}")
            
            with col2:
                st.markdown("##### 控除内訳詳細")
                for item_key, item_data in salary_data['deduction_breakdown'].items():
                    st.markdown(f"**{item_data['jp']}**: ¥{item_data['amount']:,.0f}")

# 로그인 페이지
def login():
    st.markdown(f"""
    <div class="bank-header">
        <h1 class="bank-title">{get_text('title')}</h1>
        <p class="bank-subtitle">{get_text('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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

# 언어 전환
def render_language_switcher():
    current_lang = st.session_state.language
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("English", use_container_width=True, type="primary" if current_lang == 'EN' else "secondary"):
            st.session_state.language = 'EN'
            st.rerun()
    with col2:
        if st.button("日本語", use_container_width=True, type="primary" if current_lang == 'JP' else "secondary"):
            st.session_state.language = 'JP'
            st.rerun()

# 로그아웃
def render_logout():
    if st.button(get_text('logout'), key="logout_btn", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# 메인 앱
def main():
    initialize_session_state()
    load_css()
    
    if not st.session_state.logged_in:
        login()
    else:
        # 헤더
        st.markdown(f"""
        <div class="bank-header">
            <div style="display: flex; justify-content: space-between; align-items: center; position: relative;">
                <div>
                    <h1 class="bank-title">{get_text('title')}</h1>
                    <p class="bank-subtitle">{get_text('subtitle')}</p>
                    <p style="margin: 0; opacity: 0.95;">
                        {get_text('welcome').format(st.session_state.user_data['name'])} | 
                        {get_text('account_number')}: {st.session_state.user_data['account']}
                    </p>
                </div>
                <div style="display: flex; gap: 10px; align-items: center;">
                    <div style="display: flex; gap: 5px;">
                        {render_language_switcher()}
                    </div>
                    {render_logout()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 네비게이션
        render_nav()
        
        # 페이지 내용
        if st.session_state.current_page == 'home':
            render_home()
        elif st.session_state.current_page == 'savings':
            render_savings()
        elif st.session_state.current_page == 'payroll':
            render_payroll()

if __name__ == "__main__":
    main()