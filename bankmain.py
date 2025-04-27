import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링
st.markdown("""
<style>
:root {
    --primary: #2B4A6F;
    --secondary: #3D6B9E;
    --accent: #FF6B6B;
    --background: #f8fafc;
    --card: #FFFFFF;
}

.stApp {
    background: var(--background);
    font-family: 'Noto Sans JP', sans-serif;
}

.dashboard-header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white !important;
    padding: 2rem;
    border-radius: 12px;
    margin: 2rem 0;
    text-align: center;
}

.info-card {
    background: var(--card);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    border: 1px solid #e2e8f0;
    transition: transform 0.3s;
}

.info-card:hover {
    transform: translateY(-3px);
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1.5rem;
    margin: 1.5rem 0;
}

.metric-card {
    background: var(--card);
    border-radius: 12px;
    padding: 1.2rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
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

.highlight-value {
    color: var(--accent);
    font-weight: 700;
}

.stButton>button {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
}

.stDataFrame {
    border: 1px solid #e2e8f0 !important;
    border-radius: 12px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
}

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap');
</style>
""", unsafe_allow_html=True)

# 로그인 시스템
def login():
    with st.container():
        st.markdown("""
        <div class='dashboard-header'>
            <h1 style='margin:0;'>🏦 大塚商会ローン</h1>
            <p style='color:#e2e8f0;margin:0;'>Otsuka Shokai Loan Management System</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                user_id = st.text_input("ログインID")
                password = st.text_input("パスワード", type="password")
                if st.form_submit_button("🔑 ログイン"):
                    if user_id == "sgms" and password == "qwer1234":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("認証に失敗しました")

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

# 메인 페이지
def main():
    st.markdown("""
    <div class='dashboard-header'>
        <h3 style='margin:0;'>積立貯蓄管理システム</h3>
    </div>
    """, unsafe_allow_html=True)

    # 1. 적금 계좌 등록
    with st.expander("📝 積立口座新規登録", expanded=True):
        with st.form("savings_form"):
            cols = st.columns([1,1,2,1])
            name = cols[0].text_input("顧客名", placeholder="홍길동")
            emp_num = cols[1].text_input("社員番号", placeholder="12345678")
            account = cols[2].text_input("口座番号", placeholder="098-96586-6521")
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

    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        calc = calculate_savings(data)
        
        # 2. 적금 조정
        with st.expander("⚙️ 積立条件調整", expanded=True):
            with st.form("adjust_form"):
                cols = st.columns([2,3,1])
                adjust_month = cols[0].number_input("調整対象回", min_value=1, value=1)
                new_units = cols[1].number_input("新規口座数", 
                    min_value=data['original_units']//2, 
                    max_value=data['original_units'], 
                    value=data['original_units']//2)
                if cols[2].form_submit_button("適用"):
                    data['adjustments'].append({
                        "month": adjust_month,
                        "new_units": new_units
                    })
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
            <div class='info-card'>
                <div style='color:#64748b;'>{icon} {title}</div>
                <div style='font-size:1.2rem;font-weight:600;margin-top:0.5rem;'>{value}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 4. 주요 지표
        st.markdown("### 📊 積立概要")
        st.markdown(f"""
        <div class='metric-grid'>
            <div class='metric-card'>
                <div class='metric-title'>月々積立額</div>
                <div class='metric-value'>¥{calc['monthly']:,}</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>総積立回数</div>
                <div class='metric-value'>{calc['total_months']}回</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>総積立額</div>
                <div class='metric-value'>¥{calc['total_payment']:,}</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>予想利息</div>
                <div class='metric-value'>¥{calc['total_interest']:,.1f}</div>
            </div>
            <div class='metric-card'>
                <div class='metric-title'>年利率</div>
                <div class='highlight-value'>{calc['interest_rate']}%</div>
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

if not st.session_state.logged_in:
    login()
else:
    main()