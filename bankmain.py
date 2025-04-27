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
    --background: #F5F7FA;
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

.compact-table {
    background: var(--card);
    border-radius: 8px;
    padding: 0.5rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
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

.summary-item {
    text-align: center;
    padding: 0.5rem;
    border-right: 1px solid #eee;
}
.summary-item:last-child { border-right: none; }

.logo-header {
    text-align: center;
    margin: 2rem 0;
    font-size: 1.8rem;
    color: var(--primary);
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# 로그인 시스템
def login():
    with st.container():
        st.markdown("""
        <div class='logo-header'>
            <div>大塚商会Loan</div>
            <div style="margin-top:1rem;">
                <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-briefcase">
                    <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
                    <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
                </svg>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            col1, col2, col3 = st.columns([1,2,1])
            with col2:
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
    # 상단 로고
    st.markdown("<div class='logo-header'>大塚商会Loan</div>", unsafe_allow_html=True)
    
    # 적금 계좌 등록 폼 (이전과 동일)
    # ... [적금 계좌 등록 코드 생략] ...

    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        original_monthly = data['unit_price'] * data['original_units']
        maturity_date = data['start_date'] + relativedelta(years=data['years'])
        
        # 1. 납입 조정 섹션 (이전과 동일)
        # ... [납입 조정 코드 생략] ...

        # 2. 회원 정보 (컴팩트 버전)
        with st.container():
            cols = st.columns(4)
            cols[0].markdown(f"<div class='info-card'>**고객명**<br>{data['name']}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div class='info-card'>**사원번호**<br>{data['emp_num']}</div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div class='info-card'>**계좌번호**<br>{data['account']}</div>", unsafe_allow_html=True)
            cols[3].markdown(f"<div class='info-card'>**적금 시작일**<br>{data['start_date'].strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)

        # 3. 요약 정보 그리드
        total_payment = sum(full_schedule)
        total_interest = sum(row[3] for row in deposit_data)
        
        st.markdown("""
        <div class='summary-grid'>
            <div class='summary-item'>
                <div>입금금액</div>
                <div style='font-size:1.2rem;color:var(--primary);'>¥{}</div>
            </div>
            <div class='summary-item'>
                <div>만기예정일</div>
                <div style='font-size:1.2rem;color:var(--primary);'>{}</div>
            </div>
            <div class='summary-item'>
                <div>총 납입액</div>
                <div style='font-size:1.2rem;color:var(--primary);'>¥{:,.0f}</div>
            </div>
            <div class='summary-item'>
                <div>예상이자</div>
                <div style='font-size:1.2rem;color:var(--primary);'>¥{:,.1f}</div>
            </div>
        </div>
        """.format(
            original_monthly,
            maturity_date.strftime('%Y-%m-%d'),
            total_payment,
            total_interest
        ), unsafe_allow_html=True)

        # 4. 입금 내역 테이블 (컴팩트 버전)
        with st.container():
            st.markdown("<div class='compact-table'>", unsafe_allow_html=True)
            df = pd.DataFrame(deposit_data, columns=[
                "회차", "입금액", "잔액", "예상이자", "상태", "비고"
            ]).set_index("회차")
            
            display_df = df.copy()
            display_df["예상이자"] = display_df["예상이자"].apply(lambda x: f"¥{x:,.1f}")
            
            st.dataframe(
                display_df,
                use_container_width=True,
                height=400,
                column_config={
                    "입금액": st.column_config.NumberColumn(format="¥%d"),
                    "잔액": st.column_config.NumberColumn(format="¥%d")
                }
            )
            st.markdown("</div>", unsafe_allow_html=True)

# 앱 실행
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()