# app.py
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
        # 로그인 후에는 자동으로 홈페이지로 이동
        st.switch_page("pages/1_🏠_Home.py")

if __name__ == "__main__":
    main()