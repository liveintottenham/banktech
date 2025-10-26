# pages/savings.py
import streamlit as st
import pandas as pd
import base64
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# common.py에서 필요한 함수들 임포트
from common import get_text

# 적금 계산 함수
def calculate_savings_schedule(monthly_amount, period_years, interest_rate, start_date, adjustments=None):
    total_months = period_years * 12
    monthly_interest_rate = interest_rate / 100 / 12
    today = datetime.now().date()
    
    schedule = []
    current_balance = 0
    
    for month in range(1, total_months + 1):
        payment_date = start_date + relativedelta(months=month-1)
        
        actual_amount = monthly_amount
        adjustment_note = ""
        if adjustments and month in adjustments:
            actual_amount = adjustments[month]
            adjustment_note = f"調整済: ¥{adjustments[month]:,}"
        
        monthly_interest = round(current_balance * monthly_interest_rate)
        current_balance += actual_amount + monthly_interest
        
        if payment_date < today:
            status = "✅ 入金完了"
        elif payment_date == today:
            status = "⏳ 本日入金"
        else:
            status = "📅 入金予定"
        
        schedule.append({
            '回': month,
            '入金日': payment_date.strftime('%Y/%m/%d'),
            '入金額': f"¥{actual_amount:,}",
            '利息': f"¥{monthly_interest:,}",
            '残高': f"¥{current_balance:,}",
            '状態': status,
            '備考': adjustment_note
        })
    
    total_payment = monthly_amount * total_months
    total_interest = current_balance - total_payment
    
    return {
        'schedule': schedule,
        'total_months': total_months,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'final_balance': current_balance,
        'completion_rate': len([x for x in schedule if '完了' in x['状態']]) / total_months * 100
    }

# 적금 증명서 HTML 생성
def create_savings_certificate_html(savings_data, user_data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>積立証明書 - {savings_data['name']}</title>
        <style>
            body {{ font-family: 'Hiragino Sans', sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }}
            .certificate-container {{ max-width: 900px; margin: 0 auto; background: white; padding: 40px; box-shadow: 0 0 30px rgba(0,0,0,0.2); border-radius: 12px; border: 8px double #2c5282; }}
            .header {{ text-align: center; border-bottom: 3px solid #2c5282; padding-bottom: 25px; margin-bottom: 30px; }}
            .certificate-title {{ font-size: 28px; font-weight: bold; color: #2c5282; margin-bottom: 10px; }}
            .info-section {{ display: grid; grid-template-columns: 1fr 1fr; gap: 25px; margin-bottom: 30px; }}
            .info-card {{ background: #f8fafc; padding: 20px; border-radius: 10px; border-left: 4px solid #2c5282; }}
            .calculation-section {{ background: linear-gradient(135deg, #f0fff4, #e6fffa); padding: 25px; border-radius: 10px; margin: 25px 0; border: 2px solid #38a169; }}
            .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #e2e8f0; color: #666; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="certificate-container">
            <div class="header">
                <div class="certificate-title">積立貯蓄証明書</div>
                <div style="color: #666; font-size: 16px;">Certificate of Savings Plan</div>
            </div>
            
            <div class="info-section">
                <div class="info-card">
                    <h3>基本情報</h3>
                    <div><strong>積立名:</strong> {savings_data['name']}</div>
                    <div><strong>顧客名:</strong> {user_data['name']}</div>
                    <div><strong>社員番号:</strong> {user_data['emp_num']}</div>
                </div>
                
                <div class="info-card">
                    <h3>積立詳細</h3>
                    <div><strong>開始日:</strong> {savings_data['start_date']}</div>
                    <div><strong>積立期間:</strong> {savings_data['period']}年</div>
                    <div><strong>月間積立額:</strong> ¥{savings_data['monthly_amount']:,.0f}</div>
                </div>
            </div>
            
            <div class="calculation-section">
                <h3>計算結果</h3>
                <div><strong>総支払額:</strong> ¥{savings_data['calculation']['total_payment']:,.0f}</div>
                <div><strong>総利息:</strong> ¥{savings_data['calculation']['total_interest']:,.0f}</div>
                <div><strong>最終残高:</strong> ¥{savings_data['calculation']['final_balance']:,.0f}</div>
            </div>
            
            <div class="footer">
                発行日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M')}
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def render():
    st.markdown("## 💰 積立貯蓄管理")
    
    tab1, tab2 = st.tabs(["🆕 新規積立作成", "📋 積立一覧"])
    
    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown("### 🆕 新規積立口座開設")
        
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input("顧客名", st.session_state.user_data['name'])
            employee_number = st.text_input("社員番号", st.session_state.user_data['emp_num'])
            account_number = st.text_input("口座番号", st.session_state.user_data['account'])
        
        with col2:
            savings_name = st.text_input("積立名", "定期積立預金")
            monthly_amount = st.number_input("月間積立額 (¥)", min_value=1000, value=3000, step=1000)
            period = st.selectbox("積立期間", [3, 5], index=0, format_func=lambda x: f"{x}年")
            interest_rate = st.number_input("年利率 (%)", min_value=0.1, value=2.5, step=0.1, format="%.1f")
            start_date = st.date_input("開始日", date(2025, 1, 1))
        
        if 'adjustments' not in st.session_state:
            st.session_state.adjustments = []
        
        st.markdown("#### ⚙️ 入金調整")
        st.info("特定の回で入金額を調整する場合は設定してください")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            new_month = st.number_input("調整回", min_value=1, max_value=36, value=1, key="new_month")
        with col2:
            new_amount = st.number_input("調整金額 (¥)", min_value=0, value=3000, key="new_amount")
        with col3:
            if st.button("➕ 追加", use_container_width=True):
                st.session_state.adjustments.append({'month': new_month, 'amount': new_amount})
                st.success(f"{new_month}回目を調整しました")
        
        if st.session_state.adjustments:
            st.markdown("**現在の調整内容:**")
            for i, adj in enumerate(st.session_state.adjustments):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📅 {adj['month']}回目: ¥{adj['amount']:,}")
                with col2:
                    st.write(f"⚡ デフォルト: ¥{monthly_amount:,}")
                with col3:
                    if st.button("🗑️ 削除", key=f"remove_{i}"):
                        st.session_state.adjustments.pop(i)
                        st.rerun()
        
        if st.button("🚀 積立プラン作成", use_container_width=True, type="primary"):
            adjustments_dict = {adj['month']: adj['amount'] for adj in st.session_state.adjustments}
            
            calculation = calculate_savings_schedule(
                monthly_amount, 
                period, 
                interest_rate, 
                start_date, 
                adjustments_dict
            )
            
            new_savings = {
                'id': len(st.session_state.savings_list) + 1,
                'name': savings_name,
                'customer_name': customer_name,
                'employee_number': employee_number,
                'account_number': account_number,
                'monthly_amount': monthly_amount,
                'period': period,
                'interest_rate': interest_rate,
                'start_date': start_date.strftime('%Y/%m/%d'),
                'adjustments': adjustments_dict,
                'calculation': calculation,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.savings_list.append(new_savings)
            st.session_state.adjustments = []
            st.success("🎉 積立プランが正常に作成されました！")
            st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        if not st.session_state.savings_list:
            st.info("登録されている積立プランがありません。")
        else:
            for savings in st.session_state.savings_list:
                with st.expander(f"📒 {savings['name']} - {savings['account_number']}", expanded=False):
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    
                    st.markdown("#### 📋 基本情報")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("**顧客名**")
                        st.write(savings['customer_name'])
                    with col2:
                        st.markdown("**社員番号**")
                        st.write(savings['employee_number'])
                    with col3:
                        st.markdown("**口座番号**")
                        st.write(savings['account_number'])
                    with col4:
                        st.markdown("**開始日**")
                        st.write(savings['start_date'])
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown("**月間積立額**")
                        st.write(f"¥{savings['monthly_amount']:,.0f}")
                    with col2:
                        st.markdown("**積立期間**")
                        st.write(f"{savings['period']}年")
                    with col3:
                        st.markdown("**年利率**")
                        st.write(f"{savings['interest_rate']}%")
                    with col4:
                        completion = savings['calculation']['completion_rate']
                        st.markdown("**進捗率**")
                        st.write(f"{completion:.1f}%")
                    
                    calc = savings['calculation']
                    st.markdown("#### 計算結果")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("総支払額", f"¥{calc['total_payment']:,.0f}")
                    with col2:
                        st.metric("総利息", f"¥{calc['total_interest']:,.0f}")
                    with col3:
                        st.metric("最終残高", f"¥{calc['final_balance']:,.0f}")
                    with col4:
                        st.metric("総月数", f"{calc['total_months']}")
                    
                    # 적금 증명서 다운로드
                    html_content = create_savings_certificate_html(savings, st.session_state.user_data)
                    b64 = base64.b64encode(html_content.encode()).decode()
                    href = f'<a href="data:text/html;base64,{b64}" download="積立証明書_{savings["name"]}.html">'
                    st.markdown(
                        f'{href}'
                        f'<button style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer; margin: 1rem 0; width: 100%;">'
                        f'📥 積立証明書をダウンロード'
                        f'</button>'
                        f'</a>',
                        unsafe_allow_html=True
                    )
                    
                    st.markdown("#### 入金スケジュール")
                    schedule_data = []
                    for item in savings['calculation']['schedule'][:12]:
                        schedule_data.append({
                            '回': item['回'],
                            '日付': item['入金日'],
                            '金額': item['入金額'],
                            '利息': item['利息'],
                            '残高': item['残高'],
                            '状態': item['状態'],
                            '備考': item['備考']
                        })
                    
                    schedule_df = pd.DataFrame(schedule_data)
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
                    
                    if st.button(f"🗑️ 削除", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)