import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링
st.markdown("""
<style>
:root {
    --primary: #0056a6;
    --secondary: #003366;
    --accent: #e31937;
    --background: #f5f7fa;
    --surface: #ffffff;
    --on-surface: #333333;
    --divider: #e0e0e0;
}

.stApp {
    background: var(--background);
    font-family: 'Noto Sans JP', sans-serif;
}

/* 은행 스타일의 헤더 */
.bank-header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white !important;
    padding: 1.5rem;
    margin: -1rem -1rem 1.5rem -1rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

/* 네비게이션 바 */
.nav-container {
    background: var(--surface);
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    padding: 0.5rem 1rem;
    margin: -1rem -1rem 2rem -1rem;
    display: flex;
    gap: 1rem;
    overflow-x: auto;
    white-space: nowrap;
}

.nav-item {
    color: var(--on-surface);
    font-weight: 500;
    padding: 0.75rem 1.5rem;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
    display: inline-block;
    min-width: max-content;
}

.nav-item.active {
    background: rgba(0, 86, 166, 0.1);
    color: var(--primary);
    font-weight: 600;
}

.nav-item:hover:not(.active) {
    background: rgba(0,0,0,0.05);
}

/* 대시보드 스타일 */
.dashboard-header {
    padding: 1.5rem;
    background: var(--surface);
    border-radius: 8px;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.asset-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin: 1.5rem 0;
}

.asset-card {
    background: var(--surface);
    padding: 1.25rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid var(--divider);
}

.asset-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
    margin: 0.5rem 0;
}

/* 급여 명세서 스타일 */
.paystub-container {
    background: var(--surface);
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid var(--divider);
}

.paystub-header {
    border-bottom: 2px solid var(--divider);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}

.section-title {
    color: var(--primary);
    font-size: 1.1rem;
    font-weight: 600;
    margin: 1.5rem 0 0.5rem 0;
}

.amount-row {
    display: flex;
    justify-content: space-between;
    padding: 0.75rem 0;
    border-bottom: 1px solid var(--divider);
}

.total-row {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--primary);
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 2px solid var(--divider);
}

/* 적금 관리 스타일 */
.savings-card {
    background: var(--surface);
    border-radius: 8px;
    padding: 1.25rem;
    margin: 1rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid var(--divider);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: var(--surface);
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    border: 1px solid var(--divider);
    text-align: center;
}

.metric-title {
    color: #666;
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary);
}

/* 버튼 스타일 */
.stButton>button {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
    font-weight: 500 !important;
    transition: all 0.2s !important;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
}

/* 입력 폼 스타일 */
.stTextInput>div>div>input,
.stNumberInput>div>div>input,
.stDateInput>div>div>input,
.stSelectbox>div>div>select {
    border: 1px solid var(--divider) !important;
    border-radius: 6px !important;
    padding: 0.5rem 1rem !important;
}

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
</style>
""", unsafe_allow_html=True)

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

# ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼
# 수정된 부분: st.session_state.user_data를 USER_DATA 변수에 할당
USER_DATA = st.session_state.user_data
# ▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲▲

# 급여명세서 데이터 구조
DEFAULT_PAYSLIP = {
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

# 로그인 시스템
def login():
    st.markdown("""
    <div class="bank-header">
        <h1 style="margin:0; text-align:center">大塚銀行 従業員ポータル</h1>
        <p style="margin:0; text-align:center; opacity:0.9">Otsuka Bank Employee Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            user_id = st.text_input("ログインID")
            password = st.text_input("パスワード", type="password")
            
            # 제출 버튼 추가
            if st.form_submit_button("ログイン", use_container_width=True):
                if user_id == "otsuka" and password == "bank1234":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("ログインIDまたはパスワードが正しくありません")

# 네비게이션 바
def render_nav():
    current_page = st.query_params.get("page", "home")
    
    cols = st.columns([1,1,1,3])
    with cols[0]:
        if st.button("🏠 ホーム",
                     use_container_width=True,
                     type="primary" if current_page == "home" else "secondary"):
            st.query_params.page = "home"
            st.rerun()
    with cols[1]:
        if st.button("💰 ローン管理",
                     use_container_width=True,
                     type="primary" if current_page == "loan" else "secondary"):
            st.query_params.page = "loan"
            st.rerun()
    with cols[2]:
        if st.button("📄 給与明細",
                     use_container_width=True,
                     type="primary" if current_page == "payroll" else "secondary"):
            st.query_params.page = "payroll"
            st.rerun()
    
    st.markdown("---")


# 자산 현황 대시보드
def render_dashboard():
    st.markdown(f"""
    <div class="dashboard-header">
        <div style="display:flex; align-items:center; gap:1.5rem">
            <div>
                <h2 style="margin:0">ようこそ、{st.session_state.user_data['name']}様</h2>
                <p style="color:#666">{st.session_state.user_data['department']} | 最終ログイン: {datetime.now().strftime('%Y/%m/%d %H:%M')}</p>
            </div>
            <div style="margin-left:auto; text-align:right">
                <p style="margin:0; color:#666">口座番号</p>
                <h3 style="margin:0">{st.session_state.user_data['account']}</h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 資産概要")
    with st.container():
        st.markdown("""
        <div class="asset-grid">
            <div class="asset-card">
                <div style="color:#666">💰 総資産</div>
                <div class="asset-value">¥{total:,}</div>
                <div style="color:#666">前月比 +1.2%</div>
            </div>
            <div class="asset-card">
                <div style="color:#666">🏦 普通預金</div>
                <div class="asset-value">¥{deposits:,}</div>
                <div style="color:#666">定期預金 ¥5,000,000</div>
            </div>
            <div class="asset-card">
                <div style="color:#666">🏠 ローン残高</div>
                <div class="asset-value">¥{loans:,}</div>
                <div style="color:#666">次回返済日 2025/03/25</div>
            </div>
            <div class="asset-card">
                <div style="color:#666">📈 投資資産</div>
                <div class="asset-value">¥{investments:,}</div>
                <div style="color:#666">前月比 +3.4%</div>
            </div>
        </div>
        """.format(**USER_DATA['assets']), unsafe_allow_html=True)

    st.markdown("### 最近の取引")
    recent_transactions = [
        ["2025/02/15", "給与振込", "¥340,000", "大塚銀行", "✅ 完了"],
        ["2025/02/10", "家賃支払い", "¥120,000", "SMBCアパート", "✅ 完了"],
        ["2025/02/05", "投資信託購入", "¥50,000", "大塚証券", "✅ 完了"],
        ["2025/02/01", "公共料金", "¥24,500", "東京電力", "✅ 完了"],
    ]
    st.dataframe(
        pd.DataFrame(recent_transactions, columns=["日付", "取引内容", "金額", "取引先", "状態"]),
        use_container_width=True,
        hide_index=True
    )

# 급여 명세서 생성 및 표시
def show_payroll():
    with st.form("payslip_form"):
        st.markdown("#### 支給内訳")
        
        # 기본 지급액
        income_items = []
        income_cols = st.columns([3, 2])
        income_items.append({
            "name": income_cols[0].text_input("基本給", value="基本給"),
            "amount": income_cols[1].number_input("金額 (¥)", value=340000)
        })

        # 추가 지급항목
        for i in range(3):
            cols = st.columns([3, 2])
            name = cols[0].text_input(f"追加項目 {i+1}", key=f"extra_income_{i}")
            amount = cols[1].number_input(f"金額 {i+1}", value=0, key=f"extra_amt_{i}")
            if name and amount > 0:
                income_items.append({"name": name, "amount": amount})

        st.markdown("---")
        st.markdown("#### 控除内訳")

        # 기본 공제항목
        deduction_items = []
        default_deductions = [
            {"name": "所得税", "amount": 26320},
            {"name": "住民税", "amount": 6520},
            {"name": "健康保険", "amount": 8910},
            {"name": "厚生年金", "amount": 29960},
            {"name": "雇用保険", "amount": 4550}
        ]

        for i, item in enumerate(default_deductions):
            cols = st.columns([3, 2])
            item["amount"] = cols[1].number_input(
                item["name"],
                value=item["amount"],
                key=f"ded_{i}"
            )
            deduction_items.append(item)

        # 추가 공제항목
        cols = st.columns([3, 2])
        other_deduction = {
            "name": cols[0].text_input("その他控除名", value="その他控除"),
            "amount": cols[1].number_input("金額", value=70000)
        }
        deduction_items.append(other_deduction)

        # 제출 버튼 추가
        if st.form_submit_button("明細作成", use_container_width=True):
            st.session_state.payslip_data = {
                "income_items": income_items,
                "deduction_items": deduction_items
            }
            st.rerun()

    
    # 생성된 급여명세서 표시
    if st.session_state.payslip_data:
        payslip = st.session_state.payslip_data
        total_income = sum(item["amount"] for item in payslip["income_items"])
        total_deduction = sum(item["amount"] for item in payslip["deduction_items"])
        net_pay = total_income - total_deduction
        
        st.markdown("---")
        st.markdown("### 給与明細書")
        
        with st.container():
            st.markdown("""
            <div class="paystub-container">
                <div class="paystub-header">
                    <h3 style="margin:0">大塚銀行 給与明細書</h3>
                    <div style="display:flex; gap:2rem; color:#666; margin-top:0.5rem">
                        <div>社員番号: {emp_num}</div>
                        <div>発行日: {issue_date}</div>
                        <div>支給日: {pay_date}</div>
                    </div>
                </div>

                <div class="section-title">🔼 支給内訳</div>
                {income_rows}
                <div class="amount-row total-row">
                    <span>総支給額</span>
                    <span>¥{total_income:,}</span>
                </div>

                <div class="section-title">🔽 控除内訳</div>
                {deduction_rows}
                <div class="amount-row total-row">
                    <span>総控除額</span>
                    <span>¥{total_deduction:,}</span>
                </div>

                <div class="amount-row total-row" style="font-size:1.3rem; color:var(--accent);">
                    <span>差引支給額</span>
                    <span>¥{net_pay:,}</span>
                </div>
            </div>
            """.format(
                emp_num=USER_DATA["emp_num"],
                issue_date=datetime.now().strftime('%Y/%m/%d'),
                pay_date=date.today().replace(day=25).strftime('%Y/%m/%d'),
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
                net_pay=net_pay
            ), unsafe_allow_html=True)

# 적금 관리 시스템
def loan_management():
    # 적금 계산 로직이 없으므로 임시 함수를 추가합니다.
    def calculate_savings(data):
        total_months = data['years'] * 12
        maturity_date = (data['start_date'] + relativedelta(years=data['years'])).strftime('%Y/%m/%d')
        monthly_payment = data['unit_price'] * data['current_units']
        total_payment = monthly_payment * total_months
        
        # 간단한 이자 계산 (실제 금융 계산은 더 복잡합니다)
        total_interest = total_payment * (data['interest'] / 100 / 2) * data['years']
        
        records = []
        balance = 0
        for i in range(1, total_months + 1):
            payment_date = (data['start_date'] + relativedelta(months=i-1)).strftime('%Y/%m/%d')
            
            # 조정사항 확인
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
            "total_payment": sum(r[2] for r in records), # 조정된 금액으로 총액 계산
            "total_interest": sum(r[4] for r in records),
            "interest_rate": data['interest'],
            "records": records
        }

    st.markdown("""
    <div style="margin-bottom:2rem">
        <h2>積立貯蓄管理システム</h2>
        <p style="color:#5F6368">Otsuka Shokai Savings Management System</p>
    </div>
    """, unsafe_allow_html=True)

    # 1. 적금 계좌 등록
    with st.expander("📝 積立口座新規登録", expanded=True):
        with st.form("savings_form"):
            cols = st.columns([1,1,2,1])
            name = cols[0].text_input("顧客名", value=USER_DATA['name'])
            emp_num = cols[1].text_input("社員番号", value=USER_DATA['emp_num'])
            account = cols[2].text_input("口座番号", value=USER_DATA['account'])
            start_date = cols[3].date_input("積立開始日", value=date(2025,2,25))
            
            cols2 = st.columns([1,1,1,1])
            unit_price = cols2[0].number_input("1口座金額 (¥)", value=1100, min_value=1000)
            units = cols2[1].number_input("申込口座数", value=4, min_value=1)
            years = cols2[2].selectbox("満期期間 (年)", [1,2,3,5], index=2)
            interest = cols2[3].number_input("年利率 (%)", value=10.03, min_value=0.0)
            
            if st.form_submit_button("💾 登録"):
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
    st.markdown("### 🧑‍💼 基本情報")
    cols = st.columns(4)
    info_items = [
        ("顧客名", data['name'], "👤"),
        ("社員番号", data['emp_num'], "🆔"),
        ("口座番号", data['account'], "💳"),
        ("満期日", calc['maturity_date'], "📅")
    ]
    
    for i, (title, value, icon) in enumerate(info_items):
        cols[i].markdown(f"""
        <div class="savings-card">
            <div style='color:#64748b;'>{icon} {title}</div>
            <div style='font-size:1.2rem;font-weight:600;margin-top:0.5rem;'>{value}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 4. 주요 지표
    st.markdown("### 📊 積立概要")
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-title">月々積立額</div>
            <div class="metric-value">¥{calc['monthly']:,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">総積立回数</div>
            <div class="metric-value">{calc['total_months']}回</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">総積立額</div>
            <div class="metric-value">¥{calc['total_payment']:,}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">予想利息</div>
            <div class="metric-value">¥{calc['total_interest']:,.1f}</div>
        </div>
        <div class="metric-card">
            <div class="metric-title">年利率</div>
            <div style="font-size:1.5rem;font-weight:700;color:var(--accent);">{calc['interest_rate']}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # 5. 입금 내역
    st.markdown("### 📅 入金スケジュール")
    df = pd.DataFrame(calc['records'], columns=[
        "回次", "入金日", "入金額", "累計残高", "利息", "状態", "備考"
    ]).set_index("回次")
    
    st.dataframe(
        df,
        use_container_width=True,
        height=600,
        column_config={
            "入金額": st.column_config.NumberColumn(format="¥%d"),
            "累計残高": st.column_config.NumberColumn(format="¥%d"),
            "利息": st.column_config.NumberColumn(format="¥%.1f")
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