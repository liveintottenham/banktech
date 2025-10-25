import streamlit as st
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import time
import base64
from io import BytesIO

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
        'title': 'Otsuka Bank',
        'subtitle': 'Employee Banking Portal',
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
        'security_warning': '🔒 セキュリティ警告: このページは監視されています',
        'download_payslip': '📥 給与明細をダウンロード',
        'announcement': '📢 お知らせ',
        'announcement_content': 'システムメンテナンス: 12月25日 2:00-4:00'
    },
    'JP': {
        'title': '大塚銀行',
        'subtitle': '従業員バンキングポータル',
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
        'security_warning': '🔒 セキュリティ警告: このページは監視されています',
        'download_payslip': '📥 給与明細をダウンロード',
        'announcement': '📢 お知らせ',
        'announcement_content': 'システムメンテナンス: 12月25日 2:00-4:00'
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language].get(key, LANGUAGES['EN'].get(key, key))

# 급여명세서 HTML 생성 함수
def create_payslip_html(salary_data, payslip_date, user_data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>給与明細 - {payslip_date}</title>
        <style>
            body {{
                font-family: 'Hiragino Sans', 'Hiragino Kaku Gothic ProN', 'Yu Gothic', sans-serif;
                margin: 0;
                padding: 20px;
                background: #f5f5f5;
                color: #333;
            }}
            .payslip-container {{
                max-width: 800px;
                margin: 0 auto;
                background: white;
                padding: 30px;
                box-shadow: 0 0 20px rgba(0,0,0,0.1);
                border-radius: 8px;
            }}
            .header {{
                text-align: center;
                border-bottom: 3px solid #2c5282;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .company-name {{
                font-size: 24px;
                font-weight: bold;
                color: #2c5282;
                margin-bottom: 10px;
            }}
            .title {{
                font-size: 20px;
                color: #333;
                margin-bottom: 20px;
            }}
            .info-section {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 20px;
                margin-bottom: 30px;
            }}
            .info-box {{
                background: #f8f9fa;
                padding: 15px;
                border-radius: 6px;
                border-left: 4px solid #2c5282;
            }}
            .amount-section {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 30px;
                margin-bottom: 30px;
            }}
            .income-box, .deduction-box {{
                padding: 20px;
                border-radius: 8px;
            }}
            .income-box {{
                background: #f0fff4;
                border: 2px solid #38a169;
            }}
            .deduction-box {{
                background: #fff5f5;
                border: 2px solid #e53e3e;
            }}
            .total-section {{
                background: #2c5282;
                color: white;
                padding: 25px;
                border-radius: 8px;
                text-align: center;
                margin-top: 20px;
            }}
            .total-amount {{
                font-size: 28px;
                font-weight: bold;
                margin: 10px 0;
            }}
            .detail-row {{
                display: flex;
                justify-content: space-between;
                padding: 8px 0;
                border-bottom: 1px solid #e2e8f0;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #e2e8f0;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="payslip-container">
            <div class="header">
                <div class="company-name">大塚銀行</div>
                <div class="title">給与明細書</div>
                <div>支給日: {payslip_date}</div>
            </div>
            
            <div class="info-section">
                <div class="info-box">
                    <strong>氏名</strong><br>
                    {user_data['name']}<br>
                    <strong>社員番号</strong><br>
                    {user_data['emp_num']}
                </div>
                <div class="info-box">
                    <strong>所属部署</strong><br>
                    {user_data['department']}<br>
                    <strong>口座番号</strong><br>
                    {user_data['account']}
                </div>
            </div>
            
            <div class="amount-section">
                <div class="income-box">
                    <h3 style="color: #38a169; margin-top: 0;">支給内訳</h3>
                    <div class="detail-row">
                        <span>基本給</span>
                        <span>¥{salary_data['income_breakdown']['basic_salary']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>残業代</span>
                        <span>¥{salary_data['income_breakdown']['overtime_pay']['amount']:,.0f}</span>
                    </div>
                    <div style="border-top: 2px solid #38a169; padding-top: 10px; margin-top: 10px;">
                        <div class="detail-row">
                            <strong>総支給額</strong>
                            <strong>¥{salary_data['total_income']:,.0f}</strong>
                        </div>
                    </div>
                </div>
                
                <div class="deduction-box">
                    <h3 style="color: #e53e3e; margin-top: 0;">控除内訳</h3>
                    <div class="detail-row">
                        <span>所得税</span>
                        <span>¥{salary_data['deduction_breakdown']['income_tax']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>住民税</span>
                        <span>¥{salary_data['deduction_breakdown']['residence_tax']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>健康保険</span>
                        <span>¥{salary_data['deduction_breakdown']['health_insurance']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>厚生年金</span>
                        <span>¥{salary_data['deduction_breakdown']['pension']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>雇用保険</span>
                        <span>¥{salary_data['deduction_breakdown']['employment_insurance']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>その他控除</span>
                        <span>¥{salary_data['deduction_breakdown']['other_deduction']['amount']:,.0f}</span>
                    </div>
                    <div style="border-top: 2px solid #e53e3e; padding-top: 10px; margin-top: 10px;">
                        <div class="detail-row">
                            <strong>総控除額</strong>
                            <strong>¥{salary_data['total_deductions']:,.0f}</strong>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="total-section">
                <div>差引支給額</div>
                <div class="total-amount">¥{salary_data['net_salary']:,.0f}</div>
                <div>振込予定日: {payslip_date}</div>
            </div>
            
            <div class="footer">
                この書類は大塚銀行従業員ポータルで発行されました<br>
                発行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

# CSS 스타일링 - 개선된 모던 디자인
def load_css():
    css = """
    <style>
    /* 기본 스타일 - 세련된 그레이 그라데이션 */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #f8fafc 100%);
        font-family: 'Noto Sans JP', 'Segoe UI', 'Hiragino Sans', sans-serif;
        color: #1e293b;
    }
    
    /* 헤더 스타일 - 완전히 새로 디자인 */
    .bank-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        color: white;
        padding: 2rem 0 1.5rem 0;
        margin: -1rem -1rem 0 -1rem;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.2);
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
        background: 
            radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(99, 102, 241, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(79, 70, 229, 0.15) 0%, transparent 50%);
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
    }
    
    .logo-text {
        display: flex;
        flex-direction: column;
    }
    
    .bank-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: white !important;
        letter-spacing: -0.5px;
        line-height: 1.1;
    }
    
    .bank-subtitle {
        font-size: 1.1rem !important;
        opacity: 0.9;
        margin: 0.2rem 0 0 0 !important;
        font-weight: 400;
        letter-spacing: 0.3px;
    }
    
    .user-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.3rem;
    }
    
    .welcome-text {
        font-size: 1rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    .account-info {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    /* 상단 컨트롤 섹션 */
    .top-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0;
        gap: 1rem;
    }
    
    .controls-left {
        display: flex;
        gap: 0.5rem;
        flex: 1;
    }
    
    .controls-right {
        display: flex;
        gap: 0.5rem;
    }
    
    /* 네비게이션 - 컴팩트하게 재디자인 */
    .nav-container {
        background: white;
        padding: 0;
        margin: 0 -1rem;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .nav-buttons {
        display: flex;
        justify-content: center;
        gap: 0;
        max-width: 500px;
        margin: 0 auto;
    }
    
    .nav-btn {
        flex: 1;
        background: transparent;
        border: none;
        color: #64748b;
        padding: 1rem 0.5rem;
        font-weight: 600;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        border-bottom: 2px solid transparent;
    }
    
    .nav-btn:hover {
        background: rgba(59, 130, 246, 0.05);
        color: #1e40af;
    }
    
    .nav-btn.active {
        color: #1e40af;
        border-bottom: 2px solid #3b82f6;
    }
    
    /* 공지사항 배너 */
    .announcement-banner {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 0.8rem 1.5rem;
        margin: 0 -1rem 1.5rem -1rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        display: flex;
        align-items: center;
        gap: 0.8rem;
        font-weight: 500;
        animation: slideDown 0.5s ease-out;
    }
    
    @keyframes slideDown {
        from {
            transform: translateY(-100%);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* 캡처 방지 배너 */
    .capture-warning {
        background: linear-gradient(45deg, #dc2626, #b91c1c);
        color: white;
        padding: 0.8rem;
        text-align: center;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0 -1rem 1.5rem -1rem;
        animation: alertPulse 3s ease-in-out infinite;
        position: relative;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
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
    
    @keyframes alertPulse {
        0%, 100% { 
            opacity: 1;
            box-shadow: 0 2px 8px rgba(220, 38, 38, 0.3);
        }
        50% { 
            opacity: 0.95;
            box-shadow: 0 4px 12px rgba(220, 38, 38, 0.4);
        }
    }
    
    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* 메트릭 카드 */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.2rem;
        margin: 2rem 0;
    }
    
    .metric-card {
        background: white;
        color: #1e293b;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #3b82f6, #60a5fa);
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.7rem 1.2rem !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3) !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4) !important;
    }
    
    /* 콘텐츠 카드 */
    .content-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid #f1f5f9;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    }
    
    /* 언어 스위처 컴팩트하게 */
    .lang-btn {
        background: rgba(255,255,255,0.15) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3) !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.4rem 1rem !important;
        font-size: 0.8rem !important;
    }
    
    /* 로그아웃 버튼 */
    .logout-btn {
        background: rgba(239, 68, 68, 0.9) !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
    }
    
    .logout-btn:hover {
        background: rgba(220, 38, 38, 0.9) !important;
    }
    
    /* 입력 필드 */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select {
        background: white !important;
        border: 1.5px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.7rem 1rem !important;
        font-size: 0.9rem !important;
        color: #1e293b !important;
    }
    
    .stTextInput>div>div>input:focus,
    .stNumberInput>div>div>input:focus,
    .stDateInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0px;
        background-color: white;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0 1.5rem;
        font-weight: 600;
        color: #64748b;
        border-bottom: 2px solid transparent;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1e40af !important;
        border-bottom: 2px solid #3b82f6 !important;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
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

# 공지사항 배너
def show_announcement():
    st.markdown(f'''
    <div class="announcement-banner">
        <span>📢</span>
        <span>{get_text("announcement_content")}</span>
    </div>
    ''', unsafe_allow_html=True)

# 적금 계산 함수 (기존과 동일)
def calculate_savings_schedule(monthly_amount, period_years, interest_rate, start_date, adjustments=None):
    total_months = period_years * 12
    monthly_interest_rate = interest_rate / 100 / 12
    today = datetime.now().date()
    
    schedule = []
    current_balance = 0
    
    for month in range(1, total_months + 1):
        payment_date = start_date + relativedelta(months=month-1)
        
        actual_amount = monthly_amount
        adjustment_note = ""
        if adjustments and month in adjustments:
            actual_amount = adjustments[month]
            adjustment_note = f"調整済: ¥{adjustments[month]:,}"
        
        monthly_interest = round(current_balance * monthly_interest_rate)
        current_balance += actual_amount + monthly_interest
        
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

# 급여 계산 함수 (기존과 동일)
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
    show_announcement()
    
    st.markdown(f"## 👋 {get_text('welcome').format(st.session_state.user_data['name'])}")
    
    # 요약 메트릭
    st.markdown("### 📊 資産概要")
    
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
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">総積立額</div>
            <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{total_savings:,.0f}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">前月比 +2.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">月間支払額</div>
            <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{monthly_payment:,.0f}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">実行中プラン</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">実行中プラン</div>
            <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">{active_plans}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">総プラン数</div>
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

# 적금 관리 페이지 (기존과 동일)
def render_savings():
    show_security_warnings()
    show_announcement()
    
    st.markdown("## 💰 積立貯蓄管理")
    
    tab1, tab2 = st.tabs(["🆕 新規積立作成", "📋 積立一覧"])
    
    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🆕 新規積立口座開設")
        
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
        
        if st.button("🚀 積立プラン作成", use_container_width=True, type="primary"):
            adjustments_dict = {adj['month']: adj['amount'] for adj in st.session_state.adjustments}
            
            calculation = calculate_savings_schedule(
                monthly_amount, 
                period, 
                interest_rate, 
                start_date, 
                adjustments_dict
            )
            
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
                    
                    st.markdown("#### 入金スケジュール")
                    schedule_data = []
                    for item in savings['calculation']['schedule'][:12]:
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
                    
                    if st.button(f"🗑️ 削除", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# 급여 명세서 페이지 - HTML 다운로드 기능 추가
def render_payroll():
    show_security_warnings()
    show_announcement()
    
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
        
        submitted = st.form_submit_button("📄 明細発行", use_container_width=True, type="primary")
        
        if submitted:
            salary_data = calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction)
            
            new_payslip = {
                'id': len(st.session_state.payroll_list) + 1,
                'date': payslip_date.strftime('%Y/%m/%d'),
                'salary_data': salary_data,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.payroll_list.append(new_payslip)
            
            st.success("🎉 給与明細が作成されました！")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("総支給額", f"¥{salary_data['total_income']:,.0f}")
            with col2:
                st.metric("総控除額", f"¥{salary_data['total_deductions']:,.0f}")
            with col3:
                st.metric("差引支給額", f"¥{salary_data['net_salary']:,.0f}")
            
            # HTML 다운로드 버튼
            html_content = create_payslip_html(salary_data, payslip_date.strftime('%Y年%m月%d日'), st.session_state.user_data)
            
            # HTML 파일 다운로드 링크 생성
            b64 = base64.b64encode(html_content.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="給与明細_{payslip_date.strftime("%Y%m%d")}.html" style="text-decoration: none;">'
            st.markdown(
                f'{href}'
                f'<button style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer; margin-top: 1rem;">'
                f'📥 給与明細をダウンロード（HTML形式）'
                f'</button>'
                f'</a>',
                unsafe_allow_html=True
            )
            
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
    if st.button("English", key="lang_en", use_container_width=True, 
                 type="primary" if current_lang == 'EN' else "secondary",
                 help="Switch to English"):
        st.session_state.language = 'EN'
        st.rerun()

# 로그아웃
def render_logout():
    if st.button(get_text('logout'), key="logout_btn", use_container_width=True,
                 type="secondary", help="ログアウト"):
        st.session_state.logged_in = False
        st.rerun()

# 메인 앱
def main():
    initialize_session_state()
    load_css()
    
    if not st.session_state.logged_in:
        login()
    else:
        # 새로 디자인된 헤더
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
                        <div class="welcome-text">{get_text('welcome').format(st.session_state.user_data['name'])}</div>
                        <div class="account-info">{get_text('account_number')}: {st.session_state.user_data['account']}</div>
                    </div>
                </div>
                
                <div class="top-controls">
                    <div class="controls-left">
                        {render_language_switcher()}
                    </div>
                    <div class="controls-right">
                        {render_logout()}
                    </div>
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