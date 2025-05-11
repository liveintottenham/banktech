import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링 업그레이드
st.markdown("""
<style>
:root {
    --primary: #1A73E8;
    --secondary: #4285F4;
    --accent: #FF6D00;
    --background: #F8F9FA;
    --surface: #FFFFFF;
    --on-surface: #202124;
    --divider: #DADCE0;
}

.stApp {
    background: var(--background);
    font-family: 'Roboto', sans-serif;
}

/* 머터리얼 디자인 카드 */
.mdc-card {
    background: var(--surface);
    border-radius: 16px;
    padding: 24px;
    margin: 16px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
    border: 1px solid var(--divider);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.mdc-card:hover {
    box-shadow: 0 8px 12px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}

/* 상단 네비게이션 바 */
.nav-container {
    background: var(--surface);
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    padding: 12px 24px;
    margin-bottom: 24px;
    display: flex;
    gap: 32px;
}

.nav-item {
    color: var(--on-surface);
    font-weight: 500;
    padding: 8px 16px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.2s;
}

.nav-item.active {
    background: rgba(26, 115, 232, 0.1);
    color: var(--primary);
}

/* 급여 명세서 스타일 */
.paystub-container {
    background: var(--surface);
    border-radius: 16px;
    padding: 32px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.04);
}

.paystub-header {
    border-bottom: 2px solid var(--divider);
    padding-bottom: 16px;
    margin-bottom: 24px;
}

.paystub-section {
    margin: 24px 0;
}

.amount-row {
    display: flex;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid var(--divider);
}

.total-row {
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--primary);
}

@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
</style>
""", unsafe_allow_html=True)

# 네비게이션 관리
def render_nav():
    st.markdown("""
    <div class="nav-container">
        <div class="nav-item %s" onclick="window.streamlitApi.setComponentValue('loan')">ローン管理</div>
        <div class="nav-item %s" onclick="window.streamlitApi.setComponentValue('payroll')">給与明細</div>
    </div>
    """ % (
        "active" if st.session_state.get('page') == 'loan' else "",
        "active" if st.session_state.get('page') == 'payroll' else ""
    ), unsafe_allow_html=True)

# 급여 명세서 페이지
def show_payroll():
    st.markdown("""
    <div class="paystub-container">
        <div class="paystub-header">
            <h2 style="margin:0">🏦 大塚商会 給与明細書</h2>
            <p style="color:#5F6368">発行日: {}</p>
        </div>
        
        <div class="paystub-section">
            <h3 style="color:var(--primary)">🔼 支給内訳</h3>
            <div class="amount-row">
                <span>基本給</span>
                <span>¥340,000</span>
            </div>
        </div>

        <div class="paystub-section">
            <h3 style="color:var(--primary)">🔽 控除内訳</h3>
            <div class="amount-row">
                <span>所得税</span>
                <span>¥26,320</span>
            </div>
            <div class="amount-row">
                <span>住民税</span>
                <span>¥6,520</span>
            </div>
            <div class="amount-row">
                <span>健康保険</span>
                <span>¥8,910</span>
            </div>
            <div class="amount-row">
                <span>厚生年金</span>
                <span>¥29,960</span>
            </div>
            <div class="amount-row">
                <span>雇用保険</span>
                <span>¥4,550</span>
            </div>
            <div class="amount-row">
                <span>その他控除</span>
                <span>¥70,000</span>
            </div>
        </div>

        <div class="paystub-section" style="margin-top:32px">
            <div class="amount-row total-row">
                <span>差引支給額</span>
                <span>¥193,740</span>
            </div>
        </div>
    </div>
    """.format(datetime.now().strftime('%Y年%m月%d日')), unsafe_allow_html=True)

# 기존 로ーン 관리 시스템 (원본 코드에서 변경없이 유지)
# ... [기존의 calculate_savings, login, main 함수 유지] ...

# 앱 실행 로직 업데이트
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'page' not in st.session_state:
    st.session_state.page = 'loan'

if not st.session_state.logged_in:
    login()
else:
    render_nav()
    
    # 네비게이션 처리
    if st.session_state.page == 'loan':
        main()
    elif st.session_state.page == 'payroll':
        show_payroll()

    # 네비게이션 이벤트 처리
    nav_event = st.session_state.get('nav_event')
    if nav_event:
        st.session_state.page = nav_event
        st.session_state.nav_event = None
        st.rerun()

# JavaScript 핸들러 추가
st.components.v1.html("""
<script>
window.streamlitApi = {
    setComponentValue: function(value) {
        window.parent.postMessage({
            type: 'streamlit:setComponentValue',
            api: 'component_123',
            componentValue: value
        }, '*');
    }
}
</script>
""", height=0)