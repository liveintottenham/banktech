import streamlit as st
import base64
from datetime import datetime
import pandas as pd
from common import get_text, show_security_warnings, show_announcement, main_layout

# 페이지 제목 설정
st.set_page_config(
    page_title="給与 - Otsuka Bank",
    page_icon="📄",
    layout="wide"
)

# 급여 계산 함수들
def calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction):
    total_income = basic_salary + overtime_pay
    total_deductions = income_tax + residence_tax + health_insurance + pension + employment_insurance + other_deduction
    net_salary = total_income - total_deductions
    
    return {
        'total_income': total_income,
        'total_deductions': total_deductions,
        'net_salary': net_salary,
        'income_breakdown': {
            'basic_salary': {'jp': '基本給', 'en': 'Basic Salary', 'amount': basic_salary},
            'overtime_pay': {'jp': '残業代', 'en': 'Overtime Pay', 'amount': overtime_pay}
        },
        'deduction_breakdown': {
            'income_tax': {'jp': '所得税', 'en': 'Income Tax', 'amount': income_tax},
            'residence_tax': {'jp': '住民税', 'en': 'Residence Tax', 'amount': residence_tax},
            'health_insurance': {'jp': '健康保険', 'en': 'Health Insurance', 'amount': health_insurance},
            'pension': {'jp': '厚生年金', 'en': 'Pension', 'amount': pension},
            'employment_insurance': {'jp': '雇用保険', 'en': 'Employment Insurance', 'amount': employment_insurance},
            'other_deduction': {'jp': '控除額', 'en': 'Other Deduction', 'amount': other_deduction}
        }
    }

def create_payslip_html(salary_data, payslip_date, user_data):
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <title>給与明細 - {payslip_date}</title>
        <style>
            body {{ 
                font-family: 'Hiragino Sans', 'Noto Sans JP', sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            }}
            .payslip-container {{ 
                max-width: 900px; 
                margin: 0 auto; 
                background: white; 
                padding: 40px; 
                box-shadow: 0 20px 60px rgba(0,0,0,0.3); 
                border-radius: 20px;
                border: 10px double #2c5282;
            }}
            .header {{ 
                text-align: center; 
                border-bottom: 3px solid #2c5282; 
                padding-bottom: 25px; 
                margin-bottom: 30px; 
            }}
            .company-name {{ 
                font-size: 28px; 
                font-weight: bold; 
                color: #2c5282; 
                margin-bottom: 10px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            }}
            .info-section {{ 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 25px; 
                margin-bottom: 30px; 
            }}
            .info-card {{
                background: linear-gradient(135deg, #f8fafc, #f1f5f9);
                padding: 20px;
                border-radius: 12px;
                border-left: 5px solid #2c5282;
                box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            }}
            .amount-section {{ 
                display: grid; 
                grid-template-columns: 1fr 1fr; 
                gap: 30px; 
                margin-bottom: 30px; 
            }}
            .income-box {{ 
                background: linear-gradient(135deg, #f0fff4, #dcfce7);
                padding: 25px; 
                border-radius: 15px; 
                border: 2px solid #22c55e;
                box-shadow: 0 8px 25px rgba(34, 197, 94, 0.2);
            }}
            .deduction-box {{ 
                background: linear-gradient(135deg, #fef2f2, #fee2e2);
                padding: 25px; 
                border-radius: 15px; 
                border: 2px solid #ef4444;
                box-shadow: 0 8px 25px rgba(239, 68, 68, 0.2);
            }}
            .total-section {{ 
                background: linear-gradient(135deg, #1e3a8a, #3730a3);
                color: white; 
                padding: 30px; 
                border-radius: 15px; 
                text-align: center; 
                margin-top: 30px;
                box-shadow: 0 10px 30px rgba(30, 58, 138, 0.4);
            }}
            .detail-row {{ 
                display: flex; 
                justify-content: space-between; 
                padding: 12px 0; 
                border-bottom: 1px solid #e2e8f0; 
            }}
            .amount {{
                font-weight: bold;
                font-size: 16px;
            }}
            .section-title {{
                font-size: 20px;
                font-weight: bold;
                margin-bottom: 20px;
                color: #374151;
                border-bottom: 2px solid;
                padding-bottom: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="payslip-container">
            <div class="header">
                <div class="company-name">大塚銀行 / Otsuka Bank</div>
                <div style="font-size: 24px; color: #333; margin-bottom: 15px; font-weight: 600;">給与明細書 / Payslip</div>
                <div style="font-size: 18px; color: #666; background: #f8fafc; padding: 10px; border-radius: 8px; display: inline-block;">
                    支給日 / Pay Date: {payslip_date}
                </div>
            </div>
            
            <div class="info-section">
                <div class="info-card">
                    <h3 style="color: #374151; margin-bottom: 15px;">👤 個人情報 / Personal Information</h3>
                    <div class="detail-row">
                        <span><strong>氏名 / Name:</strong></span>
                        <span style="font-weight: 600;">{user_data['name']}</span>
                    </div>
                    <div class="detail-row">
                        <span><strong>社員番号 / Employee Number:</strong></span>
                        <span style="font-weight: 600;">{user_data['emp_num']}</span>
                    </div>
                </div>
                
                <div class="info-card">
                    <h3 style="color: #374151; margin-bottom: 15px;">🏢 勤務情報 / Work Information</h3>
                    <div class="detail-row">
                        <span><strong>所属部署 / Department:</strong></span>
                        <span style="font-weight: 600;">{user_data['department']}</span>
                    </div>
                    <div class="detail-row">
                        <span><strong>口座番号 / Account Number:</strong></span>
                        <span style="font-weight: 600;">{user_data['account']}</span>
                    </div>
                </div>
            </div>
            
            <div class="amount-section">
                <div class="income-box">
                    <div class="section-title" style="color: #166534;">💵 支給内訳 / Income Breakdown</div>
                    <div class="detail-row">
                        <span>基本給 / Basic Salary</span>
                        <span class="amount" style="color: #166534;">¥{salary_data['income_breakdown']['basic_salary']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>残業代 / Overtime Pay</span>
                        <span class="amount" style="color: #166534;">¥{salary_data['income_breakdown']['overtime_pay']['amount']:,.0f}</span>
                    </div>
                    <div style="border-top: 3px solid #22c55e; padding-top: 15px; margin-top: 10px;">
                        <div class="detail-row">
                            <strong style="font-size: 18px;">総支給額 / Total Income</strong>
                            <strong class="amount" style="font-size: 20px; color: #166534;">¥{salary_data['total_income']:,.0f}</strong>
                        </div>
                    </div>
                </div>
                
                <div class="deduction-box">
                    <div class="section-title" style="color: #dc2626;">📋 控除内訳 / Deduction Breakdown</div>
                    <div class="detail-row">
                        <span>所得税 / Income Tax</span>
                        <span class="amount" style="color: #dc2626;">¥{salary_data['deduction_breakdown']['income_tax']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>住民税 / Residence Tax</span>
                        <span class="amount" style="color: #dc2626;">¥{salary_data['deduction_breakdown']['residence_tax']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>健康保険 / Health Insurance</span>
                        <span class="amount" style="color: #dc2626;">¥{salary_data['deduction_breakdown']['health_insurance']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>厚生年金 / Pension</span>
                        <span class="amount" style="color: #dc2626;">¥{salary_data['deduction_breakdown']['pension']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>雇用保険 / Employment Insurance</span>
                        <span class="amount" style="color: #dc2626;">¥{salary_data['deduction_breakdown']['employment_insurance']['amount']:,.0f}</span>
                    </div>
                    <div class="detail-row">
                        <span>控除額 / Other Deduction</span>
                        <span class="amount" style="color: #dc2626;">¥{salary_data['deduction_breakdown']['other_deduction']['amount']:,.0f}</span>
                    </div>
                    <div style="border-top: 3px solid #ef4444; padding-top: 15px; margin-top: 10px;">
                        <div class="detail-row">
                            <strong style="font-size: 18px;">総控除額 / Total Deductions</strong>
                            <strong class="amount" style="font-size: 20px; color: #dc2626;">¥{salary_data['total_deductions']:,.0f}</strong>
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="total-section">
                <div style="font-size: 20px; margin-bottom: 10px;">差引支給額 / Net Salary</div>
                <div style="font-size: 42px; font-weight: bold; margin: 15px 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">¥{salary_data['net_salary']:,.0f}</div>
                <div style="font-size: 14px; opacity: 0.9;">
                    振込予定日 / Scheduled Transfer Date: {payslip_date.split(' / ')[0]}
                </div>
            </div>
            
            <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e2e8f0; color: #64748b; font-size: 12px;">
                発行日時 / Issued: {datetime.now().strftime('%Y年%m月%d日 %H:%M / %Y/%m/%d %H:%M')}<br>
                大塚銀行 給与計算システム / Otsuka Bank Payroll System
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
    
    st.markdown(f"## 📄 {get_text('payroll_management')}")
    
    # 기존 급여 명세서 조회
    if st.session_state.payroll_list:
        st.markdown("### 📋 既存の給与明細 / Existing Payslips")
        for payslip in st.session_state.payroll_list:
            with st.expander(f"💰 {payslip['date']} - ¥{payslip['salary_data']['net_salary']:,.0f}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("総支給額", f"¥{payslip['salary_data']['total_income']:,.0f}")
                with col2:
                    st.metric("総控除額", f"¥{payslip['salary_data']['total_deductions']:,.0f}")
                with col3:
                    st.metric("差引支給額", f"¥{payslip['salary_data']['net_salary']:,.0f}")
                
                # 상세 내역 표시
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("#### 支給内訳")
                    income_data = {
                        '項目': ['基本給', '残業代'],
                        '金額': [
                            f"¥{payslip['salary_data']['income_breakdown']['basic_salary']['amount']:,.0f}",
                            f"¥{payslip['salary_data']['income_breakdown']['overtime_pay']['amount']:,.0f}"
                        ]
                    }
                    st.dataframe(pd.DataFrame(income_data), use_container_width=True, hide_index=True)
                
                with col2:
                    st.markdown("#### 控除内訳")
                    deduction_data = {
                        '項目': ['所得税', '住民税', '健康保険', '厚生年金', '雇用保険', 'その他控除'],
                        '金額': [
                            f"¥{payslip['salary_data']['deduction_breakdown']['income_tax']['amount']:,.0f}",
                            f"¥{payslip['salary_data']['deduction_breakdown']['residence_tax']['amount']:,.0f}",
                            f"¥{payslip['salary_data']['deduction_breakdown']['health_insurance']['amount']:,.0f}",
                            f"¥{payslip['salary_data']['deduction_breakdown']['pension']['amount']:,.0f}",
                            f"¥{payslip['salary_data']['deduction_breakdown']['employment_insurance']['amount']:,.0f}",
                            f"¥{payslip['salary_data']['deduction_breakdown']['other_deduction']['amount']:,.0f}"
                        ]
                    }
                    st.dataframe(pd.DataFrame(deduction_data), use_container_width=True, hide_index=True)
    
    with st.form("payroll_form"):
        st.markdown("### 🆕 新規給与明細作成 / New Payslip Creation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"#### {get_text('income_breakdown')}")
            basic_salary = st.number_input(get_text('basic_salary'), value=300000, step=10000)
            overtime_pay = st.number_input(get_text('overtime_pay'), value=50000, step=5000)
        
        with col2:
            st.markdown(f"#### {get_text('deduction_breakdown')}")
            income_tax = st.number_input(get_text('income_tax'), value=25000, step=1000)
            residence_tax = st.number_input(get_text('residence_tax'), value=15000, step=1000)
            health_insurance = st.number_input(get_text('health_insurance'), value=20000, step=1000)
            pension = st.number_input(get_text('pension'), value=30000, step=1000)
            employment_insurance = st.number_input(get_text('employment_insurance'), value=5000, step=1000)
            other_deduction = st.number_input(get_text('other_deduction'), value=10000, step=1000)
            payslip_date = st.date_input(get_text('pay_date'), datetime.now().date())
        
        submitted = st.form_submit_button(f"📄 {get_text('payslip_creation')}", use_container_width=True, type="primary")
        
        if submitted:
            salary_data = calculate_salary(basic_salary, overtime_pay, income_tax, residence_tax, health_insurance, pension, employment_insurance, other_deduction)
            
            new_payslip = {
                'id': len(st.session_state.payroll_list) + 1,
                'date': payslip_date.strftime('%Y/%m/%d'),
                'salary_data': salary_data,
                'created_at': datetime.now().strftime('%Y/%m/%d %H:%M')
            }
            
            st.session_state.payroll_list.append(new_payslip)
            
            st.success("🎉 給与明細が作成されました！ / Payslip created successfully!")
            
            # 결과 표시
            st.markdown("### 📊 計算結果 / Calculation Results")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(get_text('total_income'), f"¥{salary_data['total_income']:,.0f}")
            with col2:
                st.metric(get_text('total_deductions'), f"¥{salary_data['total_deductions']:,.0f}")
            with col3:
                st.metric(get_text('net_salary'), f"¥{salary_data['net_salary']:,.0f}")
            
            # 상세 내역
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### 💵 支給内訳詳細")
                for key, item in salary_data['income_breakdown'].items():
                    st.write(f"- {item['jp']} / {item['en']}: ¥{item['amount']:,.0f}")
            
            with col2:
                st.markdown("#### 📋 控除内訳詳細")
                for key, item in salary_data['deduction_breakdown'].items():
                    st.write(f"- {item['jp']} / {item['en']}: ¥{item['amount']:,.0f}")
            
            # HTML 다운로드
            html_content = create_payslip_html(salary_data, payslip_date.strftime('%Y年%m月%d日 / %Y/%m/%d'), st.session_state.user_data)
            b64 = base64.b64encode(html_content.encode()).decode()
            href = f'<a href="data:text/html;base64,{b64}" download="給与明細_{payslip_date.strftime("%Y%m%d")}.html">'
            st.markdown(
                f'{href}'
                f'<button style="background: linear-gradient(135deg, #10b981, #059669); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 10px; font-weight: 600; cursor: pointer; margin-top: 1rem; width: 100%;">'
                f'📥 {get_text("download_payslip")}'
                f'</button>'
                f'</a>',
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    main()