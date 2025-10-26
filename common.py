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
        'title': 'Otsuka Bank / 大塚銀行',
        'subtitle': 'Employee Banking Portal / 従業員バンキングポータル',
        'login_id': 'Login ID / ログインID',
        'password': 'Password / パスワード',
        'login': 'Login / ログイン',
        'login_error': 'Incorrect Login ID or Password / ログインIDまたはパスワードが正しくありません',
        'welcome': 'Welcome, {}',
        'logout': 'Logout / ログアウト',
        'no_capture': '⚠️ SCREEN CAPTURE AND PHOTOGRAPHY PROHIBITED / この画面のスクリーンショット・撮影は禁止されています',
        'security_warning': '🔒 SECURITY WARNING: THIS PAGE IS MONITORED / セキュリティ警告: このページは監視されています',
        'announcement': '📢 Announcement / お知らせ',
        'account_number': 'Account Number / 口座番号',
        'quick_access': 'Quick Access / クイックアクセス',
        'recent_transactions': 'Recent Transactions / 最近の取引',
        'financial_overview': 'Financial Overview / 資産概要',
        'asset_growth': 'Asset Growth Trend / 資産成長トレンド',
        'savings_distribution': 'Savings Distribution / 積立分布',
        'savings_management': 'Savings Management / 積立貯蓄管理',
        'new_savings_account': 'New Savings Account Opening / 新規積立口座開設',
        'customer_name': 'Customer Name / 顧客名',
        'employee_number': 'Employee Number / 社員番号',
        'savings_name': 'Savings Name / 積立名',
        'monthly_amount': 'Monthly Amount (¥) / 月間積立額 (¥)',
        'savings_period': 'Savings Period / 積立期間',
        'interest_rate': 'Annual Interest Rate (%) / 年利率 (%)',
        'start_date': 'Start Date / 開始日',
        'payment_adjustment': 'Payment Adjustment / 入金調整',
        'adjustment_month': 'Adjustment Month / 調整回',
        'adjustment_amount': 'Adjustment Amount (¥) / 調整金額 (¥)',
        'create_savings_plan': 'Create Savings Plan / 積立プラン作成',
        'basic_info': 'Basic Information / 基本情報',
        'savings_details': 'Saving Details / 積立詳細',
        'calculation_results': 'Calculation Results / 計算結果',
        'total_payment': 'Total Payment / 総支払額',
        'total_interest': 'Total Interest / 総利息',
        'final_balance': 'Final Balance / 最終残高',
        'payment_schedule': 'Payment Schedule / 入金スケジュール',
        'download_certificate': 'Download Savings Certificate / 積立証明書をダウンロード',
        'payroll_management': 'Payroll Management / 給与明細管理',
        'payslip_creation': 'Payslip Creation / 明細発行',
        'income_breakdown': 'Income Breakdown / 支給内訳',
        'deduction_breakdown': 'Deduction Breakdown / 控除内訳',
        'basic_salary': 'Basic Salary / 基本給',
        'overtime_pay': 'Overtime Pay / 残業代',
        'income_tax': 'Income Tax / 所得税',
        'residence_tax': 'Residence Tax / 住民税',
        'health_insurance': 'Health Insurance / 健康保険',
        'pension': 'Pension / 厚生年金',
        'employment_insurance': 'Employment Insurance / 雇用保険',
        'other_deduction': 'Other Deduction / 控除額',
        'pay_date': 'Pay Date / 給与日',
        'total_income': 'Total Income / 総支給額',
        'total_deductions': 'Total Deductions / 総控除額',
        'net_salary': 'Net Salary / 差引支給額',
        'download_payslip': 'Download Payslip / 給与明細をダウンロード',
        'progress_rate': 'Progress Rate / 進捗率',
        'total_months': 'Total Months / 総月数'
    },
    'JP': {
        'title': '大塚銀行 / Otsuka Bank',
        'subtitle': '従業員バンキングポータル / Employee Banking Portal',
        'login_id': 'ログインID / Login ID',
        'password': 'パスワード / Password',
        'login': 'ログイン / Login',
        'login_error': 'ログインIDまたはパスワードが正しくありません / Incorrect Login ID or Password',
        'welcome': 'ようこそ、{}様',
        'logout': 'ログアウト / Logout',
        'no_capture': '⚠️ この画面のスクリーンショット・撮影は禁止されています / SCREEN CAPTURE AND PHOTOGRAPHY PROHIBITED',
        'security_warning': '🔒 セキュリティ警告: このページは監視されています / SECURITY WARNING: THIS PAGE IS MONITORED',
        'announcement': '📢 お知らせ / Announcement',
        'account_number': '口座番号 / Account Number',
        'quick_access': 'クイックアクセス / Quick Access',
        'recent_transactions': '最近の取引 / Recent Transactions',
        'financial_overview': '資産概要 / Financial Overview',
        'asset_growth': '資産成長トレンド / Asset Growth Trend',
        'savings_distribution': '積立分布 / Savings Distribution',
        'savings_management': '積立貯蓄管理 / Savings Management',
        'new_savings_account': '新規積立口座開設 / New Savings Account Opening',
        'customer_name': '顧客名 / Customer Name',
        'employee_number': '社員番号 / Employee Number',
        'savings_name': '積立名 / Savings Name',
        'monthly_amount': '月間積立額 (¥) / Monthly Amount (¥)',
        'savings_period': '積立期間 / Savings Period',
        'interest_rate': '年利率 (%) / Annual Interest Rate (%)',
        'start_date': '開始日 / Start Date',
        'payment_adjustment': '入金調整 / Payment Adjustment',
        'adjustment_month': '調整回 / Adjustment Month',
        'adjustment_amount': '調整金額 (¥) / Adjustment Amount (¥)',
        'create_savings_plan': '積立プラン作成 / Create Savings Plan',
        'basic_info': '基本情報 / Basic Information',
        'savings_details': '積立詳細 / Savings Details',
        'calculation_results': '計算結果 / Calculation Results',
        'total_payment': '総支払額 / Total Payment',
        'total_interest': '総利息 / Total Interest',
        'final_balance': '最終残高 / Final Balance',
        'payment_schedule': '入金スケジュール / Payment Schedule',
        'download_certificate': '積立証明書をダウンロード / Download Savings Certificate',
        'payroll_management': '給与明細管理 / Payroll Management',
        'payslip_creation': '明細発行 / Payslip Creation',
        'income_breakdown': '支給内訳 / Income Breakdown',
        'deduction_breakdown': '控除内訳 / Deduction Breakdown',
        'basic_salary': '基本給 / Basic Salary',
        'overtime_pay': '残業代 / Overtime Pay',
        'income_tax': '所得税 / Income Tax',
        'residence_tax': '住民税 / Residence Tax',
        'health_insurance': '健康保険 / Health Insurance',
        'pension': '厚生年金 / Pension',
        'employment_insurance': '雇用保険 / Employment Insurance',
        'other_deduction': '控除額 / Other Deduction',
        'pay_date': '給与日 / Pay Date',
        'total_income': '総支給額 / Total Income',
        'total_deductions': '総控除額 / Total Deductions',
        'net_salary': '差引支給額 / Net Salary',
        'download_payslip': '給与明細をダウンロード / Download Payslip',
        'progress_rate': '進捗率 / Progress Rate',
        'total_months': '総月数 / Total Months'
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
            "name": "山田 太郎 / Taro Yamada",
            "account": "098-96586-6521",
            "emp_num": "12345678",
            "department": "IT事業部 / IT Department"
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
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #f8fafc 100%);
        font-family: 'Noto Sans JP', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* 은행 헤더 */
    .bank-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        color: white;
        padding: 1.5rem 0 0.5rem 0;
        margin: -1rem -1rem 1rem -1rem;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .bank-header::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #3b82f6, #ef4444, #f59e0b);
        z-index: 3;
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
        gap: 1rem;
    }
    
    .logo-icon {
        font-size: 2.5rem;
        background: rgba(255,255,255,0.1);
        padding: 0.8rem;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .bank-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: white !important;
    }
    
    .bank-subtitle {
        font-size: 1.1rem !important;
        opacity: 0.9;
        margin: 0.2rem 0 0 0 !important;
        font-weight: 400;
    }
    
    .user-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.3rem;
        background: rgba(255,255,255,0.1);
        padding: 0.8rem 1.2rem;
        border-radius: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* 상단 컨트롤 - 개선된 레이아웃 */
    .top-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0;
        gap: 1rem;
        padding: 0.8rem 2rem;
        background: rgba(255,255,255,0.08);
        border-top: 1px solid rgba(255,255,255,0.1);
    }
    
    .controls-group {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .status-time-group {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255,255,255,0.15);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .control-info {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        color: #1e293b;
        font-size: 0.9rem;
        font-weight: 500;
        background: rgba(255,255,255,0.9);
        border-radius: 8px;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .status-online {
        background: #dcfce7;
        color: #166534;
    }
    
    /* 캡처 금지 경고 - 둥글게 */
    .capture-warning {
        background: linear-gradient(45deg, #dc2626, #b91c1c);
        color: white;
        padding: 1.2rem;
        text-align: center;
        font-weight: 800;
        font-size: 1.1rem;
        margin: 0 -1rem 0 -1rem;
        animation: pulse 2s infinite;
        border-radius: 0 0 20px 20px;
    }
    
    /* 보안 경고 */
    .security-alert {
        background: linear-gradient(45deg, #d97706, #b45309);
        color: white;
        padding: 1rem 2rem;
        text-align: center;
        font-weight: 700;
        font-size: 1rem;
        margin: 0 -1rem 2rem -1rem;
        animation: glow 2s infinite;
        border-radius: 0 0 15px 15px;
    }
    
    /* 공지사항 섹션 - 깔끔한 버전 */
    .announcement-section-clean {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border-top: 4px solid #3b82f6;
    }
    
    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #f1f5f9;
    }
    
    /* 구분선 */
    .section-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem -1rem;
        border: none;
    }
    
    /* 메트릭 카드 */
    .metric-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 1px solid #f1f5f9;
        margin-bottom: 1rem;
        border-top: 4px solid #3b82f6;
    }
    
    .content-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        border-top: 4px solid #10b981;
    }
    
    /* 실시간 효과를 위한 애니메이션 */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 4px 12px rgba(217, 119, 6, 0.4); }
        50% { box-shadow: 0 6px 18px rgba(217, 119, 6, 0.6); }
    }
    
    /* Streamlit 버튼 스타일 */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
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
            st.markdown("### 🔐 ログイン / Login")
            with st.form("login_form"):
                user_id = st.text_input(get_text('login_id'), placeholder="otsuka / 大塚")
                password = st.text_input(get_text('password'), type="password", placeholder="bank1234")
                
                if st.form_submit_button(get_text('login'), use_container_width=True, type="primary"):
                    if user_id == "otsuka" and password == "bank1234":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error(get_text('login_error'))

def main_layout():
    """메인 레이아웃 - 모든 페이지에서 호출"""
    load_css()  # 모든 페이지에서 CSS 적용
    
    user_name_jp = st.session_state.user_data['name'].split(' / ')[0]
    
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
                <div class="user-info">
                    <div class="welcome-text">{get_text('welcome').format(user_name_jp)}</div>
                    <div class="account-info">{get_text('account_number')}: {st.session_state.user_data['account']}</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 상단 컨트롤 - 개선된 레이아웃
    st.markdown('<div class="top-controls">', unsafe_allow_html=True)
    
    # 왼쪽 그룹: 상태와 시간을 함께 표시
    st.markdown('<div class="controls-group">', unsafe_allow_html=True)
    
    # 상태와 시간을 같은 그룹으로
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M")
    st.markdown(f"""
    <div class="status-time-group">
        <div class="status-indicator status-online">
            <div style="width: 8px; height: 8px; background: #16a34a; border-radius: 50%; margin-right: 8px;"></div>
            Online / オンライン
        </div>
        <div style="color: white; margin: 0 10px;">|</div>
        <div class="control-info" style="margin: 0; background: rgba(255,255,255,0.15); color: white; border: 1px solid rgba(255,255,255,0.3);">
            <span>📅</span>
            <span>{current_time}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 오른쪽 그룹: 언어 변경과 로그아웃
    st.markdown('<div class="controls-group">', unsafe_allow_html=True)
    
    # 언어 전환 버튼
    current_lang = st.session_state.language
    if st.button("🌐 English / 日本語", key="lang_switcher", use_container_width=True,
                type="primary" if current_lang == 'EN' else "secondary"):
        st.session_state.language = 'EN' if current_lang == 'JP' else 'JP'
        st.rerun()
    
    # 로그아웃 버튼
    if st.button(get_text('logout'), key="logout_btn", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 구분선 추가
    st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

def show_security_warnings():
    """보안 경고 표시"""
    st.markdown(f'<div class="capture-warning">{get_text("no_capture")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="security-alert">{get_text("security_warning")}</div>', unsafe_allow_html=True)

def show_announcement():
    """공지사항 표시 - 깔끔한 버전으로 수정"""
    announcements = [
        {
            "icon": "🔧",
            "title": "システムメンテナンス / System Maintenance",
            "content": "12月25日 2:00-4:00 / Dec 25th 2:00-4:00",
            "date": "2024-12-20",
            "priority": "high"
        },
        {
            "icon": "📈", 
            "title": "新積立プラン開始 / New Savings Plan Available",
            "content": "高金利プランのご案内 / Information about high-interest plans",
            "date": "2024-12-18",
            "priority": "medium"
        },
        {
            "icon": "🎄",
            "title": "年末年始の営業について / Year-End Business Hours", 
            "content": "12月29日～1月4日休業 / Closed from Dec 29 to Jan 4",
            "date": "2024-12-15",
            "priority": "medium"
        }
    ]
    
    st.markdown('<div class="announcement-section-clean fade-in">', unsafe_allow_html=True)
    st.markdown(f'<div class="section-header">📢 {get_text("announcement")}</div>', unsafe_allow_html=True)
    
    for announcement in announcements:
        with st.container():
            col1, col2 = st.columns([1, 20])
            with col1:
                st.write(announcement['icon'])
            with col2:
                st.markdown(f"**{announcement['title']}**")
                st.markdown(f"{announcement['content']}")
                st.markdown(f"<small style='color: #64748b;'>{announcement['date']}</small>", unsafe_allow_html=True)
            
            st.divider()
    
    st.markdown('</div>', unsafe_allow_html=True)