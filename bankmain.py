import streamlit as st
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np

# Streamlit 페이지 설정
st.set_page_config(
    page_title="Otsuka Bank Portal",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 세션 상태 초기화
def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'language' not in st.session_state:
        st.session_state.language = 'JP'
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # 사용자 데이터
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {
            "name": "山田 太郎",
            "account": "098-96586-6521",
            "emp_num": "12345678",
            "department": "IT事業部"
        }
    
    # 적금 데이터 저장소
    if 'savings_list' not in st.session_state:
        st.session_state.savings_list = []

# 다국어 지원
LANGUAGES = {
    'JP': {
        'title': '大塚銀行 従業員ポータル',
        'subtitle': 'Otsuka Bank Employee Portal',
        'login_id': 'ログインID',
        'password': 'パスワード',
        'login': 'ログイン',
        'login_error': 'ログインIDまたはパスワードが正しくありません',
        'home': '🏠 ホーム',
        'savings': '💰 積立管理',
        'payroll': '📄 給与明細',
        'welcome': 'ようこそ、{}様',
        'account_number': '口座番号',
        'asset_overview': '資産概要',
        'total_savings': '総積立額',
        'active_plans': '実行中プラン',
        'monthly_payment': '月間支払額',
        'recent_transactions': '最近の取引',
        'quick_access': 'クイックアクセス',
        'new_savings': '新規積立作成',
        'view_savings': '積立一覧',
        'savings_management': '積立貯蓄管理',
        'savings_name': '積立名',
        'monthly_amount': '月間積立額',
        'period': '積立期間',
        'start_date': '開始日',
        'create_plan': 'プラン作成',
        'savings_details': '積立詳細',
        'payment_schedule': '入金スケジュール',
        'logout': 'ログアウト',
        'customer_name': '顧客名',
        'employee_number': '社員番号',
        'basic_info': '基本情報',
        'savings_calc': '積立計算',
        'adjust_payment': '入金調整',
        'payment_history': '入金履歴'
    },
    'KR': {
        'title': '오츠카 은행 직원 포털',
        'subtitle': 'Otsuka Bank Employee Portal',
        'login_id': '로그인 ID',
        'password': '비밀번호',
        'login': '로그인',
        'login_error': '로그인 ID 또는 비밀번호가 올바르지 않습니다',
        'home': '🏠 홈',
        'savings': '💰 적금 관리',
        'payroll': '📄 급여 명세서',
        'welcome': '{}님, 환영합니다',
        'account_number': '계좌번호',
        'asset_overview': '자산 현황',
        'total_savings': '총 적금액',
        'active_plans': '진행 중인 플랜',
        'monthly_payment': '월 납입액',
        'recent_transactions': '최근 거래',
        'quick_access': '빠른 접근',
        'new_savings': '새 적금 만들기',
        'view_savings': '적금 목록',
        'savings_management': '적금 관리',
        'savings_name': '적금 이름',
        'monthly_amount': '월 납입액',
        'period': '적금 기간',
        'start_date': '시작일',
        'create_plan': '플랜 생성',
        'savings_details': '적금 상세',
        'payment_schedule': '납입 일정',
        'logout': '로그아웃',
        'customer_name': '고객명',
        'employee_number': '사원번호',
        'basic_info': '기본 정보',
        'savings_calc': '적금 계산',
        'adjust_payment': '납입 조정',
        'payment_history': '납입 내역'
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language][key]

# CSS 스타일링
def load_css():
    css = """
    <style>
    /* 기본 스타일 */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 20px;
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        min-height: calc(100vh - 40px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .content-container {
        padding: 30px;
    }
    
    /* 헤더 스타일 */
    .bank-header {
        background: linear-gradient(135deg, #2c3e50, #34495e);
        color: white;
        padding: 2rem 3rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
    }
    
    .bank-title {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        background: linear-gradient(135deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .bank-subtitle {
        font-size: 1.2rem !important;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* 네비게이션 */
    .nav-container {
        background: #f8f9fa;
        padding: 1rem 2rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    /* 카드 스타일 */
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    /* 버튼 스타일 */
    .stButton>button {
        background: linear-gradient(135deg, #667eea, #764ba2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* 입력 필드 */
    .stTextInput>div>div>input,
    .stNumberInput>div>div>input,
    .stDateInput>div>div>input {
        border: 1px solid #e2e8f0 !important;
        border-radius: 10px !important;
        padding: 0.8rem 1rem !important;
    }
    
    /* 테이블 스타일 */
    .dataframe {
        border-radius: 10px !important;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1) !important;
    }
    
    /* 캡처 방지 배너 */
    .no-capture {
        background: linear-gradient(45deg, #ff6b6b, #ee5a24);
        color: white;
        padding: 0.5rem;
        text-align: center;
        font-weight: bold;
        position: relative;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Noto Sans JP', sans-serif;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 적금 계산 함수 (실제 은행 방식)
def calculate_savings_schedule(monthly_amount, period_years, start_date, adjustments=None):
    """
    실제 은행 적금 계산 방식
    adjustments: {회차: 조정금액} 형태의 딕셔너리
    """
    total_months = period_years * 12
    today = datetime.now().date()
    
    schedule = []
    total_paid = 0
    total_adjustments = 0
    
    for month in range(1, total_months + 1):
        payment_date = start_date + relativedelta(months=month-1)
        
        # 조정된 금액 확인
        actual_amount = monthly_amount
        adjustment_note = ""
        if adjustments and month in adjustments:
            actual_amount = adjustments[month]
            adjustment_note = f"조정: ¥{adjustments[month]:,}"
            total_adjustments += (monthly_amount - adjustments[month])
        
        # 상태 결정 (오늘 기준)
        if payment_date < today:
            status = "✅ 입금완료"
        elif payment_date == today:
            status = "⏳ 오늘입금"
        else:
            status = "📅 입금예정"
        
        total_paid += actual_amount
        
        schedule.append({
            '회차': month,
            '입금일': payment_date.strftime('%Y/%m/%d'),
            '입금액': actual_amount,
            '누적액': total_paid,
            '상태': status,
            '비고': adjustment_note
        })
    
    return {
        'schedule': schedule,
        'total_months': total_months,
        'total_amount': total_paid,
        'total_adjustments': total_adjustments,
        'completion_rate': len([x for x in schedule if x['상태'] == '✅ 입금완료']) / total_months * 100
    }

# 네비게이션
def render_nav():
    nav_items = [
        ('home', get_text('home')),
        ('savings', get_text('savings')), 
        ('payroll', get_text('payroll'))
    ]
    
    cols = st.columns(len(nav_items))
    for idx, (page, label) in enumerate(nav_items):
        with cols[idx]:
            if st.button(
                label, 
                use_container_width=True,
                type="primary" if st.session_state.current_page == page else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()

# 홈 페이지
def render_home():
    st.markdown(f"## {get_text('welcome').format(st.session_state.user_data['name'])}")
    
    # 요약 메트릭
    col1, col2, col3 = st.columns(3)
    
    # 실제 데이터 계산
    total_savings = 0
    monthly_payment = 0
    active_plans = len(st.session_state.savings_list)
    
    for savings in st.session_state.savings_list:
        calc = savings['calculation']
        total_savings += calc['total_amount']
        monthly_payment += savings['monthly_amount']
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('total_savings')}</div>
            <div style="font-size: 2rem; font-weight: 800;">¥{total_savings:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('monthly_payment')}</div>
            <div style="font-size: 2rem; font-weight: 800;">¥{monthly_payment:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; opacity: 0.9;">{get_text('active_plans')}</div>
            <div style="font-size: 2rem; font-weight: 800;">{active_plans}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # 빠른 접근
    st.markdown(f"## {get_text('quick_access')}")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(f"💰 {get_text('new_savings')}", use_container_width=True):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    with col2:
        if st.button(f"📋 {get_text('view_savings')}", use_container_width=True):
            st.session_state.current_page = 'savings'
            st.rerun()
    
    # 최근 적금 플랜
    if st.session_state.savings_list:
        st.markdown(f"## {get_text('active_plans')}")
        for savings in st.session_state.savings_list[-3:]:
            with st.container():
                st.markdown('<div class="card">', unsafe_allow_html=True)
                col1, col2, col3, col4 = st.columns([2,1,1,1])
                with col1:
                    st.write(f"**{savings['name']}**")
                    st.write(f"계좌: {savings['account_number']}")
                with col2:
                    st.write(f"월 ¥{savings['monthly_amount']:,.0f}")
                with col3:
                    st.write(f"{savings['period']}년")
                with col4:
                    completion = savings['calculation']['completion_rate']
                    st.write(f"진행률: {completion:.1f}%")
                st.markdown('</div>', unsafe_allow_html=True)

# 적금 관리 페이지
def render_savings():
    st.markdown(f"## {get_text('savings_management')}")
    
    tab1, tab2 = st.tabs(["新規積立作成", "積立一覧"])
    
    with tab1:
        st.subheader("新規積立口座開設")
        
        # 캡처 방지 배너
        st.markdown('<div class="no-capture">⚠️ この画面のスクリーンショット・撮影は禁止されています</div>', unsafe_allow_html=True)
        
        with st.form("new_savings_plan"):
            st.markdown("#### 基本情報")
            col1, col2 = st.columns(2)
            
            with col1:
                customer_name = st.text_input(get_text('customer_name'), st.session_state.user_data['name'])
                employee_number = st.text_input(get_text('employee_number'), st.session_state.user_data['emp_num'])
                account_number = st.text_input(get_text('account_number'), st.session_state.user_data['account'])
            
            with col2:
                savings_name = st.text_input(get_text('savings_name'), "定期積立預金")
                monthly_amount = st.number_input(get_text('monthly_amount'), min_value=1000, value=3000, step=1000)
                period = st.selectbox(get_text('period'), [3, 5], index=0, format_func=lambda x: f"{x}年")
                start_date = st.date_input(get_text('start_date'), date(2025, 1, 1))
            
            st.markdown("#### 入金調整設定 (任意)")
            st.info("特定の回で入金額を調整する場合は設定してください")
            
            adjustments = {}
            adjust_cols = st.columns(4)
            for i in range(4):
                with adjust_cols[i]:
                    month = st.number_input(f"調整回", min_value=1, max_value=period*12, value=(i+1)*3, key=f"adj_month_{i}")
                    amount = st.number_input(f"調整金額", min_value=0, value=0, key=f"adj_amount_{i}")
                    if amount > 0:
                        adjustments[month] = amount
            
            if st.form_submit_button(get_text('create_plan'), use_container_width=True):
                # 적금 계산
                calculation = calculate_savings_schedule(monthly_amount, period, start_date, adjustments)
                
                # 새로운 적금 플랜 생성
                new_savings = {
                    'id': len(st.session_state.savings_list) + 1,
                    'name': savings_name,
                    'customer_name': customer_name,
                    'employee_number': employee_number,
                    'account_number': account_number,
                    'monthly_amount': monthly_amount,
                    'period': period,
                    'start_date': start_date.strftime('%Y/%m/%d'),
                    'adjustments': adjustments,
                    'calculation': calculation,
                    'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
                }
                
                st.session_state.savings_list.append(new_savings)
                st.success("🎉 積立口座が正常に開設されました！")
                st.balloons()
    
    with tab2:
        st.subheader("積立口座一覧")
        
        if not st.session_state.savings_list:
            st.info("登録されている積立口座がありません。")
        else:
            for savings in st.session_state.savings_list:
                with st.expander(f"📒 {savings['name']} - {savings['account_number']}", expanded=False):
                    # 캡처 방지 배너
                    st.markdown('<div class="no-capture">⚠️ この画面のスクリーンショット・撮影は禁止されています</div>', unsafe_allow_html=True)
                    
                    # 기본 정보
                    st.markdown("#### 基本情報")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.write("**고객명**")
                        st.write(savings['customer_name'])
                    with col2:
                        st.write("**사원번호**")
                        st.write(savings['employee_number'])
                    with col3:
                        st.write("**계좌번호**")
                        st.write(savings['account_number'])
                    with col4:
                        st.write("**개설일**")
                        st.write(savings['start_date'])
                    
                    # 적금 정보
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.write("**월 납입액**")
                        st.write(f"¥{savings['monthly_amount']:,.0f}")
                    with col2:
                        st.write("**적금 기간**")
                        st.write(f"{savings['period']}년")
                    with col3:
                        st.write("**총 납입액**")
                        st.write(f"¥{savings['calculation']['total_amount']:,.0f}")
                    with col4:
                        completion = savings['calculation']['completion_rate']
                        st.write("**진행률**")
                        st.write(f"{completion:.1f}%")
                    
                    # 조정 내역
                    if savings['adjustments']:
                        st.markdown("#### 입금 조정 내역")
                        for month, amount in savings['adjustments'].items():
                            st.write(f"- {month}회차: ¥{amount:,.0f} (기본 ¥{savings['monthly_amount']:,.0f} → 조정)")
                    
                    # 입금 스케줄
                    st.markdown("#### 입금 스케줄")
                    schedule_df = pd.DataFrame(savings['calculation']['schedule'])
                    
                    # 현재까지의 입금 내역과 남은 입금 분리
                    completed_df = schedule_df[schedule_df['상태'] == '✅ 입금완료']
                    upcoming_df = schedule_df[schedule_df['상태'] != '✅ 입금완료']
                    
                    if not completed_df.empty:
                        st.markdown("##### ✅ 입금완료 내역")
                        st.dataframe(completed_df, use_container_width=True, hide_index=True)
                    
                    if not upcoming_df.empty:
                        st.markdown("##### 📅 입금예정 내역")
                        st.dataframe(upcoming_df, use_container_width=True, hide_index=True)
                    
                    # 추가 조정 기능
                    st.markdown("#### 입금 추가 조정")
                    with st.form(f"adjust_{savings['id']}"):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            adjust_month = st.number_input("조정 회차", min_value=1, max_value=savings['period']*12, value=1, key=f"new_adj_month_{savings['id']}")
                        with col2:
                            adjust_amount = st.number_input("조정 금액", min_value=0, value=savings['monthly_amount'], key=f"new_adj_amount_{savings['id']}")
                        with col3:
                            if st.form_submit_button("조정 적용"):
                                savings['adjustments'][adjust_month] = adjust_amount
                                # 재계산
                                savings['calculation'] = calculate_savings_schedule(
                                    savings['monthly_amount'], 
                                    savings['period'], 
                                    datetime.strptime(savings['start_date'], '%Y/%m/%d').date(),
                                    savings['adjustments']
                                )
                                st.success(f"{adjust_month}회차 입금액이 조정되었습니다.")
                                st.rerun()
                    
                    # 삭제 버튼
                    if st.button(f"🗑️ 삭제", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()

# 급여 명세서 페이지 (간단히)
def render_payroll():
    st.markdown("## 📄 給与明細管理")
    st.info("この機能は現在開発中です。近日中に利用可能になります。")

# 로그인 페이지
def login():
    st.markdown(f"""
    <div class="bank-header">
        <h1 class="bank-title">{get_text('title')}</h1>
        <p class="bank-subtitle">{get_text('subtitle')}</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.markdown("### ログイン")
            with st.form("login_form"):
                user_id = st.text_input(get_text('login_id'), placeholder="otsuka")
                password = st.text_input(get_text('password'), type="password", placeholder="bank1234")
                
                if st.form_submit_button(get_text('login'), use_container_width=True):
                    if user_id == "otsuka" and password == "bank1234":
                        st.session_state.logged_in = True
                        st.session_state.current_page = 'home'
                        st.rerun()
                    else:
                        st.error(get_text('login_error'))

# 언어 전환
def render_language_switcher():
    current_lang = st.session_state.language
    if current_lang == 'JP':
        if st.button("🇰🇷 한국어", key="lang_switch"):
            st.session_state.language = 'KR'
            st.rerun()
    else:
        if st.button("🇯🇵 日本語", key="lang_switch"):
            st.session_state.language = 'JP'
            st.rerun()

# 로그아웃
def render_logout():
    if st.button(get_text('logout'), key="logout_btn"):
        st.session_state.logged_in = False
        st.rerun()

# 메인 앱
def main():
    initialize_session_state()
    load_css()
    
    # 메인 컨테이너 시작
    st.markdown('<div class="main">', unsafe_allow_html=True)
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    if not st.session_state.logged_in:
        login()
    else:
        # 헤더
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"""
            <div class="bank-header">
                <h1 class="bank-title">{get_text('title')}</h1>
                <p class="bank-subtitle">{get_text('subtitle')}</p>
                <p style="margin: 0; opacity: 0.9; font-size: 1.1rem;">
                    {get_text('welcome').format(st.session_state.user_data['name'])} | 
                    {get_text('account_number')}: {st.session_state.user_data['account']}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.write("")  # 공백
            render_language_switcher()
            render_logout()
        
        # 네비게이션
        st.markdown('<div class="nav-container">', unsafe_allow_html=True)
        render_nav()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 페이지 내용
        if st.session_state.current_page == 'home':
            render_home()
        elif st.session_state.current_page == 'savings':
            render_savings()
        elif st.session_state.current_page == 'payroll':
            render_payroll()
    
    # 컨테이너 종료
    st.markdown('</div>', unsafe_allow_html=True)  # content-container
    st.markdown('</div>', unsafe_allow_html=True)  # main-container
    st.markdown('</div>', unsafe_allow_html=True)  # main

if __name__ == "__main__":
    main()