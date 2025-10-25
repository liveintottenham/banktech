import streamlit as st
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

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
        st.session_state.language = 'EN'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    if 'adjustments' not in st.session_state:
        st.session_state.adjustments = []
    
    # 사용자 데이터
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            "name": "Yamada Taro",
            "account": "098-96586-6521",
            "emp_num": "12345678",
            "department": "IT Department"
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
        'savings': '💰 Savings Management',
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
        'no_capture': '⚠️ SCREENSHOT AND PHOTOGRAPHY PROHIBITED',
        'no_capture_jp': '⚠️ この画面のスクリーンショット・撮影は禁止されています'
    },
    'JP': {
        'title': '大塚銀行 従業員ポータル',
        'subtitle': 'セキュアバンキング管理システム',
        'login_id': 'ログインID',
        'password': 'パスワード',
        'login': 'ログイン',
        'login_error': 'ログインIDまたはパスワードが正しくありません',
        'home': '🏠 ホーム',
        'savings': '💰 積立管理',
        'payroll': '📄 給与明細',
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
        'overtime_pay': '時間外手当',
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
        'no_capture': '⚠️ SCREENSHOT AND PHOTOGRAPHY PROHIBITED',
        'no_capture_jp': '⚠️ この画面のスクリーンショット・撮影は禁止されています'
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
        font-family: 'Noto Sans JP', 'Malgun Gothic', sans-serif;
    }
    
    .main-container {
        background: white;
        border-radius: 15px;
        margin: 20px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        min-height: calc(100vh - 40px);
        overflow: hidden;
    }
    
    .content-area {
        padding: 30px;
    }
    
    /* 헤더 스타일 */
    .bank-header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 2rem 3rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .bank-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
    }
    
    .bank-subtitle {
        font-size: 1.1rem !important;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* 네비게이션 */
    .nav-container {
        background: #f8f9fa;
        padding: 1rem 2rem;
        border-bottom: 1px solid #dee2e6;
    }
    
    /* 카드 스타일 */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2c3e50, #3498db);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 6px 20px rgba(44, 62, 80, 0.3);
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #2c3e50, #3498db) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.7rem 1.2rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 12px rgba(44, 62, 80, 0.4) !important;
    }
    
    /* 입력 필드 */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input,
    .stSelectbox>div>div>select {
        border: 1px solid #ced4da !important;
        border-radius: 8px !important;
        padding: 0.7rem 1rem !important;
    }
    
    /* 테이블 스타일 */
    .dataframe {
        border-radius: 8px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1) !important;
    }
    
    /* 캡처 방지 배너 */
    .no-capture {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        color: white;
        padding: 0.8rem;
        text-align: center;
        font-weight: bold;
        font-size: 0.9rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* 조정 아이템 */
    .adjustment-item {
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Noto Sans JP', sans-serif;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 적금 계산 함수 (실제 은행 방식)
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
            adjustment_note = f"Adjusted: ¥{adjustments[month]:,}"
        
        # 이자 계산
        monthly_interest = current_balance * monthly_interest_rate
        current_balance += actual_amount + monthly_interest
        
        # 상태 결정 (오늘 기준)
        if payment_date < today:
            status = "✅ Completed"
        elif payment_date == today:
            status = "⏳ Today"
        else:
            status = "📅 Scheduled"
        
        schedule.append({
            'Month': month,
            'Payment Date': payment_date.strftime('%Y/%m/%d'),
            'Payment Amount': actual_amount,
            'Interest': monthly_interest,
            'Total Balance': current_balance,
            'Status': status,
            'Note': adjustment_note
        })
    
    total_payment = sum(item['Payment Amount'] for item in schedule)
    total_interest = sum(item['Interest'] for item in schedule)
    
    return {
        'schedule': schedule,
        'total_months': total_months,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'final_balance': current_balance,
        'completion_rate': len([x for x in schedule if 'Completed' in x['Status']]) / total_months * 100
    }

# 급여 계산 함수
def calculate_salary(basic_salary, overtime_pay, bonus, allowances, insurance, tax, other_deductions):
    total_income = basic_salary + overtime_pay + bonus + allowances
    total_deductions = insurance + tax + other_deductions
    net_salary = total_income - total_deductions
    
    return {
        'total_income': total_income,
        'total_deductions': total_deductions,
        'net_salary': net_salary,
        'income_breakdown': {
            'Basic Salary': basic_salary,
            'Overtime Pay': overtime_pay,
            'Bonus': bonus,
            'Allowances': allowances
        },
        'deduction_breakdown': {
            'Insurance': insurance,
            'Tax': tax,
            'Other Deductions': other_deductions
        }
    }

# 네비게이션
def render_nav():
    nav_items = [
        ('home', get_text('home')),
        ('savings', get_text('savings')), 
        ('payroll', get_text('payroll'))
    ]
    
    cols = st.columns(len(nav_items))
    for idx, (page, label) in enumerate(nav_items):
        with cols[idx]:
            if st.button(
                label, 
                use_container_width=True,
                type="primary" if st.session_state.current_page == page else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()

# 홈 페이지
def render_home():
    st.markdown(f"## {get_text('welcome').format(st.session_state.user_data['name'])}")
    
    # 요약 메트릭
    col1, col2, col3 = st.columns(3)
    
    # 실제 데이터 계산
    total_savings = 0
    monthly_payment = 0
    active_plans = len(st.session_state.savings_list)
    
    for savings in st.session_state.savings_list:
        calc = savings['calculation']
        total_savings += calc['final_balance']
        monthly_payment += savings['monthly_amount']
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('total_savings')}</div>
            <div style="font-size: 1.8rem; font-weight: 700;">¥{total_savings:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('monthly_payment')}</div>
            <div style="font-size: 1.8rem; font-weight: 700;">¥{monthly_payment:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('active_plans')}</div>
            <div style="font-size: 1.8rem; font-weight: 700;">{active_plans}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 빠른 접근
    st.markdown(f"## {get_text('quick_access')}")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"💰 {get_text('new_savings')}", use_container_width=True):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col2:
        if st.button(f"📄 {get_text('payroll')}", use_container_width=True):
            st.session_state.current_page = 'payroll'
            st.rerun()

# 적금 관리 페이지
def render_savings():
    st.markdown(f"## {get_text('savings_management')}")
    
    tab1, tab2 = st.tabs(["New Savings Plan", "Savings List"])
    
    with tab1:
        st.subheader("Create New Savings Plan")
        
        # 캡처 방지 배너 - 일본어로 표시
        st.markdown(f'<div class="no-capture">{LANGUAGES["JP"]["no_capture_jp"]}</div>', unsafe_allow_html=True)
        
        with st.form("new_savings_plan"):
            st.markdown("#### Basic Information")
            col1, col2 = st.columns(2)
            
            with col1:
                customer_name = st.text_input(get_text('customer_name'), st.session_state.user_data['name'])
                employee_number = st.text_input(get_text('employee_number'), st.session_state.user_data['emp_num'])
                account_number = st.text_input(get_text('account_number'), st.session_state.user_data['account'])
            
            with col2:
                savings_name = st.text_input(get_text('savings_name'), "Regular Savings Plan")
                monthly_amount = st.number_input(get_text('monthly_amount'), min_value=1000, value=3000, step=1000)
                period = st.selectbox(get_text('period'), [3, 5], index=0, format_func=lambda x: f"{x} Years")
                interest_rate = st.number_input(get_text('interest_rate'), min_value=0.1, value=2.5, step=0.1, format="%.1f")
                start_date = st.date_input(get_text('start_date'), date(2025, 1, 1))
            
            st.markdown("#### Payment Adjustments")
            st.info("Set different payment amounts for specific months if needed")
            
            # 동적 조정 입력
            adjustments_dict = {}
            
            for i, adj in enumerate(st.session_state.adjustments):
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    month = st.number_input(f"Month", min_value=1, max_value=period*12, value=adj['month'], key=f"month_{i}")
                with col2:
                    amount = st.number_input(f"Amount", min_value=0, value=adj['amount'], key=f"amount_{i}")
                with col3:
                    if st.form_submit_button(f"🗑️", key=f"remove_{i}", use_container_width=True):
                        st.session_state.adjustments.pop(i)
                        st.rerun()
                adjustments_dict[month] = amount
            
            # 새 조정 추가
            col1, col2, col3 = st.columns([2, 2, 1])
            with col1:
                new_month = st.number_input("Month", min_value=1, max_value=period*12, value=1, key="new_month")
            with col2:
                new_amount = st.number_input("Amount", min_value=0, value=monthly_amount, key="new_amount")
            with col3:
                add_pressed = st.form_submit_button("➕ Add", use_container_width=True)
                if add_pressed:
                    st.session_state.adjustments.append({'month': new_month, 'amount': new_amount})
                    st.rerun()
            
            submit_button = st.form_submit_button(get_text('create_plan'), use_container_width=True)
            if submit_button:
                # 적금 계산
                calculation = calculate_savings_schedule(monthly_amount, period, interest_rate, start_date, adjustments_dict)
                
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
                st.session_state.adjustments = []  # 초기화
                st.success("🎉 Savings plan created successfully!")
                st.balloons()
    
    with tab2:
        st.subheader("Savings Plans List")
        
        if not st.session_state.savings_list:
            st.info("No savings plans registered.")
        else:
            for savings in st.session_state.savings_list:
                with st.expander(f"📒 {savings['name']} - {savings['account_number']}", expanded=False):
                    # 캡처 방지 배너 - 일본어로 표시
                    st.markdown(f'<div class="no-capture">{LANGUAGES["JP"]["no_capture_jp"]}</div>', unsafe_allow_html=True)
                    
                    # 기본 정보
                    st.markdown("#### Basic Information")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write("**Customer Name**")
                        st.write(savings['customer_name'])
                    with col2:
                        st.write("**Employee Number**")
                        st.write(savings['employee_number'])
                    with col3:
                        st.write("**Account Number**")
                        st.write(savings['account_number'])
                    with col4:
                        st.write("**Start Date**")
                        st.write(savings['start_date'])
                    
                    # 적금 정보
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write("**Monthly Amount**")
                        st.write(f"¥{savings['monthly_amount']:,.0f}")
                    with col2:
                        st.write("**Period**")
                        st.write(f"{savings['period']} years")
                    with col3:
                        st.write("**Interest Rate**")
                        st.write(f"{savings['interest_rate']}%")
                    with col4:
                        completion = savings['calculation']['completion_rate']
                        st.write("**Completion Rate**")
                        st.write(f"{completion:.1f}%")
                    
                    # 계산 결과
                    calc = savings['calculation']
                    st.markdown("#### Calculation Results")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Payment", f"¥{calc['total_payment']:,.0f}")
                    with col2:
                        st.metric("Total Interest", f"¥{calc['total_interest']:,.0f}")
                    with col3:
                        st.metric("Final Balance", f"¥{calc['final_balance']:,.0f}")
                    with col4:
                        st.metric("Total Months", f"{calc['total_months']}")
                    
                    # 입금 스케줄
                    st.markdown("#### Payment Schedule")
                    schedule_df = pd.DataFrame(savings['calculation']['schedule'])
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
                    
                    # 삭제 버튼
                    if st.button(f"🗑️ Delete", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()

# 급여 명세서 페이지
def render_payroll():
    st.markdown(f"## {get_text('payroll_management')}")
    
    # 캡처 방지 배너 - 일본어로 표시
    st.markdown(f'<div class="no-capture">{LANGUAGES["JP"]["no_capture_jp"]}</div>', unsafe_allow_html=True)
    
    with st.form("payroll_form"):
        st.subheader("Payroll Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Income Details")
            basic_salary = st.number_input(get_text('basic_salary'), value=300000, step=10000)
            overtime_pay = st.number_input(get_text('overtime_pay'), value=50000, step=5000)
            bonus = st.number_input(get_text('bonus'), value=0, step=10000)
            allowances = st.number_input(get_text('allowances'), value=15000, step=1000)
        
        with col2:
            st.markdown("#### Deduction Details")
            insurance = st.number_input(get_text('insurance'), value=45000, step=1000)
            tax = st.number_input(get_text('tax'), value=35000, step=1000)
            other_deductions = st.number_input(get_text('other_deductions'), value=10000, step=1000)
            payslip_date = st.date_input(get_text('payslip_date'), datetime.now().date())
        
        if st.form_submit_button(get_text('generate_payslip'), use_container_width=True):
            # 급여 계산
            salary_data = calculate_salary(basic_salary, overtime_pay, bonus, allowances, insurance, tax, other_deductions)
            
            # 급여 명세서 저장
            new_payslip = {
                'id': len(st.session_state.payroll_list) + 1,
                'date': payslip_date.strftime('%Y/%m/%d'),
                'salary_data': salary_data,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.payroll_list.append(new_payslip)
            
            # 결과 표시
            st.success("Payslip generated successfully!")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('total_income'), f"¥{salary_data['total_income']:,.0f}")
            with col2:
                st.metric(get_text('total_deduction'), f"¥{salary_data['total_deductions']:,.0f}")
            with col3:
                st.metric(get_text('net_salary'), f"¥{salary_data['net_salary']:,.0f}")
            
            # 상세 내역
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### Income Breakdown")
                for item, amount in salary_data['income_breakdown'].items():
                    st.write(f"{item}: ¥{amount:,.0f}")
            
            with col2:
                st.markdown("##### Deduction Breakdown")
                for item, amount in salary_data['deduction_breakdown'].items():
                    st.write(f"{item}: ¥{amount:,.0f}")
    
    # 저장된 급여 명세서 목록
    if st.session_state.payroll_list:
        st.markdown("## Saved Payslips")
        for payslip in st.session_state.payroll_list[-5:]:
            with st.expander(f"Payslip - {payslip['date']}", expanded=False):
                data = payslip['salary_data']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric(get_text('total_income'), f"¥{data['total_income']:,.0f}")
                with col2:
                    st.metric(get_text('total_deduction'), f"¥{data['total_deductions']:,.0f}")
                with col3:
                    st.metric(get_text('net_salary'), f"¥{data['net_salary']:,.0f}")

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
        with st.container():
            st.markdown("### Login")
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
    
    # 메인 컨테이너 시작
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        st.markdown('<div class="content-area">', unsafe_allow_html=True)
        login()
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # 헤더
        st.markdown('<div class="bank-header">', unsafe_allow_html=True)
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f'<h1 class="bank-title">{get_text("title")}</h1>', unsafe_allow_html=True)
            st.markdown(f'<p class="bank-subtitle">{get_text("subtitle")}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">{get_text("welcome").format(st.session_state.user_data["name"])} | {get_text("account_number")}: {st.session_state.user_data["account"]}</p>', unsafe_allow_html=True)
        
        with col2:
            st.write("")
            render_language_switcher()
            render_logout()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 네비게이션
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        render_nav()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 페이지 내용
        st.markdown('<div class="content-area">', unsafe_allow_html=True)
        if st.session_state.current_page == 'home':
            render_home()
        elif st.session_state.current_page == 'savings':
            render_savings()
        elif st.session_state.current_page == 'payroll':
            render_payroll()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 메인 컨테이너 종료
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()