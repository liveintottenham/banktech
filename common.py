# common.py
import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import time
import base64
import random

# 다국어 지원 - 일본어/영어 병행 표기
LANGUAGES = {
    'EN': {
        'title': 'Otsuka Bank / 大塚銀行',
        'subtitle': 'Employee Banking Portal / 従業員バンキングポータル',
        'login_id': 'Login ID / ログインID',
        'password': 'Password / パスワード',
        'login': 'Login / ログイン',
        'login_error': 'Incorrect Login ID or Password / ログインIDまたはパスワードが正しくありません',
        'home': '🏠 Home / ホーム',
        'savings': '💰 Savings / 積立',
        'payroll': '📄 Payroll / 給与',
        'welcome': 'Welcome, {} / ようこそ、{}様',
        'logout': 'Logout / ログアウト',
        'no_capture': '⚠️ SCREEN CAPTURE AND PHOTOGRAPHY PROHIBITED / この画面のスクリーンショット・撮影は禁止されています',
        'security_warning': '🔒 SECURITY WARNING: THIS PAGE IS MONITORED / セキュリティ警告: このページは監視されています',
        'announcement': '📢 Announcement / お知らせ',
        'announcement_content': 'System Maintenance: Dec 25th 2:00-4:00 / システムメンテナンス: 12月25日 2:00-4:00',
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
        'savings_details': 'Savings Details / 積立詳細',
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
        'home': '🏠 ホーム / Home',
        'savings': '💰 積立 / Savings',
        'payroll': '📄 給与 / Payroll',
        'welcome': 'ようこそ、{}様 / Welcome, {}',
        'logout': 'ログアウト / Logout',
        'no_capture': '⚠️ この画面のスクリーンショット・撮影は禁止されています / SCREEN CAPTURE AND PHOTOGRAPHY PROHIBITED',
        'security_warning': '🔒 セキュリティ警告: このページは監視されています / SECURITY WARNING: THIS PAGE IS MONITORED',
        'announcement': '📢 お知らせ / Announcement',
        'announcement_content': 'システムメンテナンス: 12月25日 2:00-4:00 / System Maintenance: Dec 25th 2:00-4:00',
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
    return LANGUAGES[st.session_state.language].get(key, LANGUAGES['EN'].get(key, key))

# 세션 상태 초기화
def initialize_session_state():
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

# CSS 스타일링 - 개선된 버전
def load_css():
    css = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #f8fafc 100%);
        font-family: 'Noto Sans JP', 'Segoe UI', 'Hiragino Sans', sans-serif;
    }
    
    .bank-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        color: white;
        padding: 1.5rem 0 1rem 0;
        margin: -1rem -1rem 0 -1rem;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.2);
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
        margin-bottom: 1rem;
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
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .bank-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
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
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .top-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 0.5rem 0 0 0;
        gap: 1rem;
        padding: 0.8rem 1.5rem;
        background: rgba(255,255,255,0.08);
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.15);
    }
    
    .nav-container {
        background: white;
        padding: 0;
        margin: 0 -1rem;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .capture-warning {
        background: linear-gradient(45deg, #dc2626, #b91c1c, #dc2626);
        color: white;
        padding: 1.2rem;
        text-align: center;
        font-weight: 700;
        font-size: 1.1rem;
        margin: 0 -1rem 0 -1rem;
        animation: alertPulse 1.5s ease-in-out infinite, shake 0.5s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        text-shadow: 0 1px 2px rgba(0,0,0,0.3);
    }
    
    .capture-warning::before {
        content: "";
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        animation: shine 2s ease-in-out infinite;
    }
    
    .security-alert {
        background: linear-gradient(45deg, #d97706, #b45309, #d97706);
        color: white;
        padding: 1rem 2rem;
        text-align: center;
        font-weight: 600;
        font-size: 1rem;
        margin: 0 -1rem 1rem -1rem;
        animation: glow 2s ease-in-out infinite, colorShift 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    .announcement-banner {
        background: linear-gradient(135deg, #f59e0b, #d97706, #f59e0b);
        color: white;
        padding: 1.2rem 2rem;
        margin: 0 -1rem 1.5rem -1rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        display: flex;
        align-items: center;
        gap: 1rem;
        font-weight: 600;
        font-size: 1.1rem;
        animation: gentlePulse 4s ease-in-out infinite;
    }
    
    .announcement-section {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        margin-bottom: 1.5rem;
    }
    
    .announcement-item {
        padding: 0.8rem 0;
        border-bottom: 1px solid #f1f5f9;
        display: flex;
        align-items: flex-start;
        gap: 0.8rem;
    }
    
    .announcement-item:last-child {
        border-bottom: none;
    }
    
    .announcement-icon {
        font-size: 1.2rem;
        margin-top: 0.2rem;
    }
    
    .announcement-content {
        flex: 1;
    }
    
    .announcement-title {
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: #1e293b;
    }
    
    .announcement-date {
        font-size: 0.8rem;
        color: #64748b;
    }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    }
    
    .content-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    
    .quick-access-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .quick-access-item {
        background: linear-gradient(135deg, #3b82f6, #1d4ed8);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    
    .quick-access-item:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(59, 130, 246, 0.4);
        background: linear-gradient(135deg, #1d4ed8, #1e3a8a);
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
    
    .status-offline {
        background: #fecaca;
        color: #dc2626;
    }
    
    @keyframes alertPulse {
        0%, 100% { 
            background: linear-gradient(45deg, #dc2626, #b91c1c, #dc2626);
            transform: scale(1);
        }
        50% { 
            background: linear-gradient(45deg, #b91c1c, #dc2626, #b91c1c);
            transform: scale(1.01);
        }
    }
    
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-2px); }
        75% { transform: translateX(2px); }
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    @keyframes glow {
        0%, 100% { 
            box-shadow: 0 4px 12px rgba(217, 119, 6, 0.4);
        }
        50% { 
            box-shadow: 0 6px 18px rgba(217, 119, 6, 0.6);
        }
    }
    
    @keyframes colorShift {
        0%, 100% { 
            background: linear-gradient(45deg, #d97706, #b45309, #d97706);
        }
        50% { 
            background: linear-gradient(45deg, #b45309, #d97706, #b45309);
        }
    }
    
    @keyframes gentlePulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.95; }
    }
    
    .control-button {
        background: rgba(255,255,255,0.15) !important;
        color: white !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .control-button:hover {
        background: rgba(255,255,255,0.25) !important;
        transform: translateY(-1px);
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 로그인 페이지
def login():
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
        
        # 로그인 카드
        st.markdown("""
        <div style='
            background: white; 
            border-radius: 16px; 
            padding: 2.5rem; 
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            border: 1px solid #e2e8f0;
            margin: 1rem 0;
        '>
        """, unsafe_allow_html=True)
        
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
        
        st.markdown("</div>", unsafe_allow_html=True)

# 메인 레이아웃 - 개선된 버전
def main_layout():
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
                    <div class="welcome-text">{get_text('welcome').format(st.session_state.user_data['name'].split(' / ')[0])}</div>
                    <div class="account-info">{get_text('account_number')}: {st.session_state.user_data['account']}</div>
                </div>
            </div>
            
            <div class="top-controls">
                <div class="controls-left" style="display: flex; align-items: center; gap: 1rem;">
                    <div style="display: flex; gap: 0.5rem;">
    """, unsafe_allow_html=True)
    
    # 상단 컨트롤 - 언어 전환 및 상태 표시
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        render_language_switcher()
    
    with col2:
        st.markdown(f"""
        <div class="status-indicator status-online">
            <div style="width: 8px; height: 8px; background: #16a34a; border-radius: 50%;"></div>
            Online / オンライン
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        current_time = datetime.now().strftime("%Y/%m/%d %H:%M")
        st.markdown(f"""
        <div style="color: white; font-size: 0.9rem; opacity: 0.9;">
            📅 {current_time}
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
                    </div>
                </div>
                <div class="controls-right">
    """, unsafe_allow_html=True)
    
    with col4:
        render_logout()
    
    st.markdown("""
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 언어 전환
def render_language_switcher():
    current_lang = st.session_state.language
    if st.button("English / 英語", key="lang_en", use_container_width=True, 
                 type="primary" if current_lang == 'EN' else "secondary"):
        st.session_state.language = 'EN'
        st.rerun()

# 로그아웃
def render_logout():
    if st.button(get_text('logout'), key="logout_btn", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.rerun()

# 보안 경고 표시 - 개선된 버전
def show_security_warnings():
    st.markdown(f'<div class="capture-warning">{get_text("no_capture")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="security-alert">{get_text("security_warning")}</div>', unsafe_allow_html=True)

# 공지사항 배너 - 개선된 버전
def show_announcement():
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
    
    st.markdown(f'''
    <div class="announcement-banner">
        <span>📢</span>
        <span>{get_text("announcement_content")}</span>
    </div>
    ''', unsafe_allow_html=True)
    
    # 공지사항 상세 섹션
    st.markdown("### 📢 お知らせ / Announcements")
    
    with st.container():
        for announcement in announcements:
            priority_color = {
                "high": "#ef4444",
                "medium": "#f59e0b", 
                "low": "#3b82f6"
            }.get(announcement["priority"], "#6b7280")
            
            st.markdown(f"""
            <div class="announcement-item">
                <div class="announcement-icon" style="color: {priority_color};">{announcement['icon']}</div>
                <div class="announcement-content">
                    <div class="announcement-title">{announcement['title']}</div>
                    <div>{announcement['content']}</div>
                    <div class="announcement-date">{announcement['date']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)