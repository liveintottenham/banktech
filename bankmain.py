import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링
st.markdown("""
<style>
:root {
    --primary: #1a237e;
    --secondary: #283593;
    --accent: #e53935;
    --background: #f8f9fa;
    --surface: #ffffff;
    --on-surface: #2c3e50;
    --divider: #e0e0e0;
    --success: #2e7d32;
    --warning: #f57c00;
}

.stApp {
    background: var(--background);
    font-family: 'Noto Sans JP', 'Malgun Gothic', sans-serif;
}

/* 은행 스타일의 헤더 */
.bank-header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white !important;
    padding: 2rem 1.5rem;
    margin: -1rem -1rem 2rem -1rem;
    box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    border-bottom: 4px solid var(--accent);
}

.bank-title {
    font-size: 2.2rem !important;
    font-weight: 700 !important;
    margin-bottom: 0.5rem !important;
    text-align: center;
}

.bank-subtitle {
    font-size: 1.1rem !important;
    opacity: 0.9;
    text-align: center;
    margin-bottom: 1rem !important;
}

/* 언어 선택기 */
.language-switcher {
    position: absolute;
    top: 1rem;
    right: 1rem;
}

/* 네비게이션 바 */
.nav-container {
    background: var(--surface);
    box-shadow: 0 2px 12px rgba(0,0,0,0.08);
    padding: 0;
    margin: -1rem -1rem 2.5rem -1rem;
    display: flex;
    justify-content: center;
    border-bottom: 1px solid var(--divider);
}

.nav-item {
    color: var(--on-surface);
    font-weight: 500;
    padding: 1.2rem 2rem;
    cursor: pointer;
    transition: all 0.3s ease;
    border-bottom: 3px solid transparent;
    text-decoration: none;
    display: inline-block;
    min-width: 140px;
    text-align: center;
}

.nav-item.active {
    background: rgba(26, 35, 126, 0.05);
    color: var(--primary);
    font-weight: 600;
    border-bottom: 3px solid var(--accent);
}

.nav-item:hover:not(.active) {
    background: rgba(26, 35, 126, 0.02);
    border-bottom: 3px solid rgba(26, 35, 126, 0.3);
}

/* 대시보드 스타일 */
.dashboard-header {
    padding: 2rem;
    background: var(--surface);
    border-radius: 12px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid var(--divider);
}

.welcome-section {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1rem;
}

.asset-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.asset-card {
    background: var(--surface);
    padding: 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid var(--divider);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.asset-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}

.asset-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary);
    margin: 0.75rem 0;
}

.asset-change {
    font-size: 0.9rem;
    font-weight: 500;
}

.change-positive {
    color: var(--success);
}

.change-negative {
    color: var(--accent);
}

/* 급여 명세서 스타일 */
.paystub-container {
    background: var(--surface);
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid var(--divider);
}

.paystub-header {
    border-bottom: 3px solid var(--divider);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
    text-align: center;
}

.section-title {
    color: var(--primary);
    font-size: 1.2rem;
    font-weight: 600;
    margin: 2rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--divider);
}

.amount-row {
    display: flex;
    justify-content: space-between;
    padding: 1rem 0;
    border-bottom: 1px solid var(--divider);
    align-items: center;
}

.amount-row:last-child {
    border-bottom: none;
}

.total-row {
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--primary);
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 3px solid var(--divider);
}

.net-pay-row {
    font-size: 1.5rem;
    font-weight: 800;
    color: var(--accent) !important;
    background: rgba(229, 57, 53, 0.05);
    padding: 1.5rem;
    border-radius: 8px;
    margin-top: 2rem;
}

/* 적금 관리 스타일 */
.savings-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid var(--divider);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.metric-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
    border: 1px solid var(--divider);
    text-align: center;
    transition: transform 0.2s ease;
}

.metric-card:hover {
    transform: translateY(-2px);
}

.metric-title {
    color: #666;
    font-size: 0.9rem;
    margin-bottom: 0.75rem;
    font-weight: 500;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

/* 버튼 스타일 */
.stButton>button {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 8px rgba(26, 35, 126, 0.2) !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 12px rgba(26, 35, 126, 0.3) !important;
}

/* 입력 폼 스타일 */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stDateInput>div>div>input,
.stSelectbox>div>div>select {
    border: 1px solid var(--divider) !important;
    border-radius: 8px !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
}

.stTextInput>div>div>input:focus,
.stNumberInput>div>div>input:focus,
.stDateInput>div>div>input:focus,
.stSelectbox>div>div>select:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 0 2px rgba(26, 35, 126, 0.1) !important;
}

/* 데이터프레임 스타일 */
.dataframe {
    border-radius: 8px !important;
    overflow: hidden !important;
}

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Malgun+Gothic:wght@400;500;600;700&display=swap');
</style>
""", unsafe_allow_html=True)

# 다국어 지원
if 'language' not in st.session_state:
    st.session_state.language = 'JP'  # 기본값: 일본어

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
        'total_assets': '💰 総資産',
        'deposits': '🏦 普通預金',
        'loans': '🏠 ローン残高',
        'investments': '📈 投資資産',
        'recent_transactions': '最近の取引',
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
        'basic_info': '🧑‍💼 基本情報',
        'maturity_date': '満期日',
        'savings_overview': '📊 積立概要',
        'monthly_payment': '月々積立額',
        'total_months': '総積立回数',
        'total_savings': '総積立額',
        'estimated_interest': '予想利息',
        'payment_schedule': '📅 入金スケジュール',
        'payment_date': '入金日',
        'payment_amount': '入金額',
        'cumulative_balance': '累計残高',
        'interest': '利息',
        'notes': '備考'
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
        'total_assets': '💰 총 자산',
        'deposits': '🏦 보통예금',
        'loans': '🏠 대출 잔액',
        'investments': '📈 투자 자산',
        'recent_transactions': '최근 거래 내역',
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
        'basic_info': '🧑‍💼 기본 정보',
        'maturity_date': '만기일',
        'savings_overview': '📊 적금 개요',
        'monthly_payment': '월 납입액',
        'total_months': '총 납입 횟수',
        'total_savings': '총 적금액',
        'estimated_interest': '예상 이자',
        'payment_schedule': '📅 납입 일정',
        'payment_date': '납입일',
        'payment_amount': '납입액',
        'cumulative_balance': '누적 잔액',
        'interest': '이자',
        'notes': '비고'
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language][key]

# 사용자 데이터 및 초기 설정
if 'user_data' not in st.session_state:
    st.session_state.user_data = {
        "name": "山田 太郎",
        "assets": {
            "total": 15480230,
            "deposits": 12045000,
            "loans": 2560000,
            "investments": 875230,
            "savings": 3500000
        },
        "account": "098-96586-6521",
        "emp_num": "12345678",
        "department": "IT事業部"
    }

if 'payslip_data' not in st.session_state:
    st.session_state.payslip_data = {
        "income_items": [
            {"name": "基本給", "amount": 340000}
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

USER_DATA = st.session_state.user_data

# 로그인 시스템
def login():
    st.markdown(f"""
    <div class="bank-header">
        <div class="language-switcher">
            {render_language_switcher()}
        </div>
        <h1 class="bank-title">{get_text('title')}</h1>
        <p class="bank-subtitle">{get_text('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            user_id = st.text_input(get_text('login_id'))
            password = st.text_input(get_text('password'), type="password")
            
            if st.form_submit_button(get_text('login'), use_container_width=True):
                if user_id == "otsuka" and password == "bank1234":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error(get_text('login_error'))

def render_language_switcher():
    current_lang = st.session_state.language
    if current_lang == 'JP':
        if st.button("한국어", key="lang_switch"):
            st.session_state.language = 'KR'
            st.rerun()
    else:
        if st.button("日本語", key="lang_switch"):
            st.session_state.language = 'JP'
            st.rerun()
    return ""

# 네비게이션 바
def render_nav():
    current_page = st.query_params.get("page", "home")
    
    st.markdown("""
    <div class="nav-container">
        <a class="nav-item %s" href="?page=home">%s</a>
        <a class="nav-item %s" href="?page=loan">%s</a>
        <a class="nav-item %s" href="?page=payroll">%s</a>
    </div>
    """ % (
        "active" if current_page == "home" else "", get_text('home'),
        "active" if current_page == "loan" else "", get_text('loan'),
        "active" if current_page == "payroll" else "", get_text('payroll')
    ), unsafe_allow_html=True)

# 자산 현황 대시보드
def render_dashboard():
    st.markdown(f"""
    <div class="dashboard-header">
        <div class="welcome-section">
            <div>
                <h2 style="margin:0">{get_text('welcome').format(USER_DATA['name'])}</h2>
                <p style="color:#666">{USER_DATA['department']} | {get_text('last_login')}: {datetime.now().strftime('%Y/%m/%d %H:%M')}</p>
            </div>
            <div style="margin-left:auto; text-align:right">
                <p style="margin:0; color:#666">{get_text('account_number')}</p>
                <h3 style="margin:0">{USER_DATA['account']}</h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"### {get_text('asset_overview')}")
    with st.container():
        st.markdown("""
        <div class="asset-grid">
            <div class="asset-card">
                <div style="color:#666">%s</div>
                <div class="asset-value">¥{total:,}</div>
                <div class="asset-change change-positive">前月比 +1.2%%</div>
            </div>
            <div class="asset-card">
                <div style="color:#666">%s</div>
                <div class="asset-value">¥{deposits:,}</div>
                <div style="color:#666">定期預金 ¥5,000,000</div>
            </div>
            <div class="asset-card">
                <div style="color:#666">%s</div>
                <div class="asset-value">¥{loans:,}</div>
                <div style="color:#666">次回返済日 2025/03/25</div>
            </div>
            <div class="asset-card">
                <div style="color:#666">%s</div>
                <div class="asset-value">¥{investments:,}</div>
                <div class="asset-change change-positive">前月比 +3.4%%</div>
            </div>
        </div>
        """ % (get_text('total_assets'), get_text('deposits'), get_text('loans'), get_text('investments'))
        .format(**USER_DATA['assets']), unsafe_allow_html=True)

    st.markdown(f"### {get_text('recent_transactions')}")
    recent_transactions = [
        ["2025/02/15", "給与振込", "¥340,000", "大塚銀行", "✅ 完了"],
        ["2025/02/10", "家賃支払い", "¥120,000", "SMBCアパート", "✅ 完了"],
        ["2025/02/05", "投資信託購入", "¥50,000", "大塚証券", "✅ 完了"],
        ["2025/02/01", "公共料金", "¥24,500", "東京電力", "✅ 完了"],
    ]
    
    df_columns = [get_text('date'), get_text('description'), get_text('amount'), get_text('counterparty'), get_text('status')]
    st.dataframe(
        pd.DataFrame(recent_transactions, columns=df_columns),
        use_container_width=True,
        hide_index=True
    )

# 급여 명세서 생성 및 표시
def show_payroll():
    st.markdown(f"### {get_text('payslip_title')}")
    
    with st.form("payslip_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {get_text('income_breakdown')}")
            base_salary = st.number_input(get_text('basic_salary'), value=340000, step=10000)
            
            st.markdown("**追加支給項目**")
            extra_income_1 = st.number_input("役職手当", value=50000, step=5000)
            extra_income_2 = st.number_input("時間外手当", value=25000, step=5000)
            extra_income_3 = st.number_input("交通費", value=15000, step=1000)
            
        with col2:
            st.markdown(f"#### {get_text('deduction_breakdown')}")
            income_tax = st.number_input("所得税", value=26320, step=1000)
            residence_tax = st.number_input("住民税", value=6520, step=500)
            health_insurance = st.number_input("健康保険", value=8910, step=500)
            pension = st.number_input("厚生年金", value=29960, step=1000)
            employment_insurance = st.number_input("雇用保険", value=4550, step=500)
            other_deductions = st.number_input("その他控除", value=70000, step=5000)

        if st.form_submit_button(get_text('create_payslip'), use_container_width=True):
            st.session_state.payslip_data = {
                "income_items": [
                    {"name": get_text('basic_salary'), "amount": base_salary},
                    {"name": "役職手当", "amount": extra_income_1},
                    {"name": "時間外手当", "amount": extra_income_2},
                    {"name": "交通費", "amount": extra_income_3}
                ],
                "deduction_items": [
                    {"name": "所得税", "amount": income_tax},
                    {"name": "住民税", "amount": residence_tax},
                    {"name": "健康保険", "amount": health_insurance},
                    {"name": "厚生年金", "amount": pension},
                    {"name": "雇用保険", "amount": employment_insurance},
                    {"name": "その他控除", "amount": other_deductions}
                ]
            }
            st.rerun()
    
    # 생성된 급여명세서 표시
    if st.session_state.payslip_data:
        payslip = st.session_state.payslip_data
        total_income = sum(item["amount"] for item in payslip["income_items"])
        total_deduction = sum(item["amount"] for item in payslip["deduction_items"])
        net_pay = total_income - total_deduction
        
        st.markdown("---")
        
        with st.container():
            st.markdown("""
            <div class="paystub-container">
                <div class="paystub-header">
                    <h3 style="margin:0">大塚銀行 給与明細書</h3>
                    <div style="display:flex; justify-content:center; gap:3rem; color:#666; margin-top:1rem">
                        <div>社員番号: {emp_num}</div>
                        <div>発行日: {issue_date}</div>
                        <div>支給日: {pay_date}</div>
                    </div>
                </div>

                <div class="section-title">🔼 {income_title}</div>
                {income_rows}
                <div class="amount-row total-row">
                    <span>{total_income_text}</span>
                    <span>¥{total_income:,}</span>
                </div>

                <div class="section-title">🔽 {deduction_title}</div>
                {deduction_rows}
                <div class="amount-row total-row">
                    <span>{total_deduction_text}</span>
                    <span>¥{total_deduction:,}</span>
                </div>

                <div class="amount-row net-pay-row">
                    <span>{net_pay_text}</span>
                    <span>¥{net_pay:,}</span>
                </div>
            </div>
            """.format(
                emp_num=USER_DATA["emp_num"],
                issue_date=datetime.now().strftime('%Y/%m/%d'),
                pay_date=date.today().replace(day=25).strftime('%Y/%m/%d'),
                income_title=get_text('income_breakdown'),
                deduction_title=get_text('deduction_breakdown'),
                income_rows="".join([
                    f'<div class="amount-row"><span>{item["name"]}</span><span>¥{item["amount"]:,}</span></div>'
                    for item in payslip["income_items"]
                ]),
                deduction_rows="".join([
                    f'<div class="amount-row"><span>{item["name"]}</span><span>¥{item["amount"]:,}</span></div>'
                    for item in payslip["deduction_items"]
                ]),
                total_income=total_income,
                total_deduction=total_deduction,
                net_pay=net_pay,
                total_income_text=get_text('total_income'),
                total_deduction_text=get_text('total_deduction'),
                net_pay_text=get_text('net_pay')
            ), unsafe_allow_html=True)

# 적금 관리 시스템
def loan_management():
    def calculate_savings(data):
        total_months = data['years'] * 12
        maturity_date = (data['start_date'] + relativedelta(years=data['years'])).strftime('%Y/%m/%d')
        monthly_payment = data['unit_price'] * data['current_units']
        total_payment = monthly_payment * total_months
        
        # 간단한 이자 계산
        total_interest = total_payment * (data['interest'] / 100 / 2) * data['years']
        
        records = []
        balance = 0
        for i in range(1, total_months + 1):
            payment_date = (data['start_date'] + relativedelta(months=i-1)).strftime('%Y/%m/%d')
            
            current_payment = monthly_payment
            note = ""
            for adj in data.get('adjustments', []):
                if adj['month'] == i:
                    current_payment = data['unit_price'] * adj['new_units']
                    note = f"口座数変更: {adj['new_units']}"
                    break
            
            balance += current_payment
            interest_for_month = balance * (data['interest'] / 100 / 12)
            records.append([
                i,
                payment_date,
                current_payment,
                balance,
                interest_for_month,
                "予定" if date.today() < (data['start_date'] + relativedelta(months=i-1)) else "完了",
                note
            ])
            
        return {
            "total_months": total_months,
            "maturity_date": maturity_date,
            "monthly": monthly_payment,
            "total_payment": sum(r[2] for r in records),
            "total_interest": sum(r[4] for r in records),
            "interest_rate": data['interest'],
            "records": records
        }

    st.markdown(f"""
    <div style="margin-bottom:2rem">
        <h2>{get_text('savings_management')}</h2>
        <p style="color:#5F6368">{get_text('savings_subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. 적금 계좌 등록
    with st.expander("📝 積立口座新規登録", expanded=True):
        with st.form("savings_form"):
            cols = st.columns([1,1,2,1])
            name = cols[0].text_input(get_text('customer_name'), value=USER_DATA['name'])
            emp_num = cols[1].text_input(get_text('employee_number'), value=USER_DATA['emp_num'])
            account = cols[2].text_input(get_text('account_number'), value=USER_DATA['account'])
            start_date = cols[3].date_input(get_text('start_date'), value=date(2025,2,25))
            
            cols2 = st.columns([1,1,1,1])
            unit_price = cols2[0].number_input(get_text('unit_price'), value=1100, min_value=1000)
            units = cols2[1].number_input(get_text('units'), value=4, min_value=1)
            years = cols2[2].selectbox(get_text('years'), [1,2,3,5], index=2)
            interest = cols2[3].number_input(get_text('interest_rate'), value=10.03, min_value=0.0)
            
            if st.form_submit_button(get_text('register')):
                st.session_state.savings_data = {
                    "name": name, "emp_num": emp_num, "account": account,
                    "start_date": start_date, "unit_price": unit_price,
                    "original_units": units, "current_units": units,
                    "years": years, "interest": interest,
                    "adjustments": []
                }
                st.success("積立口座が登録されました")

    if 'savings_data' not in st.session_state:
        st.session_state.savings_data = {
            "name": USER_DATA['name'],
            "emp_num": USER_DATA['emp_num'],
            "account": USER_DATA['account'],
            "start_date": date(2025,2,25),
            "unit_price": 1100,
            "original_units": 4,
            "current_units": 4,
            "years": 3,
            "interest": 10.03,
            "adjustments": []
        }

    data = st.session_state.savings_data
    calc = calculate_savings(data)
    
    # 2. 적금 조정
    with st.expander("⚙️ 積立条件調整", expanded=True):
        with st.form("adjust_form"):
            cols = st.columns([2,3,1])
            adjust_month = cols[0].number_input("調整対象回", min_value=1, max_value=calc['total_months'], value=1)
            new_units = cols[1].number_input("新規口座数",
                min_value=1,
                max_value=data['original_units']*2,
                value=data['original_units']//2)
            if cols[2].form_submit_button("適用"):
                data['adjustments'].append({
                    "month": adjust_month,
                    "new_units": new_units
                })
                st.success(f"{adjust_month}回目の積立金額を調整しました")
                st.rerun()
    
    # 3. 고객 정보
    st.markdown(f"### {get_text('basic_info')}")
    cols = st.columns(4)
    info_items = [
        (get_text('customer_name'), data['name'], "👤"),
        (get_text('employee_number'), data['emp_num'], "🆔"),
        (get_text('account_number'), data['account'], "💳"),
        (get_text('maturity_date'), calc['maturity_date'], "📅")
    ]
    
    for i, (title, value, icon) in enumerate(info_items):
        cols[i].markdown(f"""
        <div class="savings-card">
            <div style='color:#64748b;'>{icon} {title}</div>
            <div style='font-size:1.2rem;font-weight:600;margin-top:0.5rem;'>{value}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 4. 주요 지표
    st.markdown(f"### {get_text('savings_overview')}")
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-title">{get_text('monthly_payment')}</div>
            <div class="metric-value">¥{calc['monthly']:,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">{get_text('total_months')}</div>
            <div class="metric-value">{calc['total_months']}回</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">{get_text('total_savings')}</div>
            <div class="metric-value">¥{calc['total_payment']:,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">{get_text('estimated_interest')}</div>
            <div class="metric-value">¥{calc['total_interest']:,.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">{get_text('interest_rate')}</div>
            <div style="font-size:1.5rem;font-weight:700;color:var(--accent);">{calc['interest_rate']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 5. 입금 내역
    st.markdown(f"### {get_text('payment_schedule')}")
    df_columns = ["回次", get_text('payment_date'), get_text('payment_amount'), 
                 get_text('cumulative_balance'), get_text('interest'), "状態", get_text('notes')]
    df = pd.DataFrame(calc['records'], columns=df_columns).set_index("回次")
    
    st.dataframe(
        df,
        use_container_width=True,
        height=600,
        column_config={
            get_text('payment_amount'): st.column_config.NumberColumn(format="¥%d"),
            get_text('cumulative_balance'): st.column_config.NumberColumn(format="¥%d"),
            get_text('interest'): st.column_config.NumberColumn(format="¥%.1f")
        }
    )

# 앱 실행 로직
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    render_nav()
    
    current_page = st.query_params.get("page", "home")
    if current_page == 'home':
        render_dashboard()
    elif current_page == 'loan':
        loan_management()
    elif current_page == 'payroll':
        show_payroll()