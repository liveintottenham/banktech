import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링 (프로페셔널 버전)
st.markdown("""
<style>
:root {
    --primary: #2B4A6F;
    --secondary: #3D6B9E;
    --accent: #FF6B6B;
    --background: #f8fafc;
    --card: #FFFFFF;
}

.metric-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 1rem;
    margin: 1rem 0;
}

.metric-card {
    background: var(--card);
    border-radius: 10px;
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
</style>
""", unsafe_allow_html=True)

# 메인 계산 로직
def calculate_savings(data):
    original_monthly = data['unit_price'] * data['original_units']
    adjusted_months = data['years'] * 12 + len(data['adjustments'])
    
    # 총 적금액 계산 (원금은 동일)
    total_payment = original_monthly * data['years'] * 12
    
    # 이자 계산 (조정된 월별 잔액 기준)
    balance = 0
    total_interest = 0
    
    for i in range(1, adjusted_months + 1):
        current_units = data['original_units']
        for adj in data['adjustments']:
            if adj['month'] == i:
                current_units = adj['new_units']
        
        amount = data['unit_price'] * current_units
        balance += amount
        monthly_interest = balance * (data['interest']/100)/12
        total_interest += monthly_interest
    
    return {
        "monthly": original_monthly,
        "total_months": adjusted_months,
        "total_payment": total_payment,
        "total_interest": total_interest,
        "interest_rate": data['interest']
    }

# 메인 페이지
def main():
    # ... [기존 로그인 및 폼 코드 생략] ...

    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        calc = calculate_savings(data)
        
        # 5. 주요 지표 (5칸 그리드)
        st.markdown("### 📊 積立概要")
        with st.container():
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
                    <div class='metric-value highlight-value'>{calc['interest_rate']}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ... [기존 입금 내역 테이블 코드 생략] ...

# 앱 실행
if __name__ == "__main__":
    main()