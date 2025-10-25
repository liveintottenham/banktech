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

# 다국어 지원 - 영어와 일본어만
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
        'no_capture_jp': '⚠️ この画面のスクリーンショット・撮影は禁止されています',
        'income_tax': 'Income Tax',
        'residence_tax': 'Residence Tax',
        'health_insurance': 'Health Insurance',
        'pension': 'Pension',
        'employment_insurance': 'Employment Insurance',
        'other_deduction': 'Other Deduction'
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
        'no_capture': '⚠️ SCREENSHOT AND PHOTOGRAPHY PROHIBITED',
        'no_capture_jp': '⚠️ この画面のスクリーンショット・撮影は禁止されています',
        'income_tax': '所得税',
        'residence_tax': '住民税',
        'health_insurance': '健康保険',
        'pension': '厚生年金',
        'employment_insurance': '雇用保険',
        'other_deduction': '控除額'
    }
}

def get_text(key):
    # 키가 없으면 영어로 기본값 반환
    return LANGUAGES[st.session_state.language].get(key, LANGUAGES['EN'].get(key, key))

# CSS 스타일링 - 매우 간단하게 수정
def load_css():
    css = """
    <style>
    /* 매우 간단한 스타일 - 하얀색 도형 문제 해결 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Noto Sans JP', 'Segoe UI', sans-serif;
    }
    
    /* 헤더 스타일 */
    .bank-header {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white;
        padding: 2rem;
        margin: -1rem -1rem 2rem -1rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .bank-title {
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        margin-bottom: 0.5rem !important;
        color: white !important;
        text-align: center;
    }
    
    .bank-subtitle {
        font-size: 1.1rem !important;
        opacity: 0.9;
        text-align: center;
        margin-bottom: 1rem !important;
    }
    
    /* 네비게이션 */
    .nav-container {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        border-bottom: 1px solid #e0e0e0;
        display: flex;
        justify-content: center;
        gap: 1rem;
    }
    
    /* 카드 스타일 */
    .metric-card {
        background: linear-gradient(135deg, #6366F1, #8B5CF6);
        color: white;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        margin-bottom: 1rem;
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #6366F1, #8B5CF6) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4) !important;
    }
    
    /* 캡처 방지 배너 */
    .no-capture {
        background: linear-gradient(45deg, #EF4444, #DC2626);
        color: white;
        padding: 1rem;
        text-align: center;
        font-weight: bold;
        border-radius: 8px;
        margin-bottom: 1rem;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* 이중 언어 표기 */
    .bilingual {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
        padding: 0.5rem;
        background: #f8f9fa;
        border-radius: 6px;
    }
    
    .bilingual-en {
        font-weight: 600;
        color: #1F2937;
    }
    
    .bilingual-jp {
        font-size: 0.85rem;
        color: #6B7280;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700&display=swap');
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

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
            adjustment_note = f"Adjusted: ¥{adjustments[month]:,}"
        
        # 이자 계산 (반올림)
        monthly_interest = round(current_balance * monthly_interest_rate)
        current_balance += actual_amount + monthly_interest
        
        # 상태 결정 (오늘 기준)
        if payment_date < today:
            status = "✅ Completed"
            status_jp = "✅ 入金完了"
        elif payment_date == today:
            status = "⏳ Today"
            status_jp = "⏳ 本日入金"
        else:
            status = "📅 Scheduled"
            status_jp = "📅 入金予定"
        
        schedule.append({
            'Month': month,
            'Payment Date': payment_date.strftime('%Y/%m/%d'),
            'Payment Amount': actual_amount,
            'Interest': monthly_interest,
            'Total Balance': current_balance,
            'Status': status,
            'Status_JP': status_jp,
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
def calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction):
    total_income = basic_salary + overtime_pay
    total_deductions = income_tax + residence_tax + health_insurance + pension + employment_insurance + other_deduction
    net_salary = total_income - total_deductions
    
    return {
        'total_income': total_income,
        'total_deductions': total_deductions,
        'net_salary': net_salary,
        'income_breakdown': {
            'basic_salary': {'en': 'Basic Salary', 'jp': '基本給', 'amount': basic_salary},
            'overtime_pay': {'en': 'Overtime Pay', 'jp': '残業代', 'amount': overtime_pay}
        },
        'deduction_breakdown': {
            'income_tax': {'en': 'Income Tax', 'jp': '所得税', 'amount': income_tax},
            'residence_tax': {'en': 'Residence Tax', 'jp': '住民税', 'amount': residence_tax},
            'health_insurance': {'en': 'Health Insurance', 'jp': '健康保険', 'amount': health_insurance},
            'pension': {'en': 'Pension', 'jp': '厚生年金', 'amount': pension},
            'employment_insurance': {'en': 'Employment Insurance', 'jp': '雇用保険', 'amount': employment_insurance},
            'other_deduction': {'en': 'Other Deduction', 'jp': '控除額', 'amount': other_deduction}
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
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Asset Growth Trend")
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        values = [14200000, 14500000, 14800000, 15000000, 15200000, 15400000, 15600000, 15800000, 16000000, 16200000, 16400000, 16600000]
        
        chart_data = pd.DataFrame({
            'Month': months,
            'Total Assets': values
        })
        st.area_chart(chart_data.set_index('Month'), height=300)
    
    with col2:
        st.markdown("### Savings Distribution")
        if st.session_state.savings_list:
            labels = [savings['name'] for savings in st.session_state.savings_list]
            values = [savings['monthly_amount'] * savings['period'] * 12 for savings in st.session_state.savings_list]
            chart_data = pd.DataFrame({
                'Category': labels,
                'Amount': values
            })
            st.bar_chart(chart_data.set_index('Category'), height=300)
        else:
            st.info("No savings plans yet")
    
    # 빠른 접근
    st.markdown(f"## {get_text('quick_access')}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"💰 {get_text('new_savings')}", use_container_width=True):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col2:
        if st.button(f"📊 {get_text('view_savings')}", use_container_width=True):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col3:
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
        
        # 조정 관리를 위한 별도의 폼
        if 'temp_adjustments' not in st.session_state:
            st.session_state.temp_adjustments = {}
        
        # 기본 정보 입력
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
        
        # 조정 입력
        st.markdown("#### Payment Adjustments")
        st.info("Set different payment amounts for specific months if needed")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            new_month = st.number_input("Month", min_value=1, max_value=36, value=1, key="new_month")
        with col2:
            new_amount = st.number_input("Amount", min_value=0, value=3000, key="new_amount")
        with col3:
            if st.button("➕ Add Adjustment", use_container_width=True):
                st.session_state.temp_adjustments[new_month] = new_amount
                st.success(f"Adjustment for month {new_month} added!")
        
        # 현재 조정 목록 표시
        if st.session_state.temp_adjustments:
            st.markdown("**Current Adjustments:**")
            for month, amount in st.session_state.temp_adjustments.items():
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📅 Month {month}: ¥{amount:,}")
                with col2:
                    st.write(f"⚡ Default: ¥{monthly_amount:,}")
                with col3:
                    if st.button(f"🗑️", key=f"remove_{month}"):
                        del st.session_state.temp_adjustments[month]
                        st.rerun()
        
        # 최종 생성 버튼
        if st.button("🚀 Create Savings Plan", use_container_width=True, type="primary"):
            adjustments = st.session_state.temp_adjustments.copy()
            
            # 적금 계산
            calculation = calculate_savings_schedule(
                monthly_amount, 
                period, 
                interest_rate, 
                start_date, 
                adjustments
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
                'adjustments': adjustments,
                'calculation': calculation,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.savings_list.append(new_savings)
            # 임시 데이터 초기화
            st.session_state.temp_adjustments = {}
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
                    
                    # 기본 정보 - 이중 언어 표기
                    st.markdown("#### Basic Information / 基本情報")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Customer Name</span><span class="bilingual-jp">顧客名</span></div>', unsafe_allow_html=True)
                        st.write(savings['customer_name'])
                    with col2:
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Employee Number</span><span class="bilingual-jp">社員番号</span></div>', unsafe_allow_html=True)
                        st.write(savings['employee_number'])
                    with col3:
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Account Number</span><span class="bilingual-jp">口座番号</span></div>', unsafe_allow_html=True)
                        st.write(savings['account_number'])
                    with col4:
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Start Date</span><span class="bilingual-jp">開始日</span></div>', unsafe_allow_html=True)
                        st.write(savings['start_date'])
                    
                    # 적금 정보 - 이중 언어 표기
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Monthly Amount</span><span class="bilingual-jp">月間積立額</span></div>', unsafe_allow_html=True)
                        st.write(f"¥{savings['monthly_amount']:,.0f}")
                    with col2:
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Period</span><span class="bilingual-jp">積立期間</span></div>', unsafe_allow_html=True)
                        st.write(f"{savings['period']} years / {savings['period']}年")
                    with col3:
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Interest Rate</span><span class="bilingual-jp">年利率</span></div>', unsafe_allow_html=True)
                        st.write(f"{savings['interest_rate']}%")
                    with col4:
                        completion = savings['calculation']['completion_rate']
                        st.markdown('<div class="bilingual"><span class="bilingual-en">Completion Rate</span><span class="bilingual-jp">進捗率</span></div>', unsafe_allow_html=True)
                        st.write(f"{completion:.1f}%")
                    
                    # 계산 결과 - 이중 언어 표기
                    calc = savings['calculation']
                    st.markdown("#### Calculation Results / 計算結果")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Payment / 総支払額", f"¥{calc['total_payment']:,.0f}")
                    with col2:
                        st.metric("Total Interest / 総利息", f"¥{calc['total_interest']:,.0f}")
                    with col3:
                        st.metric("Final Balance / 最終残高", f"¥{calc['final_balance']:,.0f}")
                    with col4:
                        st.metric("Total Months / 総月数", f"{calc['total_months']}")
                    
                    # 입금 스케줄 - 이중 언어 표기
                    st.markdown("#### Payment Schedule / 入金スケジュール")
                    schedule_data = []
                    for item in savings['calculation']['schedule'][:12]:  # 처음 12개만 표시
                        schedule_data.append({
                            'Month/回': item['Month'],
                            'Date/日付': item['Payment Date'],
                            'Amount/金額': f"¥{item['Payment Amount']:,.0f}",
                            'Interest/利息': f"¥{item['Interest']:,.0f}",
                            'Balance/残高': f"¥{item['Total Balance']:,.0f}",
                            'Status/状態': f"{item['Status']} / {item['Status_JP']}",
                            'Note/備考': item['Note']
                        })
                    
                    schedule_df = pd.DataFrame(schedule_data)
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
                    
                    # 삭제 버튼
                    if st.button(f"🗑️ Delete / 削除", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()

# 급여 명세서 페이지
def render_payroll():
    st.markdown("## Payroll Management / 給与明細管理")
    
    # 캡처 방지 배너 - 일본어로 표시
    st.markdown(f'<div class="no-capture">{LANGUAGES["JP"]["no_capture_jp"]}</div>', unsafe_allow_html=True)
    
    with st.form("payroll_form"):
        st.subheader("Payroll Information / 給与情報")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Income Details / 支給内訳")
            basic_salary = st.number_input("Basic Salary / 基本給", value=300000, step=10000, key="basic_salary")
            overtime_pay = st.number_input("Overtime Pay / 残業代", value=50000, step=5000, key="overtime_pay")
        
        with col2:
            st.markdown("#### Deduction Details / 控除内訳")
            income_tax = st.number_input("Income Tax / 所得税", value=25000, step=1000, key="income_tax")
            residence_tax = st.number_input("Residence Tax / 住民税", value=15000, step=1000, key="residence_tax")
            health_insurance = st.number_input("Health Insurance / 健康保険", value=20000, step=1000, key="health_insurance")
            pension = st.number_input("Pension / 厚生年金", value=30000, step=1000, key="pension")
            employment_insurance = st.number_input("Employment Insurance / 雇用保険", value=5000, step=1000, key="employment_insurance")
            other_deduction = st.number_input("Other Deduction / 控除額", value=10000, step=1000, key="other_deduction")
            payslip_date = st.date_input("Payslip Date / 給与日", datetime.now().date(), key="payslip_date")
        
        if st.form_submit_button("📄 Generate Payslip / 明細発行", use_container_width=True, type="primary"):
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
            st.success("🎉 Payslip generated successfully! / 給与明細が作成されました！")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Income / 総支給額", f"¥{salary_data['total_income']:,.0f}")
            with col2:
                st.metric("Total Deduction / 総控除額", f"¥{salary_data['total_deductions']:,.0f}")
            with col3:
                st.metric("Net Salary / 差引支給額", f"¥{salary_data['net_salary']:,.0f}")
            
            # 상세 내역 - 이중 언어 표기
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("##### Income Breakdown / 支給内訳詳細")
                for item_key, item_data in salary_data['income_breakdown'].items():
                    st.markdown(f'<div class="bilingual"><span class="bilingual-en">{item_data["en"]}: ¥{item_data["amount"]:,.0f}</span><span class="bilingual-jp">{item_data["jp"]}</span></div>', unsafe_allow_html=True)
            
            with col2:
                st.markdown("##### Deduction Breakdown / 控除内訳詳細")
                for item_key, item_data in salary_data['deduction_breakdown'].items():
                    st.markdown(f'<div class="bilingual"><span class="bilingual-en">{item_data["en"]}: ¥{item_data["amount"]:,.0f}</span><span class="bilingual-jp">{item_data["jp"]}</span></div>', unsafe_allow_html=True)

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
    
    if not st.session_state.logged_in:
        login()
    else:
        # 헤더
        st.markdown(f"""
        <div class="bank-header">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h1 class="bank-title">{get_text('title')}</h1>
                    <p class="bank-subtitle">{get_text('subtitle')}</p>
                    <p style="margin: 0; opacity: 0.9;">
                        {get_text('welcome').format(st.session_state.user_data['name'])} | 
                        {get_text('account_number')}: {st.session_state.user_data['account']}
                    </p>
                </div>
                <div style="display: flex; gap: 10px;">
                    {render_language_switcher()}
                    {render_logout()}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 네비게이션
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        render_nav()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 페이지 내용
        if st.session_state.current_page == 'home':
            render_home()
        elif st.session_state.current_page == 'savings':
            render_savings()
        elif st.session_state.current_page == 'payroll':
            render_payroll()

if __name__ == "__main__":
    main()