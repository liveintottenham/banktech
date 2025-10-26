import streamlit as st
import pandas as pd
import base64
import plotly.graph_objects as go
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from common import get_text, show_security_warnings, show_announcement, main_layout

# 페이지 제목 설정
st.set_page_config(
    page_title="積立 - Otsuka Bank",
    page_icon="💰",
    layout="wide"
)

# 적금 계산 함수들 - 오류 수정 버전
def calculate_savings_schedule(monthly_amount, period_years, interest_rate, start_date, adjustments=None):
    total_months = period_years * 12
    monthly_interest_rate = interest_rate / 100 / 12
    today = datetime.now().date()
    
    schedule = []
    current_balance = 0
    total_paid = 0
    
    for month in range(1, total_months + 1):
        payment_date = start_date + relativedelta(months=month-1)
        
        actual_amount = monthly_amount
        adjustment_note = ""
        if adjustments and month in adjustments:
            actual_amount = adjustments[month]
            adjustment_note = f"調整済 / Adjusted: ¥{adjustments[month]:,}"
        
        monthly_interest = round(current_balance * monthly_interest_rate)
        current_balance += actual_amount + monthly_interest
        
        # 상태 설정 로직 수정
        if payment_date < today:
            status = "✅ 入金完了 / Payment Completed"
            total_paid += actual_amount
        elif payment_date == today:
            status = "⏳ 本日入金 / Payment Today"
            total_paid += actual_amount
        else:
            status = "📅 入金予定 / Scheduled Payment"
        
        schedule.append({
            'month': month,
            'payment_date': payment_date,
            'amount': actual_amount,
            'interest': monthly_interest,
            'balance': current_balance,
            'status': status,
            'notes': adjustment_note
        })
    
    total_payment = monthly_amount * total_months
    total_interest = current_balance - total_payment
    
    return {
        'schedule': schedule,
        'total_months': total_months,
        'total_payment': total_payment,
        'total_interest': total_interest,
        'final_balance': current_balance,
        'total_paid': total_paid,
        'remaining_months': len([x for x in schedule if x['payment_date'] > today]),
        'completion_rate': (len([x for x in schedule if x['payment_date'] <= today]) / total_months) * 100
    }

def create_savings_certificate_html(savings_data, user_data):
    """더 전문적인 적금 증명서 생성"""
    
    # 차트 데이터 준비
    schedule = savings_data['calculation']['schedule']
    months = [f"{item['month']}回" for item in schedule]
    balances = [item['balance'] for item in schedule]
    payments = [item['amount'] for item in schedule]
    
    # 진행 상황 계산
    today = datetime.now().date()
    completed = len([x for x in schedule if x['payment_date'] <= today])
    total = len(schedule)
    progress_percent = (completed / total) * 100
    
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>積立証明書 - {savings_data['name']}</title>
        <style>
            body {{ 
                font-family: 'Hiragino Sans', 'Noto Sans JP', sans-serif; 
                margin: 0; 
                padding: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .certificate-container {{ 
                max-width: 1000px; 
                margin: 20px auto; 
                background: white; 
                padding: 40px; 
                box-shadow: 0 20px 60px rgba(0,0,0,0.3); 
                border-radius: 20px; 
                border: 15px double #2c5282;
                position: relative;
            }}
            .watermark {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) rotate(-45deg);
                font-size: 120px;
                color: rgba(30, 58, 138, 0.1);
                font-weight: bold;
                z-index: 0;
            }}
            .header {{ 
                text-align: center; 
                border-bottom: 3px solid #2c5282; 
                padding-bottom: 25px; 
                margin-bottom: 30px;
                position: relative;
                z-index: 1;
            }}
            .certificate-title {{ 
                font-size: 32px; 
                font-weight: bold; 
                color: #2c5282; 
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }}
            .info-grid {{ 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 25px; 
                margin-bottom: 30px;
                position: relative;
                z-index: 1;
            }}
            .info-card {{ 
                background: linear-gradient(135deg, #f8fafc, #f1f5f9);
                padding: 25px; 
                border-radius: 15px; 
                border-left: 5px solid #2c5282;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .calculation-section {{ 
                background: linear-gradient(135deg, #dbeafe, #e0f2fe);
                padding: 30px; 
                border-radius: 15px; 
                margin: 30px 0; 
                border: 2px solid #3b82f6;
                position: relative;
                z-index: 1;
            }}
            .progress-section {{
                background: linear-gradient(135deg, #f0fdf4, #dcfce7);
                padding: 25px;
                border-radius: 15px;
                margin: 25px 0;
                border: 2px solid #22c55e;
                position: relative;
                z-index: 1;
            }}
            .progress-bar {{
                width: 100%;
                height: 20px;
                background: #e2e8f0;
                border-radius: 10px;
                overflow: hidden;
                margin: 15px 0;
            }}
            .progress-fill {{
                height: 100%;
                background: linear-gradient(90deg, #10b981, #22c55e);
                width: {progress_percent}%;
                transition: width 1s ease;
            }}
            .footer {{ 
                text-align: center; 
                margin-top: 40px; 
                padding-top: 20px; 
                border-top: 2px solid #e2e8f0; 
                color: #666; 
                font-size: 14px;
                position: relative;
                z-index: 1;
            }}
            .value {{
                font-size: 18px;
                font-weight: bold;
                color: #1e40af;
            }}
            .highlight {{
                background: linear-gradient(135deg, #fef3c7, #fde68a);
                padding: 5px 10px;
                border-radius: 5px;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="certificate-container">
            <div class="watermark">OTS UKA BANK</div>
            
            <div class="header">
                <div class="certificate-title">積立貯蓄証明書</div>
                <div style="color: #666; font-size: 18px; margin-bottom: 10px;">Savings Certificate</div>
                <div style="color: #94a3b8; font-size: 14px;">Certificate of Savings Plan</div>
            </div>
            
            <div class="info-grid">
                <div class="info-card">
                    <h3 style="color: #374151; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">基本情報 / Basic Information</h3>
                    <div style="margin: 15px 0;"><strong>積立名:</strong> <span class="value">{savings_data['name']}</span></div>
                    <div style="margin: 15px 0;"><strong>顧客名:</strong> <span class="value">{user_data['name']}</span></div>
                    <div style="margin: 15px 0;"><strong>社員番号:</strong> <span class="highlight">{user_data['emp_num']}</span></div>
                </div>
                
                <div class="info-card">
                    <h3 style="color: #374151; border-bottom: 2px solid #e2e8f0; padding-bottom: 10px;">積立詳細 / Savings Details</h3>
                    <div style="margin: 15px 0;"><strong>開始日:</strong> <span class="value">{savings_data['start_date']}</span></div>
                    <div style="margin: 15px 0;"><strong>積立期間:</strong> <span class="value">{savings_data['period']}年 / years</span></div>
                    <div style="margin: 15px 0;"><strong>月間積立額:</strong> <span class="value">¥{savings_data['monthly_amount']:,.0f}</span></div>
                    <div style="margin: 15px 0;"><strong>年利率:</strong> <span class="value">{savings_data['interest_rate']}%</span></div>
                </div>
            </div>
            
            <div class="progress-section">
                <h3 style="color: #166534; margin-bottom: 20px;">📊 積立進捗状況 / Savings Progress</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 20px;">
                    <div>
                        <div>完了回数 / Completed: <span class="value">{completed}回</span></div>
                        <div>残り回数 / Remaining: <span class="value">{total - completed}回</span></div>
                    </div>
                    <div>
                        <div>総回数 / Total: <span class="value">{total}回</span></div>
                        <div>進捗率 / Progress: <span class="value">{progress_percent:.1f}%</span></div>
                    </div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
            </div>
            
            <div class="calculation-section">
                <h3 style="color: #1e40af; margin-bottom: 25px;">💰 計算結果 / Calculation Results</h3>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <div style="font-size: 14px; color: #64748b;">総支払額 / Total Payment</div>
                        <div style="font-size: 24px; font-weight: bold; color: #1e40af;">¥{savings_data['calculation']['total_payment']:,.0f}</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <div style="font-size: 14px; color: #64748b;">総利息 / Total Interest</div>
                        <div style="font-size: 24px; font-weight: bold; color: #10b981;">¥{savings_data['calculation']['total_interest']:,.0f}</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <div style="font-size: 14px; color: #64748b;">現在までの支払額 / Paid to Date</div>
                        <div style="font-size: 24px; font-weight: bold; color: #f59e0b;">¥{savings_data['calculation']['total_paid']:,.0f}</div>
                    </div>
                    <div style="text-align: center; padding: 15px; background: white; border-radius: 10px; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
                        <div style="font-size: 14px; color: #64748b;">最終残高 / Final Balance</div>
                        <div style="font-size: 24px; font-weight: bold; color: #ef4444;">¥{savings_data['calculation']['final_balance']:,.0f}</div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <div style="margin-bottom: 10px;">発行日時 / Issued: {datetime.now().strftime('%Y年%m月%d日 %H:%M / %Y/%m/%d %H:%M')}</div>
                <div style="font-size: 12px; color: #94a3b8;">大塚銀行 / Otsuka Bank - 従業員バンキングポータル / Employee Banking Portal</div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

def main():
    main_layout()
    show_security_warnings()
    show_announcement()
    
    st.markdown(f"## 💰 {get_text('savings_management')}")
    
    tab1, tab2 = st.tabs(["🆕 新規積立作成 / New Savings Creation", "📋 積立一覧 / Savings List"])
    
    with tab1:
        st.markdown('<div class="content-card">', unsafe_allow_html=True)
        st.markdown(f"### 🆕 {get_text('new_savings_account')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            customer_name = st.text_input(get_text('customer_name'), st.session_state.user_data['name'])
            employee_number = st.text_input(get_text('employee_number'), st.session_state.user_data['emp_num'])
            account_number = st.text_input(get_text('account_number'), st.session_state.user_data['account'])
        
        with col2:
            savings_name = st.text_input(get_text('savings_name'), "定期積立預金 / Regular Savings")
            monthly_amount = st.number_input(get_text('monthly_amount'), min_value=1000, value=3000, step=1000)
            period = st.selectbox(get_text('savings_period'), [3, 5], index=0, format_func=lambda x: f"{x}年 / {x} years")
            interest_rate = st.number_input(get_text('interest_rate'), min_value=0.1, value=2.5, step=0.1, format="%.1f")
            start_date = st.date_input(get_text('start_date'), date(2025, 1, 1))
        
        if 'adjustments' not in st.session_state:
            st.session_state.adjustments = []
        
        st.markdown(f"#### ⚙️ {get_text('payment_adjustment')}")
        st.info("特定の回で入金額を調整する場合は設定してください / Set adjustments for specific payment months if needed")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        with col1:
            new_month = st.number_input(get_text('adjustment_month'), min_value=1, max_value=period*12, value=1, key="new_month")
        with col2:
            new_amount = st.number_input(get_text('adjustment_amount'), min_value=0, value=3000, key="new_amount")
        with col3:
            if st.button("➕ 追加 / Add", use_container_width=True):
                st.session_state.adjustments.append({'month': new_month, 'amount': new_amount})
                st.success(f"{new_month}回目を調整しました / Adjusted month {new_month}")
        
        if st.session_state.adjustments:
            st.markdown("**現在の調整内容 / Current Adjustments:**")
            for i, adj in enumerate(st.session_state.adjustments):
                col1, col2, col3 = st.columns([3, 2, 1])
                with col1:
                    st.write(f"📅 {adj['month']}回目 / Month {adj['month']}: ¥{adj['amount']:,}")
                with col2:
                    st.write(f"⚡ デフォルト / Default: ¥{monthly_amount:,}")
                with col3:
                    if st.button("🗑️ 削除 / Delete", key=f"remove_{i}"):
                        st.session_state.adjustments.pop(i)
                        st.rerun()
        
        if st.button(f"🚀 {get_text('create_savings_plan')}", use_container_width=True, type="primary"):
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
            st.success("🎉 積立プランが正常に作成されました！ / Savings plan created successfully!")
            st.balloons()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        if not st.session_state.savings_list:
            st.info("登録されている積立プランがありません。 / No savings plans registered.")
        else:
            for savings in st.session_state.savings_list:
                with st.expander(f"📒 {savings['name']} - {savings['account_number']}", expanded=False):
                    st.markdown('<div class="content-card">', unsafe_allow_html=True)
                    
                    st.markdown(f"#### 📋 {get_text('basic_info')}")
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown("**顧客名 / Customer Name**")
                        st.write(savings['customer_name'])
                    with col2:
                        st.markdown("**社員番号 / Employee Number**")
                        st.write(savings['employee_number'])
                    with col3:
                        st.markdown("**口座番号 / Account Number**")
                        st.write(savings['account_number'])
                    with col4:
                        st.markdown("**開始日 / Start Date**")
                        st.write(savings['start_date'])
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.markdown("**月間積立額 / Monthly Amount**")
                        st.write(f"¥{savings['monthly_amount']:,.0f}")
                    with col2:
                        st.markdown("**積立期間 / Savings Period**")
                        st.write(f"{savings['period']}年 / years")
                    with col3:
                        st.markdown("**年利率 / Interest Rate**")
                        st.write(f"{savings['interest_rate']}%")
                    with col4:
                        completion = savings['calculation']['completion_rate']
                        st.markdown(f"**{get_text('progress_rate')}**")
                        st.progress(completion/100)
                        st.write(f"{completion:.1f}%")
                    
                    calc = savings['calculation']
                    st.markdown(f"#### {get_text('calculation_results')}")
                    
                    # 현재까지 납입 현황 표시
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(get_text('total_payment'), f"¥{calc['total_payment']:,.0f}")
                    with col2:
                        st.metric(get_text('total_interest'), f"¥{calc['total_interest']:,.0f}")
                    with col3:
                        st.metric("現在までの支払額 / Paid to Date", f"¥{calc['total_paid']:,.0f}")
                    with col4:
                        st.metric(get_text('final_balance'), f"¥{calc['final_balance']:,.0f}")
                    
                    # 진행 상황 시각화
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("完了回数 / Completed", f"{calc['total_months'] - calc['remaining_months']}回")
                    with col2:
                        st.metric("残り回数 / Remaining", f"{calc['remaining_months']}回")
                    
                    # 적금 증명서 다운로드
                    html_content = create_savings_certificate_html(savings, st.session_state.user_data)
                    b64 = base64.b64encode(html_content.encode()).decode()
                    href = f'<a href="data:text/html;base64,{b64}" download="積立証明書_{savings["name"]}.html">'
                    st.markdown(
                        f'{href}'
                        f'<button style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer; margin: 1rem 0; width: 100%;">'
                        f'📥 {get_text("download_certificate")}'
                        f'</button>'
                        f'</a>',
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(f"#### {get_text('payment_schedule')} (最初の12回 / First 12 months)")
                    schedule_data = []
                    for item in savings['calculation']['schedule'][:12]:
                        schedule_data.append({
                            '回 / No.': item['month'],
                            '入金日 / Payment Date': item['payment_date'].strftime('%Y/%m/%d'),
                            '入金額 / Amount': f"¥{item['amount']:,}",
                            '利息 / Interest': f"¥{item['interest']:,}",
                            '残高 / Balance': f"¥{item['balance']:,}",
                            '状態 / Status': item['status'],
                            '備考 / Notes': item['notes']
                        })
                    
                    schedule_df = pd.DataFrame(schedule_data)
                    st.dataframe(schedule_df, use_container_width=True, hide_index=True)
                    
                    if st.button(f"🗑️ 削除 / Delete", key=f"delete_{savings['id']}"):
                        st.session_state.savings_list = [s for s in st.session_state.savings_list if s['id'] != savings['id']]
                        st.rerun()
                    
                    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()