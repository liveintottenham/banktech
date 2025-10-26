# bankmain.py
import streamlit as st

# common.py에서 필요한 함수들 임포트
from common import initialize_session_state, load_css, login, main_layout, show_security_warnings, show_announcement

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