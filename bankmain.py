import streamlit as st
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pandas as pd

# CSS 스타일링
st.markdown("""
<style>
:root {
    --primary: #2E3B4E;
    --secondary: #4E6B8A;
    --accent: #FF6B6B;
    --background: #F5F7FA;
    --card: #FFFFFF;
}

.info-card {
    background: var(--card);
    border-radius: 10px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    border-left: 4px solid var(--primary);
}

.info-card strong {
    font-weight: 700 !important;
    color: var(--primary);
}

.savings-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.5rem;
    margin: 2rem 0;
}

.logo-header {
    text-align: center;
    font-size: 2rem;
    color: var(--primary);
    font-weight: 700;
    margin: 2rem 0;
    padding: 1rem;
    border-bottom: 3px solid var(--primary);
}
</style>
""", unsafe_allow_html=True)

# 로그인 시스템
def login():
    st.markdown("""
    <div class='logo-header'>
        <div>🏦 大塚商会ローン</div>
        <div style='font-size:1rem; color:#666; margin-top:0.5rem;'>Otsuka Shokai Loan Service</div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        user_id = st.text_input("ログインID")
        password = st.text_input("パスワード", type="password")
        if st.form_submit_button("🔑 ログイン"):
            if user_id == "sgms" and password == "qwer1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("ログイン失敗")

# 메인 페이지
def main():
    st.markdown("<div class='logo-header'>🏦 大塚商会ローン</div>", unsafe_allow_html=True)
    
    # 1. 積立口座登録 (한국어 입력 유지)
    with st.expander("📝 積立口座新規登録", expanded=True):
        with st.form("savings_form"):
            cols = st.columns([1,1,2,1])
            name = cols[0].text_input("顧客名", placeholder="홍길동")
            emp_num = cols[1].text_input("社員番号", placeholder="12345678")
            account = cols[2].text_input("口座番号", placeholder="098-96586-6521")
            start_date = cols[3].date_input("積立開始日", value=date(2025,2,25))
            
            cols2 = st.columns([1,1,1,1])
            unit_price = cols2[0].number_input("1口座当たり金額 (¥)", value=1100, min_value=1000)
            units = cols2[1].number_input("申込口座数", value=4, min_value=1)
            years = cols2[2].selectbox("満期期間", [1,2,3,5], index=2)
            interest = cols2[3].number_input("年利率 (%)", value=10.03, min_value=0.0)
            
            if st.form_submit_button("💾 保存"):
                st.session_state.savings_data = {
                    "name": name, "emp_num": emp_num, "account": account,
                    "start_date": start_date, "unit_price": unit_price,
                    "original_units": units, "current_units": units,
                    "years": years, "interest": interest,
                    "adjustments": []
                }

    if 'savings_data' in st.session_state:
        data = st.session_state.savings_data
        monthly = data['unit_price'] * data['current_units']
        maturity = data['start_date'] + relativedelta(years=data['years'])
        
        # 2. 積立調整設定 (한국어 입력 유지)
        with st.expander("⚙️ 積立調整設定", expanded=True):
            with st.form("adjust_form"):
                cols = st.columns([2,3,1])
                adjust_month = cols[0].number_input("調整回次", min_value=1, value=1)
                new_units = cols[1].number_input("変更口座数", 
                    min_value=data['original_units']//2, 
                    max_value=data['original_units'], 
                    value=data['original_units']//2)
                if cols[2].form_submit_button("適用"):
                    data['adjustments'].append({
                        "month": adjust_month,
                        "new_units": new_units
                    })
                    st.rerun()
        
        # 3. 顧客情報 (볼드체 강조)
        st.markdown("### 🧑💼 顧客情報")
        with st.container():
            cols = st.columns(4)
            cols[0].markdown(f"""
            <div class='info-card'>
                <strong>顧客名</strong><br>
                {data['name']}
            </div>
            """, unsafe_allow_html=True)
            cols[1].markdown(f"""
            <div class='info-card'>
                <strong>社員番号</strong><br>
                {data['emp_num']}
            </div>
            """, unsafe_allow_html=True)
            cols[2].markdown(f"""
            <div class='info-card'>
                <strong>口座番号</strong><br>
                {data['account']}
            </div>
            """, unsafe_allow_html=True)
            cols[3].markdown(f"""
            <div class='info-card'>
                <strong>満期日</strong><br>
                {maturity.strftime('%Y-%m-%d')}
            </div>
            """, unsafe_allow_html=True)
        
        # 4. 積立概要
        st.markdown("### 📊 積立概要")
        with st.container():
            st.markdown(f"""
            <div class='savings-grid'>
                <div class='info-card'>
                    <strong>💰 月々積立額</strong><br>
                    <span style='font-size:1.5rem;'>¥{monthly:,}</span>
                </div>
                <div class='info-card'>
                    <strong>📆 総積立回数</strong><br>
                    <span style='font-size:1.5rem;'>{data['years']*12}回</span>
                </div>
                <div class='info-card'>
                    <strong>💵 総積立額</strong><br>
                    <span style='font-size:1.5rem;'>¥{monthly*data['years']*12:,}</span>
                </div>
                <div class='info-card'>
                    <strong>💹 予想利息</strong><br>
                    <span style='font-size:1.5rem;'>¥{monthly*data['years']*12*(data['interest']/100):,.1f}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # 5. 入金明細
        st.markdown("### 📅 入金明細")
        records = []
        balance = 0
        for i in range(1, data['years']*12 + 1 + len(data['adjustments'])):
            deposit_date = data['start_date'] + relativedelta(months=i-1)
            current_units = data['original_units']
            
            for adj in data['adjustments']:
                if adj['month'] == i:
                    current_units = adj['new_units']
            
            amount = data['unit_price'] * current_units
            balance += amount
            interest_amt = balance * (data['interest']/100)/12
            
            records.append([
                f"{i}回目 ({deposit_date.strftime('%y.%m.%d')})",
                f"¥{amount:,}",
                f"¥{balance:,}",
                f"¥{interest_amt:,.1f}",
                "✅ 完了" if deposit_date < datetime.now().date() else "⏳ 待機中",
                "🔧 調整" if any(adj['month']==i for adj in data['adjustments']) else ""
            ])
        
        df = pd.DataFrame(records, columns=["回次", "入金額", "残高", "利息", "状態", "備考"])
        st.dataframe(
            df.set_index("回次"), 
            use_container_width=True,
            column_config={
                "入金額": st.column_config.NumberColumn(format="¥%d"),
                "残高": st.column_config.NumberColumn(format="¥%d"),
                "利息": st.column_config.NumberColumn(format="¥%.1f")
            }
        )

# 앱 실행
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()