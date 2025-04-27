import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링 (간소화)
st.markdown("""
<style>
:root {
    --primary: #2B4A6F;
    --secondary: #3D6B9E;
    --card: #FFFFFF;
}

.info-card {
    background: var(--card);
    border-radius: 8px;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    border-left: 3px solid var(--primary);
}

.summary-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin: 1rem 0;
    background: var(--card);
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.logo-header {
    text-align: center;
    margin: 1rem 0;
    font-size: 1.8rem;
    color: var(--primary);
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# 로그인 시스템
def login():
    st.markdown("""
    <div class='logo-header'>
        大塚商会Loan<br>
        <span style='font-size:1rem;color:#666;'>Otsuka Shokai Loan Service</span>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        if st.form_submit_button("로그인"):
            if user_id == "sgms" and password == "qwer1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("로그인 실패")

# 메인 페이지
def main():
    st.markdown("<div class='logo-header'>大塚商会Loan</div>", unsafe_allow_html=True)
    
    # 1. 적금 등록 폼
    with st.expander("🎯 적금 계좌 등록", expanded=True):
        with st.form("savings_form"):
            name = st.text_input("고객명", value="홍길동")
            emp_num = st.text_input("사원번호", value="12345678")
            account = st.text_input("계좌번호", value="098-96586-6521")
            start_date = st.date_input("적금 시작일", value=date(2025,2,25))
            
            unit_price = st.number_input("1구좌당 가격 (¥)", value=1100, min_value=1000)
            units = st.number_input("구좌 수", value=4, min_value=1)
            years = st.selectbox("만기기간(년)", [1,2,3,5], index=2)
            interest = st.number_input("연이자율(%)", value=10.03, min_value=0.0)
            
            if st.form_submit_button("저장하기"):
                st.session_state.savings_data = {
                    "name": name, "emp_num": emp_num, "account": account,
                    "start_date": start_date, "unit_price": unit_price,
                    "units": units, "years": years, "interest": interest
                }
                st.rerun()

    # 2. 저장된 데이터 표시
    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        monthly = data['unit_price'] * data['units']
        maturity = data['start_date'] + relativedelta(years=data['years'])
        
        # 회원 정보 카드
        cols = st.columns(4)
        cols[0].markdown(f"<div class='info-card'>**고객명**<br>{data['name']}</div>", unsafe_allow_html=True)
        cols[1].markdown(f"<div class='info-card'>**계좌번호**<br>{data['account']}</div>", unsafe_allow_html=True)
        cols[2].markdown(f"<div class='info-card'>**월 납입액**<br>¥{monthly:,}</div>", unsafe_allow_html=True)
        cols[3].markdown(f"<div class='info-card'>**만기일**<br>{maturity.strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)
        
        # 요약 그리드
        st.markdown("""
        <div class='summary-grid'>
            <div style='text-align:center;'>
                <div>입금금액</div>
                <div style='font-size:1.2rem;color:var(--primary);'>¥{:,}</div>
            </div>
            <div style='text-align:center;'>
                <div>만기예정일</div>
                <div style='font-size:1.2rem;color:var(--primary);'>{}</div>
            </div>
            <div style='text-align:center;'>
                <div>총 납입액</div>
                <div style='font-size:1.2rem;color:var(--primary);'>¥{:,}</div>
            </div>
            <div style='text-align:center;'>
                <div>예상이자</div>
                <div style='font-size:1.2rem;color:var(--primary);'>¥{:,.1f}</div>
            </div>
        </div>
        """.format(
            monthly,
            maturity.strftime('%Y-%m-%d'),
            monthly * data['years'] * 12,
            monthly * data['years'] * 12 * (data['interest']/100)
        ), unsafe_allow_html=True)
        
        # 입금 내역
        st.subheader("📊 입금 내역")
        records = []
        balance = 0
        for i in range(1, data['years']*12 + 1):
            deposit_date = data['start_date'] + relativedelta(months=i-1)
            balance += monthly
            interest_amt = balance * (data['interest']/100)/12
            records.append([
                f"{i}회차 ({deposit_date.strftime('%y.%m.%d')})",
                f"¥{monthly:,}",
                f"¥{balance:,}",
                f"¥{interest_amt:,.1f}",
                "✅ 완료" if deposit_date < datetime.now().date() else "⏳ 대기"
            ])
        
        df = pd.DataFrame(records, columns=["회차", "입금액", "잔액", "이자", "상태"])
        st.dataframe(df.set_index("회차"), use_container_width=True)

# 앱 실행
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()