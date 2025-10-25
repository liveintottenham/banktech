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
        st.session_state.language = 'JP'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
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
    'JP': {
        'title': '大塚銀行 従業員ポータル',
        'subtitle': 'Otsuka Bank Employee Portal',
        'login_id': 'ログインID',
        'password': 'パスワード',
        'login': 'ログイン',
        'login_error': 'ログインIDまたはパスワードが正しくありません',
        'home': '🏠 ホーム',
        'savings': '💰 積立管理',
        'payroll': '📄 給与明細',
        'welcome': 'ようこそ、{}様',
        'last_login': '最終ログイン',
        'account_number': '口座番号',
        'asset_overview': '資産概要',
        'total_savings': '総積立額',
        'active_plans': '実行中プラン',
        'monthly_payment': '月間支払額',
        'recent_transactions': '最近の取引',
        'quick_access': 'クイックアクセス',
        'new_savings': '新規積立作成',
        'savings_calc': '積立計算機',
        'view_savings': '積立一覧',
        'date': '日付',
        'description': '説明',
        'amount': '金額',
        'status': '状態',
        'savings_management': '積立貯蓄管理',
        'savings_name': '積立名',
        'target_amount': '目標金額',
        'monthly_amount': '月間積立額',
        'period': '積立期間',
        'start_date': '開始日',
        'interest_rate': '年利率',
        'calculate': '計算',
        'create_plan': 'プラン作成',
        'savings_details': '積立詳細',
        'total_months': '総期間',
        'total_payment': '総支払額',
        'final_amount': '満期金額',
        'expected_interest': '予想利息',
        'payment_schedule': '支払いスケジュール',
        'payroll_management': '給与明細管理',
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
        'logout': 'ログアウト'
    },
    'KR': {
        'title': '오츠카 은행 직원 포털',
        'subtitle': 'Otsuka Bank Employee Portal',
        'login_id': '로그인 ID',
        'password': '비밀번호',
        'login': '로그인',
        'login_error': '로그인 ID 또는 비밀번호가 올바르지 않습니다',
        'home': '🏠 홈',
        'savings': '💰 적금 관리',
        'payroll': '📄 급여 명세서',
        'welcome': '{}님, 환영합니다',
        'last_login': '최종 로그인',
        'account_number': '계좌번호',
        'asset_overview': '자산 현황',
        'total_savings': '총 적금액',
        'active_plans': '진행 중인 플랜',
        'monthly_payment': '월 납입액',
        'recent_transactions': '최근 거래',
        'quick_access': '빠른 접근',
        'new_savings': '새 적금 만들기',
        'savings_calc': '적금 계산기',
        'view_savings': '적금 목록',
        'date': '날짜',
        'description': '설명',
        'amount': '금액',
        'status': '상태',
        'savings_management': '적금 관리',
        'savings_name': '적금 이름',
        'target_amount': '목표 금액',
        'monthly_amount': '월 납입액',
        'period': '적금 기간',
        'start_date': '시작일',
        'interest_rate': '연이율',
        'calculate': '계산하기',
        'create_plan': '플랜 생성',
        'savings_details': '적금 상세',
        'total_months': '총 기간',
        'total_payment': '총 납입액',
        'final_amount': '만기 금액',
        'expected_interest': '예상 이자',
        'payment_schedule': '납입 일정',
        'payroll_management': '급여 명세서 관리',
        'basic_salary': '기본급',
        'overtime_pay': '초과근무수당',
        'bonus': '상여금',
        'allowances': '기타 수당',
        'insurance': '사회보험료',
        'tax': '세금',
        'other_deductions': '기타 공제',
        'net_salary': '실 수령액',
        'generate_payslip': '명세서 생성',
        'payslip_date': '급여일',
        'income_items': '지급 내역',
        'deduction_items': '공제 내역',
        'logout': '로그아웃'
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language][key]

# CSS 스타일링
def load_css():
    css = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Noto Sans JP', 'Malgun Gothic', sans-serif;
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        margin: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        min-height: calc(100vh - 40px);
    }
    
    .bank-header {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: white;
        padding: 2rem 3rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .bank-title {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .nav-container {
        background: white;
        border-radius: 15px;
        padding: 1rem 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        display: flex;
        gap: 1rem;
    }
    
    .nav-btn {
        flex: 1;
        padding: 1rem 1.5rem;
        border: none;
        border-radius: 10px;
        background: transparent;
        color: #666;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .nav-btn.active {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border: 1px solid rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 적금 계산 함수
def calculate_savings_plan(monthly_amount, period_years, interest_rate, start_date):
    total_months = period_years * 12
    monthly_rate = interest_rate / 100 / 12
    
    schedule = []
    current_balance = 0
    
    for month in range(1, total_months + 1):
        payment_date = start_date + relativedelta(months=month-1)
        
        # 이자 계산
        interest = current_balance * monthly_rate
        current_balance += monthly_amount + interest
        
        schedule.append({
            'month': month,
            'date': payment_date.strftime('%Y/%m/%d'),
            'payment': monthly_amount,
            'interest': interest,
            'balance': current_balance,
            'status': '予定' if payment_date > datetime.now().date() else '完了'
        })
    
    total_payment = monthly_amount * total_months
    total_interest = current_balance - total_payment
    
    return {
        'schedule': schedule,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'final_balance': current_balance,
        'total_months': total_months
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
            '基本給': basic_salary,
            '時間外手当': overtime_pay,
            'ボーナス': bonus,
            'その他手当': allowances
        },
        'deduction_breakdown': {
            '社会保険料': insurance,
            '税金': tax,
            'その他控除': other_deductions
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
    
    total_savings = sum(savings['monthly_amount'] * savings['period'] * 12 for savings in st.session_state.savings_list)
    monthly_payment = sum(savings['monthly_amount'] for savings in st.session_state.savings_list)
    active_plans = len(st.session_state.savings_list)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('total_savings')}</div>
            <div style="font-size: 2rem; font-weight: 800;">¥{total_savings:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('monthly_payment')}</div>
            <div style="font-size: 2rem; font-weight: 800;">¥{monthly_payment:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('active_plans')}</div>
            <div style="font-size: 2rem; font-weight: 800;">{active_plans}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 빠른 접근
    st.markdown(f"## {get_text('quick_access')}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button(f"📈 {get_text('new_savings')}", use_container_width=True, height=100):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col2:
        if st.button(f"🧮 {get_text('savings_calc')}", use_container_width=True, height=100):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col3:
        if st.button(f"📋 {get_text('view_savings')}", use_container_width=True, height=100):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    # 최근 적금 플랜
    if st.session_state.savings_list:
        st.markdown(f"## {get_text('active_plans')}")
        for savings in st.session_state.savings_list[-3:]:  # 최근 3개만 표시
            with st.container():
                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    st.write(f"**{savings['name']}**")
                    st.write(f"월 ¥{savings['monthly_amount']:,.0f} · {savings['period']}년")
                with col2:
                    st.write(f"총 ¥{savings['monthly_amount'] * savings['period'] * 12:,.0f}")
                with col3:
                    st.write(f"시작: {savings['start_date']}")

# 적금 관리 페이지
def render_savings():
    st.markdown(f"## {get_text('savings_management')}")
    
    tab1, tab2, tab3 = st.tabs(["新規積立作成", "積立計算機", "積立一覧"])
    
    with tab1:
        st.subheader("新規積立プラン作成")
        
        with st.form("new_savings_plan"):
            col1, col2 = st.columns(2)
            
            with col1:
                savings_name = st.text_input(get_text('savings_name'), "マイ積立プラン")
                monthly_amount = st.number_input(get_text('monthly_amount'), min_value=1000, value=50000, step=1000)
                period = st.selectbox(get_text('period'), [1, 2, 3, 5, 10], index=2)
            
            with col2:
                start_date = st.date_input(get_text('start_date'), datetime.now().date())
                interest_rate = st.number_input(get_text('interest_rate'), min_value=0.0, value=2.5, step=0.1)
                target_amount = st.number_input(get_text('target_amount'), min_value=0, value=0)
            
            if st.form_submit_button(get_text('create_plan')):
                # 적금 계산
                calculation = calculate_savings_plan(monthly_amount, period, interest_rate, start_date)
                
                # 새로운 적금 플랜 생성
                new_savings = {
                    'id': len(st.session_state.savings_list) + 1,
                    'name': savings_name,
                    'monthly_amount': monthly_amount,
                    'period': period,
                    'start_date': start_date.strftime('%Y/%m/%d'),
                    'interest_rate': interest_rate,
                    'target_amount': target_amount,
                    'calculation': calculation,
                    'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
                }
                
                st.session_state.savings_list.append(new_savings)
                st.success(f"積立プラン '{savings_name}' が作成されました！")
                st.rerun()
    
    with tab2:
        st.subheader("積立計算機")
        
        col1, col2 = st.columns(2)
        
        with col1:
            calc_monthly = st.number_input("月間積立額", min_value=1000, value=50000, step=1000, key="calc_monthly")
            calc_period = st.selectbox("積立期間", [1, 2, 3, 5, 10], index=2, key="calc_period")
        
        with col2:
            calc_interest = st.number_input("年利率 (%)", min_value=0.0, value=2.5, step=0.1, key="calc_interest")
            calc_start = st.date_input("開始日", datetime.now().date(), key="calc_start")
        
        if st.button(get_text('calculate')):
            result = calculate_savings_plan(calc_monthly, calc_period, calc_interest, calc_start)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("総支払額", f"¥{result['total_payment']:,.0f}")
            with col2:
                st.metric("予想利息", f"¥{result['total_interest']:,.0f}")
            with col3:
                st.metric("満期金額", f"¥{result['final_balance']:,.0f}")
            with col4:
                st.metric("総期間", f"{result['total_months']}ヶ月")
            
            # 상세 스케줄
            st.subheader("支払いスケジュール (最初の12ヶ月)")
            schedule_df = pd.DataFrame(result['schedule'][:12])
            st.dataframe(schedule_df, use_container_width=True)
    
    with tab3:
        st.subheader("積立プラン一覧")
        
        if not st.session_state.savings_list:
            st.info("登録されている積立プランがありません。")
        else:
            for savings in st.session_state.savings_list:
                with st.expander(f"{savings['name']} - ¥{savings['monthly_amount']:,.0f}/月", expanded=False):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write("**月間積立額**")
                        st.write(f"¥{savings['monthly_amount']:,.0f}")
                    
                    with col2:
                        st.write("**積立期間**")
                        st.write(f"{savings['period']}年")
                    
                    with col3:
                        st.write("**開始日**")
                        st.write(savings['start_date'])
                    
                    with col4:
                        st.write("**年利率**")
                        st.write(f"{savings['interest_rate']}%")
                    
                    # 계산 결과 표시
                    calc = savings['calculation']
                    st.write("**計算結果**")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("総支払額", f"¥{calc['total_payment']:,.0f}")
                    with col2:
                        st.metric("予想利息", f"¥{calc['total_interest']:,.0f}")
                    with col3:
                        st.metric("満期金額", f"¥{calc['final_balance']:,.0f}")
                    
                    # 삭제 버튼
                    if st.button(f"削除", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()

# 급여 명세서 페이지
def render_payroll():
    st.markdown(f"## {get_text('payroll_management')}")
    
    with st.form("payroll_form"):
        st.subheader("給与情報入力")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 支給内訳")
            basic_salary = st.number_input(get_text('basic_salary'), value=300000, step=10000)
            overtime_pay = st.number_input(get_text('overtime_pay'), value=50000, step=5000)
            bonus = st.number_input(get_text('bonus'), value=0, step=10000)
            allowances = st.number_input(get_text('allowances'), value=15000, step=1000)
        
        with col2:
            st.markdown("#### 控除内訳")
            insurance = st.number_input(get_text('insurance'), value=45000, step=1000)
            tax = st.number_input(get_text('tax'), value=35000, step=1000)
            other_deductions = st.number_input(get_text('other_deductions'), value=10000, step=1000)
            payslip_date = st.date_input(get_text('payslip_date'), datetime.now().date())
        
        if st.form_submit_button(get_text('generate_payslip')):
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
            st.success("給与明細が作成されました！")
            
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
                for item, amount in salary_data['income_breakdown'].items():
                    st.write(f"{item}: ¥{amount:,.0f}")
            
            with col2:
                st.markdown("##### 控除内訳詳細")
                for item, amount in salary_data['deduction_breakdown'].items():
                    st.write(f"{item}: ¥{amount:,.0f}")
    
    # 저장된 급여 명세서 목록
    if st.session_state.payroll_list:
        st.markdown("## 保存された給与明細")
        for payslip in st.session_state.payroll_list[-5:]:  # 최근 5개만 표시
            with st.expander(f"給与明細 - {payslip['date']}", expanded=False):
                data = payslip['salary_data']
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("総支給額", f"¥{data['total_income']:,.0f}")
                with col2:
                    st.metric("総控除額", f"¥{data['total_deductions']:,.0f}")
                with col3:
                    st.metric("差引支給額", f"¥{data['net_salary']:,.0f}")

# 로그인 페이지
def login():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown(f"""
        <div class="bank-header">
            <h1 class="bank-title">{get_text('title')}</h1>
            <p class="bank-subtitle">{get_text('subtitle')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            st.subheader("ログイン")
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
    
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        login()
    else:
        # 헤더
        st.markdown(f"""
        <div class="bank-header">
            <div style="display: flex; justify-content: between; align-items: start;">
                <div>
                    <h1 class="bank-title">{get_text('title')}</h1>
                    <p class="bank-subtitle">{get_text('subtitle')}</p>
                    <p style="margin: 0; opacity: 0.9;">
                        {get_text('welcome').format(st.session_state.user_data['name'])} | 
                        {get_text('account_number')}: {st.session_state.user_data['account']}
                    </p>
                </div>
                <div style="margin-left: auto;">
                    {render_language_switcher()}
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
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_language_switcher():
    current_lang = st.session_state.language
    if current_lang == 'JP':
        if st.button("🇰🇷 한국어", key="lang_switch"):
            st.session_state.language = 'KR'
            st.rerun()
    else:
        if st.button("🇯🇵 日本語", key="lang_switch"):
            st.session_state.language = 'JP'
            st.rerun()
    return ""

def render_logout():
    if st.button(get_text('logout'), key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()
    return ""

if __name__ == "__main__":
    main()