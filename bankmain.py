import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap');

:root {
    --primary: #2E3B4E;
    --secondary: #4E6B8A;
    --accent: #FF6B6B;
    --background: #F5F7FA;
    --card: #FFFFFF;
}

* {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background-color: var(--background);
}

.bank-header {
    background: linear-gradient(135deg, var(--primary), var(--secondary));
    color: white;
    padding: 1.5rem;
    border-radius: 0 0 15px 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    margin-bottom: 2rem;
}

.info-card {
    background: var(--card);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border-left: 5px solid var(--accent);
}

.adjust-section {
    background: var(--card);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.table-container {
    background: var(--card);
    border-radius: 12px;
    padding: 1rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.stButton>button {
    background: linear-gradient(135deg, var(--primary), var(--secondary)) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    font-weight: 500 !important;
    transition: all 0.3s !important;
}

.stButton>button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
}

.metric-box {
    background: var(--card);
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# 로그인 시스템
def login():
    with st.container():
        st.markdown("<div class='bank-header'><h1 style='color:white;text-align:center;'>🏦 JP Bank</h1></div>", unsafe_allow_html=True)
        with st.form("login_form"):
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
                st.image("https://via.placeholder.com/200x50?text=JP+BANK", width=200)
                user_id = st.text_input("아이디", key="user_id")
                password = st.text_input("비밀번호", type="password", key="password")
                if st.form_submit_button("로그인", use_container_width=True):
                    if user_id == "sgms" and password == "qwer1234":
                        st.session_state.logged_in = True
                        st.rerun()
                    else:
                        st.error("잘못된 아이디 또는 비밀번호")

# 메인 페이지
def main():
    # 상단 네비게이션
    st.markdown("""
    <div class='bank-header'>
        <div style="display: flex; justify-content: space-around; padding: 0.5rem 0;">
            <div style="font-weight:700;">🏠 홈</div>
            <div style="font-weight:700;">💰 입금</div>
            <div style="font-weight:700;">💳 출금</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 적금 계좌 등록 폼
    with st.expander("🎯 적금 계좌 신규 등록", expanded=True):
        with st.form("savings_form"):
            cols = st.columns([1,1,2,1])
            with cols[0]: name = st.text_input("고객명", placeholder="홍길동")
            with cols[1]: emp_num = st.text_input("사원번호", placeholder="12345678")
            with cols[2]: account = st.text_input("계좌번호", placeholder="098-96586-6521")
            with cols[3]: start_date = st.date_input("적금 시작일", date(2025,2,25))

            cols2 = st.columns([1,1,1,1])
            with cols2[0]: unit_price = st.number_input("1구좌당 가격 (¥)", min_value=1000, step=100, value=1100)
            with cols2[1]: units = st.number_input("신청구좌 수", min_value=1, max_value=10, step=1, value=4)
            with cols2[2]: years = st.selectbox("만기기간", [1,2,3,5], index=2)
            with cols2[3]: interest = st.number_input("연이자율 (%)", min_value=0.0, max_value=15.0, value=10.03, step=0.01)

            if st.form_submit_button("💾 저장하기", use_container_width=True):
                st.session_state.savings_data = {
                    "name": name, "emp_num": emp_num, "account": account,
                    "start_date": start_date, "unit_price": unit_price,
                    "original_units": units, "current_units": units,
                    "years": years, "interest": interest,
                    "adjustments": [],
                    "extra_payments": []
                }
                st.rerun()

    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        original_monthly = data['unit_price'] * data['original_units']
        maturity_date = data['start_date'] + relativedelta(years=data['years'])
        
        # 1. 납입 조정 섹션 (최상단으로 이동)
        with st.container():
            st.markdown("<div class='adjust-section'><h3>🔧 납입 조정</h3></div>", unsafe_allow_html=True)
            with st.form("adjust_form"):
                cols = st.columns([1,2,1])
                with cols[0]:
                    adjust_month = st.number_input("조정할 회차", min_value=1, step=1)
                with cols[1]:
                    new_amount = st.number_input("조정 금액 (¥)", 
                                               min_value=original_monthly//2,
                                               max_value=original_monthly,
                                               value=original_monthly//2,
                                               step=100)
                with cols[2]:
                    st.write("<div style='height:27px;'></div>", unsafe_allow_html=True)
                    if st.form_submit_button("조정 적용", use_container_width=True):
                        if new_amount < original_monthly:
                            remaining = original_monthly - new_amount
                            data['adjustments'].append({
                                "month": adjust_month,
                                "adjusted_amount": new_amount,
                                "remaining": remaining
                            })
                            data['extra_payments'].append(remaining)
                            st.rerun()

        # 2. 회원 정보 섹션
        with st.container():
            st.markdown("<div class='info-card'><h3>👤 회원 정보</h3></div>", unsafe_allow_html=True)
            info_cols = st.columns([1,1,1,1])
            info_cols[0].metric("고객명", data['name'])
            info_cols[1].metric("사원번호", data['emp_num'])
            info_cols[2].metric("계좌번호", data['account'])
            info_cols[3].metric("만기예정일", maturity_date.strftime('%Y-%m-%d'))

        # 3. 통계 정보 섹션
        deposit_data = []
        current_balance = 0
        total_months = data['years'] * 12 + len(data['extra_payments'])
        base_schedule = [original_monthly] * (data['years'] * 12)
        
        for adj in data['adjustments']:
            if adj["month"]-1 < len(base_schedule):
                base_schedule[adj["month"]-1] = adj["adjusted_amount"]
        
        full_schedule = base_schedule + data['extra_payments']
        
        for idx, amount in enumerate(full_schedule, start=1):
            deposit_date = data['start_date'] + relativedelta(months=idx-1)
            current_balance += amount
            monthly_interest = current_balance * (data['interest']/100)/12
            status = "✅ 입금완료" if deposit_date < datetime.now().date() else "⏳ 대기중"
            note = ""
            
            for adj in data['adjustments']:
                if adj["month"] == idx:
                    note = f"🔻 조정적용 ({adj['adjusted_amount']}¥)"
                elif idx > len(base_schedule):
                    note = "➕ 추가 회차"

            deposit_data.append([
                f"{idx}회차 ({deposit_date.strftime('%y.%m.%d')})",
                f"¥{amount:,}",
                f"¥{current_balance:,}",
                monthly_interest,
                status,
                note
            ])

        total_payment = sum(full_schedule)
        total_interest = sum(row[3] for row in deposit_data)
        
        with st.container():
            cols = st.columns(2)
            with cols[0]:
                st.markdown(f"""
                <div class='metric-box'>
                    <h4>💰 총 납입액</h4>
                    <h2 style='color: var(--primary);'>¥{total_payment:,}</h2>
                </div>
                """, unsafe_allow_html=True)
            with cols[1]:
                st.markdown(f"""
                <div class='metric-box'>
                    <h4>💹 예상 총 이자</h4>
                    <h2 style='color: var(--primary);'>¥{total_interest:,.1f}</h2>
                </div>
                """, unsafe_allow_html=True)

        # 4. 입금 내역 표시
        with st.container():
            st.markdown("<div class='table-container'><h3>📊 입금 내역</h3></div>", unsafe_allow_html=True)
            df = pd.DataFrame(deposit_data, columns=[
                "회차", "입금액", "잔액", "예상이자", "상태", "비고"
            ]).set_index("회차")
            
            display_df = df.copy()
            display_df["예상이자"] = display_df["예상이자"].apply(lambda x: f"¥{x:,.1f}")
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=600,
                column_config={
                    "입금액": st.column_config.NumberColumn(format="¥%d"),
                    "잔액": st.column_config.NumberColumn(format="¥%d")
                }
            )

# 앱 실행
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()