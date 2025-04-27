import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="JP Bank - 적금 관리 시스템",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS 스타일링
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nanum+Gothic:wght@400;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nanum Gothic', sans-serif;
}

/* 상단 네비게이션 바 */
.stApp header {
    background: #2E3B4E;
    color: white !important;
    padding: 1rem 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

/* 입력 섹션 스타일 */
.input-section {
    background: #F8F9FA;
    border-radius: 15px;
    padding: 2rem;
    margin: 2rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
}

/* 정보 표시 카드 */
.info-card {
    background: white;
    border-radius: 15px;
    padding: 2rem;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    border-left: 4px solid #2E3B4E;
}

/* 테이블 스타일 */
table.dataframe {
    width: 100%;
    border-collapse: collapse;
    margin: 1rem 0;
}

table.dataframe th {
    background: #2E3B4E !important;
    color: white !important;
    font-weight: 700;
}

table.dataframe td, table.dataframe th {
    padding: 1rem !important;
    text-align: center !important;
}

/* 버튼 스타일 */
.stButton>button {
    background: #2E3B4E !important;
    color: white !important;
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    transition: all 0.3s;
}

.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# 입력 폼 섹션
with st.container():
    st.header("🎯 적금 계좌 신규 등록")
    with st.form("savings_form"):
        cols = st.columns([1,1,2,1])
        with cols[0]: name = st.text_input("고객명", placeholder="홍길동")
        with cols[1]: emp_num = st.text_input("사원번호", placeholder="12345678")
        with cols[2]: account = st.text_input("계좌번호", placeholder="098-96586-6521")
        with cols[3]: start_date = st.date_input("적금 시작일", datetime(2025,2,25))

        cols2 = st.columns([1,1,1,1])
        with cols2[0]: unit_price = st.number_input("1구좌당 가격 (¥)", min_value=1000, step=100, value=1100)
        with cols2[1]: units = st.number_input("신청구좌 수", min_value=1, max_value=10, step=1, value=4)
        with cols2[2]: years = st.selectbox("만기기간", [1,2,3,5], index=2)
        with cols2[3]: interest = st.number_input("연이자율 (%)", min_value=0.0, max_value=15.0, value=10.03, step=0.01)

        if st.form_submit_button("💾 저장하기", use_container_width=True):
            st.session_state.saved_data = True

# 저장된 데이터 표시
if 'saved_data' in st.session_state:
    # 회원 정보 계산
    maturity_date = start_date + timedelta(days=365*years)
    monthly_deposit = unit_price * units
    inquiry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 회원 정보 표시
    with st.container():
        st.header("📋 회원 정보")
        info_cols = st.columns([1,1,1,1])
        info_cols[0].metric("고객명", name)
        info_cols[1].metric("사원번호", emp_num)
        info_cols[2].metric("계좌번호", account)
        info_cols[3].metric("조회일시", inquiry_time)
        
        st.divider()
        
        # 적금 정보 테이블
        savings_info = pd.DataFrame({
            "적금 시작일": [start_date.strftime("%Y-%m-%d")],
            "만기 예정일": [maturity_date.strftime("%Y-%m-%d")],
            "월 입금액": [f"¥{monthly_deposit:,}"],
            "총 적금액": [f"¥{(monthly_deposit * years*12):,}"],
            "예상 만기수령액": [f"¥{int(monthly_deposit * years*12 * (1 + interest/100)):,}"]
        }).T.reset_index()
        
        st.table(savings_info.style.set_properties(**{
            'font-size': '16px',
            'text-align': 'center',
            'background-color': '#F8F9FA'
        }))

    # 입금 내역 생성
    st.header("📅 입금 내역")
    deposit_data = []
    current_balance = 0
    
    for i in range(1, years*12 +1):
        deposit_date = start_date + timedelta(days=30*(i-1))
        current_balance += monthly_deposit
        monthly_interest = current_balance * (interest/100)/12
        
        deposit_data.append([
            f"{i}회차 ({deposit_date.strftime('%y.%m.%d')})",
            f"¥{monthly_deposit:,}",
            f"¥{current_balance:,}",
            f"¥{monthly_interest:,.1f}",
            "✅ 입금완료" if deposit_date < datetime.now() else "⏳ 대기중"
        ])
    
    # 테이블 표시
    df = pd.DataFrame(deposit_data, columns=[
        "회차별 안내", "입금액", "잔액", "예상이자", "입금확인"
    ]).set_index("회차별 안내")
    
    st.dataframe(df, use_container_width=True, height=600)
    
    # 액션 버튼
    btn_cols = st.columns([1,1,1,5])
    btn_cols[0].button("🚫 해지하기", use_container_width=True)
    btn_cols[1].button("🔄 구좌 변경", use_container_width=True)
    btn_cols[2].button("💸 분할납부", use_container_width=True)