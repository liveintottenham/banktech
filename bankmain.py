# bankmain.py
import streamlit as st
from common import initialize_session_state, load_css, login

def main():
    # Streamlit 페이지 설정
    st.set_page_config(
        page_title="Otsuka Bank Portal",
        page_icon="🏦",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    initialize_session_state()
    load_css()
    
    if not st.session_state.logged_in:
        login()
    else:
        # 메인 앱에서는 홈페이지 내용만 표시
        from pages._01_Home import render_home
        render_home()

if __name__ == "__main__":
    main()