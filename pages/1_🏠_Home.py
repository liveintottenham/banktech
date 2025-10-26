# pages/1_🏠_Home.py
import streamlit as st
import pandas as pd
from common import get_text, show_security_warnings, show_announcement, main_layout
import random
from datetime import datetime, timedelta

# 페이지 제목 설정 (사이드바에 표시됨)
st.set_page_config(
    page_title="ホーム - Otsuka Bank",
    page_icon="🏠",
    layout="wide"
)

def generate_recent_transactions():
    """최근 거래 내역 생성"""
    transactions = []
    base_date = datetime.now()
    types = ["振込", "引き出し", "入金", "積立", "給与"]
    
    for i in range(10):
        date = base_date - timedelta(days=random.randint(0, 30))
        amount = random.randint(1000, 500000)
        transaction_type = random.choice(types)
        
        transactions.append({
            "date": date.strftime("%m/%d"),
            "description": f"{transaction_type} / {['Transfer', 'Withdrawal', 'Deposit', 'Savings', 'Salary'][types.index(transaction_type)]}",
            "amount": f"¥{amount:,}",
            "type": transaction_type
        })
    
    return transactions

def main():
    main_layout()
    show_security_warnings()
    show_announcement()
    
    # 사용자 환영 메시지 - 수정된 부분
    user_name_jp = st.session_state.user_data['name'].split(' / ')[0]
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"## 👋 {get_text('welcome').format(user_name_jp)}")
    with col2:
        st.markdown(f"""
        <div style="text-align: right; color: #64748b; font-size: 0.9rem;">
            🏢 {st.session_state.user_data['department']}<br>
            🔢 社員番号 / Employee No: {st.session_state.user_data['emp_num']}
        </div>
        """, unsafe_allow_html=True)
    
    # 요약 메트릭
    st.markdown(f"### 📊 {get_text('financial_overview')}")
    
    total_savings = 0
    monthly_payment = 0
    active_plans = len(st.session_state.savings_list)
    
    for savings in st.session_state.savings_list:
        calc = savings['calculation']
        total_savings += calc['final_balance']
        monthly_payment += savings['monthly_amount']
    
    # 랜덤 데이터로 실제 은행처럼 보이게
    total_assets = total_savings + 12500000  # 기본 자산 추가
    monthly_income = 350000  # 기본 월 수입
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">総資産 / Total Assets</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{total_assets:,.0f}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">前月比 +2.3% / +2.3% from last month</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">総積立額 / Total Savings</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{total_savings:,.0f}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">月間 +¥{monthly_payment:,.0f} / Monthly +¥{monthly_payment:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">月間収入 / Monthly Income</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{monthly_income:,.0f}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">前年比 +5.2% / +5.2% from last year</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">実行中プラン / Active Plans</div>
            <div style="font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">{active_plans}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">総プラン数 / Total Plans</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 빠른 접근 그리드
    st.markdown(f"### ⚡ {get_text('quick_access')}")
    
    quick_actions = [
        {"icon": "💰", "title": "新規積立作成\nCreate New Savings", "page": "pages/2_💰_Savings.py"},
        {"icon": "📊", "title": "積立一覧表示\nView Savings List", "page": "pages/2_💰_Savings.py"},
        {"icon": "📄", "title": "給与明細作成\nCreate Payslip", "page": "pages/3_📄_Payroll.py"},
        {"icon": "💳", "title": "口座振込\nAccount Transfer", "page": "pages/2_💰_Savings.py"},
        {"icon": "📈", "title": "資産分析\nAsset Analysis", "page": "pages/1_🏠_Home.py"},
        {"icon": "⚙️", "title": "設定\nSettings", "page": "pages/1_🏠_Home.py"}
    ]
    
    cols = st.columns(3)
    for i, action in enumerate(quick_actions):
        with cols[i % 3]:
            if st.button(
                f"{action['icon']} {action['title']}", 
                use_container_width=True,
                key=f"quick_{i}"
            ):
                st.switch_page(action['page'])
    
    # 차트와 거래 내역 섹션
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"### 📈 {get_text('asset_growth')}")
        months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        values = [14200000, 14500000, 14800000, 15000000, 15200000, 15400000, 15600000, 15800000, 16000000, 16200000, 16400000, 16600000]
        
        chart_data = pd.DataFrame({
            '月 / Month': months,
            '資産 / Assets': values
        })
        st.area_chart(chart_data.set_index('月 / Month'), height=300)
    
    with col2:
        st.markdown(f"### 🎯 {get_text('savings_distribution')}")
        if st.session_state.savings_list:
            labels = [savings['name'] for savings in st.session_state.savings_list]
            values = [savings['monthly_amount'] * savings['period'] * 12 for savings in st.session_state.savings_list]
            chart_data = pd.DataFrame({
                'カテゴリ / Category': labels,
                '金額 / Amount': values
            })
            st.bar_chart(chart_data.set_index('カテゴリ / Category'), height=300)
        else:
            st.info("積立プランがありません / No savings plans")
    
    # 최근 거래 내역
    st.markdown(f"### 💳 {get_text('recent_transactions')}")
    transactions = generate_recent_transactions()
    
    for transaction in transactions:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col1:
            st.write(transaction['date'])
        with col2:
            st.write(transaction['description'])
        with col3:
            amount_color = "#ef4444" if transaction['type'] in ['引き出し', '振込'] else "#10b981"
            st.markdown(f"<div style='color: {amount_color}; text-align: right; font-weight: 600;'>{transaction['amount']}</div>", unsafe_allow_html=True)
        
        st.divider()

if __name__ == "__main__":
    main()