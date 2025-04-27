import streamlit as st
from datetime import datetime
import pandas as pd

# 페이지 설정
st.set_page_config(
    page_title="積立貯蓄のお知らせ",
    page_icon="📊",
    layout="wide"
)

# 사이드바 입력 섹션
with st.sidebar:
    st.header("基本情報入力")
    emp_name = st.text_input("氏名")
    emp_number = st.text_input("社員番号")
    report_date = st.date_input("報告基準日", datetime.today())

# 메인 콘텐츠 영역
st.title("積立貯蓄のお知らせ")
st.divider()

# 섹션 A: 積立内容
with st.expander("Ⓐ お積立内容", expanded=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        start_date = st.date_input("積立開始日")
    with col2:
        st.text_input("積立コース", "定期預金", disabled=True)
    with col3:
        monthly_amount = st.number_input("毎月積立額 (円)", min_value=0, step=1000)
    with col4:
        bonus_amount = st.number_input("賞与積立額 (円)", min_value=0, step=1000)

# 섹션 B: 残高 및 이동 명세
with st.expander("Ⓑ お預かり残高および異動明細", expanded=True):
    cols = st.columns(6)
    previous_balance = cols[0].number_input("前回残高 (円)", min_value=0)
    deposits = cols[1].number_input("入金合計 (円)", min_value=0)
    withdrawals = cols[2].number_input("出金合計 (円)", min_value=0)
    income = cols[3].number_input("手取収益 (円)", min_value=0)
    other = cols[4].number_input("その他入出金 (円)", value=0)
    current_balance = cols[5].number_input("現在残高 (円)", min_value=0)

# 섹션 C: 金銭信託口座
with st.expander("Ⓒ お預かり残高内訳(金銭信託口座)"):
    trust_cols = st.columns(5)
    trust_account = trust_cols[0].text_input("口座番号")
    trust_principal = trust_cols[1].number_input("元本 (円)", min_value=0)
    trust_open_date = trust_cols[2].date_input("口座開設日")
    trust_years = trust_cols[3].number_input("開設経過年数", min_value=0)
    trust_rate = trust_cols[4].number_input("予定配当率 (%)", min_value=0.0, format="%.2f")

# 섹션 D: 定期預金口座
with st.expander("Ⓓ お預かり残高内訳(定期預金口座)"):
    deposit_cols = st.columns(4)
    deposit_account = deposit_cols[0].text_input("口座番号 ")
    deposit_principal = deposit_cols[1].number_input("元本 (円) ", min_value=0)
    deposit_rate = deposit_cols[2].number_input("約定利率 (%)", min_value=0.0, format="%.2f")
    deposit_maturity = deposit_cols[3].date_input("満期日")

# 리포트 생성 버튼
if st.button("報告書生成"):
    # 데이터 프레임 생성 예시
    report_data = {
        "項目": ["氏名", "社員番号", "報告日", "現在残高"],
        "内容": [emp_name, emp_number, report_date, f"{current_balance:,} 円"]
    }
    
    # 리포트 표시
    st.success("報告書が生成されました")
    st.divider()
    
    # PDF 생성 기능 추가 가능 (reportlab 등 라이브러리 사용)
    st.download_button(
        label="PDFでダウンロード",
        data=pd.DataFrame(report_data).to_csv().encode('utf-8'),
        file_name=f"積立報告書_{emp_name}_{report_date}.csv",
        mime="text/csv"
    )

# Footer
st.divider()
st.caption("※記載内容に相違がある場合は、積立貯蓄のお知らせに記載の照会先へご連絡ください。")
