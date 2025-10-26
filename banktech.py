# app.py
import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd
import numpy as np
import time
import base64

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
    
    # 급여 데이터 저장소
    if 'payroll_list' not in st.session_state:
        st.session_state.payroll_list = []

# 다국어 지원
LANGUAGES = {
    'EN': {
        'title': 'Otsuka Bank',
        'subtitle': 'Employee Banking Portal',
        'login_id': 'Login ID',
        'password': 'Password',
        'login': 'Login',
        'login_error': 'Incorrect Login ID or Password',
        'home': '🏠 Home',
        'savings': '💰 Savings',
        'payroll': '📄 Payroll',
        'welcome': 'Welcome, {}',
        'logout': 'Logout',
        'no_capture': '⚠️ この画面のスクリーンショット・撮影は禁止されています',
        'security_warning': '🔒 セキュリティ警告: このページは監視されています',
        'announcement': '📢 お知らせ',
        'announcement_content': 'システムメンテナンス: 12月25日 2:00-4:00'
    },
    'JP': {
        'title': '大塚銀行',
        'subtitle': '従業員バンキングポータル',
        'login_id': 'ログインID',
        'password': 'パスワード',
        'login': 'ログイン',
        'login_error': 'ログインIDまたはパスワードが正しくありません',
        'home': '🏠 ホーム',
        'savings': '💰 積立',
        'payroll': '📄 給与',
        'welcome': 'ようこそ、{}様',
        'logout': 'ログアウト',
        'no_capture': '⚠️ この画面のスクリーンショット・撮影は禁止されています',
        'security_warning': '🔒 セキュリティ警告: このページは監視されています',
        'announcement': '📢 お知らせ',
        'announcement_content': 'システムメンテナンス: 12月25日 2:00-4:00'
    }
}

def get_text(key):
    return LANGUAGES[st.session_state.language].get(key, LANGUAGES['EN'].get(key, key))

# CSS 스타일링
def load_css():
    css = """
    <style>
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 50%, #f8fafc 100%);
        font-family: 'Noto Sans JP', 'Segoe UI', 'Hiragino Sans', sans-serif;
    }
    
    .bank-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
        color: white;
        padding: 2rem 0 1rem 0;
        margin: -1rem -1rem 0 -1rem;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.2);
        position: relative;
    }
    
    .header-content {
        position: relative;
        z-index: 2;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .logo-section {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    
    .bank-logo {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .logo-icon {
        font-size: 2.5rem;
        background: rgba(255,255,255,0.1);
        padding: 0.8rem;
        border-radius: 12px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .bank-title {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        margin: 0 !important;
        color: white !important;
    }
    
    .bank-subtitle {
        font-size: 1.1rem !important;
        opacity: 0.9;
        margin: 0.2rem 0 0 0 !important;
        font-weight: 400;
    }
    
    .user-info {
        display: flex;
        flex-direction: column;
        align-items: flex-end;
        gap: 0.3rem;
    }
    
    .top-controls {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 1rem 0 0 0;
        gap: 1rem;
    }
    
    .nav-container {
        background: white;
        padding: 0;
        margin: 0 -1rem;
        border-bottom: 1px solid #e2e8f0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .capture-warning {
        background: linear-gradient(45deg, #dc2626, #b91c1c);
        color: white;
        padding: 1.5rem;
        text-align: center;
        font-weight: 700;
        font-size: 1.2rem;
        margin: 0 -1rem 1rem -1rem;
        animation: alertPulse 2s ease-in-out infinite;
    }
    
    .security-alert {
        background: linear-gradient(45deg, #d97706, #b45309);
        color: white;
        padding: 1rem 2rem;
        text-align: center;
        font-weight: 600;
        font-size: 1rem;
        margin: 0 -1rem 1.5rem -1rem;
        animation: glow 3s ease-in-out infinite;
    }
    
    .announcement-banner {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 1.2rem 2rem;
        margin: 0 -1rem 1rem -1rem;
        border-radius: 0 0 12px 12px;
        box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        display: flex;
        align-items: center;
        gap: 1rem;
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    @keyframes alertPulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.95; }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 4px 12px rgba(217, 119, 6, 0.4); }
        50% { box-shadow: 0 6px 18px rgba(217, 119, 6, 0.6); }
    }
    
    .metric-card {
        background: white;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.06);
        border: 1px solid #f1f5f9;
    }
    
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800&display=swap');
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# 보안 경고 표시
def show_security_warnings():
    st.markdown(f'<div class="capture-warning">{get_text("no_capture")}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="security-alert">{get_text("security_warning")}</div>', unsafe_allow_html=True)

# 공지사항 배너
def show_announcement():
    st.markdown(f'''
    <div class="announcement-banner">
        <span>📢</span>
        <span>{get_text("announcement_content")}</span>
    </div>
    ''', unsafe_allow_html=True)

# 언어 전환
def render_language_switcher():
    current_lang = st.session_state.language
    if st.button("English", key="lang_en", use_container_width=True, 
                 type="primary" if current_lang == 'EN' else "secondary"):
        st.session_state.language = 'EN'
        st.rerun()

# 로그아웃
def render_logout():
    if st.button(get_text('logout'), key="logout_btn", use_container_width=True, type="secondary"):
        st.session_state.logged_in = False
        st.rerun()

# 네비게이션
def render_nav():
    nav_items = [
        ('home', '🏠 ホーム'),
        ('savings', '💰 積立'), 
        ('payroll', '📄 給与')
    ]
    
    st.markdown('<div class="nav-container">', unsafe_allow_html=True)
    
    cols = st.columns(len(nav_items))
    for idx, (page, label) in enumerate(nav_items):
        with cols[idx]:
            is_active = st.session_state.current_page == page
            if st.button(
                label, 
                key=f"nav_{page}",
                use_container_width=True,
                type="primary" if is_active else "secondary"
            ):
                st.session_state.current_page = page
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# 로그인 페이지
def login():
    st.markdown(f"""
    <div class="bank-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="bank-logo">
                    <div class="logo-icon">🏦</div>
                    <div class="logo-text">
                        <h1 class="bank-title">{get_text('title')}</h1>
                        <p class="bank-subtitle">{get_text('subtitle')}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="height: 2rem"></div>', unsafe_allow_html=True)
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

# 메인 레이아웃
def main_layout():
    st.markdown(f"""
    <div class="bank-header">
        <div class="header-content">
            <div class="logo-section">
                <div class="bank-logo">
                    <div class="logo-icon">🏦</div>
                    <div class="logo-text">
                        <h1 class="bank-title">{get_text('title')}</h1>
                        <p class="bank-subtitle">{get_text('subtitle')}</p>
                    </div>
                </div>
                <div class="user-info">
                    <div class="welcome-text">{get_text('welcome').format(st.session_state.user_data['name'])}</div>
                    <div class="account-info">{get_text('account_number')}: {st.session_state.user_data['account']}</div>
                </div>
            </div>
            
            <div class="top-controls">
                <div class="controls-left">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        render_language_switcher()
    
    st.markdown("""
                </div>
                <div class="controls-right">
    """, unsafe_allow_html=True)
    
    with col2:
        render_logout()
    
    st.markdown("""
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    render_nav()

# 메인 앱
def main():
    initialize_session_state()
    load_css()
    
    if not st.session_state.logged_in:
        login()
    else:
        main_layout()
        show_security_warnings()
        show_announcement()
        
        # 페이지 라우팅
        if st.session_state.current_page == 'home':
            from pages import home
            home.render()
        elif st.session_state.current_page == 'savings':
            from pages import savings
            savings.render()
        elif st.session_state.current_page == 'payroll':
            from pages import payroll
            payroll.render()

if __name__ == "__main__":
    main()