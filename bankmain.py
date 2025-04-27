import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# 로그인 시스템
def login():
    st.title("🏦 JP Bank - 로그인")
    with st.form("login_form"):
        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        if st.form_submit_button("로그인"):
            if user_id == "sgms" and password == "qwer1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("잘못된 아이디 또는 비밀번호")

# 상단 메뉴 바 (수정된 버전)
def show_menu():
    st.markdown("""
    <style>
    .menu {
        display: flex;
        justify-content: space-around;
        padding: 10px;
        background: #f0f2f6;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .menu a {
        color: black;
        text-decoration: none;
        font-weight: bold;
    }
    </style>
    <div class="menu">
        <a href="#">🏠 홈</a>
        <a href="#">💰 입금</a>
        <a href="#">💳 출금</a>
    </div>
    """, unsafe_allow_html=True)

# 메인 페이지
def main():
    show_menu()  # 수정된 메뉴 표시
    
    st.title("📈 적금 관리 시스템")
    
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

            if st.form_submit_button("💾 저장하기"):
                st.session_state.savings_data = {
                    "name": name, "emp_num": emp_num, "account": account,
                    "start_date": start_date, "unit_price": unit_price,
                    "original_units": units, "current_units": units,
                    "years": years, "interest": interest,
                    "adjustments": []
                }
                st.rerun()

    # 저장된 데이터 표시
    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        monthly_deposit = data['unit_price'] * data['current_units']
        maturity_date = data['start_date'] + relativedelta(years=data['years'])
        
        # 회원 정보 표시
        st.header("👤 회원 정보")
        info_cols = st.columns([1,1,1,1])
        info_cols[0].metric("고객명", data['name'])
        info_cols[1].metric("사원번호", data['emp_num'])
        info_cols[2].metric("계좌번호", data['account'])
        info_cols[3].metric("조회일시", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        # 구좌 조정 기능
        with st.expander("🔧 구좌 변경", expanded=False):
            with st.form("adjust_form"):
                new_units = st.number_input(
                    "변경할 구좌 수", 
                    min_value=max(1, data['original_units']//2), 
                    max_value=data['original_units'],
                    value=data['original_units']//2,
                    step=1
                )
                if st.form_submit_button("구좌 변경 적용"):
                    if new_units != data['current_units']:
                        data['adjustments'].append({
                            "date": datetime.now().date(),
                            "from": data['current_units'],
                            "to": new_units
                        })
                        data['current_units'] = new_units
                        st.rerun()
        
        # 입금 내역 생성
        st.header("📊 입금 내역")
        deposit_data = []
        current_balance = 0
        total_months = data['years'] * 12
        adjusted = False
        
        for i in range(1, total_months + 1 + len(data['adjustments'])):
            deposit_date = data['start_date'] + relativedelta(months=+(i-1))
            
            # 조정 여부 확인
            current_deposit = data['unit_price'] * data['current_units']
            if not adjusted and data['adjustments']:
                if i == 1:  # 첫 달 조정
                    current_deposit = data['unit_price'] * (data['original_units'] // 2)
                    adjusted = True
            
            current_balance += current_deposit
            monthly_interest = current_balance * (data['interest']/100)/12
            
            status = "✅ 입금완료" if deposit_date < datetime.now().date() else "⏳ 대기중"
            
            deposit_data.append([
                f"{i}회차 ({deposit_date.strftime('%y.%m.%d')})",
                f"¥{current_deposit:,}",
                f"¥{current_balance:,}",
                f"¥{monthly_interest:,.1f}",
                status
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

# 앱 실행
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()