# common.py
import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import time
import base64
import random

# 다국어 지원
LANGUAGES = {
    'EN': {
        'title': 'Otsuka Bank',
        'subtitle': 'Employee Banking Portal',
        'login_id': 'Login ID',
        'password': 'Password',
        'login': 'Login',
        'login_error': 'Incorrect Login ID or Password',
        'welcome': 'Welcome, {}',
        'logout': 'Logout',
        'no_capture': '⚠️ SCREEN CAPTURE AND PHOTOGRAPHY PROHIBITED',
        'security_warning': '🔒 SECURITY WARNING: THIS PAGE IS MONITORED',
        'announcement': 'Announcement',
        'account_number': 'Account Number',
        'quick_access': 'Quick Access',
        'recent_transactions': 'Recent Transactions',
        'financial_overview': 'Financial Overview',
        'asset_growth': 'Asset Growth Trend',
        'savings_distribution': 'Savings Distribution',
        'savings_management': 'Savings Management',
        'new_savings_account': 'New Savings Account Opening',
        'customer_name': 'Customer Name',
        'employee_number': 'Employee Number',
        'savings_name': 'Savings Name',
        'monthly_amount': 'Monthly Amount (¥)',
        'savings_period': 'Savings Period',
        'interest_rate': 'Annual Interest Rate (%)',
        'start_date': 'Start Date',
        'payment_adjustment': 'Payment Adjustment',
        'adjustment_month': 'Adjustment Month',
        'adjustment_amount': 'Adjustment Amount (¥)',
        'create_savings_plan': 'Create Savings Plan',
        'basic_info': 'Basic Information',
        'savings_details': 'Saving Details',
        'calculation_results': 'Calculation Results',
        'total_payment': 'Total Payment',
        'total_interest': 'Total Interest',
        'final_balance': 'Final Balance',
        'payment_schedule': 'Payment Schedule',
        'download_certificate': 'Download Savings Certificate',
        'payroll_management': 'Payroll Management',
        'payslip_creation': 'Payslip Creation',
        'income_breakdown': 'Income Breakdown',
        'deduction_breakdown': 'Deduction Breakdown',
        'basic_salary': 'Basic Salary',
        'overtime_pay': 'Overtime Pay',
        'income_tax': 'Income Tax',
        'residence_tax': 'Residence Tax',
        'health_insurance': 'Health Insurance',
        'pension': 'Pension',
        'employment_insurance': 'Employment Insurance',
        'other_deduction': 'Other Deduction',
        'pay_date': 'Pay Date',
        'total_income': 'Total Income',
        'total_deductions': 'Total Deductions',
        'net_salary': 'Net Salary',
        'download_payslip': 'Download Payslip',
        'progress_rate': 'Progress Rate',
        'total_months': 'Total Months'
    },
    'JP': {
        'title': '大塚銀行',
        'subtitle': '従業員バンキングポータル',
        'login_id': 'ログインID',
        'password': 'パスワード',
        'login': 'ログイン',
        'login_error': 'ログインIDまたはパスワードが正しくありません',
        'welcome': 'ようこそ、{}様',
        'logout': 'ログアウト',
        'no_capture': '⚠️ この画面のスクリーンショット・撮影は禁止されています',
        'security_warning': '🔒 セキュリティ警告: このページは監視されています',
        'announcement': 'お知らせ',
        'account_number': '口座番号',
        'quick_access': 'クイックアクセス',
        'recent_transactions': '最近の取引',
        'financial_overview': '資産概要',
        'asset_growth': '資産成長トレンド',
        'savings_distribution': '積立分布',
        'savings_management': '積立貯蓄管理',
        'new_savings_account': '新規積立口座開設',
        'customer_name': '顧客名',
        'employee_number': '社員番号',
        'savings_name': '積立名',
        'monthly_amount': '月間積立額 (¥)',
        'savings_period': '積立期間',
        'interest_rate': '年利率 (%)',
        'start_date': '開始日',
        'payment_adjustment': '入金調整',
        'adjustment_month': '調整回',
        'adjustment_amount': '調整金額 (¥)',
        'create_savings_plan': '積立プラン作成',
        'basic_info': '基本情報',
        'savings_details': '積立詳細',
        'calculation_results': '計算結果',
        'total_payment': '総支払額',
        'total_interest': '総利息',
        'final_balance': '最終残高',
        'payment_schedule': '入金スケジュール',
        'download_certificate': '積立証明書をダウンロード',
        'payroll_management': '給与明細管理',
        'payslip_creation': '明細発行',
        'income_breakdown': '支給内訳',
        'deduction_breakdown': '控除内訳',
        'basic_salary': '基本給',
        'overtime_pay': '残業代',
        'income_tax': '所得税',
        'residence_tax': '住民税',
        'health_insurance': '健康保険',
        'pension': '厚生年金',
        'employment_insurance': '雇用保険',
        'other_deduction': '控除額',
        'pay_date': '給与日',
        'total_income': '総支給額',
        'total_deductions': '総控除額',
        'net_salary': '差引支給額',
        'download_payslip': '給与明細をダウンロード',
        'progress_rate': '進捗率',
        'total_months': '総月数'
    }
}

def get_text(key):
    """텍스트를 현재 언어로 반환"""
    return LANGUAGES[st.session_state.language].get(key, LANGUAGES['EN'].get(key, key))

def initialize_session_state():
    """세션 상태 초기화"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'language' not in st.session_state:
        st.session_state.language = 'JP'
    
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

# CSS를 항상 적용하는 함수 (페이지마다 호출해야 함)
def load_css():
    """CSS를 로드하고 적용 - 모든 페이지에서 호출해야 함"""
    css = """
    <style>
    /* 기본 스타일 */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        font-family: 'Noto Sans JP', 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 모던한 은행 헤더 */
    .bank-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem 0 0.5rem 0;
        margin: -1rem -1rem 1rem -1rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
        position: relative;
        overflow: hidden;
        border-radius: 0 0 24px 24px;
    }
    
    .bank-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 100" opacity="0.1"><path d="M500 50Q550 30 600 50T700 30T800 50T900 30T1000 50V100H0V50Q100 30 200 50T300 30T400 50Z" fill="white"/></svg>');
        background-size: cover;
        background-position: bottom;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 0.5rem;
    }
    
    .bank-logo {
        display: flex;
        align-items: center;
        gap: 1.5rem;
    }
    
    .logo-icon {
        font-size: 3rem;
        background: rgba(255,255,255,0.15);
        padding: 1rem;
        border-radius: 20px;
        border: 2px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .logo-text {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .bank-title {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        letter-spacing: -0.5px;
    }
    
    .bank-subtitle {
        font-size: 1.2rem !important;
        opacity: 0.95;
        margin: 0 !important;
        font-weight: 400;
        color: rgba(255,255,255,0.9);
    }
    
    .user-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.5rem;
        background: rgba(255,255,255,0.15);
        padding: 1rem 1.5rem;
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    /* 초콤팩트한 상단 컨트롤 - 완전히 재설계 */
    .ultra-compact-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0;
        padding: 0.5rem 2rem;
        background: rgba(255,255,255,0.1);
        border-top: 1px solid rgba(255,255,255,0.15);
        backdrop-filter: blur(10px);
        gap: 1rem;
    }
    
    .control-items {
        display: flex;
        align-items: center;
        gap: 1rem;
        width: 100%;
        justify-content: space-between;
    }
    
    .status-time-buttons {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .status-indicator {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.3rem 0.7rem;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 600;
        background: rgba(34, 197, 94, 0.9);
        color: white;
        white-space: nowrap;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .time-display {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        color: #1e293b;
        font-size: 0.75rem;
        font-weight: 500;
        background: rgba(255,255,255,0.9);
        padding: 0.3rem 0.7rem;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.3);
        white-space: nowrap;
    }
    
    .button-group {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* 초소형 버튼 스타일 */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.75rem !important;
        padding: 0.3rem 0.7rem !important;
        height: auto !important;
        min-height: unset !important;
        margin: 0 !important;
    }
    
    /* 강력한 플래시 효과 */
    .capture-warning {
        background: linear-gradient(45deg, #ef4444, #dc2626, #b91c1c);
        color: white;
        padding: 1rem;
        text-align: center;
        font-weight: 800;
        font-size: 1.1rem;
        margin: 0 -1rem 0 -1rem;
        border-radius: 0 0 16px 16px;
        backdrop-filter: blur(10px);
        animation: strongPulse 1.5s infinite;
        text-shadow: 0 0 10px rgba(255,255,255,0.5);
        border-bottom: 3px solid #fff;
    }
    
    /* 강력한 보안 경고 */
    .security-alert {
        background: linear-gradient(45deg, #f59e0b, #d97706, #b45309);
        color: white;
        padding: 0.8rem 2rem;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        margin: 0 -1rem 2rem -1rem;
        border-radius: 0 0 12px 12px;
        backdrop-filter: blur(10px);
        animation: strongGlow 2s infinite;
        text-shadow: 0 0 8px rgba(255,255,255,0.4);
        border-bottom: 2px solid #fff;
    }
    
    /* 모던한 공지사항 */
    .announcement-modern {
        margin-bottom: 2rem;
    }
    
    .announcement-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .announcement-item {
        padding: 1.25rem;
        margin-bottom: 1rem;
        background: white;
        border-radius: 12px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    .announcement-item:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-1px);
    }
    
    /* 구분선 */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
        border: none;
    }
    
    /* 모던한 카드 */
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid #f1f5f9;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 1.75rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        margin-bottom: 1rem;
        transition: all 0.3s ease;
    }
    
    .content-card:hover {
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    }
    
    /* 거래 내역 간격 조정 */
    .compact-transaction {
        padding: 0.5rem 0;
        border-bottom: 1px solid #f1f5f9;
    }
    
    .compact-transaction:last-child {
        border-bottom: none;
    }
    
    .transaction-section-spacing {
        margin-top: 2rem !important;
    }
    
    /* 강력한 애니메이션 */
    @keyframes strongPulse {
        0%, 100% { 
            opacity: 1;
            box-shadow: 0 0 25px rgba(239, 68, 68, 0.6);
            background: linear-gradient(45deg, #ef4444, #dc2626, #b91c1c);
        }
        50% { 
            opacity: 0.8;
            box-shadow: 0 0 40px rgba(239, 68, 68, 0.9);
            background: linear-gradient(45deg, #dc2626, #b91c1c, #991b1b);
        }
    }
    
    @keyframes strongGlow {
        0%, 100% { 
            box-shadow: 0 4px 25px rgba(245, 158, 11, 0.6);
            background: linear-gradient(45deg, #f59e0b, #d97706, #b45309);
        }
        50% { 
            box-shadow: 0 6px 35px rgba(245, 158, 11, 0.9);
            background: linear-gradient(45deg, #d97706, #b45309, #92400e);
        }
    }
    
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
    
    /* 반응형 디자인 */
    @media (max-width: 768px) {
        .control-items {
            flex-direction: column;
            gap: 0.5rem;
        }
        
        .status-time-buttons {
            justify-content: center;
            width: 100%;
        }
        
        .button-group {
            justify-content: center;
            width: 100%;
        }
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800&display=swap');
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def login():
    """로그인 페이지"""
    load_css()
    
    st.markdown(f"""
    <div class="bank-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="bank-logo">
                    <div class="logo-icon">🏦</div>
                    <div class="logo-text">
                        <h1 class="bank-title">{get_text('title')}</h1>
                        <p class="bank-subtitle">{get_text('subtitle')}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="height: 2rem"></div>', unsafe_allow_html=True)
        
        with st.container():
            st.markdown("### 🔐 ログイン")
            with st.form("login_form"):
                user_id = st.text_input(get_text('login_id'), placeholder="otsuka")
                password = st.text_input(get_text('password'), type="password", placeholder="bank1234")
                
                if st.form_submit_button(get_text('login'), use_container_width=True, type="primary"):
                    if user_id == "otsuka" and password == "bank1234":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error(get_text('login_error'))

def main_layout():
    """메인 레이아웃 - 모든 페이지에서 호출"""
    load_css()
    
    user_name_jp = st.session_state.user_data['name']
    
    st.markdown(f"""
    <div class="bank-header fade-in-up">
        <div class="header-content">
            <div class="logo-section">
                <div class="bank-logo">
                    <div class="logo-icon">🏦</div>
                    <div class="logo-text">
                        <h1 class="bank-title">{get_text('title')}</h1>
                        <p class="bank-subtitle">{get_text('subtitle')}</p>
                    </div>
                </div>
                <div class="user-info">
                    <div class="welcome-text">{get_text('welcome').format(user_name_jp)}</div>
                    <div class="account-info">{get_text('account_number')}: {st.session_state.user_data['account']}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 초콤팩트한 상단 컨트롤 - 한 줄로 완전 압축
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M")
    
    # 한 줄에 모든 컨트롤 배치
    col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 1, 1])
    
    with col1:
        # 온라인 상태
        st.markdown("""
        <div class="status-indicator">
            <div style="width: 6px; height: 6px; background: white; border-radius: 50%;"></div>
            Online
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # 날짜
        st.markdown(f"""
        <div class="time-display">
            <span>📅</span>
            <span>{current_time}</span>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # 언어 전환 버튼
        current_lang = st.session_state.language
        lang_text = "EN" if current_lang == 'JP' else "JP"
        if st.button(f"🌐 {lang_text}", key="lang_switcher", use_container_width=True):
            st.session_state.language = 'EN' if current_lang == 'JP' else 'JP'
            st.rerun()
    
    with col4:
        # 로그아웃 버튼
        if st.button("🚪", key="logout_btn", use_container_width=True, help=get_text('logout')):
            st.session_state.logged_in = False
            st.rerun()
    
    with col5:
        st.empty()  # 여유 공간
    
    # 구분선 추가
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

def show_security_warnings():
    """보안 경고 표시 - 순서 변경"""
    st.markdown(f'<div class="capture-warning">{get_text("no_capture")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="security-alert">{get_text("security_warning")}</div>', unsafe_allow_html=True)

def show_announcement():
    """모던한 공지사항 표시"""
    announcements = [
        {
            "icon": "🔧",
            "title": "システムメンテナンス",
            "content": "12月25日 2:00-4:00",
            "date": "2024-12-20",
            "priority": "high"
        },
        {
            "icon": "📈", 
            "title": "新積立プラン開始",
            "content": "高金利プランのご案内",
            "date": "2024-12-18",
            "priority": "medium"
        },
        {
            "icon": "🎄",
            "title": "年末年始の営業について", 
            "content": "12月29日～1月4日休業",
            "date": "2024-12-15",
            "priority": "medium"
        }
    ]
    
    st.markdown('<div class="announcement-modern fade-in-up">', unsafe_allow_html=True)
    st.markdown(f'<div class="announcement-header">📢 {get_text("announcement")}</div>', unsafe_allow_html=True)
    
    for announcement in announcements:
        st.markdown(f"""
        <div class="announcement-item">
            <div style="display: flex; align-items: flex-start; gap: 1rem;">
                <div style="font-size: 1.5rem; margin-top: 0.1rem;">{announcement['icon']}</div>
                <div style="flex: 1;">
                    <div style="font-weight: 600; color: #1e293b; margin-bottom: 0.5rem; font-size: 1.1rem;">{announcement['title']}</div>
                    <div style="color: #475569; margin-bottom: 0.5rem; font-size: 0.95rem; line-height: 1.4;">{announcement['content']}</div>
                    <div style="font-size: 0.85rem; color: #64748b; font-weight: 500;">{announcement['date']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)