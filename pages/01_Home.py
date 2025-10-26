# pages/01_Home.py
import streamlit as st
import pandas as pd
from common import get_text, show_security_warnings, show_announcement, main_layout

def render_home():
    main_layout()
    show_security_warnings()
    show_announcement()
    
    st.markdown(f"## 👋 {get_text('welcome').format(st.session_state.user_data['name'])}")
    
    # 요약 메트릭
    st.markdown("### 📊 資産概要")
    
    total_savings = 0
    monthly_payment = 0
    active_plans = len(st.session_state.savings_list)
    
    for savings in st.session_state.savings_list:
        calc = savings['calculation']
        total_savings += calc['final_balance']
        monthly_payment += savings['monthly_amount']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">総積立額</div>
            <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{total_savings:,.0f}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">前月比 +2.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">月間支払額</div>
            <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">¥{monthly_payment:,.0f}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">実行中プラン</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.85rem; opacity: 0.8; margin-bottom: 1rem;">実行中プラン</div>
            <div style="font-size: 2rem; font-weight: 700; margin-bottom: 0.5rem; color: #1e40af;">{active_plans}</div>
            <div style="font-size: 0.75rem; opacity: 0.6;">総プラン数</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 차트 섹션
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 資産成長トレンド")
        months = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']
        values = [14200000, 14500000, 14800000, 15000000, 15200000, 15400000, 15600000, 15800000, 16000000, 16200000, 16400000, 16600000]
        
        chart_data = pd.DataFrame({
            '月': months,
            '資産': values
        })
        st.area_chart(chart_data.set_index('月'), height=300)
    
    with col2:
        st.markdown("### 🎯 積立分布")
        if st.session_state.savings_list:
            labels = [savings['name'] for savings in st.session_state.savings_list]
            values = [savings['monthly_amount'] * savings['period'] * 12 for savings in st.session_state.savings_list]
            chart_data = pd.DataFrame({
                'カテゴリ': labels,
                '金額': values
            })
            st.bar_chart(chart_data.set_index('カテゴリ'), height=300)
        else:
            st.info("積立プランがありません")
    
    # 빠른 접근
    st.markdown("### ⚡ クイックアクセス")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💰 新規積立作成", use_container_width=True, type="primary"):
            st.switch_page("pages/02_Savings.py")
    
    with col2:
        if st.button("📊 積立一覧表示", use_container_width=True):
            st.switch_page("pages/02_Savings.py")
    
    with col3:
        if st.button("📄 給与明細作成", use_container_width=True):
            st.switch_page("pages/03_Payroll.py")

# Streamlit이 이 페이지를 로드할 때 실행
if __name__ == "__main__":
    render_home()