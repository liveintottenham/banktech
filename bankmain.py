import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import streamlit.components.v1 as components

# CSS 스타일링
st.markdown("""
<style>
:root {
    --primary: #1A73E8;
    --secondary: #4285F4;
    --accent: #FF6D00;
    --background: #F8F9FA;
    --surface: #FFFFFF;
    --on-surface: #202124;
    --divider: #DADCE0;
}

.stApp {
    background: var(--background);
    font-family: 'Roboto', sans-serif;
}

/* 네비게이션 바 */
.nav-container {
    background: var(--surface);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    padding: 12px 24px;
    margin: -1rem -1rem 2rem;
    display: flex;
    gap: 32px;
}

.nav-item {
    color: var(--on-surface);
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.nav-item.active {
    background: rgba(26, 115, 232, 0.1);
    color: var(--primary);
}

/* 대시보드 스타일 */
.dashboard-header {
    padding: 2rem;
    background: var(--surface);
    border-radius: 16px;
    margin-bottom: 2rem;
}

.asset-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.asset-card {
    background: var(--surface);
    padding: 1.5rem;
    border-radius: 16px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
}

.asset-value {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--primary);
    margin: 1rem 0;
}

/* 급여 명세서 스타일 */
.paystub-container {
    background: var(--surface);
    border-radius: 16px;
    padding: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
}

.amount-row {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid var(--divider);
}

.total-row {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--primary);
}

/* 적금 관리 스타일 */
.savings-card {
    background: var(--surface);
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1.5rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: var(--surface);
    border-radius: 12px;
    padding: 1.2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
    text-align: center;
}

.metric-title {
    color: #64748b;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--primary);
}

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
</style>
""", unsafe_allow_html=True)

# 사용자 데이터
USER_DATA = {
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

# 적금 계산 함수
def calculate_savings(data):
    original_monthly = data['unit_price'] * data['original_units']
    adjusted_months = data['years'] * 12 + len(data['adjustments'])
    total_payment = original_monthly * data['years'] * 12
    
    balance = 0
    total_interest = 0
    records = []
    
    for i in range(1, adjusted_months + 1):
        current_units = data['original_units']
        for adj in data['adjustments']:
            if adj['month'] == i:
                current_units = adj['new_units']
        
        amount = data['unit_price'] * current_units
        balance += amount
        monthly_interest = balance * (data['interest']/100)/12
        total_interest += monthly_interest
        
        deposit_date = data['start_date'] + relativedelta(months=i-1)
        records.append([
            f"{i}回目",
            deposit_date.strftime('%Y/%m/%d'),
            f"¥{amount:,}",
            f"¥{balance:,}",
            f"¥{monthly_interest:,.1f}",
            "✅ 完了" if deposit_date < datetime.now().date() else "⏳ 予定",
            "🔧 調整" if any(adj['month']==i for adj in data['adjustments']) else ""
        ])
    
    return {
        "monthly": original_monthly,
        "total_months": adjusted_months,
        "total_payment": total_payment,
        "total_interest": total_interest,
        "interest_rate": data['interest'],
        "records": records,
        "maturity_date": (data['start_date'] + relativedelta(years=data['years'])).strftime('%Y-%m-%d')
    }

# 로그인 시스템
def login():
    with st.container():
        st.markdown("""
        <div style='text-align:center; padding:4rem 0'>
            <h1>🏦 大塚商会 ポータル</h1>
            <p style='color:#5F6368'>Otsuka Shokai Employee Portal</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                user_id = st.text_input("ログインID")
                password = st.text_input("パスワード", type="password")
                if st.form_submit_button("ログイン"):
                    if user_id == "sgms" and password == "qwer1234":
                        st.session_state.logged_in = True
                        st.session_state.page = "home"
                        st.rerun()
                    else:
                        st.error("認証に失敗しました")

# 네비게이션 바
def render_nav():
    st.markdown(f"""
    <div class="nav-container">
        <div class="nav-item {'active' if st.session_state.page == 'home' else ''}" 
            onclick="window.streamlitApi.setComponentValue('home')">ホーム</div>
        <div class="nav-item {'active' if st.session_state.page == 'loan' else ''}" 
            onclick="window.streamlitApi.setComponentValue('loan')">ローン管理</div>
        <div class="nav-item {'active' if st.session_state.page == 'payroll' else ''}" 
            onclick="window.streamlitApi.setComponentValue('payroll')">給与明細</div>
    </div>
    """, unsafe_allow_html=True)

# 자산 현황 대시보드
def render_dashboard():
    st.markdown(f"""
    <div class="dashboard-header">
        <div style="display:flex; align-items:center; gap:2rem">
            <div>
                <h2 style="margin:0">ようこそ、{USER_DATA['name']}様</h2>
                <p style="color:#5F6368">{USER_DATA['department']} | 最終ログイン: {datetime.now().strftime('%Y/%m/%d %H:%M')}</p>
            </div>
            <div style="margin-left:auto; text-align:right">
                <p style="margin:0; color:#5F6368">口座番号</p>
                <h3 style="margin:0">{USER_DATA['account']}</h3>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 資産概要")
    with st.container():
        st.markdown("""
        <div class="asset-grid">
            <div class="asset-card">
                <div style="color:#5F6368">💰 総資産</div>
                <div class="asset-value">¥{total:,}</div>
                <div style="color:#5F6368">前月比 +1.2%</div>
            </div>
            <div class="asset-card">
                <div style="color:#5F6368">🏦 普通預金</div>
                <div class="asset-value">¥{deposits:,}</div>
                <div style="color:#5F6368">定期預金 ¥5,000,000</div>
            </div>
            <div class="asset-card">
                <div style="color:#5F6368">🏠 ローン残高</div>
                <div class="asset-value">¥{loans:,}</div>
                <div style="color:#5F6368">次回返済日 2025/03/25</div>
            </div>
            <div class="asset-card">
                <div style="color:#5F6368">📈 投資資産</div>
                <div class="asset-value">¥{investments:,}</div>
                <div style="color:#5F6368">前月比 +3.4%</div>
            </div>
            <div class="asset-card">
                <div style="color:#5F6368">🎯 積立預金</div>
                <div class="asset-value">¥{savings:,}</div>
                <div style="color:#5F6368">満期予定 2027/05/20</div>
            </div>
        </div>
        """.format(**USER_DATA['assets']), unsafe_allow_html=True)

    st.markdown("### 最近の取引")
    recent_transactions = [
        ["2025/02/15", "給与振込", "¥340,000", "三菱UFJ銀行", "✅ 完了"],
        ["2025/02/10", "家賃支払い", "¥120,000", "SMBCアパート", "✅ 完了"],
        ["2025/02/05", "投資信託購入", "¥50,000", "SBI証券", "✅ 完了"],
        ["2025/02/01", "公共料金", "¥24,500", "東京電力", "✅ 完了"],
    ]
    st.dataframe(
        pd.DataFrame(recent_transactions, columns=["日付", "取引内容", "金額", "取引先", "状態"]),
        use_container_width=True,
        hide_index=True
    )

# 급여 명세서
def show_payroll():
    payroll_data = {
        "income": {
            "基本給": 340000,
            "職務手当": 50000,
            "通勤手当": 15000,
            "住宅手当": 20000
        },
        "deductions": {
            "所得税": 26320,
            "住民税": 6520,
            "健康保険": 8910,
            "厚生年金": 29960,
            "雇用保険": 4550,
            "その他控除": 70000
        }
    }

    total_income = sum(payroll_data['income'].values())
    total_deductions = sum(payroll_data['deductions'].values())
    net_pay = total_income - total_deductions

    with st.container():
        st.markdown(f"""
        <div class="paystub-container">
            <div style="border-bottom:2px solid var(--divider); padding-bottom:1rem; margin-bottom:2rem">
                <h2 style="margin:0">🏦 大塚商会 給与明細書</h2>
                <div style="display:flex; gap:2rem; color:#5F6368; margin-top:1rem">
                    <div>社員番号: {USER_DATA['emp_num']}</div>
                    <div>発行日: {datetime.now().strftime('%Y/%m/%d')}</div>
                    <div>支給日: 2025/02/25</div>
                </div>
            </div>

            <div style="margin:2rem 0">
                <h3 style="color:var(--primary); margin-bottom:1rem">🔼 支給内訳</h3>
                {"".join([f"""
                <div class="amount-row">
                    <span>{name}</span>
                    <span>¥{value:,}</span>
                </div>
                """ for name, value in payroll_data['income'].items()])}
                <div class="amount-row total-row">
                    <span>総支給額</span>
                    <span>¥{total_income:,}</span>
                </div>
            </div>

            <div style="margin:2rem 0">
                <h3 style="color:var(--primary); margin-bottom:1rem">🔽 控除内訳</h3>
                {"".join([f"""
                <div class="amount-row">
                    <span>{name}</span>
                    <span>¥{value:,}</span>
                </div>
                """ for name, value in payroll_data['deductions'].items()])}
                <div class="amount-row total-row">
                    <span>総控除額</span>
                    <span>¥{total_deductions:,}</span>
                </div>
            </div>

            <div style="margin-top:3rem">
                <div class="amount-row total-row">
                    <span>差引支給額</span>
                    <span>¥{net_pay:,}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# 적금 관리 시스템
def loan_management():
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
    st.markdown("### 🧑💼 基本情報")
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

# 앱 실행
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'home'

if not st.session_state.logged_in:
    login()
else:
    render_nav()
    
    if st.session_state.page == 'home':
        render_dashboard()
    elif st.session_state.page == 'loan':
        loan_management()
    elif st.session_state.page == 'payroll':
        show_payroll()

# 네비게이션 핸들링
components.html(
    """
    <script>
    window.streamlitApi = {
        setComponentValue: function(value) {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue',
                api: 'component_123',
                componentValue: value
            }, '*');
        }
    }
    </script>
    """, 
    height=0
)

nav_event = st.session_state.get('component_123')
if nav_event:
    st.session_state.page = nav_event
    st.rerun()