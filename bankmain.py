import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링 (전문 은행 UI 버전)
st.markdown("""
<style>
:root {
    --primary: #2E3B4E;
    --secondary: #4E6B8A;
    --accent: #FF6B6B;
    --background: #F5F7FA;
    --card: #FFFFFF;
}

.stApp {
    background: var(--background);
}

.info-card {
    background: var(--card);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border-left: 4px solid var(--primary);
}

.savings-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin: 2rem 0;
}

.savings-item {
    background: var(--card);
    border-radius: 10px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}

.stButton>button {
    background: var(--primary) !important;
    color: white !important;
    border-radius: 8px !important;
    transition: all 0.3s !important;
}

.logo-header {
    text-align: center;
    font-size: 2rem;
    color: var(--primary);
    font-weight: 700;
    margin: 2rem 0;
    padding: 1rem;
    border-bottom: 3px solid var(--primary);
}
</style>
""", unsafe_allow_html=True)

# 로그인 시스템
def login():
    st.markdown("""
    <div class='logo-header'>
        <div>🏦 大塚商会Loan</div>
        <div style='font-size:1rem; color:#666; margin-top:0.5rem;'>Otsuka Shokai Loan Service</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        user_id = st.text_input("아이디")
        password = st.text_input("비밀번호", type="password")
        if st.form_submit_button("🔑 로그인"):
            if user_id == "sgms" and password == "qwer1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("로그인 실패")

# 메인 페이지
def main():
    st.markdown("<div class='logo-header'>🏦 大塚商会Loan</div>", unsafe_allow_html=True)
    
    # 1. 적금 계좌 등록
    with st.expander("📝 적금 계좌 신규 등록", expanded=True):
        with st.form("savings_form"):
            cols = st.columns([1,1,2,1])
            name = cols[0].text_input("고객명", value="홍길동")
            emp_num = cols[1].text_input("사원번호", value="12345678")
            account = cols[2].text_input("계좌번호", value="098-96586-6521")
            start_date = cols[3].date_input("적금 시작일", value=date(2025,2,25))
            
            cols2 = st.columns([1,1,1,1])
            unit_price = cols2[0].number_input("1구좌당 가격 (¥)", value=1100, min_value=1000)
            units = cols2[1].number_input("신청구좌", value=4, min_value=1)
            years = cols2[2].selectbox("만기기간", [1,2,3,5], index=2)
            interest = cols2[3].number_input("연이자율(%)", value=10.03, min_value=0.0)
            
            if st.form_submit_button("💾 저장하기"):
                st.session_state.savings_data = {
                    "name": name, "emp_num": emp_num, "account": account,
                    "start_date": start_date, "unit_price": unit_price,
                    "original_units": units, "current_units": units,
                    "years": years, "interest": interest,
                    "adjustments": []
                }

    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        monthly = data['unit_price'] * data['current_units']
        maturity = data['start_date'] + relativedelta(years=data['years'])
        
        # 2. 구좌 변경 기능 (복원)
        with st.expander("⚙️ 납입 조정 설정", expanded=True):
            with st.form("adjust_form"):
                cols = st.columns([2,3,1])
                adjust_month = cols[0].number_input("조정 회차", min_value=1, value=1)
                new_units = cols[1].number_input("변경 구좌수", 
                    min_value=data['original_units']//2, 
                    max_value=data['original_units'], 
                    value=data['original_units']//2)
                if cols[2].form_submit_button("적용"):
                    data['adjustments'].append({
                        "month": adjust_month,
                        "new_units": new_units
                    })
                    st.rerun()
        
        # 3. 회원 정보 & 요약 (UI 개선)
        st.markdown("### 🧑💼 회원 정보")
        with st.container():
            cols = st.columns(4)
            cols[0].markdown(f"<div class='info-card'>👤 **고객명**<br>{data['name']}</div>", unsafe_allow_html=True)
            cols[1].markdown(f"<div class='info-card'>🆔 **사원번호**<br>{data['emp_num']}</div>", unsafe_allow_html=True)
            cols[2].markdown(f"<div class='info-card'>💳 **계좌번호**<br>{data['account']}</div>", unsafe_allow_html=True)
            cols[3].markdown(f"<div class='info-card'>📅 **만기일**<br>{maturity.strftime('%Y-%m-%d')}</div>", unsafe_allow_html=True)
        
        # 4. 요약 정보 그리드
        st.markdown("### 📊 적금 요약")
        with st.container():
            st.markdown("""
            <div class='savings-grid'>
                <div class='savings-item'>
                    <div>💰 월 납입액</div>
                    <div style='font-size:1.5rem;color:var(--primary);'>¥{:,}</div>
                </div>
                <div class='savings-item'>
                    <div>📆 총 납입회차</div>
                    <div style='font-size:1.5rem;color:var(--primary);'>{:,}회</div>
                </div>
                <div class='savings-item'>
                    <div>💵 총 납입액</div>
                    <div style='font-size:1.5rem;color:var(--primary);'>¥{:,}</div>
                </div>
                <div class='savings-item'>
                    <div>💹 예상이자</div>
                    <div style='font-size:1.5rem;color:var(--primary);'>¥{:,.1f}</div>
                </div>
            </div>
            """.format(
                monthly,
                data['years']*12 + len(data['adjustments']),
                monthly * data['years']*12,
                monthly * data['years']*12 * (data['interest']/100)
            ), unsafe_allow_html=True)
        
        # 5. 입금 내역 (아이콘 복원)
        st.markdown("### 📅 입금 내역")
        records = []
        balance = 0
        for i in range(1, data['years']*12 + 1 + len(data['adjustments'])):
            deposit_date = data['start_date'] + relativedelta(months=i-1)
            current_units = data['original_units']
            
            # 조정 적용
            for adj in data['adjustments']:
                if adj['month'] == i:
                    current_units = adj['new_units']
            
            amount = data['unit_price'] * current_units
            balance += amount
            interest_amt = balance * (data['interest']/100)/12
            
            records.append([
                f"{i}회차 ({deposit_date.strftime('%y.%m.%d')})",
                f"¥{amount:,}",
                f"¥{balance:,}",
                f"¥{interest_amt:,.1f}",
                "✅ 완료" if deposit_date < datetime.now().date() else "⏳ 대기중",
                "🔧 조정" if any(adj['month']==i for adj in data['adjustments']) else ""
            ])
        
        df = pd.DataFrame(records, columns=["회차", "입금액", "잔액", "이자", "상태", "비고"])
        st.dataframe(
            df.set_index("회차"), 
            use_container_width=True,
            column_config={
                "입금액": st.column_config.NumberColumn(format="¥%d"),
                "잔액": st.column_config.NumberColumn(format="¥%d"),
                "이자": st.column_config.NumberColumn(format="¥%.1f")
            }
        )

# 앱 실행
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()