# pages/1_🏠_Home.py
import streamlit as st
import pandas as pd
from common import get_text, show_security_warnings, show_announcement, main_layout

st.set_page_config(
    page_title="ホーム - Otsuka Bank",
    page_icon="🏠",
    layout="wide"
)

def main():
    main_layout()
    show_security_warnings()
    show_announcement()
    
    user_name_jp = st.session_state.user_data['name'].split(' / ')[0]
    
    st.markdown(f"## 👋 {get_text('welcome').format(user_name_jp)}")
    
    # 메트릭 카드
    st.markdown("### 📊 資産概要 / Financial Overview")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">総資産 / Total Assets</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1e40af;">¥16,600,000</div>
            <div style="font-size: 0.8rem; color: #10b981;">前月比 +2.3%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">総積立額 / Total Savings</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1e40af;">¥3,250,000</div>
            <div style="font-size: 0.8rem; color: #10b981;">月間 +¥50,000</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">月間収入 / Monthly Income</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1e40af;">¥350,000</div>
            <div style="font-size: 0.8rem; color: #10b981;">前年比 +5.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        active_plans = len(st.session_state.savings_list)
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #64748b; margin-bottom: 0.5rem;">実行中プラン / Active Plans</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #1e40af;">{active_plans}</div>
            <div style="font-size: 0.8rem; color: #64748b;">総プラン数</div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()